# tinyleaf

<p align="center">
  <img src="assets/brand/tinyleaf-leafpen-readme-light.svg" alt="Tinyleaf" width="560">
</p>

[![PyPI version](https://img.shields.io/pypi/v/tinyleaf?color=green)](https://pypi.org/project/tinyleaf/)
[![GitHub release](https://img.shields.io/github/v/release/Oaklight/tinyleaf?color=green)](https://github.com/Oaklight/tinyleaf/releases/latest)
[![CI](https://github.com/Oaklight/tinyleaf/actions/workflows/lint.yml/badge.svg)](https://github.com/Oaklight/tinyleaf/actions/workflows/lint.yml)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Documentation](https://img.shields.io/badge/docs-readthedocs-blue)](https://tinyleaf.readthedocs.io)

[中文版](./README_zh.md) | [Documentation](https://tinyleaf.readthedocs.io) | [Brand assets](./BRAND.md)

**Tinyleaf is a tiny, local-first TeX editor that runs in your browser.**

It is built for people who want an Overleaf-like editing experience without running a full Overleaf stack. Install one Python package, point it at a LaTeX project, and edit from a clean web UI with PDF preview, compile logs, Git tools, search, outline, and multi-tab editing.

```bash
pip install tinyleaf

# Open one project. Docker-based TeX Live compilation is enabled by default.
tinyleaf /path/to/my-thesis

# Or use a local TeX installation instead.
tinyleaf /path/to/my-thesis --no-docker

# Launch the project registry.
tinyleaf
```

## Why Tinyleaf?

Tinyleaf sits between a local editor and a full collaborative LaTeX platform:

- **Local-first** — your projects stay on your filesystem
- **Self-hosted** — run it on your laptop, workstation, lab server, or VPS
- **Small runtime** — no database, no Node.js service, no Redis, no MongoDB
- **Browser UI** — CodeMirror editor, PDF preview, file tree, Git panel, and settings
- **Flexible compilation** — Dockerized TeX Live by default, or local `latexmk` with `--no-docker`
- **Single-user focused** — designed for individual writing workflows, not a multi-user SaaS clone

## Features

### Editing

- CodeMirror 6 editor with LaTeX syntax highlighting
- Multi-tab editing with quick open (`Ctrl+P`)
- Auto-pair `\begin{...}` / `\end{...}`
- Project-wide search
- LaTeX outline sidebar with recursive `\input` / `\include` support
- `\ref{}`, `\cite{}`, and `\label{}` autocomplete from project symbols

### PDF and compilation

- PDF.js preview with live reload
- Page navigation, zoom controls, and text search
- Real-time compile logs over SSE
- Clickable `file.tex:line` entries in compile output
- SyncTeX forward/reverse search
- Word/page statistics via `texcount`
- Export project as ZIP

### Projects and workflow

- Single-project mode: open any directory directly
- Multi-project registry stored at `~/.config/tinyleaf/projects.json`
- File tree with create, upload, rename, delete, and search
- Git status, diff, commit, push, pull, and log from the UI
- 7 UI themes with light/dark mode
- English and Chinese UI

## Installation

```bash
pip install tinyleaf
```

Tinyleaf has **zero Python runtime dependencies** beyond the standard library. The web editor assets are bundled with the package.

For compilation, choose one of:

| Backend | Command | Requirements |
|---|---|---|
| Docker TeX Live | `tinyleaf /path/to/project` | Docker installed |
| Local TeX Live | `tinyleaf /path/to/project --no-docker` | `latexmk` available in `PATH` |

## Usage

```text
usage: tinyleaf [-h] [-V] [--projects-dir DIR] [--config-dir DIR]
                [--docker | --no-docker] [--image IMAGE] [--port PORT]
                [--host HOST] [--no-browser]
                [project_path]
```

Common examples:

```bash
# Open a project and compile with Docker.
tinyleaf ~/papers/my-paper

# Use local latexmk instead of Docker.
tinyleaf ~/papers/my-paper --no-docker

# Bind to all interfaces on a server.
tinyleaf ~/papers/my-paper --host 0.0.0.0 --port 14159

# Start the multi-project registry view.
tinyleaf
```

## Multi-project registry

When launched without a `project_path`, Tinyleaf opens a project registry. The registry maps project names to absolute paths anywhere on the filesystem.

From the project page you can:

- **Open Folder** — register an existing directory
- **New Project** — create a new project at a chosen location
- **Remove** — unregister a project, optionally deleting files
- **Switch views** — grid/list layout with persistent preferences

## Keyboard shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+S` | Save current file |
| `Ctrl+Enter` | Compile |
| `Ctrl+P` | Quick open |
| `Ctrl+Shift+F` | Project search |
| `Ctrl+Shift+C` | Git commit |
| `Ctrl+Shift+P` | Git push |
| `Ctrl+/` | Shortcut help |

## Docker Compose

For a simple containerized setup:

```bash
docker compose up
```

Tinyleaf starts at `http://localhost:14159`.

## Tinyleaf vs. Overleaf CE

| | Tinyleaf | Overleaf CE |
|---|---|---|
| Primary use case | Personal/local TeX editing | Multi-user collaborative platform |
| Install | `pip install tinyleaf` | Docker Compose stack |
| Runtime services | Python stdlib server | MongoDB, Redis, Node.js, CLSI, etc. |
| Project storage | Your filesystem | Application-managed storage |
| Compilation | Docker TeX Live or local `latexmk` | CLSI service |
| Git workflow | Built-in lightweight UI | Git Bridge |
| Collaboration | Single-user focused | Multi-user |

Tinyleaf is not trying to replace the full Overleaf collaboration model. It is for writers who want a fast, self-hosted browser editor for their own TeX projects.

## Documentation

- [Documentation](https://tinyleaf.readthedocs.io)
- [Brand assets](./BRAND.md)
- [Trademark and naming policy](./TRADEMARKS.md)

## License

AGPL-3.0-or-later
