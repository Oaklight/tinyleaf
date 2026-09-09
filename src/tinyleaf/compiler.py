"""Compilation backend for tinyleaf.

Supports local latexmk and Docker-based compilation.
"""

import asyncio
import os
import uuid

_DONE_SENTINEL = object()


class CompileJob:
    """Tracks a single compilation run."""

    def __init__(
        self,
        compile_id,
        project_dir,
        main_file,
        engine,
        use_docker,
        docker_image,
        registry_mirror=None,
    ):
        self.compile_id = compile_id
        self.project_dir = project_dir
        self.main_file = main_file
        self.engine = engine
        self.use_docker = use_docker
        self.docker_image = docker_image
        self.registry_mirror = registry_mirror
        self.log_lines = []
        self.status = "running"  # running | success | error | cancelled
        self.pdf_path = None
        self.proc = None  # asyncio.subprocess.Process reference for cancellation
        self._cancelled = False
        self._done_event = asyncio.Event()
        self._subscribers: list[asyncio.Queue] = []
        self._task = None  # asyncio.Task running the compilation

    def append_log(self, line, level="info"):
        entry = {"line": line, "level": level}
        self.log_lines.append(entry)
        for q in self._subscribers:
            q.put_nowait(entry)

    def get_logs_from(self, index):
        return list(self.log_lines[index:])

    def finish(self, status, pdf_path=None):
        self.status = status
        self.pdf_path = pdf_path
        for q in self._subscribers:
            q.put_nowait(_DONE_SENTINEL)
        self._done_event.set()

    async def wait(self):
        await self._done_event.wait()

    def cancel(self):
        """Cancel this compilation by killing the subprocess."""
        self._cancelled = True
        if self.proc and self.proc.returncode is None:
            self.proc.kill()
        self.append_log("Cancelled by user.", level="warning")
        self.finish("cancelled")

    async def log_stream(self):
        """Async generator yielding log entries as they arrive.

        Each caller gets its own queue, so multiple consumers (e.g. two
        browser tabs) receive all log entries independently.
        """
        q: asyncio.Queue = asyncio.Queue()
        self._subscribers.append(q)
        try:
            # Replay entries logged before this consumer connected
            for entry in list(self.log_lines):
                yield entry
            if self.is_done:
                return
            while True:
                entry = await q.get()
                if entry is _DONE_SENTINEL:
                    return
                yield entry
        finally:
            self._subscribers.remove(q)

    @property
    def is_cancelled(self):
        return self._cancelled

    @property
    def is_done(self):
        return self._done_event.is_set()


# Global compile job registry (single-threaded asyncio, no lock needed)
_jobs: dict[str, CompileJob] = {}


def get_job(compile_id):
    return _jobs.get(compile_id)


def cancel_compile(compile_id):
    """Cancel a running compilation job.

    Returns:
        True if the job was found and cancelled, False otherwise.
    """
    job = get_job(compile_id)
    if not job or job.is_done:
        return False
    job.cancel()
    return True


async def start_compile(
    project_dir,
    main_file="main.tex",
    engine="pdflatex",
    use_docker=False,
    docker_image="oaklight/texlive:alpine-science-cn",
    registry_mirror=None,
):
    """Start a compilation and return the compile_id.

    Args:
        project_dir: Absolute path to the project directory.
        main_file: Main .tex file relative to project_dir.
        engine: Compilation engine (pdflatex, lualatex, xelatex).
        use_docker: Whether to use Docker for compilation.
        docker_image: Docker image to use.
        registry_mirror: Optional registry mirror (e.g. "docker.1ms.run").

    Returns:
        compile_id string.
    """
    compile_id = uuid.uuid4().hex[:12]
    job = CompileJob(
        compile_id,
        project_dir,
        main_file,
        engine,
        use_docker,
        docker_image,
        registry_mirror=registry_mirror,
    )

    _jobs[compile_id] = job
    job._task = asyncio.create_task(_run_compile(job))
    return compile_id


