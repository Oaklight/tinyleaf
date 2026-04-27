"""CLI entry point for tinyleaf."""

import argparse
import os
import shutil
import sys
import webbrowser

from tinyleaf import registry
from tinyleaf.server import run_server

DEFAULT_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "tinyleaf")


def main():
    parser = argparse.ArgumentParser(
        prog="tinyleaf",
        description="Lightweight web-based LaTeX editor",
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
        "--docker",
        action="store_true",
        help="Use Docker for compilation (default: local latexmk)",
    )
    parser.add_argument(
        "--image",
        default="oaklight/texlive:alpine-science-cn",
        help="Docker image to use (default: oaklight/texlive:alpine-science-cn)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Server port (default: 8080)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Server host (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Don't auto-open browser on start",
    )

    args = parser.parse_args()

    # Validate
    if args.project_path and args.projects_dir:
        parser.error("Cannot specify both project_path and --projects-dir")

    # Determine mode
    if args.project_path:
        mode = "single"
        project_path = os.path.abspath(args.project_path)
        if not os.path.isdir(project_path):
            print(f"Error: '{project_path}' is not a directory", file=sys.stderr)
            sys.exit(1)
        config_dir = None
    else:
        mode = "multi"
        config_dir = os.path.abspath(args.config_dir)
        registry.ensure_config_dir(config_dir)
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
            print("  Downloading JS modules...")
            if proxy:
                print(f"  Using proxy: {proxy}")
            try:
                vendor.download_vendor(vendor_dir, proxy=proxy)
                print("  JS modules ready")
            except Exception as e:
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

    config = {
        "mode": mode,
        "project_path": project_path,
        "config_dir": config_dir,
        "use_docker": use_docker,
        "docker_image": args.image,
        "host": args.host,
        "port": args.port,
    }

    url = f"http://{args.host}:{args.port}"
    print(f"Starting tinyleaf ({mode} mode)")
    if use_docker:
        print(f"  Compiler: Docker ({args.image})")
    else:
        print("  Compiler: local latexmk")
    if mode == "single":
        print(f"  Project:  {project_path}")
    else:
        print(f"  Config:   {config_dir}")
    print(f"  URL:      {url}")

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
