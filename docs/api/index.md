# API Reference

Tinyleaf exposes a RESTful HTTP API consumed by the browser frontend. All responses use UTF-8 encoding. Errors return `{"error": "description"}`.

!!! note "Single vs. Multi-project mode"
    In **single-project mode**, project management endpoints (`POST /api/projects`, `DELETE`, etc.) are unavailable. In **multi-project mode**, all endpoints are active.

---

## Mode & Docker

### `GET /api/mode`

Returns the server mode and Docker configuration.

**Response:**

```json
{
  "mode": "single",
  "docker": true,
  "image": "oaklight/texlive:alpine-science-cn",
  "version": "0.1.0"
}
```

### `GET /api/docker/images`

Lists available Docker image tags and whether they exist locally.

**Response:**

```json
[
  {"tag": "alpine-science-cn", "name": "oaklight/texlive:alpine-science-cn", "local": true},
  {"tag": "alpine-science", "name": "oaklight/texlive:alpine-science", "local": false}
]
```

### `POST /api/docker/pull`

Pull a Docker image. Returns when the pull completes.

**Request:** `{"image": "oaklight/texlive:alpine-science"}`

**Response:** `{"success": true, "message": "Pulled oaklight/texlive:alpine-science"}`

### `POST /api/docker/rmi`

Remove a local Docker image.

**Request:** `{"image": "oaklight/texlive:alpine-science"}`

**Response:** `{"success": true, "message": "Removed oaklight/texlive:alpine-science"}`

---

## Projects

### `GET /api/projects`

List all registered projects.

**Response:**

