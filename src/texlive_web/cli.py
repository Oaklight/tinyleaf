"""CLI entry point for texlive-web."""

import argparse
import os
import shutil
import sys
import webbrowser

from texlive_web.server import run_server


def main():
    parser = argparse.ArgumentParser(
        prog="texlive-web",
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
        help="Multi-project mode: directory containing project folders",
    )
    parser.add_argument(
        "--docker",
        action="store_true",
        help="Use Docker for compilation (default: local latexmk)",
    )
    parser.add_argument(
        "--image",
        default="oaklight/texlive:latest",
        help="Docker image to use (default: oaklight/texlive:latest)",
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

    # Validate: must specify exactly one of project_path or --projects-dir
    if args.project_path and args.projects_dir:
        parser.error("Cannot specify both project_path and --projects-dir")
    if not args.project_path and not args.projects_dir:
        parser.error("Must specify either project_path or --projects-dir")

    # Determine mode
    if args.project_path:
        mode = "single"
        project_path = os.path.abspath(args.project_path)
        if not os.path.isdir(project_path):
            print(f"Error: '{project_path}' is not a directory", file=sys.stderr)
            sys.exit(1)
        projects_dir = None
    else:
        mode = "multi"
        projects_dir = os.path.abspath(args.projects_dir)
        os.makedirs(projects_dir, exist_ok=True)
        project_path = None

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
        "projects_dir": projects_dir,
        "use_docker": use_docker,
        "docker_image": args.image,
        "host": args.host,
        "port": args.port,
    }

    url = f"http://{args.host}:{args.port}"
    print(f"Starting texlive-web ({mode} mode)")
    if use_docker:
        print(f"  Compiler: Docker ({args.image})")
    else:
        print("  Compiler: local latexmk")
    if mode == "single":
        print(f"  Project:  {project_path}")
    else:
        print(f"  Projects: {projects_dir}")
    print(f"  URL:      {url}")

    if not args.no_browser:
        webbrowser.open(url)

    run_server(config)


if __name__ == "__main__":
    main()
