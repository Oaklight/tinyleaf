"""Vendor JS module manager for tinyleaf.

Downloads ESM bundles from jsdelivr, rewrites cross-package imports
to local relative paths, and stores them in a vendor directory.
"""

import hashlib
import json
import os
import re
import threading
import urllib.error
import urllib.request
from datetime import datetime, timezone

CDN_BASE = "https://cdn.jsdelivr.net"

# Top-level packages to download (npm specifier → local filename)
VENDOR_PACKAGES = [
    ("@codemirror/view@6", "cm-view.js"),
    ("@codemirror/state@6", "cm-state.js"),
    ("@codemirror/commands@6", "cm-commands.js"),
    ("@codemirror/language@6", "cm-language.js"),
    ("@codemirror/autocomplete@6", "cm-autocomplete.js"),
    ("@codemirror/search@6", "cm-search.js"),
    ("codemirror-lang-latex", "cm-lang-latex.js"),
]

# PDF.js files (self-contained, no import rewriting needed)
PDFJS_FILES = [
    ("pdfjs-dist@4.9.155/build/pdf.min.mjs", "pdfjs.js"),
    ("pdfjs-dist@4.9.155/build/pdf.worker.min.mjs", "pdfjs-worker.js"),
]

MANIFEST_FILE = "manifest.json"

# Matches jsdelivr ESM cross-references: from"/npm/pkg@ver/+esm" or from "/npm/..."
_IMPORT_RE = re.compile(r"""(from\s*["'])(/npm/[^"']+)(["'])""")

_lock = threading.Lock()

# Module-level opener, set by _build_opener() when proxy is configured
_opener = None


def _build_opener(proxy=None):
    """Build a urllib opener, optionally with proxy support.

    For HTTPS through HTTP proxy, we set environment variables instead of
    using ProxyHandler, which avoids SSL tunnel issues.
    """
    if proxy:
        os.environ["http_proxy"] = proxy
        os.environ["https_proxy"] = proxy
    else:
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
    # Use ProxyHandler with empty dict to force re-reading env vars
    return urllib.request.build_opener(urllib.request.ProxyHandler())


