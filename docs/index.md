---
title: Tinyleaf
hide:
  - navigation
  - title
---

<div class="tinyleaf-hero" markdown>

![Tinyleaf banner](assets/brand/tinyleaf-leafpen-readme-light.svg){ .tinyleaf-hero__banner .tinyleaf-hero__banner--light }
![Tinyleaf banner](assets/brand/tinyleaf-leafpen-readme-dark.svg){ .tinyleaf-hero__banner .tinyleaf-hero__banner--dark }

<p class="tinyleaf-hero__tagline">A lightweight LaTeX editor tuned for a fast, focused writing flow.</p>

<p class="tinyleaf-hero__desc">Open a project, edit LaTeX, preview the PDF, and keep the compile loop close at hand. Tinyleaf keeps writing quick, focused, and distraction-free.</p>

<p class="tinyleaf-badges">
  <a href="https://pypi.org/project/tinyleaf/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/tinyleaf?color=059669"></a>
  <a href="https://github.com/Oaklight/tinyleaf/releases/latest"><img alt="GitHub release" src="https://img.shields.io/badge/release-v0.5.0-059669"></a>
  <a href="https://github.com/Oaklight/tinyleaf/actions/workflows/lint.yml"><img alt="CI" src="https://github.com/Oaklight/tinyleaf/actions/workflows/lint.yml/badge.svg"></a>
  <a href="https://www.gnu.org/licenses/agpl-3.0"><img alt="License: AGPL v3" src="https://img.shields.io/badge/License-AGPL_v3-047857.svg"></a>
</p>

<p class="tinyleaf-actions">
  <a class="tinyleaf-button tinyleaf-button--primary" href="getting-started/quickstart/">Quick Start</a>
  <a class="tinyleaf-button tinyleaf-button--secondary" href="screenshots/">View Screenshots</a>
  <a class="tinyleaf-button tinyleaf-button--secondary" href="https://github.com/Oaklight/tinyleaf">GitHub</a>
</p>

</div>

![Editor view](assets/tinyleaf-editor.png)

## Highlights

- **Zero dependencies** — stdlib only (`http.server` + `threading` + `subprocess`)
- **Two modes** — single project or multi-project with a persistent registry
- **Two compilation backends** — local `latexmk` or Docker containers (default)
- **CodeMirror 6** editor with multi-language syntax highlighting
- **PDF.js** preview with zoom, HD rendering, text search, and page navigation
- **LaTeX autocomplete** — `\ref{}`, `\cite{}`, `\label{}` with project symbol scanning
- **Git integration** — status, diff, commit, push, pull from the UI
- **Multi-tab editor** with quick-open (`Ctrl+P`) and auto-pair `\begin`/`\end`
- **7 themes** with dark/light toggle (emerald accent)
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
