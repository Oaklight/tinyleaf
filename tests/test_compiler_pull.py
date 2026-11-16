"""Tests for Docker image pull ordering and mirror fallback."""

import asyncio
import os

from tinyleaf import compiler

IMAGE = "oaklight/texlive:alpine-science-cn"


def _fake_docker(tmp_path):
    bindir = tmp_path / "bin"
    bindir.mkdir()
    docker = bindir / "docker"
    docker.write_text(
        """#!/bin/sh
echo "$@" >> "$DLOG"
if [ "$1" = "image" ]; then
  if [ -f "$DSTATE" ]; then exit 0; else exit 1; fi
fi
if [ "$1" = "pull" ]; then
  case "$*" in
    *"mirror.local/"*)
      if [ "$MIRROR_FAILS" = "1" ]; then exit 1; fi
      ;;
  esac
  touch "$DSTATE"
  echo "abc123: Pull complete"
  echo "pulled $*"
  exit 0
fi
exit 0
""",
        encoding="utf-8",
    )
    docker.chmod(0o755)
    return bindir, tmp_path / "calls.log", tmp_path / "pulled.state"


def _env(monkeypatch, bindir, calls, state, mirror_fails):
    monkeypatch.setenv("PATH", f"{bindir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("DLOG", str(calls))
    monkeypatch.setenv("DSTATE", str(state))
    monkeypatch.setenv("MIRROR_FAILS", "1" if mirror_fails else "0")


def _calls(path):
    return path.read_text(encoding="utf-8").splitlines()


def test_image_is_pulled_before_latexmk_probe(tmp_path, monkeypatch):
    bindir, calls_log, state = _fake_docker(tmp_path)
    _env(monkeypatch, bindir, calls_log, state, mirror_fails=False)

    project = tmp_path / "project"
    project.mkdir()
    (project / "main.tex").write_text(
        "\\documentclass{article}\\begin{document}x\\end{document}\n",
        encoding="utf-8",
    )

    async def run_compile():
        compile_id = await compiler.start_compile(
            project_dir=str(project),
            main_file="main.tex",
            engine="pdflatex",
            use_docker=True,
            docker_image=IMAGE,
        )
        job = compiler.get_job(compile_id)
        try:
            await asyncio.wait_for(job.wait(), timeout=30)
        finally:
            compiler._jobs.pop(compile_id, None)
        return job

    asyncio.run(run_compile())
    calls = _calls(calls_log)

    pull_index = next(i for i, call in enumerate(calls) if call.startswith("pull "))
    first_run_index = next(i for i, call in enumerate(calls) if call.startswith("run "))

    assert calls[0] == f"image inspect {IMAGE}"
    assert pull_index < first_run_index
    assert sum(1 for call in calls if call.startswith("pull ")) == 1
    # The probe now succeeds, so the compile uses one latexmk invocation
    # instead of the four-step fallback.
    assert any("latexmk -pdf" in call for call in calls)
    assert not any("bibtex" in call for call in calls)


def test_mirror_failure_falls_back_to_default_registry(tmp_path, monkeypatch):
    bindir, calls_log, state = _fake_docker(tmp_path)
    _env(monkeypatch, bindir, calls_log, state, mirror_fails=True)

    success, message = asyncio.run(
        compiler.docker_pull_image(IMAGE, registry_mirror="mirror.local")
    )
    calls = _calls(calls_log)

    assert (success, message) == (True, "OK")
    assert f"pull mirror.local/{IMAGE}" in calls
    assert f"pull {IMAGE}" in calls
    assert not any(call.startswith("tag ") for call in calls)


def test_mirror_success_retags_image(tmp_path, monkeypatch):
    bindir, calls_log, state = _fake_docker(tmp_path)
    _env(monkeypatch, bindir, calls_log, state, mirror_fails=False)

    success, message = asyncio.run(
        compiler.docker_pull_image(IMAGE, registry_mirror="mirror.local")
    )
    calls = _calls(calls_log)

    assert (success, message) == (True, "OK")
    assert f"pull mirror.local/{IMAGE}" in calls
    assert f"tag mirror.local/{IMAGE} {IMAGE}" in calls
    assert f"rmi mirror.local/{IMAGE}" in calls


def test_no_mirror_pulls_once(tmp_path, monkeypatch):
    bindir, calls_log, state = _fake_docker(tmp_path)
    _env(monkeypatch, bindir, calls_log, state, mirror_fails=False)

    success, message = asyncio.run(compiler.docker_pull_image(IMAGE))
    calls = _calls(calls_log)

    assert (success, message) == (True, "OK")
    assert [call for call in calls if call.startswith("pull ")] == [f"pull {IMAGE}"]


def test_pull_progress_state_is_recorded(tmp_path, monkeypatch):
    bindir, calls_log, state = _fake_docker(tmp_path)
    _env(monkeypatch, bindir, calls_log, state, mirror_fails=False)
    compiler._pull_states.pop(IMAGE, None)

    try:
        success, message = asyncio.run(compiler.docker_pull_image(IMAGE))
        record = compiler.get_pull_state(IMAGE)
    finally:
        compiler._pull_states.pop(IMAGE, None)

    assert (success, message) == (True, "OK")
    assert record["done"] is True
    assert record["success"] is True
    assert record["layers_done"] == 1
    assert any("Pull complete" in line for line in record["lines"])
    assert record["finished_at"] >= record["started_at"]
