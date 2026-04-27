"""Compilation backend for tinyleaf.

Supports local latexmk and Docker-based compilation.
"""

import os
import subprocess
import threading
import uuid


class CompileJob:
    """Tracks a single compilation run."""

    def __init__(self, compile_id, project_dir, main_file, engine, use_docker, docker_image):
        self.compile_id = compile_id
        self.project_dir = project_dir
        self.main_file = main_file
        self.engine = engine
        self.use_docker = use_docker
        self.docker_image = docker_image
        self.log_lines = []
        self.status = "running"  # running | success | error
        self.pdf_path = None
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

    @property
    def is_done(self):
        return self._done_event.is_set()


# Global compile job registry
_jobs: dict[str, CompileJob] = {}
_jobs_lock = threading.Lock()


def get_job(compile_id):
    with _jobs_lock:
        return _jobs.get(compile_id)


def start_compile(
    project_dir,
    main_file="main.tex",
    engine="pdflatex",
    use_docker=False,
    docker_image="oaklight/texlive:latest",
):
    """Start a compilation and return the compile_id.

    Args:
        project_dir: Absolute path to the project directory.
        main_file: Main .tex file relative to project_dir.
        engine: Compilation engine (pdflatex, lualatex, xelatex).
        use_docker: Whether to use Docker for compilation.
        docker_image: Docker image to use.

    Returns:
        compile_id string.
    """
    compile_id = uuid.uuid4().hex[:12]
    job = CompileJob(compile_id, project_dir, main_file, engine, use_docker, docker_image)

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

        for line in proc.stdout:
            line = line.rstrip("\n")
            level = _classify_log_line(line)
            job.append_log(line, level=level)

        proc.wait()

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
