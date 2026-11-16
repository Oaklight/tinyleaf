"""Tests for token auth, host allow-list, read-only, and Origin checks (#115)."""

import json

import pytest

from tinyleaf import cli, server
from tinyleaf._vendor.httpserver import Request

TOKEN = "s3cret-token"


def _request(method="GET", path="/api/projects", headers=None, body=b"", query_string=""):
    lowered = {key.lower(): value for key, value in (headers or {}).items()}
    lowered.setdefault("host", "127.0.0.1:14159")
    return Request(method, path, query_string, lowered, body, ("127.0.0.1", 1), server.app)


def _body(response):
    return json.loads(response.body)


@pytest.fixture
def config(monkeypatch):
    value = {
        "host": "127.0.0.1",
        "allowed_hosts": [],
        "token": "",
        "read_only": False,
        "ssl_cert": None,
    }
    monkeypatch.setattr(server, "_config", value)
    return value


class TestTokenAuth:
    def test_loopback_without_token_is_allowed(self, config):
        assert server.enforce_access(_request()) is None

    def test_token_required_without_credentials(self, config):
        config["token"] = TOKEN

        response = server.enforce_access(_request())

        assert response.status_code == 401
        assert _body(response)["code"] == "unauthorized"
        assert response.headers["WWW-Authenticate"] == "Bearer"

    def test_valid_bearer_token(self, config):
        config["token"] = TOKEN
        request = _request(headers={"Authorization": f"Bearer {TOKEN}"})
        assert server.enforce_access(request) is None

    def test_wrong_bearer_token(self, config):
        config["token"] = TOKEN
        request = _request(headers={"Authorization": "Bearer nope"})
        assert server.enforce_access(request).status_code == 401

    def test_valid_session_cookie(self, config):
        config["token"] = TOKEN
        request = _request(headers={"Cookie": f"tinyleaf_session={TOKEN}"})
        assert server.enforce_access(request) is None

    @pytest.mark.parametrize("path", ["/api/health", "/api/version"])
    def test_health_and_version_are_public(self, config, path):
        config["token"] = TOKEN
        assert server.enforce_access(_request(path=path)) is None

    def test_schema_reports_auth_required(self, config):
        config["token"] = TOKEN
        assert server._schema_payload()["auth_required"] is True


class TestHostAllowList:
    def test_unknown_host_rejected(self, config):
        response = server.enforce_access(_request(headers={"Host": "evil.example"}))
        assert response.status_code == 400
        assert _body(response)["code"] == "host_not_allowed"

    def test_allowed_host_with_port(self, config):
        config["allowed_hosts"] = ["papers.example.com"]
        request = _request(headers={"Host": "papers.example.com:14159"})
        assert server.enforce_access(request) is None

    def test_ipv6_host_header(self, config):
        config["host"] = "::1"
        request = _request(headers={"Host": "[::1]:14159"})
        assert server.enforce_access(request) is None

    @pytest.mark.parametrize(
        "header, expected",
        [
            ("example.com:14159", "example.com"),
            ("[::1]:14159", "::1"),
            ("localhost", "localhost"),
        ],
    )
    def test_host_name_parsing(self, header, expected):
        assert server._host_name(header) == expected


class TestReadOnly:
    def test_get_passes(self, config):
        config["read_only"] = True
        assert server.enforce_access(_request(method="GET", path="/api/projects")) is None

    def test_mutation_rejected(self, config):
        config["read_only"] = True
        response = server.enforce_access(_request(method="POST", path="/api/projects"))
        assert response.status_code == 403
        assert _body(response)["code"] == "read_only"

    def test_login_still_allowed(self, config):
        config["read_only"] = True
        config["token"] = TOKEN
        request = _request(
            method="POST",
            path="/api/auth/session",
            headers={"Authorization": f"Bearer {TOKEN}"},
        )
        assert server.enforce_access(request) is None


class TestOrigin:
    def test_cross_site_origin_rejected(self, config):
        request = _request(method="POST", headers={"Origin": "http://evil.example"})
        response = server.enforce_access(request)
        assert response.status_code == 403
        assert _body(response)["code"] == "origin_not_allowed"

    def test_same_origin_allowed(self, config):
        request = _request(method="POST", headers={"Origin": "http://127.0.0.1:14159"})
        assert server.enforce_access(request) is None

    def test_cross_site_fetch_metadata_rejected(self, config):
        request = _request(method="POST", headers={"Sec-Fetch-Site": "cross-site"})
        assert server.enforce_access(request).status_code == 403


class TestSessionEndpoint:
    def test_valid_token_sets_cookie(self, config):
        config["token"] = TOKEN
        request = _request(
            method="POST",
            path="/api/auth/session",
            body=json.dumps({"token": TOKEN}).encode(),
        )

        response = server.api_auth_session(request)

        assert _body(response) == {"authenticated": True}
        cookie = "; ".join(response._cookie_headers)
        assert f"tinyleaf_session={TOKEN}" in cookie
        assert "HttpOnly" in cookie
        assert "SameSite=Strict" in cookie

    def test_wrong_token_is_401(self, config):
        config["token"] = TOKEN
        request = _request(
            method="POST",
            path="/api/auth/session",
            body=json.dumps({"token": "wrong"}).encode(),
        )

        response = server.api_auth_session(request)

        assert response.status_code == 401
        assert _body(response)["code"] == "unauthorized"

    def test_no_token_configured(self, config):
        request = _request(method="POST", path="/api/auth/session", body=b"{}")
        assert server.api_auth_session(request) == {
            "authenticated": False,
            "auth_required": False,
        }


class TestTokenBootstrap:
    def test_valid_token_redirects_and_sets_cookie(self, config):
        config["token"] = TOKEN
        request = _request(path="/", query_string=f"token={TOKEN}")

        response = server.serve_index(request)

        assert response.status_code == 302
        assert response.headers["Location"] == "/"
        assert f"tinyleaf_session={TOKEN}" in "; ".join(response._cookie_headers)

    def test_wrong_token_is_401(self, config):
        config["token"] = TOKEN
        request = _request(path="/", query_string="token=wrong")
        assert server.serve_index(request).status_code == 401

    def test_index_served_when_no_token_configured(self, config):
        request = _request(path="/", query_string="token=irrelevant")
        assert server.serve_index(request).status_code == 200


class TestCliAuthPolicy:
    @pytest.mark.parametrize(
        "host, token, insecure, blocked",
        [
            ("127.0.0.1", "", False, False),
            ("localhost", "", False, False),
            ("0.0.0.0", "", False, True),
            ("0.0.0.0", TOKEN, False, False),
            ("0.0.0.0", "", True, False),
        ],
    )
    def test_auth_policy(self, host, token, insecure, blocked):
        error = cli._auth_policy_error(host, token, insecure)
        assert (error is not None) is blocked