def _build_latexmk_args(engine, main_file):
    """Build latexmk command arguments."""
    engine_flag = {
        "pdflatex": "-pdf",
        "lualatex": "-lualatex",
        "xelatex": "-xelatex",
    }.get(engine, "-pdf")

    return [
        "latexmk",
        engine_flag,
        "-cd",
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
        main_file,
    ]


def _build_multipass_cmds(engine, main_file):
    """Build multi-pass compile commands for direct engine use.

    Flow: engine -> bibtex -> engine -> engine (3 passes with bibliography).
    """
    base = os.path.splitext(main_file)[0]
    common_flags = ["-synctex=1", "-interaction=nonstopmode", "-file-line-error"]
    engine_cmd = [engine] + common_flags + [main_file]
    bibtex_cmd = ["bibtex", base]
    return [engine_cmd, bibtex_cmd, engine_cmd, engine_cmd]


async def _run_compile(job: CompileJob):
    """Run the compilation as an async task.

    Cancellation is cooperative via job._cancelled flag + proc.kill(),
    not via asyncio task cancellation, so CancelledError won't bypass
    the except handler.
    """
    try:
        if job.engine == "latexmk":
            cmds = [_build_latexmk_args("pdflatex", job.main_file)]
        elif job.engine in ("pdflatex", "lualatex", "xelatex"):
            if await _has_latexmk(job):
                cmds = [_build_latexmk_args(job.engine, job.main_file)]
            else:
                cmds = _build_multipass_cmds(job.engine, job.main_file)
        else:
            cmds = [_build_latexmk_args("pdflatex", job.main_file)]

        if job.use_docker:
            if not await _docker_image_exists(job.docker_image):
                if job.is_cancelled:
                    return
                if not await _docker_pull(job, job.docker_image, job.registry_mirror):
                    return

            if job.is_cancelled:
                return

            docker_prefix = [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{job.project_dir}:/workspace",
                "-w",
                "/workspace",
                job.docker_image,
            ]
            cmds = [docker_prefix + c for c in cmds]

        last_rc = 0
        for cmd in cmds:
            if job.is_cancelled:
                return

            job.append_log(f"$ {' '.join(cmd)}", level="info")

            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=job.project_dir if not job.use_docker else None,
            )
            job.proc = proc

            assert proc.stdout is not None
            async for raw_line in proc.stdout:
                if job.is_cancelled:
                    break
                line = raw_line.decode("utf-8", errors="replace").rstrip("\n")
                level = _classify_log_line(line)
                job.append_log(line, level=level)

            await proc.wait()
            last_rc = proc.returncode

            if job.is_cancelled:
                return

            is_bibtex = cmd[-1].endswith((".aux",)) or "bibtex" in cmd
            if last_rc != 0 and not is_bibtex:
                break

        base = os.path.splitext(job.main_file)[0]
        pdf_name = base + ".pdf"
        pdf_full = os.path.join(job.project_dir, pdf_name)

        if last_rc == 0 and os.path.exists(pdf_full):
            job.finish("success", pdf_path=pdf_name)
        else:
            job.append_log(
                f"Compilation failed (exit code {last_rc})",
                level="error",
            )
            if os.path.exists(pdf_full):
                job.finish("error", pdf_path=pdf_name)
            else:
                job.finish("error")

    except Exception as e:
        if not job.is_cancelled:
            job.append_log(f"Internal error: {e}", level="error")
            job.finish("error")


def _classify_log_line(line):
    """Classify a log line as info/warning/error."""
    lower = line.lower()
    if "error" in lower or "!" in line[:5]:
        return "error"
    if "warning" in lower or "overfull" in lower or "underfull" in lower:
        return "warning"
    return "info"


