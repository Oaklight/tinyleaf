"""Vendor JS module manager for tinyleaf.

Downloads ESM bundles from jsdelivr, rewrites cross-package imports
to local relative paths, and stores them in a vendor directory.
"""

import hashlib
import json
import os
import re
import sys
import threading
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    ("@lezer/highlight@1", "lezer-highlight.js"),
    ("codemirror-lang-latex", "cm-lang-latex.js"),
    ("@codemirror/lang-markdown@6", "cm-lang-markdown.js"),
    ("@codemirror/lang-javascript@6", "cm-lang-javascript.js"),
    ("@codemirror/lang-python@6", "cm-lang-python.js"),
    ("@codemirror/lang-json@6", "cm-lang-json.js"),
    ("@codemirror/lang-css@6", "cm-lang-css.js"),
    ("@codemirror/lang-html@6", "cm-lang-html.js"),
    ("@codemirror/lang-yaml@6", "cm-lang-yaml.js"),
]

# PDF.js files (self-contained, no import rewriting needed)
PDFJS_FILES = [
    ("pdfjs-dist@4.9.155/build/pdf.min.mjs", "pdfjs.js"),
    ("pdfjs-dist@4.9.155/build/pdf.worker.min.mjs", "pdfjs-worker.js"),
]

MANIFEST_FILE = "manifest.json"
_MANIFEST_VERSION = 2
_MAX_WORKERS = 8

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


def _sha256(content):
    """Compute SHA-256 hex digest of string or bytes content."""
    if isinstance(content, str):
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def _url_for_package(specifier):
    """Build the jsdelivr ESM URL for a package specifier."""
    return f"{CDN_BASE}/npm/{specifier}/+esm"


def _dep_filename(url):
    """Generate a stable filename for a dependency URL."""
    h = hashlib.sha1(url.encode()).hexdigest()[:10]
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


def _discover_deps(content, url_map, pkg_map):
    """Parse ESM content for import references, return new deps to fetch.

    Args:
        content: Raw ESM source text.
        url_map: URL -> local_name mapping (mutated to register new deps).
        pkg_map: base package name -> local_name mapping (mutated).

    Returns:
        List of (url, local_name) tuples for deps not yet fetched.
    """
    new_deps = []
    for m in _IMPORT_RE.finditer(content):
        ref_path = m.group(2)
        ref_url = CDN_BASE + ref_path
        if ref_url in url_map:
            continue
        base = _pkg_base_name(ref_path)
        if base in pkg_map:
            url_map[ref_url] = pkg_map[base]
            continue
        dep_name = _dep_filename(ref_path)
        pkg_map[base] = dep_name
        url_map[ref_url] = dep_name
        new_deps.append((ref_url, dep_name))
    return new_deps


def _rewrite_imports(content, url_map):
    """Rewrite jsdelivr cross-package imports to local relative paths."""

    def replace_import(m):
        prefix, ref_path, suffix = m.group(1), m.group(2), m.group(3)
        ref_url = CDN_BASE + ref_path
        local = url_map.get(ref_url)
        if local:
            return f"{prefix}./{local}{suffix}"
        return m.group(0)

    return _IMPORT_RE.sub(replace_import, content)


