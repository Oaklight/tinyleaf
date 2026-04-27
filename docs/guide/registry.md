# Multi-Project Registry

When tinyleaf is launched without a `project_path` argument, it enters **multi-project mode** backed by a project registry.

## How It Works

Projects are stored in `~/.config/tinyleaf/projects.json`:

```json
{
  "my-thesis": {
    "path": "/home/user/documents/thesis",
    "added_at": "2025-01-15T10:30:00"
  },
  "paper-2025": {
    "path": "/home/user/research/paper",
    "added_at": "2025-02-20T14:00:00"
  }
}
```

Each entry maps a project name to an **absolute filesystem path**. Projects can live anywhere — they don't need to be in the same parent directory.

## Managing Projects

### From the UI

- **Open Folder** — browse the server filesystem and register an existing directory
- **New Project** — specify a name and parent path to create a new project with a default `main.tex`
- **Rename** — change a project's display name
- **Remove** — unregister a project, with an optional checkbox to also delete files from disk
- **Search** — filter projects by name or path using the search box

### View Modes

The project list supports two view modes, toggled via buttons in the toolbar:

- **Grid view** — card layout showing project name, path, and git badge
- **List view** — compact single-column layout with timestamps

Your view preference is persisted in `localStorage`.

![Grid view](../assets/tinyleaf-project-list-en.png)

### CLI Options

```bash
# Registry mode (default when no path given)
tinyleaf

# Custom config directory
tinyleaf --config-dir /path/to/config

# Legacy migration: auto-register all subdirectories
tinyleaf --projects-dir /path/to/old/projects
```

## Git Badge

Projects that are git repositories display a git badge next to the project name. This provides a quick visual indicator of version control status.

## Stale Projects

If a registered project's directory no longer exists on disk, it is displayed with a dashed border and "(missing)" label. You can remove stale entries from the project page.

## Thread Safety

The registry uses a `threading.Lock` and atomic writes (`os.replace`) to ensure consistency under concurrent access from the threaded HTTP server.
