"""Tests for explicit ProxyHandler use in vendor downloads (issue #90)."""

import os
import urllib.request
from unittest.mock import patch

from tinyleaf import vendor


def _proxy_handler(opener):
    for handler in opener.handlers:
        if isinstance(handler, urllib.request.ProxyHandler):
            return handler
    raise AssertionError("opener has no ProxyHandler")


def test_build_opener_does_not_mutate_environ(monkeypatch):
    monkeypatch.setenv("http_proxy", "http://env-proxy:1111")
    monkeypatch.setenv("https_proxy", "http://env-proxy:2222")
    before = dict(os.environ)
    vendor._build_opener("http://explicit:8080")
    assert dict(os.environ) == before


def test_build_opener_uses_explicit_proxy():
    handler = _proxy_handler(vendor._build_opener("http://explicit:8080"))
    assert handler.proxies == {
        "http": "http://explicit:8080",
        "https": "http://explicit:8080",
    }


def test_build_opener_without_proxy_ignores_environment(monkeypatch):
    monkeypatch.setenv("http_proxy", "http://env-proxy:1111")
    monkeypatch.setenv("https_proxy", "http://env-proxy:2222")
    opener = vendor._build_opener()
    # An empty ProxyHandler installs no proxy methods, so urllib drops it and
    # environment proxies are never consulted.
    assert not any(isinstance(h, urllib.request.ProxyHandler) for h in opener.handlers)


def test_module_has_no_mutable_global_opener():
    assert not hasattr(vendor, "_opener")


def test_download_vendor_does_not_mutate_environ(tmp_path, monkeypatch):
    monkeypatch.setenv("http_proxy", "http://env-proxy:1111")
    before = dict(os.environ)
    with (
        patch.object(vendor, "_fetch", return_value="export const x = 1;"),
        patch.object(vendor, "_fetch_binary", return_value=b"binary"),
    ):
        vendor.download_vendor(str(tmp_path / "vendor"), proxy="http://explicit:8080")
    assert dict(os.environ) == before
