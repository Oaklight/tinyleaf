"""Tests for vendor JS module download with parallel fetching."""

import json
import os
import urllib.error
from unittest.mock import patch


from tinyleaf.vendor import (
    _dep_filename,
    _discover_deps,
    _pkg_base_name,
    _rewrite_imports,
    _sha256,
    download_vendor,
    get_manifest,
    is_vendor_ready,
    VENDOR_PACKAGES,
    PDFJS_FILES,
)


class TestHelpers:
    def test_sha256_string(self):
        h = _sha256("hello")
        assert len(h) == 64
        assert h == _sha256("hello")
        assert h != _sha256("world")

    def test_sha256_bytes(self):
        assert _sha256(b"hello") == _sha256("hello")

    def test_dep_filename_scoped(self):
        url = "https://cdn.jsdelivr.net/npm/@lezer/common@1.2.3/+esm"
        name = _dep_filename(url)
        assert name.startswith("dep-")
        assert name.endswith(".js")
        assert "lezer-common" in name

    def test_dep_filename_unscoped(self):
        url = "https://cdn.jsdelivr.net/npm/crelt@1.0.6/+esm"
        name = _dep_filename(url)
        assert "crelt" in name

    def test_dep_filename_stable(self):
        url = "https://cdn.jsdelivr.net/npm/crelt@1.0.6/+esm"
        assert _dep_filename(url) == _dep_filename(url)

    def test_pkg_base_name_scoped(self):
        assert _pkg_base_name("/npm/@codemirror/state@6.5.4/+esm") == "@codemirror/state"

    def test_pkg_base_name_unscoped(self):
        assert _pkg_base_name("/npm/crelt@1.0.6/+esm") == "crelt"


class TestDiscoverDeps:
    def test_discovers_new_dep(self):
        content = 'import{foo}from"/npm/@lezer/common@1.5.1/+esm";'
        url_map = {}
        pkg_map = {}
        deps = _discover_deps(content, url_map, pkg_map)
        assert len(deps) == 1
        url, name = deps[0]
        assert "@lezer/common" in url
        assert name.startswith("dep-")

    def test_skips_known_url(self):
        url = "https://cdn.jsdelivr.net/npm/@lezer/common@1.5.1/+esm"
        content = 'from"/npm/@lezer/common@1.5.1/+esm"'
        url_map = {url: "existing.js"}
        pkg_map = {}
        deps = _discover_deps(content, url_map, pkg_map)
        assert len(deps) == 0

    def test_deduplicates_by_pkg_name(self):
        content = 'from"/npm/@lezer/common@1.5.1/+esm"'
        url_map = {}
        pkg_map = {"@lezer/common": "lezer-common.js"}
        deps = _discover_deps(content, url_map, pkg_map)
        assert len(deps) == 0
        # But url_map should be updated
        assert len(url_map) == 1

    def test_multiple_deps(self):
        content = 'from"/npm/@lezer/common@1.5.1/+esm";from"/npm/crelt@1.0.6/+esm";'
        url_map = {}
        pkg_map = {}
        deps = _discover_deps(content, url_map, pkg_map)
        assert len(deps) == 2


class TestRewriteImports:
    def test_rewrites_known_import(self):
        content = 'import{foo}from"/npm/@lezer/common@1.5.1/+esm";'
        url_map = {"https://cdn.jsdelivr.net/npm/@lezer/common@1.5.1/+esm": "dep-lezer-common.js"}
        result = _rewrite_imports(content, url_map)
        assert 'from"./dep-lezer-common.js"' in result

    def test_preserves_unknown_import(self):
        content = 'from"/npm/unknown@1.0.0/+esm"'
        url_map = {}
        result = _rewrite_imports(content, url_map)
        assert result == content

    def test_multiple_rewrites(self):
        content = 'from"/npm/a@1/+esm";from"/npm/b@2/+esm";'
        url_map = {
            "https://cdn.jsdelivr.net/npm/a@1/+esm": "a.js",
            "https://cdn.jsdelivr.net/npm/b@2/+esm": "b.js",
        }
        result = _rewrite_imports(content, url_map)
        assert 'from"./a.js"' in result
        assert 'from"./b.js"' in result


