"""Tests for API origin policy and Docker image allow-list."""

import asyncio

import pytest

from tinyleaf import cli, handlers
from tinyleaf._vendor.httpserver import HTTPException


@pytest.fixture
def config(tmp_path):
    project = tmp_path / "proj"
    project.mkdir()
    (project / "main.tex").write_text(
        "\\documentclass{article}\\begin{document}x\\end{document}\n",
        encoding="utf-8",
    )
    return {
        "mode": "single",
        "project_path": str(project),
        "config_dir": str(tmp_path / "cfg"),
        "use_docker": True,
        "docker_image": "oaklight/texlive:alpine-science-cn",
    }


def test_known_images_are_allowed(config):
    assert handlers._validate_docker_image("oaklight/texlive:alpine-science", config)
    assert handlers._validate_docker_image(config["docker_image"], config)


def test_arbitrary_image_is_rejected(config):
    with pytest.raises(HTTPException) as exc:
        handlers._validate_docker_image("attacker/evil:latest", config)
    assert exc.value.status_code == 400


def test_pull_rejects_arbitrary_image(config):
    with pytest.raises(HTTPException) as exc:
        asyncio.run(handlers.handle_docker_pull({"image": "attacker/evil:latest"}, config))
    assert exc.value.status_code == 400


def test_compile_rejects_arbitrary_image(config):
    with pytest.raises(HTTPException) as exc:
        asyncio.run(
            handlers.handle_compile(
                {"docker_image": "attacker/evil:latest", "use_docker": True},
                config,
                "proj",
            )
        )
    assert exc.value.status_code == 400


def test_put_config_rejects_arbitrary_image(config):
    with pytest.raises(HTTPException) as exc:
        handlers.handle_put_config({"docker_image": "attacker/evil:latest"}, config, "proj")
    assert exc.value.status_code == 400


def test_default_image_from_server_config_is_allowed(tmp_path):
    project = tmp_path / "proj"
    project.mkdir()
    config = {
        "mode": "single",
        "project_path": str(project),
        "use_docker": True,
        "docker_image": "my/private-texlive:2026",
    }
    assert handlers._validate_docker_image("my/private-texlive:2026", config)


def test_server_sends_no_cors_headers():
    from tinyleaf import server
    from tinyleaf._vendor.httpserver import Request, Response

    request = Request("GET", "/", "", {}, b"", ("127.0.0.1", 1), server.app)
    response = Response(body=b"ok")
    for hook in server.app._after_request_handlers:
        hook(request, response)
    for hook in server.app._on_response_started_handlers:
        hook(request, response)
    assert "Access-Control-Allow-Origin" not in response.headers


@pytest.mark.parametrize(
    "host, expected",
    [
        ("127.0.0.1", True),
        ("::1", True),
        ("localhost", True),
        ("0.0.0.0", False),
        ("::", False),
        ("192.168.1.10", False),
    ],
)
def test_is_loopback(host, expected):
    assert cli._is_loopback(host) is expected