async def _has_latexmk(job):
    """Check if latexmk is available (in Docker or locally)."""
    try:
        if job.use_docker:
            proc = await asyncio.create_subprocess_exec(
                "docker",
                "run",
                "--rm",
                job.docker_image,
                "which",
                "latexmk",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
        else:
            proc = await asyncio.create_subprocess_exec(
                "which",
                "latexmk",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
        await asyncio.wait_for(proc.wait(), timeout=15)
        return proc.returncode == 0
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()
        return False
    except Exception:
        return False


async def _docker_image_exists(image):
    """Check if a Docker image exists locally."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "docker",
            "image",
            "inspect",
            image,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await asyncio.wait_for(proc.wait(), timeout=10)
        return proc.returncode == 0
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()
        return False
    except Exception:
        return False


async def _docker_pull(job, image, registry_mirror=None):
    """Pull a Docker image, streaming output to the compile job log.

    Returns:
        True if pull succeeded, False otherwise.
    """
    if registry_mirror:
        pull_image = f"{registry_mirror}/{image}"
        job.append_log(
            f"Image '{image}' not found locally, pulling from mirror {registry_mirror}..."
        )
    else:
        pull_image = image
        job.append_log(f"Image '{image}' not found locally, pulling...")

    try:
        proc = await asyncio.create_subprocess_exec(
            "docker",
            "pull",
            pull_image,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        job.proc = proc

        assert proc.stdout is not None
        async for raw_line in proc.stdout:
            if job.is_cancelled:
                proc.kill()
                await proc.wait()
                return False
            job.append_log(raw_line.decode("utf-8", errors="replace").rstrip("\n"))
        await proc.wait()

        if job.is_cancelled:
            return False

        if proc.returncode != 0:
            job.append_log(f"Failed to pull image '{pull_image}'", level="error")
            job.finish("error")
            return False

        if registry_mirror and pull_image != image:
            retag = await asyncio.create_subprocess_exec(
                "docker",
                "tag",
                pull_image,
                image,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await asyncio.wait_for(retag.wait(), timeout=10)
            rmi = await asyncio.create_subprocess_exec(
                "docker",
                "rmi",
                pull_image,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await asyncio.wait_for(rmi.wait(), timeout=10)
            job.append_log(f"Retagged '{pull_image}' -> '{image}'")

        job.append_log("Image ready.")
        return True

    except Exception as e:
        job.append_log(f"Pull error: {e}", level="error")
        job.finish("error")
        return False


async def docker_pull_image(image, registry_mirror=None):
    """Pull a Docker image (standalone, not tied to a compile job).

    Returns:
        Tuple of (success: bool, message: str).
    """
    if registry_mirror:
        pull_image = f"{registry_mirror}/{image}"
    else:
        pull_image = image

    try:
        proc = await asyncio.create_subprocess_exec(
            "docker",
            "pull",
            pull_image,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        _pull_procs[image] = proc

        assert proc.stdout is not None
        output_lines = []
        async for raw_line in proc.stdout:
            output_lines.append(raw_line.decode("utf-8", errors="replace"))
        await proc.wait()

        _pull_procs.pop(image, None)

        if proc.returncode != 0:
            stderr = "".join(output_lines).strip()
            if proc.returncode in (-9, -15):
                return False, "Cancelled"
            return False, stderr or "Pull failed"

        if registry_mirror and pull_image != image:
            retag = await asyncio.create_subprocess_exec(
                "docker",
                "tag",
                pull_image,
                image,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await asyncio.wait_for(retag.wait(), timeout=10)
            rmi = await asyncio.create_subprocess_exec(
                "docker",
                "rmi",
                pull_image,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await asyncio.wait_for(rmi.wait(), timeout=10)

        return True, "OK"
    except asyncio.TimeoutError:
        _pull_procs.pop(image, None)
        return False, "Pull timed out"
    except Exception as e:
        _pull_procs.pop(image, None)
        return False, str(e)


# Track standalone pull processes for cancellation
_pull_procs: dict[str, asyncio.subprocess.Process] = {}


def cancel_docker_pull(image):
    """Cancel a running standalone docker pull.

    Returns:
        True if a pull was found and killed, False otherwise.
    """
    proc = _pull_procs.pop(image, None)
    if proc and proc.returncode is None:
        proc.kill()
        return True
    return False


async def docker_remove_image(image):
    """Remove a local Docker image.

    Returns:
        Tuple of (success: bool, message: str).
    """
    try:
        proc = await asyncio.create_subprocess_exec(
            "docker",
            "rmi",
            image,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
        if proc.returncode == 0:
            return True, "OK"
        return False, stderr.decode("utf-8", errors="replace").strip() or "Remove failed"
    except Exception as e:
        return False, str(e)
