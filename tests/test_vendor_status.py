"""Tests for vendor readiness and partial-failure reporting (issue #86)."""

import json
import urllib.error
import warnings
from unittest.mock import patch

from tinyleaf import handlers, vendor

ALL_MODULES = vendor.VENDOR_PACKAGES + vendor.PDFJS_FILES


def _write_manifest(vendor_dir):
    manifest = {"version": 2, "files": {}}
    (vendor_dir / vendor.MANIFEST_FILE).write_text(json.dumps(manifest), encoding="utf-8")
    return manifest


def _touch_modules(vendor_dir, skip=None):
    for _, name in ALL_MODULES:
        if name != skip:
            (vendor_dir / name).touch()


def test_status_not_ready_when_manifest_exists_but_files_missing(tmp_path):
    vendor_dir = tmp_path / "vendor"
    vendor_dir.mkdir()
    _write_manifest(vendor_dir)
    _touch_modules(vendor_dir, skip=vendor.VENDOR_PACKAGES[0][1])

    result = handlers.handle_vendor_status({"config_dir": str(tmp_path)})

    assert result["ready"] is False
    assert result["manifest"]["version"] == 2


def test_status_ready_when_all_files_present(tmp_path):
    vendor_dir = tmp_path / "vendor"
    vendor_dir.mkdir()
    _write_manifest(vendor_dir)
    _touch_modules(vendor_dir)

    result = handlers.handle_vendor_status({"config_dir": str(tmp_path)})

    assert result["ready"] is True


def test_status_single_mode():
    result = handlers.handle_vendor_status({"config_dir": None})
    assert result == {"ready": False, "reason": "single mode"}


def test_update_reports_partial_failure(tmp_path, monkeypatch):
    config_dir = tmp_path / "config"
    failed = [{"url": "https://example.invalid/x.js", "name": "x.js", "error": "boom"}]

    def fake_download(vendor_dir, proxy=None, failures=None):
        failures.extend(failed)
        return {"version": 2, "files": {}}

    monkeypatch.setattr(vendor, "download_vendor", fake_download)
    result = handlers.handle_update_vendor({}, {"config_dir": str(config_dir)})

    assert result["ok"] is False
    assert result["ready"] is False
    assert result["failed"] == failed


def test_update_reports_success_when_no_failures(tmp_path, monkeypatch):
    config_dir = tmp_path / "config"

    def fake_download(vendor_dir, proxy=None, failures=None):
        return {"version": 2, "files": {}}

    monkeypatch.setattr(vendor, "download_vendor", fake_download)
    result = handlers.handle_update_vendor({}, {"config_dir": str(config_dir)})

    assert result["ok"] is True
    assert result["failed"] == []


def test_download_vendor_collects_failures(tmp_path):
    failures = []
    error = urllib.error.URLError("offline")

    with (
        patch.object(vendor, "_fetch", side_effect=error),
        patch.object(vendor, "_fetch_binary", side_effect=error),
        warnings.catch_warnings(),
    ):
        warnings.simplefilter("ignore")
        vendor.download_vendor(str(tmp_path / "vendor"), failures=failures)

    expected = {name for _, name in ALL_MODULES}
    assert {entry["name"] for entry in failures} == expected
    assert all(entry["error"] for entry in failures)
    assert all(entry["url"].startswith("https://") for entry in failures)
