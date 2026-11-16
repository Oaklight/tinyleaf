"""Tests for compile-job lifecycle helpers."""

from tinyleaf import compiler


class _FakeProc:
    def __init__(self):
        self.returncode = None
        self.killed = False

    def kill(self):
        self.killed = True
        self.returncode = -9


def _make_job(name="t-shutdown"):
    return compiler.CompileJob(
        name,
        "/tmp",
        "main.tex",
        "pdflatex",
        use_docker=True,
        docker_image="oaklight/texlive:alpine-science-cn",
    )


def test_shutdown_all_cancels_running_jobs_and_pulls():
    job = _make_job()
    proc = _FakeProc()
    compiler._jobs[job.compile_id] = job
    compiler._pull_procs["oaklight/texlive:alpine-science-cn"] = proc
    try:
        compiler.shutdown_all()

        assert job.status == "cancelled"
        assert job.is_done
        assert proc.killed
        assert "oaklight/texlive:alpine-science-cn" not in compiler._pull_procs
    finally:
        compiler._jobs.pop(job.compile_id, None)
        compiler._pull_procs.pop("oaklight/texlive:alpine-science-cn", None)


def test_shutdown_all_leaves_finished_jobs_alone():
    job = _make_job("t-finished")
    job.finish("success")
    compiler._jobs[job.compile_id] = job
    try:
        compiler.shutdown_all()

        assert job.status == "success"
    finally:
        compiler._jobs.pop(job.compile_id, None)


def test_shutdown_all_ignores_exited_pull_process():
    proc = _FakeProc()
    proc.returncode = 0
    compiler._pull_procs["done-image"] = proc
    try:
        compiler.shutdown_all()

        assert not proc.killed
        assert "done-image" not in compiler._pull_procs
    finally:
        compiler._pull_procs.pop("done-image", None)