class TestDownloadVendor:
    """Tests for download_vendor using mocked network."""

    def _mock_fetch(self, url_content_map):
        """Create a mock _fetch that returns content from a dict."""

        def fake_fetch(url):
            if url in url_content_map:
                return url_content_map[url]
            raise urllib.error.URLError(f"Not found: {url}")

        return fake_fetch

    def test_downloads_all_packages(self, tmp_path):
        vendor_dir = str(tmp_path / "vendor")
        esm_content = "export const x = 1;"
        binary_content = b"binary data"

        url_content = {}
        for spec, _ in VENDOR_PACKAGES:
            url = f"https://cdn.jsdelivr.net/npm/{spec}/+esm"
            url_content[url] = esm_content
        for spec, _ in PDFJS_FILES:
            url = f"https://cdn.jsdelivr.net/npm/{spec}"
            url_content[url] = binary_content

        with (
            patch("tinyleaf.vendor._fetch", side_effect=self._mock_fetch(url_content)),
            patch(
                "tinyleaf.vendor._fetch_binary", side_effect=lambda url: url_content.get(url, b"")
            ),
        ):
            manifest = download_vendor(vendor_dir)

        assert manifest["version"] == 2
        assert manifest["file_count"] == len(VENDOR_PACKAGES) + len(PDFJS_FILES)
        for _, name in VENDOR_PACKAGES + PDFJS_FILES:
            assert os.path.exists(os.path.join(vendor_dir, name))
            assert name in manifest["files"]
            assert "sha256" in manifest["files"][name]

    def test_progress_callback(self, tmp_path):
        vendor_dir = str(tmp_path / "vendor")
        esm_content = "export const x = 1;"
        binary_content = b"binary data"

        url_content = {}
        for spec, _ in VENDOR_PACKAGES:
            url = f"https://cdn.jsdelivr.net/npm/{spec}/+esm"
            url_content[url] = esm_content
        for spec, _ in PDFJS_FILES:
            url = f"https://cdn.jsdelivr.net/npm/{spec}"
            url_content[url] = binary_content

        progress_calls = []

        def on_progress(done, total, name):
            progress_calls.append((done, total, name))

        with (
            patch("tinyleaf.vendor._fetch", side_effect=self._mock_fetch(url_content)),
            patch(
                "tinyleaf.vendor._fetch_binary", side_effect=lambda url: url_content.get(url, b"")
            ),
        ):
            download_vendor(vendor_dir, progress=on_progress)

        assert len(progress_calls) == len(VENDOR_PACKAGES) + len(PDFJS_FILES)
        # Last call should have done == total
        last = progress_calls[-1]
        assert last[0] == last[1]

    def test_transitive_deps(self, tmp_path):
        vendor_dir = str(tmp_path / "vendor")

        dep_url = "https://cdn.jsdelivr.net/npm/@lezer/common@1.5.1/+esm"
        top_content = 'import{x}from"/npm/@lezer/common@1.5.1/+esm";export const y=x;'
        dep_content = "export const x = 42;"
        binary_content = b"binary"

        url_content = {}
        # First package has a transitive dep
        first_spec, first_name = VENDOR_PACKAGES[0]
        url_content[f"https://cdn.jsdelivr.net/npm/{first_spec}/+esm"] = top_content
        url_content[dep_url] = dep_content

        # Rest are simple
        for spec, _ in VENDOR_PACKAGES[1:]:
            url_content[f"https://cdn.jsdelivr.net/npm/{spec}/+esm"] = "export const z = 1;"
        for spec, _ in PDFJS_FILES:
            url_content[f"https://cdn.jsdelivr.net/npm/{spec}"] = binary_content

        with (
            patch("tinyleaf.vendor._fetch", side_effect=self._mock_fetch(url_content)),
            patch(
                "tinyleaf.vendor._fetch_binary", side_effect=lambda url: url_content.get(url, b"")
            ),
        ):
            manifest = download_vendor(vendor_dir)

        # Should have top-level + pdfjs + 1 transitive dep
        assert manifest["file_count"] == len(VENDOR_PACKAGES) + len(PDFJS_FILES) + 1

        # Check rewriting happened
        with open(os.path.join(vendor_dir, first_name)) as f:
            rewritten = f.read()
        assert "/npm/" not in rewritten
        assert 'from"./' in rewritten

    def test_incremental_skips_unchanged(self, tmp_path):
        vendor_dir = str(tmp_path / "vendor")
        esm_content = "export const x = 1;"
        binary_content = b"binary data"

        url_content = {}
        for spec, _ in VENDOR_PACKAGES:
            url = f"https://cdn.jsdelivr.net/npm/{spec}/+esm"
            url_content[url] = esm_content
        for spec, _ in PDFJS_FILES:
            url = f"https://cdn.jsdelivr.net/npm/{spec}"
            url_content[url] = binary_content

        with (
            patch("tinyleaf.vendor._fetch", side_effect=self._mock_fetch(url_content)),
            patch(
                "tinyleaf.vendor._fetch_binary", side_effect=lambda url: url_content.get(url, b"")
            ),
        ):
            download_vendor(vendor_dir)

        # Record mtimes
        import time

        time.sleep(0.1)
        mtimes = {}
        for f in os.listdir(vendor_dir):
            if f.endswith(".js"):
                mtimes[f] = os.path.getmtime(os.path.join(vendor_dir, f))

        # Second download with same content
        with (
            patch("tinyleaf.vendor._fetch", side_effect=self._mock_fetch(url_content)),
            patch(
                "tinyleaf.vendor._fetch_binary", side_effect=lambda url: url_content.get(url, b"")
            ),
        ):
            download_vendor(vendor_dir)

        # Files should not have been rewritten
        for f, old_mtime in mtimes.items():
            new_mtime = os.path.getmtime(os.path.join(vendor_dir, f))
            assert abs(new_mtime - old_mtime) < 0.01, f"{f} was rewritten unnecessarily"

    def test_partial_failure_continues(self, tmp_path):
        vendor_dir = str(tmp_path / "vendor")
        esm_content = "export const x = 1;"
        binary_content = b"binary data"

        url_content = {}
        failed_spec = VENDOR_PACKAGES[0][0]
        for spec, _ in VENDOR_PACKAGES:
            url = f"https://cdn.jsdelivr.net/npm/{spec}/+esm"
            if spec == failed_spec:
                continue  # this one will fail
            url_content[url] = esm_content
        for spec, _ in PDFJS_FILES:
            url = f"https://cdn.jsdelivr.net/npm/{spec}"
            url_content[url] = binary_content

        with (
            patch("tinyleaf.vendor._fetch", side_effect=self._mock_fetch(url_content)),
            patch(
                "tinyleaf.vendor._fetch_binary", side_effect=lambda url: url_content.get(url, b"")
            ),
        ):
            manifest = download_vendor(vendor_dir)

        # Should have all files except the failed one
        assert manifest["file_count"] == len(VENDOR_PACKAGES) + len(PDFJS_FILES) - 1
        assert VENDOR_PACKAGES[0][1] not in manifest["files"]

        # Other files should exist
        for _, name in VENDOR_PACKAGES[1:]:
            assert os.path.exists(os.path.join(vendor_dir, name))

    def test_manifest_has_sha256(self, tmp_path):
        vendor_dir = str(tmp_path / "vendor")
        esm_content = "export const x = 1;"
        binary_content = b"binary data"

        url_content = {}
        for spec, _ in VENDOR_PACKAGES:
            url_content[f"https://cdn.jsdelivr.net/npm/{spec}/+esm"] = esm_content
        for spec, _ in PDFJS_FILES:
            url_content[f"https://cdn.jsdelivr.net/npm/{spec}"] = binary_content

        with (
            patch("tinyleaf.vendor._fetch", side_effect=self._mock_fetch(url_content)),
            patch(
                "tinyleaf.vendor._fetch_binary", side_effect=lambda url: url_content.get(url, b"")
            ),
        ):
            manifest = download_vendor(vendor_dir)

        for name, info in manifest["files"].items():
            assert "sha256" in info, f"Missing sha256 for {name}"
            assert len(info["sha256"]) == 64