def _fetch(url):
    """Download a URL and return content as string."""
    req = urllib.request.Request(url, headers={"User-Agent": "tinyleaf-vendor/1.0"})
    opener = _opener or urllib.request.build_opener()
    with opener.open(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def _fetch_binary(url):
    """Download a URL and return content as bytes."""
    req = urllib.request.Request(url, headers={"User-Agent": "tinyleaf-vendor/1.0"})
    opener = _opener or urllib.request.build_opener()
    with opener.open(req, timeout=60) as resp:
        return resp.read()


def _url_for_package(specifier):
    """Build the jsdelivr ESM URL for a package specifier."""
    return f"{CDN_BASE}/npm/{specifier}/+esm"


def _dep_filename(url):
    """Generate a stable filename for a dependency URL."""
    h = hashlib.sha1(url.encode()).hexdigest()[:10]
    # Extract a readable portion from the URL
    # e.g. /npm/@lezer/common@1.2.3/+esm -> lezer-common-1.2.3
    match = re.search(r"/npm/(@?[^/+]+(?:/[^/+]+)?@[^/+]+)", url)
    if match:
        name = match.group(1).replace("/", "-").replace("@", "").lstrip("-")
        return f"dep-{name}-{h[:6]}.js"
    return f"dep-{h}.js"


def _pkg_base_name(ref_path):
    """Extract base package name without version from a jsdelivr path.

    E.g. '/npm/@codemirror/state@6.5.4/+esm' -> '@codemirror/state'
         '/npm/crelt@1.0.6/+esm' -> 'crelt'
    """
    match = re.search(r"/npm/((?:@[^/]+/)?[^@/]+)@", ref_path)
    return match.group(1) if match else ref_path


def _download_esm(url, local_name, vendor_dir, url_map, pkg_map):
    """Download an ESM file, recursively resolve imports, rewrite paths.

    Args:
        url: Full jsdelivr URL to download.
        local_name: Local filename to save as.
        vendor_dir: Destination directory.
        url_map: Dict mapping URLs to local filenames (shared across calls).
        pkg_map: Dict mapping base package names to local filenames for dedup.
    """
    if url in url_map:
        return

    url_map[url] = local_name
    content = _fetch(url)

    def replace_import(m):
        prefix, ref_path, suffix = m.group(1), m.group(2), m.group(3)
        ref_url = CDN_BASE + ref_path

        if ref_url in url_map:
            return f"{prefix}./{url_map[ref_url]}{suffix}"

        # Deduplicate: if we already downloaded a different version of the
        # same package, reuse that file instead of downloading again.
        base = _pkg_base_name(ref_path)
        if base in pkg_map:
            url_map[ref_url] = pkg_map[base]
            return f"{prefix}./{pkg_map[base]}{suffix}"

        dep_name = _dep_filename(ref_path)
        pkg_map[base] = dep_name
        _download_esm(ref_url, dep_name, vendor_dir, url_map, pkg_map)
        return f"{prefix}./{url_map[ref_url]}{suffix}"

    rewritten = _IMPORT_RE.sub(replace_import, content)

    filepath = os.path.join(vendor_dir, local_name)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(rewritten)


def _download_pdfjs(vendor_dir):
    """Download PDF.js files (self-contained, no rewriting needed)."""
    for specifier, local_name in PDFJS_FILES:
        url = f"{CDN_BASE}/npm/{specifier}"
        data = _fetch_binary(url)
        filepath = os.path.join(vendor_dir, local_name)
        with open(filepath, "wb") as f:
            f.write(data)


def download_vendor(vendor_dir, proxy=None):
    """Download all vendor JS modules to the given directory.

    Args:
        vendor_dir: Destination directory for vendor files.
        proxy: Optional HTTP proxy URL (e.g. "http://localhost:7890").

    Returns:
        The manifest dict that was written.
    """
    global _opener
    with _lock:
        _opener = _build_opener(proxy)
        os.makedirs(vendor_dir, exist_ok=True)

        url_map = {}  # jsdelivr URL → local filename
        pkg_map = {}  # base package name → local filename (dedup)

        # Pre-populate pkg_map with top-level packages so that when
        # e.g. cm-view.js references @codemirror/state internally,
        # it resolves to cm-state.js (our top-level file) instead of
        # creating a separate dep file. This ensures a single module
        # instance for shared packages like @codemirror/state.
        for specifier, local_name in VENDOR_PACKAGES:
            # "@codemirror/view@6" -> "@codemirror/view"
            base = re.sub(r"@[^/]*$", "", specifier)
            pkg_map[base] = local_name

        # Download CodeMirror ESM packages
        for specifier, local_name in VENDOR_PACKAGES:
            url = _url_for_package(specifier)
            _download_esm(url, local_name, vendor_dir, url_map, pkg_map)

        # Download PDF.js
        _download_pdfjs(vendor_dir)

        # Build manifest
        files = {}
        for specifier, local_name in VENDOR_PACKAGES + PDFJS_FILES:
            filepath = os.path.join(vendor_dir, local_name)
            if os.path.exists(filepath):
                files[local_name] = {
                    "package": specifier,
                    "size": os.path.getsize(filepath),
                }

        # Include dependency files
        for url, dep_name in url_map.items():
            filepath = os.path.join(vendor_dir, dep_name)
            if dep_name not in files and os.path.exists(filepath):
                files[dep_name] = {
                    "package": url.replace(CDN_BASE + "/npm/", "").replace("/+esm", ""),
                    "size": os.path.getsize(filepath),
                }

        manifest = {
            "version": 1,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "file_count": len(files),
            "files": files,
        }

        manifest_path = os.path.join(vendor_dir, MANIFEST_FILE)
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        return manifest


def get_manifest(vendor_dir):
    """Read the vendor manifest.

    Returns:
        The manifest dict, or None if not found.
    """
    path = os.path.join(vendor_dir, MANIFEST_FILE)
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def is_vendor_ready(vendor_dir):
    """Check if vendor files are downloaded and manifest exists."""
    manifest = get_manifest(vendor_dir)
    if not manifest:
        return False
    # Check that at least the main files exist
    for _, local_name in VENDOR_PACKAGES + PDFJS_FILES:
        if not os.path.exists(os.path.join(vendor_dir, local_name)):
            return False
    return True


PROXY_FILE = "proxy.txt"


def save_proxy(config_dir, proxy):
    """Persist the proxy URL to config_dir/proxy.txt."""
    path = os.path.join(config_dir, PROXY_FILE)
    if proxy:
        with open(path, "w", encoding="utf-8") as f:
            f.write(proxy.strip())
    else:
        # Clear proxy
        try:
            os.remove(path)
        except FileNotFoundError:
            pass


def load_proxy(config_dir):
    """Load proxy URL from config_dir/proxy.txt.

    Returns:
        The proxy URL string, or None if not set.
    """
    path = os.path.join(config_dir, PROXY_FILE)
    try:
        with open(path, encoding="utf-8") as f:
            proxy = f.read().strip()
            return proxy or None
    except FileNotFoundError:
        return None
