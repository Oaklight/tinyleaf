# tinyleaf

<p align="center">
  <img src="assets/brand/tinyleaf-leafpen-readme-light.svg" alt="Tinyleaf" width="560">
</p>

[![PyPI version](https://img.shields.io/pypi/v/tinyleaf?color=green)](https://pypi.org/project/tinyleaf/)
[![GitHub release](https://img.shields.io/github/v/release/Oaklight/tinyleaf?color=green)](https://github.com/Oaklight/tinyleaf/releases/latest)
[![CI](https://github.com/Oaklight/tinyleaf/actions/workflows/lint.yml/badge.svg)](https://github.com/Oaklight/tinyleaf/actions/workflows/lint.yml)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Documentation](https://img.shields.io/badge/docs-readthedocs-blue)](https://tinyleaf.readthedocs.io)

[中文版](./README_zh.md) | [Documentation](https://tinyleaf.readthedocs.io)

A lightweight, self-hosted **Overleaf alternative** that runs entirely from a single `pip install`. No database, no Node.js, no Docker required — just Python's standard library and a TeX Live installation. One command to start editing LaTeX in your browser.

```bash
pip install tinyleaf && tinyleaf /path/to/my-thesis
```

<!-- Screenshot / demo GIF placeholder — replace with actual media -->
<!-- ![tinyleaf screenshot](docs/images/screenshot.png) -->

## Features

* **CLI-first** — `pip install tinyleaf && tinyleaf /path` to start editing
* **Two modes** — Single project or multi-project with registry (`~/.config/tinyleaf/projects.json`)
* **Two compilation backends** — Local `latexmk` (default) or Docker
* **CodeMirror 6** editor with LaTeX syntax highlighting
* **PDF.js** preview with live reload after compilation
* **SSE** real-time compilation log streaming
* **Git integration** — auto-detect `.git`, commit/push from UI
* **Zero Python dependencies** — stdlib only (`http.server` + `threading` + `subprocess`)
* **7 themes** with dark/light toggle
* **i18n** — English and Chinese

## Quick Start

```bash
pip install tinyleaf

# Single project mode (local compilation)
tinyleaf /path/to/my-thesis

# Single project mode (Docker compilation)
tinyleaf /path/to/my-thesis --docker

# Multi-project mode (registry)
tinyleaf
```

## Usage

```
usage: tinyleaf [-h] [--projects-dir DIR] [--config-dir DIR] [--docker]
                [--image IMAGE] [--port PORT] [--host HOST] [--no-browser]
                [project_path]

positional arguments:
  project_path          Single project directory to open

options:
  --config-dir DIR      Config directory for project registry
                        (default: ~/.config/tinyleaf)
  --projects-dir DIR    Legacy: migrate subdirs into registry
  --docker              Use Docker for compilation (default: local latexmk)
  --image IMAGE         Docker image to use (default: oaklight/texlive:latest)
  --port PORT           Server port (default: 14159, env: TINYLEAF_PORT)
  --host HOST           Server host (default: 127.0.0.1)
  --no-browser          Don't auto-open browser on start
```

## Multi-Project Registry

When launched without a `project_path`, tinyleaf enters **multi-project mode**. Projects are tracked in `~/.config/tinyleaf/projects.json` — each entry maps a name to an absolute path anywhere on the filesystem.

From the project page you can:

- **Open Folder** — browse the server filesystem and register an existing directory
- **New Project** — create a new project at a chosen location
- **Remove** — unregister a project (optionally delete files)

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

This starts the web editor on `http://localhost:14159` with a persistent TeX Live container for compilation.

## Why tinyleaf?

| | tinyleaf | Overleaf CE |
|---|---------|-------------|
| Install | `pip install tinyleaf` | Docker Compose (MongoDB + Redis + Node + CLSI + …) |
| Dependencies | **Zero** (Python stdlib only) | 6+ services |
| Memory | ~30 MB | ~1 GB+ |
| Startup | Instant | Minutes |
| Compilation | Local `latexmk` or Docker | Built-in CLSI |
| Git | Built-in UI | Server-side Git bridge |
| Collaboration | Single-user | Multi-user |

tinyleaf is designed for **individual users** who want a browser-based LaTeX editing experience without the operational overhead of a full Overleaf deployment.

## License

AGPL-3.0-or-later
