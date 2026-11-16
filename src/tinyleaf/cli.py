"""CLI entry point for tinyleaf."""

import argparse
import os
import shutil
import sys
import webbrowser

from tinyleaf import __version__, registry
from tinyleaf.server import run_server

DEFAULT_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "tinyleaf")
DEFAULT_PORT = 14159
DEFAULT_HOST = "127.0.0.1"


def _get_pypi_latest(pkg: str = "tinyleaf") -> str | None:
    """Query PyPI for the latest stable version of a package.

    Returns:
        Version string or None if the query fails.
    """
    import json
    import urllib.request

    try:
        url = f"https://pypi.org/pypi/{pkg}/json"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            return data.get("info", {}).get("version")
    except Exception:
        return None


def _parse_version(v: str) -> tuple[int, ...]:
    """Parse a version string like '0.4.0' into a comparable tuple."""
    return tuple(int(x) for x in v.split(".") if x.isdigit())


def _print_version():
    """Print version with update check."""
    print(f"tinyleaf {__version__}")
    latest = _get_pypi_latest()
    if latest is None:
        print("  (could not check for updates)")
    elif _parse_version(latest) > _parse_version(__version__):
        print(f"  Update available: {__version__} → {latest}")
        print("  Run: pip install --upgrade tinyleaf")
    else:
        print("  ✓ up to date")


def _check_port_available(host: str, port: int):
    """Exit with a clean message if the port is already in use."""
    import errno
    import socket

    info = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    if not info:
        print(f"Error: cannot resolve host {host!r}.", file=sys.stderr)
        sys.exit(1)

    af, socktype, proto, _canonname, sa = info[0]
    try:
        with socket.socket(af, socktype, proto) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(sa)
    except OSError as e:
        if e.errno == errno.EADDRINUSE:
            print(
                f"Error: port {port} is already in use. Use --port to specify a different port.",
                file=sys.stderr,
            )
        else:
            print(f"Error: cannot bind to {host}:{port}: {e}", file=sys.stderr)
        sys.exit(1)


def _is_loopback(host: str) -> bool:
    """Return True for loopback addresses and ``localhost``."""
    import ipaddress

    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return host == "localhost"


def _resolve_browse_roots(explicit, project_path, projects_dir):
    """Resolve the directories the file browser may access.

    Explicit ``--browse-root`` values replace the defaults. Otherwise the
    browser may access the home directory plus the active project (single
    mode) and the legacy ``--projects-dir``. Those are paths tinyleaf already
    serves, so the Open Folder dialog can reach them without an extra flag.

    Args:
        explicit: Values from ``--browse-root`` (None or a list).
        project_path: Active project in single mode, else None.
        projects_dir: Legacy projects directory, else None.

    Returns:
        Absolute directory paths, in priority order.
    """
    if explicit:
        return [os.path.abspath(os.path.expanduser(path)) for path in explicit]

    roots = [os.path.abspath(os.path.expanduser("~"))]
    for extra in (project_path, projects_dir):
        if not extra:
            continue
        path = os.path.abspath(os.path.expanduser(extra))
        if os.path.isdir(path) and path not in roots:
            roots.append(path)
    return roots


