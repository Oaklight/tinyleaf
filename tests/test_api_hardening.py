"""Tests for API hardening: envelopes, request ids, headers, browse roots (#114)."""

import asyncio
import json
import subprocess

import pytest

from tinyleaf import handlers, server
from tinyleaf._vendor.httpserver import HTTPException, Request, Response
from tinyleaf.server import APIError


def _request(method="GET", path="/", headers=None, query_string=""):
    lowered = {key.lower(): value for key, value in (headers or {}).items()}
    lowered.setdefault("host", "127.0.0.1:14159")
    return Request(method, path, query_string, lowered, b"", ("127.0.0.1", 1234), server.app)


def _json(response):
    return json.loads(response.body)


class TestRequestId:
    def test_generated(self):
        request = _request()
        server.assign_request_id(request)
        assert len(request.state.request_id) == 16

    def test_valid_client_id_preserved(self):
        request = _request(headers={"X-Request-Id": "abc-123"})
        server.assign_request_id(request)
        assert request.state.request_id == "abc-123"

    def test_invalid_client_id_replaced(self):
        request = _request(headers={"X-Request-Id": "bad id!"})
        server.assign_request_id(request)
        assert request.state.request_id != "bad id!"


class TestResponseHeaders:
    def test_security_headers_and_request_id(self):
        request = _request()
        server.assign_request_id(request)
        response = Response(body=b"ok")

        server.add_response_headers(request, response)

        assert response.headers["X-Request-Id"] == request.state.request_id
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["X-Frame-Options"] == "DENY"
        assert response.headers["Referrer-Policy"] == "no-referrer"
        assert "camera=()" in response.headers["Permissions-Policy"]
        csp = response.headers["Content-Security-Policy"]
        assert "frame-ancestors 'none'" in csp
        assert "default-src 'self'" in csp

    def test_static_and_404_dispatch_include_headers(self):
        static_request = _request(path="/static/css/app.css")
        static_response = asyncio.run(server.app._dispatch(static_request))
        server.add_response_headers(static_request, static_response)
        assert static_response.status_code == 200
        assert static_response.headers["X-Content-Type-Options"] == "nosniff"
        assert static_response.headers["X-Request-Id"] == static_request.state.request_id

        missing_request = _request(path="/no-such-route")
        missing_response = asyncio.run(server.app._dispatch(missing_request))
        server.add_response_headers(missing_request, missing_response)
        body = _json(missing_response)
        assert missing_response.status_code == 404
        assert body["code"] == "not_found"
        assert body["request_id"] == missing_request.state.request_id
        assert missing_response.headers["X-Frame-Options"] == "DENY"


class TestErrorEnvelope:
    def test_http_exception(self):
        request = _request()
        server.assign_request_id(request)

        response = server.handle_http_exception(request, HTTPException(404, "Nothing here"))

        assert response.status_code == 404
        assert _json(response) == {
            "error": "Nothing here",
            "code": "not_found",
            "detail": None,
            "request_id": request.state.request_id,
        }

    def test_api_error_keeps_code_and_detail(self):
        request = _request()
        server.assign_request_id(request)
        error = APIError(
            503,
            "texcount not found",
            "dependency_missing",
            {"dependency": "texcount"},
        )

        response = server.handle_http_exception(request, error)

        body = _json(response)
        assert response.status_code == 503
        assert body["code"] == "dependency_missing"
        assert body["detail"] == {"dependency": "texcount"}

    def test_unexpected_exception_is_500(self):
        request = _request()
        server.assign_request_id(request)

        response = server.handle_unexpected_exception(request, RuntimeError("boom"))

        body = _json(response)
        assert response.status_code == 500
        assert body["code"] == "internal_error"
        assert body["error"] == "Internal Server Error"


class TestMetadataRoutes:
    def test_health_and_version(self, monkeypatch):
        monkeypatch.setattr(server, "_config", {"mode": "multi"})

        health = server.api_health(None)
        assert health["status"] == "ok"
        assert health["mode"] == "multi"
        assert "config_dir" not in health
        assert "project_path" not in health

        assert server.api_version(None) == {
            "name": "tinyleaf",
            "version": server.__version__,
        }

    def test_schema_lists_api_routes(self, monkeypatch):
        monkeypatch.setattr(server, "_config", {"mode": "multi"})

        schema = server.api_schema(None)
        paths = {(item["method"], item["path"]) for item in schema["routes"]}

        assert ("GET", "/api/health") in paths
        assert ("GET", "/api/version") in paths
        assert ("GET", "/api/projects/{name}/files") in paths
        assert ("GET", "/api/projects/{name}/files/{file_path}") in paths
        assert schema["auth_required"] is False