```json
[
  {
    "name": "my-thesis",
    "path": "/home/user/documents/thesis",
    "added_at": "2025-01-15T10:30:00",
    "exists": true,
    "git": true
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Project display name |
| `path` | string | Absolute filesystem path |
| `exists` | bool | Whether the directory exists on disk |
| `git` | bool | Whether the directory is a git repository |

### `POST /api/projects`

Create a new project with a default `main.tex`.

**Request:**

```json
{"name": "new-paper", "path": "/home/user/documents"}
```

**Response (201):**

```json
{"name": "new-paper", "path": "/home/user/documents/new-paper"}
```

**Errors:** `409` if directory already exists, `400` if name is invalid.

### `POST /api/projects/register`

Register an existing directory as a project.

**Request:**

```json
{"path": "/home/user/documents/thesis", "name": "my-thesis"}
```

The `name` field is optional — defaults to the directory basename.

**Response (201):**

```json
{"name": "my-thesis", "path": "/home/user/documents/thesis", "added_at": "2025-01-15T10:30:00"}
```

### `DELETE /api/projects/{name}`

Unregister a project. Optionally delete files from disk.

**Request:**

```json
{"delete_files": false}
```

**Response:**

```json
{"deleted": "my-thesis", "files_deleted": false}
```

### `POST /api/projects/{name}/rename-project`

Rename a project's display name.

**Request:** `{"new_name": "thesis-v2"}`

**Response:** `{"old_name": "my-thesis", "new_name": "thesis-v2"}`

---

## Filesystem Browser

### `GET /api/fs/browse?path={dir_path}`

List subdirectories at the given path. Used by the "Open Folder" dialog.

**Response:**

```json
{"path": "/home/user", "dirs": ["documents", "projects", "Desktop"]}
```

---

## Files

### `GET /api/projects/{name}/files`

Returns the full file tree as a nested structure.

**Response:**

```json
[
  {
    "name": "main.tex",
    "path": "main.tex",
    "type": "file",
    "mtime": 1706000000
  },
  {
    "name": "sections",
    "path": "sections",
    "type": "dir",
    "children": [
      {"name": "intro.tex", "path": "sections/intro.tex", "type": "file", "mtime": 1706000000}
    ]
  }
]
```

### `GET /api/projects/{name}/files/{file_path}`

Read file content (UTF-8 text files only).

**Response:**

```json
{"path": "main.tex", "content": "\\documentclass{article}\n...", "mtime": 1706000000}
```

**Errors:** `400` if the file is binary, `404` if not found.

### `GET /api/projects/{name}/check/{file_path}`

Check if a file exists and get its modification time. Useful for detecting external changes.

**Response:**

```json
{"path": "main.tex", "mtime": 1706000000}
```

Returns `{"exists": false}` if the file does not exist.

### `PUT /api/projects/{name}/files/{file_path}`

Write file content. Creates parent directories automatically.

**Request:**

```json
{"content": "\\documentclass{article}\n..."}
```

**Response:** `{"path": "main.tex", "saved": true}`

### `DELETE /api/projects/{name}/files/{file_path}`

Delete a file or directory (recursive).

**Response:** `{"path": "old-file.tex", "deleted": true}`

### `POST /api/projects/{name}/mkdir`

Create a new directory.

**Request:** `{"path": "figures/plots"}`

**Response:** `{"path": "figures/plots", "created": true}`

**Errors:** `409` if the path already exists.

### `POST /api/projects/{name}/rename`

Rename or move a file or directory.

**Request:**

```json
{"old_path": "intro.tex", "new_path": "sections/intro.tex"}
```

**Response:** `{"old_path": "intro.tex", "new_path": "sections/intro.tex", "renamed": true}`

### `POST /api/projects/{name}/upload`

Upload files via multipart form data.

**Request:** `Content-Type: multipart/form-data`

| Field | Type | Description |
|-------|------|-------------|
| `files` | file(s) | One or more files to upload |
| `target_dir` | string | Optional subdirectory path |

**Response:**

```json
{"uploaded": ["figures/plot1.png", "figures/plot2.png"], "count": 2}
```

---

## Configuration

### `GET /api/projects/{name}/config`

Read project configuration. Returns auto-detected values if no `.tinyleaf.json` exists.

**Response:**

```json
{
  "main_file": "main.tex",
  "engine": "pdflatex",
  "use_docker": true,
  "docker_image": "oaklight/texlive:alpine-science-cn"
}
```

### `PUT /api/projects/{name}/config`

Update project configuration. Fields are merged with existing values.

**Request:**

```json
{"engine": "lualatex", "main_file": "thesis.tex"}
```

**Response:** Full config object after merge.

### `GET /api/settings`

Read global settings (multi-project mode only).

### `PUT /api/settings`

Update global settings. Merged with existing values.

**Request:**

```json
{"registry_mirror": "docker.1ms.run"}
```

---

## Compilation

### `POST /api/projects/{name}/compile`

Start an asynchronous compilation job.

**Request (all fields optional):**

```json
{
  "main_file": "main.tex",
  "engine": "pdflatex",
  "use_docker": true,
  "docker_image": "oaklight/texlive:alpine-science-cn"
}
```

**Response:**

```json
{"compile_id": "a1b2c3d4", "main_file": "main.tex", "engine": "pdflatex"}
```

### `GET /api/projects/{name}/compile/{compile_id}/stream`

Server-Sent Events (SSE) stream for compilation logs.

**Event types:**

| Event | Data | Description |
|-------|------|-------------|
| `log` | `{"line": "...", "level": "info"}` | A line of compilation output |
| `done` | `{"status": "success", "pdf_url": "/api/projects/.../output/main.pdf"}` | Compilation finished |

The `level` field is one of `info`, `warning`, or `error`. The `status` field is one of `success`, `error`, or `cancelled`.

### `POST /api/projects/{name}/compile/{compile_id}/cancel`

Cancel a running compilation.

**Response:** `{"cancelled": true}`

### `GET /api/projects/{name}/output/{file_path}`

Download a compiled output file (PDF, images, etc.). Returns the binary file with appropriate `Content-Type`.

### `POST /api/projects/{name}/clean`

Remove LaTeX build artifacts (`.aux`, `.log`, `.synctex.gz`, etc.).

**Response:**

```json
{"removed": ["main.aux", "main.log", "main.synctex.gz"], "count": 3}
```

---

## Git

All Git endpoints return `{"git": false}` if the project is not a Git repository.

### `GET /api/projects/{name}/git/status`

**Response:**

```json
{
  "git": true,
  "branch": "main",
  "files": [
    {"path": "main.tex", "status": "M"},
    {"path": "new-file.tex", "status": "??"}
  ],
  "ahead": 1,
  "behind": 0
}
```

Status codes follow git porcelain format: `M` (modified), `A` (added), `D` (deleted), `??` (untracked), etc.

### `GET /api/projects/{name}/git/diff`

Returns the full project diff as plain text.

### `GET /api/projects/{name}/git/diff/{file_path}`

Returns the diff for a single file as plain text.

### `GET /api/projects/{name}/git/log`

Returns the last 20 commits.

**Response:**

```json
[
  {
    "hash": "a1b2c3d",
    "message": "Add introduction section",
    "author": "Alice",
    "date": "2025-01-15T10:30:00"
  }
]
```

### `POST /api/projects/{name}/git/commit`

Stage files and create a commit.

**Request:**

```json
{"message": "Update thesis draft", "files": ["main.tex", "sections/intro.tex"]}
```

If `files` is omitted, all changed files are staged.

**Response:** `{"success": true, "message": "Committed a1b2c3d"}`

### `POST /api/projects/{name}/git/push`

Push to the remote repository.

**Response:** `{"success": true, "message": "Pushed to origin/main"}`

### `POST /api/projects/{name}/git/pull`

Pull from the remote repository.

**Response:** `{"success": true, "message": "Already up to date"}`

---

## SyncTeX

SyncTeX provides bidirectional navigation between source files and compiled PDF output. Requires a `.synctex.gz` file generated by compiling with `-synctex=1` (enabled by default in tinyleaf).

### `GET /api/projects/{name}/synctex?page={N}&x={X}&y={Y}`

Inverse search: find the source location for a point on a PDF page.

**Query parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | int | 1-based page number |
| `x` | float | Horizontal position in PDF points (72 DPI) |
| `y` | float | Vertical position in PDF points (72 DPI) |

**Response:**

```json
{"file": "main.tex", "line": 42}
```

**Errors:** `404` if no SyncTeX file exists or no match is found.

### `GET /api/projects/{name}/synctex/forward?file={path}&line={N}`

Forward search: find the PDF position for a source file and line number.

**Query parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `file` | string | Source file path (relative to project root) |
| `line` | int | 1-based line number |

**Response:**

```json
{"page": 1, "x": 150.0, "y": 300.0}
```

Coordinates are in PDF points (72 DPI).

**Errors:** `400` if parameters are missing, `404` if no SyncTeX file exists or no match is found.
