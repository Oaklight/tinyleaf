"""Compilation backend for tinyleaf.

Supports local latexmk and Docker-based compilation.
"""

import asyncio
import os
import time
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


def _docker_run_prefix(project_dir, image):
    """Build the ``docker run`` arguments used for compilation.

    The container runs as the invoking user so it does not leave root-owned
    output files in the bind-mounted project. ``HOME`` points at the writable
    container ``/tmp`` because the image has no home for an arbitrary uid.
    Platforms without ``os.getuid`` (Windows) keep the image default user.
    """
    prefix = ["docker", "run", "--rm"]
    if hasattr(os, "getuid"):
        prefix += ["--user", f"{os.getuid()}:{os.getgid()}", "-e", "HOME=/tmp"]
    prefix += [
        "-v",
        f"{project_dir}:/workspace",
        "-w",
        "/workspace",
        image,
    ]
    return prefix


async def _run_compile(job: CompileJob):
    """Run the compilation as an async task.

    Cancellation is cooperative via job._cancelled flag + proc.kill(),
    not via asyncio task cancellation, so CancelledError won't bypass
    the except handler.
    """
    try:
        # Ensure the image is present before probing for latexmk. `docker run`
        # implicitly pulls a missing image, and the probe's 15s timeout would
        # kill that pull, then the explicit pull would start over.
        if job.use_docker:
            if not await _docker_image_exists(job.docker_image):
                if job.is_cancelled:
                    return
                if not await _docker_pull(job, job.docker_image, job.registry_mirror):
                    return
            if job.is_cancelled:
                return

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
            docker_prefix = _docker_run_prefix(job.project_dir, job.docker_image)
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
    """Check if latexmk is available (in Docker or locally).

    When Docker is in use this must not trigger a pull: `docker run` on a
    missing image pulls implicitly, which is exactly the behaviour the
    compile flow now avoids.
    """
    try:
        if job.use_docker and not await _docker_image_exists(job.docker_image):
            return False
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


async def _retag_image(pull_image, image):
    """Retag a mirror-pulled image to its canonical name and drop the mirror tag."""
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


async def _docker_pull(job, image, registry_mirror=None):
    """Pull a Docker image, streaming output to the compile job log.

    Tries the configured mirror first, then the default registry. A slow or
    broken mirror therefore cannot block the first compile.

    Returns:
        True if pull succeeded, False otherwise.
    """
    candidates = []
    if registry_mirror:
        candidates.append((f"{registry_mirror}/{image}", True))
    candidates.append((image, False))

    for pull_image, via_mirror in candidates:
        if job.is_cancelled:
            return False

        if via_mirror:
            job.append_log(
                f"Image '{image}' not found locally, pulling from mirror {registry_mirror}..."
            )
        elif registry_mirror:
            job.append_log(
                f"Pull from mirror failed; retrying '{image}' from the default registry...",
                level="warning",
            )
        else:
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
        except Exception as e:
            job.append_log(f"Pull error: {e}", level="error")
            job.finish("error")
            return False

        if job.is_cancelled:
            return False

        if proc.returncode == 0:
            if via_mirror:
                await _retag_image(pull_image, image)
                job.append_log(f"Retagged '{pull_image}' -> '{image}'")
            job.append_log("Image ready.")
            return True

        job.append_log(f"Failed to pull image '{pull_image}'", level="error")

    job.finish("error")
    return False


async def docker_pull_image(image, registry_mirror=None):
    """Pull a Docker image (standalone, not tied to a compile job).

    Tries the configured mirror first, then the default registry.

    Returns:
        Tuple of (success: bool, message: str).
    """
    reset_pull_state(image)

    candidates = []
    if registry_mirror:
        candidates.append((f"{registry_mirror}/{image}", True))
    candidates.append((image, False))

    last_error = "Pull failed"
    for pull_image, via_mirror in candidates:
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
                line = raw_line.decode("utf-8", errors="replace").rstrip("\n")
                output_lines.append(line + "\n")
                _record_pull_line(image, line)
            await proc.wait()

            _pull_procs.pop(image, None)

            if proc.returncode != 0:
                if proc.returncode in (-9, -15):
                    _finish_pull_state(image, False, "Cancelled")
                    return False, "Cancelled"
                last_error = "".join(output_lines).strip() or "Pull failed"
                continue

            if via_mirror:
                await _retag_image(pull_image, image)

            _finish_pull_state(image, True, "OK")
            return True, "OK"
        except asyncio.TimeoutError:
            _pull_procs.pop(image, None)
            last_error = "Pull timed out"
        except Exception as e:
            _pull_procs.pop(image, None)
            last_error = str(e)

    _finish_pull_state(image, False, last_error)
    return False, last_error


# Track standalone pull processes for cancellation
_pull_procs: dict[str, asyncio.subprocess.Process] = {}

# Progress state for the manual pull endpoint (single-threaded asyncio).
_pull_states: dict[str, dict] = {}


def reset_pull_state(image):
    """Start a fresh progress record for a manual image pull."""
    _pull_states[image] = {
        "image": image,
        "lines": [],
        "layers_done": 0,
        "done": False,
        "success": None,
        "message": "",
        "started_at": time.time(),
        "finished_at": None,
    }


def get_pull_state(image):
    """Return the progress record for *image*, or None."""
    return _pull_states.get(image)


def _record_pull_line(image, line):
    state = _pull_states.get(image)
    if state is None:
        return
    lines = state["lines"]
    lines.append(line)
    if len(lines) > 200:
        del lines[:-200]
    if "Pull complete" in line:
        state["layers_done"] += 1


def _finish_pull_state(image, success, message):
    state = _pull_states.get(image)
    if state is None:
        return
    state["done"] = True
    state["success"] = success
    state["message"] = message
    state["finished_at"] = time.time()


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


def shutdown_all():
    """Cancel every running compile job and image pull.

    Registered as a server shutdown hook so child processes do not outlive
    the HTTP server (zerodep httpserver ``on_shutdown`` signal).
    """
    for job in list(_jobs.values()):
        if not job.is_done:
            job.cancel()
    for image in list(_pull_procs):
        proc = _pull_procs.pop(image, None)
        if proc is not None and proc.returncode is None:
            proc.kill()


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
