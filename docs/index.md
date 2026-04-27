---
hide:
  - navigation
---

# Tinyleaf

**Lightweight, zero-dependency web-based LaTeX editor.**

Tinyleaf is a CLI-first LaTeX editor that runs in your browser. It requires no Python dependencies beyond the standard library, and supports both local and Docker-based compilation.

![Editor view](assets/tinyleaf-editor.png)

## Highlights

- **Zero dependencies** — stdlib only (`http.server` + `threading` + `subprocess`)
- **Two modes** — single project or multi-project with a persistent registry
- **Two compilation backends** — local `latexmk` or Docker containers (default)
- **CodeMirror 6** editor with multi-language syntax highlighting
- **PDF.js** preview with zoom controls and HD rendering
- **Git integration** — status, diff, commit, push, pull from the UI
- **7 themes** with dark/light toggle
- **i18n** — English and Chinese
- **Keyboard shortcuts** — full shortcut help panel (`Ctrl+/`)

## Quick Start

```bash
pip install tinyleaf

# Single project (Docker compilation enabled by default)
tinyleaf /path/to/my-thesis

# Multi-project (registry mode)
tinyleaf

# Local compilation (no Docker)
tinyleaf /path/to/my-thesis --no-docker
```

See [more screenshots](screenshots.md) for a full tour of the UI.

## Links

- [GitHub Repository](https://github.com/Oaklight/tinyleaf)
- [PyPI Package](https://pypi.org/project/tinyleaf/)
