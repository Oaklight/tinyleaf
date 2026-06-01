---
hide:
  - navigation
---

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-05-25

### Added

- New Tinyleaf leaf-pen brand system, with logo assets integrated into README and documentation sites
- Brand assets page for the documentation site

### Changed

- Project license changed from MIT to AGPL-3.0-or-later for 0.5.0 and later; previously published releases remain under the license terms under which they were originally published
- Default wordmark updated to STIX Two Text
- Leaf-pen spine and pen tip unified with Pale Mint (`#d1fae5`)

## [0.4.0] - 2026-05-25

### Added

- **\ref/\cite/\label autocomplete** — context-aware completions triggered by `\ref{`, `\cite{`, `\label{` with symbols scanned from `.tex` and `.bib` files
- **PDF text search** (`Ctrl+F` in PDF pane) — search within rendered PDF with match highlighting and prev/next navigation
- **Export project as ZIP** — download the entire project as a `.zip` archive
- **Word/page count** — `texcount`-based word and page statistics displayed in the status bar
- **PDF page navigation** — page input field and prev/next buttons in the PDF toolbar
- **Auto-pair `\begin{env}` → `\end{env}`** — typing `\begin{...}` automatically inserts matching `\end{...}`
- **Quick Open** (`Ctrl+P`) — fuzzy file switcher palette
- **Multi-tab editor** — open multiple files in tabs with `Ctrl+W` to close and `Ctrl+Tab` to cycle
- **Git diff viewer** — production-quality staged/unstaged split diff view
- **LaTeX outline** sidebar tab — document structure from `\section`, `\subsection`, etc. with `\input`/`\include` recursion
- **Clickable compile log** — `filename:line` references in log output jump to the source location
- **SyncTeX tooltip** — hover text on PDF pages showing `Ctrl+Click to jump to source`
- **`--version` / `-V` flag** — shows current version with PyPI update check
- **Emerald theme** — light theme accent changed from blue to emerald green (#059669)
- **SVG leaf logo** — custom favicon and toolbar brand icon

### Changed

- Default port changed from `8080` to `14159` (π)
- Duplicate Commit/Push buttons removed from toolbar (kept in Git sidebar)
- PDF search button uses SVG icon instead of emoji
- Checkboxes follow theme accent color via `accent-color`
- `Ctrl+H` intercepted to open editor find/replace panel instead of browser history

### Internal

- **Frontend sharding** — monolithic `index.html` (~5700 lines) split into `index.html` + `css/app.css` + `js/app.js`
- Static file serving with `/static/` route, MIME type detection, and path traversal protection
- Inline `onclick` handlers migrated to `addEventListener` for ES module compatibility

## [0.3.0] - 2026-05-18

### Added

- **Layout switcher** (Overleaf-style) in statusbar bottom-left — three presets:
    - **Editor**: sidebar + editor, PDF hidden
    - **Split**: all three panels visible (default)
    - **PDF**: PDF only, sidebar and editor hidden
- **Sidebar toggle button** in toolbar — shown when a project is open
- **Compile log toggle** button moved to statusbar; `Ctrl+\`` shortcut to open/close log panel
- Keyboard shortcuts for layout switching: `Ctrl+Shift+1` / `2` / `3`
- `Ctrl+B` shortcut to toggle sidebar (disabled in PDF-only mode)
- Layout preference persisted to `localStorage`
- New shortcuts shown in the keyboard shortcuts popup (EN/ZH)

### Changed

- Compile log toggle button moved from toolbar to statusbar (right side)
- Layout switcher placed at far left of statusbar for visual prominence

### Internal

- Added CI lint workflow (ruff + ty via pre-commit) on push and PR
- Added release workflow (manual `workflow_dispatch`)
- Fixed `ty` type narrowing: `assert proc.stdout is not None` in `compiler.py`
- Excluded `_vendor/` from ruff formatting

## [0.2.0] - 2026-04-29

### Added

- **Project-wide text search** (`Ctrl+Shift+F`) — grep-style search across all project files with results grouped by file, keyword highlighting, and click-to-jump navigation
- **Close file button** (×) in breadcrumb bar — return editor to blank state
- Case-sensitive toggle for project search

### Fixed

- **CDN fallback**: switch from jsdelivr to esm.sh for proper module deduplication — fixes CodeMirror crash ("multiple instances of @codemirror/state") in single-project mode without vendor files
- Add try-catch fallback when language extensions conflict with CDN modules (editor works without syntax highlighting)

### Changed

- Breadcrumb bar layout: locate button moved to the left of the filename, close button on the right

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

[0.4.0]: https://github.com/Oaklight/tinyleaf/releases/tag/v0.4.0
[0.3.0]: https://github.com/Oaklight/tinyleaf/releases/tag/v0.3.0
[0.2.0]: https://github.com/Oaklight/tinyleaf/releases/tag/v0.2.0
[0.1.0]: https://github.com/Oaklight/tinyleaf/releases/tag/v0.1.0