class TestBrowseRoots:
    def test_inside_root(self, tmp_path):
        root = tmp_path / "root"
        (root / "sub").mkdir(parents=True)

        result = handlers.handle_browse_filesystem(
            {"path": [str(root)]}, {"browse_roots": [str(root)]}
        )

        assert result["path"] == str(root)
        assert result["dirs"] == ["sub"]

    def test_outside_root_rejected(self, tmp_path):
        root = tmp_path / "root"
        root.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()

        with pytest.raises(HTTPException) as excinfo:
            handlers.handle_browse_filesystem(
                {"path": [str(outside)]}, {"browse_roots": [str(root)]}
            )

        assert excinfo.value.status_code == 403

    def test_mixed_prefix_sibling_rejected(self, tmp_path):
        root = tmp_path / "proj"
        root.mkdir()
        sibling = tmp_path / "proj-secret"
        sibling.mkdir()

        with pytest.raises(HTTPException) as excinfo:
            handlers.handle_browse_filesystem(
                {"path": [str(sibling)]}, {"browse_roots": [str(root)]}
            )

        assert excinfo.value.status_code == 403

    def test_symlink_escape_rejected(self, tmp_path):
        root = tmp_path / "root"
        root.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        (root / "link").symlink_to(outside, target_is_directory=True)

        with pytest.raises(HTTPException) as excinfo:
            handlers.handle_browse_filesystem(
                {"path": [str(root / "link")]}, {"browse_roots": [str(root)]}
            )

        assert excinfo.value.status_code == 403


def _single_config(tmp_path):
    return {
        "mode": "single",
        "project_path": str(tmp_path),
        "config_dir": str(tmp_path),
        "use_docker": False,
        "docker_image": "oaklight/texlive:latest",
    }


class TestDependencyErrors:
    def test_missing_texcount_is_dependency_missing(self, tmp_path, monkeypatch):
        (tmp_path / "main.tex").write_text("\\documentclass{article}", encoding="utf-8")

        def raise_missing(*args, **kwargs):
            raise FileNotFoundError("texcount")

        monkeypatch.setattr(handlers.subprocess, "run", raise_missing)

        with pytest.raises(APIError) as excinfo:
            handlers.handle_word_count(_single_config(tmp_path), "project")

        assert excinfo.value.status_code == 503
        assert excinfo.value.code == "dependency_missing"
        assert excinfo.value.detail["dependency"] == "texcount"
        assert "hint" in excinfo.value.detail

    def test_texcount_timeout_is_504(self, tmp_path, monkeypatch):
        (tmp_path / "main.tex").write_text("\\documentclass{article}", encoding="utf-8")

        def raise_timeout(*args, **kwargs):
            raise subprocess.TimeoutExpired(cmd="texcount", timeout=30)

        monkeypatch.setattr(handlers.subprocess, "run", raise_timeout)

        with pytest.raises(APIError) as excinfo:
            handlers.handle_word_count(_single_config(tmp_path), "project")

        assert excinfo.value.status_code == 504
        assert excinfo.value.code == "timeout"

    def test_texcount_failure_is_processing_failed(self, tmp_path, monkeypatch):
        (tmp_path / "main.tex").write_text("\\documentclass{article}", encoding="utf-8")

        class Result:
            returncode = 1
            stdout = ""
            stderr = "TeX syntax error"

        monkeypatch.setattr(handlers.subprocess, "run", lambda *args, **kwargs: Result())

        with pytest.raises(APIError) as excinfo:
            handlers.handle_word_count(_single_config(tmp_path), "project")

        assert excinfo.value.status_code == 422
        assert excinfo.value.code == "processing_failed"
        assert excinfo.value.detail["stderr"] == "TeX syntax error"

    def test_synctex_parse_error_is_processing_failed(self, tmp_path, monkeypatch):
        (tmp_path / "main.tex").write_text("x", encoding="utf-8")
        (tmp_path / "main.synctex.gz").write_bytes(b"garbage")
        (tmp_path / ".tinyleaf.json").write_text(
            json.dumps({"main_file": "main.tex"}), encoding="utf-8"
        )

        def raise_corrupt(*args, **kwargs):
            raise ValueError("corrupt synctex")

        monkeypatch.setattr(handlers.synctex, "parse_synctex", raise_corrupt)

        with pytest.raises(APIError) as excinfo:
            handlers.handle_synctex_query(
                {"page": ["1"], "x": ["10"], "y": ["20"]},
                _single_config(tmp_path),
                "project",
            )

        assert excinfo.value.status_code == 422
        assert excinfo.value.code == "processing_failed"
