# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-28

Initial release of tinyleaf (formerly texlive-web).

### Added

#### Core

- **CLI-first design** with `pip install tinyleaf && tinyleaf /path` to start editing
- **Single project mode** for opening a specific LaTeX project directory
- **Multi-project mode** with JSON-based project registry (`~/.config/tinyleaf/projects.json`)
    - Open Folder to browse and register existing directories
    - New Project to create a project at a chosen location
    - Rename and Remove projects from the UI
    - Grid and list view toggle with persistent preference
    - Project search filtering by name and path
- **Two compilation backends**: local `latexmk` and Docker (default: enabled)
- **Zero Python dependencies** — stdlib only (`http.server`, `threading`, `subprocess`)

#### Editor

- **CodeMirror 6** editor with LaTeX syntax highlighting
- Multi-language syntax highlighting (LaTeX, Markdown, JavaScript, Python, JSON, CSS, HTML, YAML)
- Auto-save with configurable interval
- Main file selector with auto-detection of `\documentclass`
- File path breadcrumb with locate-in-tree button
- External file change detection via mtime polling
- Binary file blocking (images previewed in PDF pane instead)

#### PDF Preview

- **PDF.js** viewer with live reload after compilation
- Zoom controls (+, -, Fit, percentage) and HD/fast rendering toggle
- **SyncTeX** bidirectional search powered by a pure-Python parser
    - **Inverse search**: `Ctrl+Click` on PDF to jump to the corresponding source line
    - **Forward search**: `Ctrl+Shift+Enter` in editor to jump to the corresponding PDF position with highlight flash
- Color-coded status bar messages (error/warning/success)
- Compile cancellation support

#### Sidebar & File Tree

- Resizable and collapsible sidebar and PDF panels
- Files and Git tabs
- File tree with expand/collapse state persistence
- Collapse-all button, search, upload, new file/folder, delete, rename
- **Project-wide text search** (`Ctrl+Shift+F`) — grep-style search across all project files with results grouped by file, keyword highlighting, and click-to-jump navigation
- LaTeX build artifacts grayed out in tree

#### Git Integration

- Git status, diff (including per-file diff view), commit, push, pull, and log
- Selective file staging for commits
- Git badge on project cards indicating repository status

#### Settings & UI

- 7 themes with dark/light toggle (Light, Indigo Dark, Dracula, etc.)
- Docker toggle with image management (pull, delete, registry mirror)
- Auto-pull Docker images on first compile
- About popup with version, GitHub, and PyPI links
- Keyboard shortcuts help panel (`Ctrl+/`)
- i18n support (English and Chinese)
- Vendor JS modules with CDN fallback and proxy support

#### Compilation

- SSE (Server-Sent Events) real-time compilation log streaming
- Log panel with copy button
- Clean build artifacts button
- Docker Compose support for self-contained deployment

#### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save file |
| `Ctrl+Enter` | Compile |
| `Ctrl+Shift+Enter` | Jump to PDF (forward search) |
| `Ctrl+Click` (PDF) | Jump to source (inverse search) |
| `Ctrl+Shift+E` | Files tab |
| `Ctrl+Shift+F` | Search tab |
| `Ctrl+Shift+G` | Git tab |
| `Ctrl+Shift+Alt+C` | Git commit |
| `Ctrl+Shift+Alt+P` | Git push |
| `Ctrl+/` | Show shortcuts |

### Changed

- Renamed project from `texlive-web` to `tinyleaf`
- Renamed Python package from `texlive_web` to `tinyleaf`
- Updated CLI entry point, config directory, and program name
- Default compilation backend changed to Docker (use `--no-docker` for local)

[0.1.0]: https://github.com/Oaklight/tinyleaf/releases/tag/v0.1.0