def main():
    parser = argparse.ArgumentParser(
        prog="tinyleaf",
        description="Lightweight web-based LaTeX editor",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="Show version and check for updates",
    )
    parser.add_argument(
        "project_path",
        nargs="?",
        help="Single project directory to open",
    )
    parser.add_argument(
        "--projects-dir",
        metavar="DIR",
        help="Legacy: migrate subdirs into registry, then use registry mode",
    )
    parser.add_argument(
        "--config-dir",
        metavar="DIR",
        default=DEFAULT_CONFIG_DIR,
        help=f"Config directory for project registry (default: {DEFAULT_CONFIG_DIR})",
    )
    parser.add_argument(
        "--browse-root",
        metavar="DIR",
        action="append",
        help=(
            "Directory the file browser may access (repeatable; default: $HOME, "
            "the active project, and --projects-dir)"
        ),
    )
    parser.add_argument(
        "--docker",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Use Docker for compilation (default: enabled)",
    )
    parser.add_argument(
        "--image",
        default="oaklight/texlive:alpine-science-cn",
        help="Docker image to use (default: oaklight/texlive:alpine-science-cn)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("TINYLEAF_PORT", DEFAULT_PORT)),
        help=f"Server port (default: {DEFAULT_PORT}, env: TINYLEAF_PORT)",
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("TINYLEAF_HOST", DEFAULT_HOST),
        help=f"Server host (default: {DEFAULT_HOST}, env: TINYLEAF_HOST)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Don't auto-open browser on start",
    )
    parser.add_argument(
        "--ssl-cert",
        metavar="FILE",
        help="TLS certificate file; enables HTTPS",
    )
    parser.add_argument(
        "--ssl-key",
        metavar="FILE",
        help="TLS private key file (optional if the certificate file contains it)",
    )

    args = parser.parse_args()

    if args.version:
        _print_version()
        sys.exit(0)

    # Validate TLS options
    if args.ssl_key and not args.ssl_cert:
        parser.error("--ssl-key requires --ssl-cert")
    if args.ssl_cert and not os.path.isfile(args.ssl_cert):
        print(f"Error: TLS certificate not found: {args.ssl_cert}", file=sys.stderr)
        sys.exit(1)
    if args.ssl_key and not os.path.isfile(args.ssl_key):
        print(f"Error: TLS private key not found: {args.ssl_key}", file=sys.stderr)
        sys.exit(1)

    # Validate
    if args.project_path and args.projects_dir:
        parser.error("Cannot specify both project_path and --projects-dir")

    config_dir = os.path.abspath(args.config_dir)
    registry.ensure_config_dir(config_dir)

    # Determine mode
    if args.project_path:
        mode = "single"
        project_path = os.path.abspath(args.project_path)
        if not os.path.isdir(project_path):
            print(f"Error: '{project_path}' is not a directory", file=sys.stderr)
            sys.exit(1)
    else:
        mode = "multi"
        project_path = None

        # Backward compat: migrate --projects-dir subdirs into registry
        if args.projects_dir:
            projects_dir = os.path.abspath(args.projects_dir)
            if os.path.isdir(projects_dir):
                count = _migrate_projects_dir(config_dir, projects_dir)
                if count:
                    print(f"  Migrated {count} project(s) from {projects_dir}")

    # Auto-download vendor JS modules on first start
    from tinyleaf import vendor

    vendor_dir = os.path.join(config_dir, "vendor")
    if not vendor.is_vendor_ready(vendor_dir):
        proxy = vendor.load_proxy(config_dir)
        if proxy:
            print(f"  Using proxy: {proxy}")

        def _progress(done, total, name):
            print(f"\r  Downloading JS modules... {done}/{total}\033[K", end="", flush=True)

        try:
            vendor.download_vendor(vendor_dir, proxy=proxy, progress=_progress)
            print("\r  JS modules ready\033[K")
        except Exception as e:
            print()
            print(f"  Warning: failed to download JS modules: {e}", file=sys.stderr)
            print("  Editor will try CDN as fallback", file=sys.stderr)

    # Check compilation backend
    use_docker = args.docker
    if not use_docker and not shutil.which("latexmk"):
        print(
            "Warning: 'latexmk' not found in PATH. Add --docker to use Docker for compilation.",
            file=sys.stderr,
        )
        print("Continuing anyway — compilation will fail without latexmk.", file=sys.stderr)

    if use_docker and not shutil.which("docker"):
        print("Error: --docker specified but 'docker' not found in PATH", file=sys.stderr)
        sys.exit(1)

    browse_roots = _resolve_browse_roots(args.browse_root, project_path, args.projects_dir)
    for root in browse_roots:
        if not os.path.isdir(root):
            print(f"Error: --browse-root is not a directory: {root}", file=sys.stderr)
            sys.exit(1)

    config = {
        "mode": mode,
        "project_path": project_path,
        "config_dir": config_dir,
        "use_docker": use_docker,
        "docker_image": args.image,
        "host": args.host,
        "port": args.port,
        "ssl_cert": args.ssl_cert,
        "ssl_key": args.ssl_key,
        "browse_roots": browse_roots,
    }

    scheme = "https" if args.ssl_cert else "http"
    url = f"{scheme}://{args.host}:{args.port}"
    print(f"Starting tinyleaf ({mode} mode)")
    if use_docker:
        print(f"  Compiler: Docker ({args.image})")
    else:
        print("  Compiler: local latexmk")
    if mode == "single":
        print(f"  Project:  {project_path}")
    else:
        print(f"  Config:   {config_dir}")
    if args.ssl_cert:
        print(f"  TLS:      {args.ssl_cert}")
    print(f"  URL:      {url}")

    _check_port_available(args.host, args.port)

    if not _is_loopback(args.host):
        print(
            f"Warning: the API has no authentication. Binding to {args.host} "
            "exposes project files and compile controls to the network.",
            file=sys.stderr,
        )

    if not args.no_browser:
        webbrowser.open(url)

    run_server(config)


def _migrate_projects_dir(config_dir, projects_dir):
    """Migrate subdirectories of a projects dir into the registry."""
    count = 0
    for entry in sorted(os.listdir(projects_dir)):
        full = os.path.join(projects_dir, entry)
        if not os.path.isdir(full) or entry.startswith("."):
            continue
        try:
            registry.register_project(config_dir, entry, full)
            count += 1
        except ValueError:
            pass  # name collision, skip
    return count


if __name__ == "__main__":
    main()
