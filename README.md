# texlive-web

[中文版](./README_zh.md)

Lightweight web-based LaTeX editor powered by [TeX Live Docker images](https://github.com/Oaklight/texlive).

## Features

* **CLI-first** — `pip install texlive-web && texlive-web /path` to start editing
* **Two modes** — Single project or multi-project (Overleaf-like)
* **Two compilation backends** — Local `latexmk` (default) or Docker
* **CodeMirror 6** editor with LaTeX syntax highlighting
* **PDF.js** preview with live reload after compilation
* **SSE** real-time compilation log streaming
* **Git integration** — auto-detect `.git`, commit/push from UI
* **Zero Python dependencies** — stdlib only (`http.server` + `threading` + `subprocess`)
* **Dark/Light theme** toggle

## Quick Start

```bash
pip install texlive-web

# Single project mode (local compilation)
texlive-web /path/to/my-thesis

# Single project mode (Docker compilation)
texlive-web /path/to/my-thesis --docker

# Multi-project mode
texlive-web --projects-dir /path/to/projects
```

## Usage

```
usage: texlive-web [-h] [--projects-dir DIR] [--docker] [--image IMAGE]
                   [--port PORT] [--host HOST] [--no-browser] [project_path]

positional arguments:
  project_path          Single project directory to open

options:
  --projects-dir DIR    Multi-project mode: directory containing project folders
  --docker              Use Docker for compilation (default: local latexmk)
  --image IMAGE         Docker image to use (default: oaklight/texlive:latest)
  --port PORT           Server port (default: 8080)
  --host HOST           Server host (default: 127.0.0.1)
  --no-browser          Don't auto-open browser on start
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save current file |
| `Ctrl+Enter` | Compile |
| `Ctrl+Shift+C` | Git commit |
| `Ctrl+Shift+P` | Git push |

## Docker Compose

For a self-contained setup with Docker compilation:

```bash
docker compose up
```

This starts the web editor on `http://localhost:8080` with a persistent TeX Live container for compilation.

## License

MIT
