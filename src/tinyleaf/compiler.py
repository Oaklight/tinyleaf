"""Compilation backend for tinyleaf.

Supports local latexmk and Docker-based compilation.
"""

import os
import subprocess
import threading
import uuid


class CompileJob:
    """Tracks a single compilation run."""

    def __init__(self, compile_id, project_dir, main_file, engine, use_docker, docker_image,
                 registry_mirror=None):
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
        self.proc = None  # subprocess.Popen reference for cancellation
        self._cancelled = False
        self._lock = threading.Lock()
        self._done_event = threading.Event()

    def append_log(self, line, level="info"):
        with self._lock:
            self.log_lines.append({"line": line, "level": level})

    def get_logs_from(self, index):
        with self._lock:
            return list(self.log_lines[index:])

    def finish(self, status, pdf_path=None):
        self.status = status
        self.pdf_path = pdf_path
        self._done_event.set()

    def wait(self, timeout=None):
        self._done_event.wait(timeout)

    def cancel(self):
        """Cancel this compilation by killing the subprocess."""
        self._cancelled = True
        if self.proc and self.proc.poll() is None:
            self.proc.kill()
        self.append_log("Cancelled by user.", level="warning")
        self.finish("cancelled")

    @property
    def is_cancelled(self):
        return self._cancelled

    @property
    def is_done(self):
        return self._done_event.is_set()


# Global compile job registry
_jobs: dict[str, CompileJob] = {}
_jobs_lock = threading.Lock()


def get_job(compile_id):
    with _jobs_lock:
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


def start_compile(
    project_dir,
    main_file="main.tex",
    engine="pdflatex",
    use_docker=False,
    docker_image="oaklight/texlive:latest",
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
    job = CompileJob(compile_id, project_dir, main_file, engine, use_docker, docker_image,
                     registry_mirror=registry_mirror)

    with _jobs_lock:
        _jobs[compile_id] = job

    thread = threading.Thread(target=_run_compile, args=(job,), daemon=True)
    thread.start()
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
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
        main_file,
    ]


def _run_compile(job: CompileJob):
    """Run the compilation in a background thread."""
    try:
        latexmk_args = _build_latexmk_args(job.engine, job.main_file)

        if job.use_docker:
            # Auto-pull image if not available locally
            if not _docker_image_exists(job.docker_image):
                if job.is_cancelled:
                    return
                if not _docker_pull(job, job.docker_image, job.registry_mirror):
                    return  # pull failed, job already finished with error

            if job.is_cancelled:
                return

            cmd = [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{job.project_dir}:/workspace",
                "-w",
                "/workspace",
                job.docker_image,
            ] + latexmk_args
        else:
            cmd = latexmk_args

        job.append_log(f"$ {' '.join(cmd)}", level="info")

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=job.project_dir if not job.use_docker else None,
            text=True,
            bufsize=1,
        )
        job.proc = proc

        for line in proc.stdout:
            if job.is_cancelled:
                break
            line = line.rstrip("\n")
            level = _classify_log_line(line)
            job.append_log(line, level=level)

        proc.wait()

        if job.is_cancelled:
            return

        # Find output PDF
        base = os.path.splitext(job.main_file)[0]
        pdf_name = base + ".pdf"
        pdf_full = os.path.join(job.project_dir, pdf_name)

        if proc.returncode == 0 and os.path.exists(pdf_full):
            job.finish("success", pdf_path=pdf_name)
        else:
            job.append_log(
                f"Compilation failed (exit code {proc.returncode})",
                level="error",
            )
            # Still report PDF if it was partially generated
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


def _docker_image_exists(image):
    """Check if a Docker image exists locally."""
    try:
        result = subprocess.run(
            ["docker", "image", "inspect", image],
            capture_output=True, timeout=10,
        )
        return result.returncode == 0
    except Exception:
        return False


def _docker_pull(job, image, registry_mirror=None):
    """Pull a Docker image, streaming output to the compile job log.

    If registry_mirror is set, pulls from the mirror and retags to the
    original name.

    Returns:
        True if pull succeeded, False otherwise.
    """
    if registry_mirror:
        # e.g. "oaklight/texlive:tag" -> "docker.1ms.run/oaklight/texlive:tag"
        pull_image = f"{registry_mirror}/{image}"
        job.append_log(f"Image '{image}' not found locally, pulling from mirror {registry_mirror}...")
    else:
        pull_image = image
        job.append_log(f"Image '{image}' not found locally, pulling...")

    try:
        proc = subprocess.Popen(
            ["docker", "pull", pull_image],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1,
        )
        job.proc = proc

        for line in proc.stdout:
            if job.is_cancelled:
                proc.kill()
                proc.wait()
                return False
            job.append_log(line.rstrip("\n"))
        proc.wait()

        if job.is_cancelled:
            return False

        if proc.returncode != 0:
            job.append_log(f"Failed to pull image '{pull_image}'", level="error")
            job.finish("error")
            return False

        # Retag if pulled from mirror
        if registry_mirror and pull_image != image:
            subprocess.run(["docker", "tag", pull_image, image], timeout=10)
            subprocess.run(["docker", "rmi", pull_image], capture_output=True, timeout=10)
            job.append_log(f"Retagged '{pull_image}' -> '{image}'")

        job.append_log("Image ready.")
        return True

    except Exception as e:
        job.append_log(f"Pull error: {e}", level="error")
        job.finish("error")
        return False


def docker_pull_image(image, registry_mirror=None):
    """Pull a Docker image (standalone, not tied to a compile job).

    Args:
        image: Full image name (e.g. "oaklight/texlive:alpine-science-cn").
        registry_mirror: Optional registry mirror host.

    Returns:
        Tuple of (success: bool, message: str).
    """
    if registry_mirror:
        pull_image = f"{registry_mirror}/{image}"
    else:
        pull_image = image

    try:
        proc = subprocess.Popen(
            ["docker", "pull", pull_image],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True,
        )
        with _pull_procs_lock:
            _pull_procs[image] = proc

        output_lines = []
        for line in proc.stdout:
            output_lines.append(line)
        proc.wait()

        with _pull_procs_lock:
            _pull_procs.pop(image, None)

        if proc.returncode != 0:
            stderr = "".join(output_lines).strip()
            if proc.returncode == -9 or proc.returncode == -15:
                return False, "Cancelled"
            return False, stderr or "Pull failed"

        if registry_mirror and pull_image != image:
            subprocess.run(["docker", "tag", pull_image, image], timeout=10)
            subprocess.run(["docker", "rmi", pull_image], capture_output=True, timeout=10)

        return True, "OK"
    except subprocess.TimeoutExpired:
        return False, "Pull timed out"
    except Exception as e:
        with _pull_procs_lock:
            _pull_procs.pop(image, None)
        return False, str(e)


# Track standalone pull processes for cancellation
_pull_procs: dict[str, subprocess.Popen] = {}
_pull_procs_lock = threading.Lock()


def cancel_docker_pull(image):
    """Cancel a running standalone docker pull.

    Returns:
        True if a pull was found and killed, False otherwise.
    """
    with _pull_procs_lock:
        proc = _pull_procs.pop(image, None)
    if proc and proc.poll() is None:
        proc.kill()
        return True
    return False


def docker_remove_image(image):
    """Remove a local Docker image.

    Args:
        image: Full image name to remove.

    Returns:
        Tuple of (success: bool, message: str).
    """
    try:
        result = subprocess.run(
            ["docker", "rmi", image],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            return True, "OK"
        return False, result.stderr.strip() or "Remove failed"
    except Exception as e:
        return False, str(e)