class TestManifestAndReady:
    def test_get_manifest_missing(self, tmp_path):
        assert get_manifest(str(tmp_path)) is None

    def test_get_manifest_valid(self, tmp_path):
        manifest = {"version": 2, "files": {}}
        with open(tmp_path / "manifest.json", "w") as f:
            json.dump(manifest, f)
        result = get_manifest(str(tmp_path))
        assert result == manifest

    def test_get_manifest_corrupt(self, tmp_path):
        with open(tmp_path / "manifest.json", "w") as f:
            f.write("not json")
        assert get_manifest(str(tmp_path)) is None

    def test_is_vendor_ready_false_no_manifest(self, tmp_path):
        assert not is_vendor_ready(str(tmp_path))

    def test_is_vendor_ready_false_missing_files(self, tmp_path):
        manifest = {"version": 2, "files": {"cm-view.js": {}}}
        with open(tmp_path / "manifest.json", "w") as f:
            json.dump(manifest, f)
        assert not is_vendor_ready(str(tmp_path))

    def test_is_vendor_ready_true(self, tmp_path):
        manifest = {"version": 2, "files": {}}
        with open(tmp_path / "manifest.json", "w") as f:
            json.dump(manifest, f)
        for _, name in VENDOR_PACKAGES + PDFJS_FILES:
            (tmp_path / name).touch()
        assert is_vendor_ready(str(tmp_path))