def download_vendor(vendor_dir, proxy=None, progress=None):
    """Download all vendor JS modules to the given directory.

    Fetches packages in parallel, resolves transitive dependencies level
    by level, and writes rewritten ESM files. Supports incremental updates
    by comparing content hashes with the existing manifest.

    Args:
        vendor_dir: Destination directory for vendor files.
        proxy: Optional HTTP proxy URL (e.g. "http://localhost:7890").
        progress: Optional callback(done, total, filename) for progress.

    Returns:
        The manifest dict that was written.
    """
    global _opener
    with _lock:
        _opener = _build_opener(proxy)
        os.makedirs(vendor_dir, exist_ok=True)

        old_manifest = get_manifest(vendor_dir)
        old_files = old_manifest.get("files", {}) if old_manifest else {}

        url_map = {}  # jsdelivr URL -> local filename
        pkg_map = {}  # base package name -> local filename (dedup)
        contents = {}  # url -> raw content string
        all_failures = []

        # Pre-populate pkg_map with top-level packages
        for specifier, local_name in VENDOR_PACKAGES:
            base = re.sub(r"@[^/]*$", "", specifier)
            pkg_map[base] = local_name

        # Build initial work list
        esm_queue = []
        for specifier, local_name in VENDOR_PACKAGES:
            url = _url_for_package(specifier)
            url_map[url] = local_name
            esm_queue.append((url, local_name))

        total_est = len(esm_queue) + len(PDFJS_FILES)
        done_count = [0]

        def _report(name):
            done_count[0] += 1
            if progress:
                progress(done_count[0], total_est, name)

        with ThreadPoolExecutor(max_workers=_MAX_WORKERS) as executor:
            # Start PDF.js downloads alongside ESM packages
            pdfjs_futures = {}
            for specifier, local_name in PDFJS_FILES:
                url = f"{CDN_BASE}/npm/{specifier}"
                pdfjs_futures[executor.submit(_fetch_binary, url)] = (
                    url,
                    local_name,
                    specifier,
                )

            # BFS: fetch ESM packages level by level, discovering deps
            while esm_queue:
                future_map = {executor.submit(_fetch, url): (url, name) for url, name in esm_queue}
                next_queue = []
                for future in as_completed(future_map):
                    url, name = future_map[future]
                    try:
                        content = future.result()
                        contents[url] = content
                        new_deps = _discover_deps(content, url_map, pkg_map)
                        next_queue.extend(new_deps)
                    except Exception as e:
                        all_failures.append((url, name, e))
                    _report(name)

                if next_queue:
                    total_est += len(next_queue)
                esm_queue = next_queue

            # Collect PDF.js results
            for future in as_completed(pdfjs_futures):
                url, local_name, specifier = pdfjs_futures[future]
                try:
                    data = future.result()
                    file_hash = _sha256(data)
                    if old_files.get(local_name, {}).get("sha256") != file_hash:
                        filepath = os.path.join(vendor_dir, local_name)
                        with open(filepath, "wb") as f:
                            f.write(data)
                except Exception as e:
                    all_failures.append((url, local_name, e))
                _report(local_name)

        # Rewrite imports and write ESM files (skip unchanged)
        for url, content in contents.items():
            local_name = url_map[url]
            rewritten = _rewrite_imports(content, url_map)
            file_hash = _sha256(rewritten)
            if old_files.get(local_name, {}).get("sha256") != file_hash:
                filepath = os.path.join(vendor_dir, local_name)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(rewritten)

        # Build manifest
        files = {}
        for specifier, local_name in VENDOR_PACKAGES:
            url = _url_for_package(specifier)
            if url in contents:
                rewritten = _rewrite_imports(contents[url], url_map)
                files[local_name] = {
                    "package": specifier,
                    "size": len(rewritten.encode("utf-8")),
                    "sha256": _sha256(rewritten),
                }

        for specifier, local_name in PDFJS_FILES:
            filepath = os.path.join(vendor_dir, local_name)
            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    data = f.read()
                files[local_name] = {
                    "package": specifier,
                    "size": len(data),
                    "sha256": _sha256(data),
                }

        for url, dep_name in url_map.items():
            if dep_name not in files and url in contents:
                rewritten = _rewrite_imports(contents[url], url_map)
                files[dep_name] = {
                    "package": url.replace(CDN_BASE + "/npm/", "").replace("/+esm", ""),
                    "size": len(rewritten.encode("utf-8")),
                    "sha256": _sha256(rewritten),
                }

        manifest = {
            "version": _MANIFEST_VERSION,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "file_count": len(files),
            "files": files,
        }

        manifest_path = os.path.join(vendor_dir, MANIFEST_FILE)
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        if all_failures:
            names = [name for _, name, _ in all_failures]
            print(
                f"  Warning: failed to download {len(names)} file(s): {', '.join(names)}",
                file=sys.stderr,
            )

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
