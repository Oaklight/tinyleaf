"""Tests for the manual Docker pull progress endpoint (issue #94)."""

import pytest

from tinyleaf import compiler, handlers
from tinyleaf._vendor.httpserver import HTTPException

IMAGE = "oaklight/texlive:alpine-science-cn"


@pytest.fixture
def config(tmp_path):
    return {
        "mode": "single",
        "project_path": str(tmp_path),
        "use_docker": True,
        "docker_image": IMAGE,
    }


def test_unknown_pull_state(config):
    compiler._pull_states.pop(IMAGE, None)

    assert handlers.handle_docker_pull_status({"image": [IMAGE]}, config) == {
        "known": False,
        "image": IMAGE,
    }


def test_progress_state_reported(config):
    compiler.reset_pull_state(IMAGE)
    compiler._record_pull_line(IMAGE, "abc123: Pull complete")
    result = handlers.handle_docker_pull_status({"image": [IMAGE]}, config)
    compiler._pull_states.pop(IMAGE, None)

    assert result["known"] is True
    assert result["done"] is False
    assert result["layers_done"] == 1
    assert result["lines"] == ["abc123: Pull complete"]
    assert "elapsed" in result


def test_finished_state_reported(config):
    compiler.reset_pull_state(IMAGE)
    compiler._finish_pull_state(IMAGE, True, "OK")
    result = handlers.handle_docker_pull_status({"image": [IMAGE]}, config)
    compiler._pull_states.pop(IMAGE, None)

    assert result["done"] is True
    assert result["success"] is True
    assert result["message"] == "OK"


def test_status_rejects_unknown_image(config):
    with pytest.raises(HTTPException) as exc:
        handlers.handle_docker_pull_status({"image": ["attacker/evil:latest"]}, config)
    assert exc.value.status_code == 400


def test_status_requires_image(config):
    with pytest.raises(HTTPException) as exc:
        handlers.handle_docker_pull_status({}, config)
    assert exc.value.status_code == 400
