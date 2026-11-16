"""Tests for CLI automation and the mutation audit log (#116)."""

import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path

from tinyleaf import cli, server
from tinyleaf._vendor.httpserver import Request, Response


def _request(method="POST", path="/api/projects", headers=None, request_id="rid-123"):
    lowered = {key.lower(): value for key, value in (headers or {}).items()}
    lowered.setdefault("host", "127.0.0.1:14159")
    request = Request(method, path, "", lowered, b"", ("127.0.0.1", 1234), server.app)
    request.state.started_at = time.monotonic() - 0.01
    request.state.request_id = request_id
    return request


class TestPortResolution:
    def test_zero_resolves_to_free_port(self):
        port = cli._resolve_port("127.0.0.1", 0)
        assert port > 0

    def test_explicit_port_is_kept(self):
        assert cli._resolve_port("127.0.0.1", 41234) == 41234


class TestStartupPayload:
    def test_shape(self):
        payload = cli._startup_payload(
            "multi", "http://127.0.0.1:14159", "127.0.0.1", 14159, True, "/cfg", False
        )

        assert set(payload) == {
            "status",
            "mode",
            "url",
            "host",
            "port",
            "pid",
            "version",
            "docker",
            "config_dir",
            "read_only",
        }
        assert payload["status"] == "ok"
        assert payload["pid"] == os.getpid()
        assert payload["docker"] is True
        assert payload["read_only"] is False
        assert json.loads(json.dumps(payload)) == payload


class TestPidFile:
    def test_write_and_remove(self, tmp_path):
        path = tmp_path / "tinyleaf.pid"

        cli._write_pid_file(str(path))
        assert path.read_text(encoding="utf-8") == f"{os.getpid()}\n"

        cli._remove_pid_file(str(path))
        assert not path.exists()

    def test_remove_missing_is_noop(self, tmp_path):
        cli._remove_pid_file(str(tmp_path / "missing.pid"))


class TestLogging:
    def test_log_file_receives_audit_lines(self, tmp_path):
        log_path = tmp_path / "tinyleaf.log"
        code = (
            "import logging; from tinyleaf.cli import _configure_logging; "
            f"_configure_logging({str(log_path)!r}, 'INFO'); "
            "logging.getLogger('tinyleaf.audit').info('mutation method=POST path=/x')"
        )
        env = dict(os.environ)
        env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")

        subprocess.run([sys.executable, "-c", code], check=True, env=env)

        assert "mutation method=POST path=/x" in log_path.read_text(encoding="utf-8")


class TestAuditHook:
    def test_mutation_is_logged(self, caplog):
        caplog.set_level(logging.INFO, logger="tinyleaf.audit")

        server.audit_mutation(_request(), Response(body=b"ok", status_code=201))

        record = caplog.records[-1]
        assert record.name == "tinyleaf.audit"
        assert "mutation method=POST" in record.getMessage()
        assert "path=/api/projects" in record.getMessage()
        assert "status=201" in record.getMessage()
        assert "request_id=rid-123" in record.getMessage()
        assert "duration_ms=" in record.getMessage()
        assert "client=127.0.0.1" in record.getMessage()

    def test_get_is_not_logged(self, caplog):
        caplog.set_level(logging.INFO, logger="tinyleaf.audit")

        server.audit_mutation(_request(method="GET", path="/api/projects"), Response(body=b"ok"))

        assert not [record for record in caplog.records if "mutation " in record.getMessage()]

    def test_body_and_query_are_not_logged(self, caplog):
        caplog.set_level(logging.INFO, logger="tinyleaf.audit")
        request = Request(
            "POST",
            "/api/projects",
            "token=secret-value",
            {"host": "127.0.0.1:14159"},
            b'{"content": "secret body"}',
            ("127.0.0.1", 1234),
            server.app,
        )
        request.state.started_at = time.monotonic()
        request.state.request_id = "rid-1"

        server.audit_mutation(request, Response(body=b"ok"))

        message = caplog.records[-1].getMessage()
        assert "secret-value" not in message
        assert "secret body" not in message
