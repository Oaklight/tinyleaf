"""Project registry for tinyleaf.

Manages a JSON-based registry that maps project names to filesystem paths.
Stored at ``<config_dir>/projects.json``.
"""

import json
import os
import shutil
import threading
from datetime import datetime

REGISTRY_FILE = "projects.json"

_lock = threading.Lock()


def ensure_config_dir(config_dir):
    """Create the config directory if it does not exist."""
    os.makedirs(config_dir, exist_ok=True)


def load_registry(config_dir):
    """Read and parse the registry file.

    Returns:
        A dict with ``version`` and ``projects`` keys.
    """
    path = os.path.join(config_dir, REGISTRY_FILE)
    with _lock:
        if not os.path.exists(path):
            return {"version": 1, "projects": {}}
        with open(path, encoding="utf-8") as f:
            return json.load(f)


def save_registry(config_dir, data):
    """Atomically write the registry file."""
    path = os.path.join(config_dir, REGISTRY_FILE)
    tmp_path = path + ".tmp"
    with _lock:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, path)


def list_projects(config_dir):
    """Return all registered projects sorted by name.

    Returns:
        List of dicts: ``[{name, path, added_at, exists}]``.
    """
    data = load_registry(config_dir)
    result = []
    for name, info in sorted(data["projects"].items()):
        result.append(
            {
                "name": name,
                "path": info["path"],
                "added_at": info.get("added_at", ""),
                "exists": os.path.isdir(info["path"]),
            }
        )
    return result


def get_project_path(config_dir, name):
    """Look up a project path by name.

    Returns:
        Absolute path string or None if not found.
    """
    data = load_registry(config_dir)
    info = data["projects"].get(name)
    return info["path"] if info else None


def register_project(config_dir, name, path):
    """Register an existing directory as a project.

    Args:
        config_dir: Config directory containing the registry.
        name: Project name (no slashes, no leading dots).
        path: Absolute filesystem path to the project directory.

    Returns:
        Dict with the new entry info.

    Raises:
        ValueError: If name is invalid, path is not absolute, path
            does not exist, or name already taken.
    """
    if not name or "/" in name or name.startswith("."):
        raise ValueError(f"Invalid project name: {name}")
    if not os.path.isabs(path):
        raise ValueError("Path must be absolute")
    if not os.path.isdir(path):
        raise ValueError(f"Directory not found: {path}")

    data = load_registry(config_dir)
    if name in data["projects"]:
        raise ValueError(f"Project name already exists: {name}")

    entry = {
        "path": path,
        "added_at": datetime.now().isoformat(timespec="seconds"),
    }
    data["projects"][name] = entry
    save_registry(config_dir, data)
    return entry


def unregister_project(config_dir, name, delete_files=False):
    """Remove a project from the registry.

    Args:
        config_dir: Config directory containing the registry.
        name: Project name to remove.
        delete_files: If True, also delete the project directory from disk.

    Raises:
        KeyError: If the project name is not in the registry.
    """
    data = load_registry(config_dir)
    if name not in data["projects"]:
        raise KeyError(f"Project not found: {name}")

    project_path = data["projects"][name]["path"]
    del data["projects"][name]
    save_registry(config_dir, data)

    if delete_files and os.path.isdir(project_path):
        shutil.rmtree(project_path)


def rename_project(config_dir, old_name, new_name):
    """Rename a project in the registry.

    Args:
        config_dir: Config directory containing the registry.
        old_name: Current project name.
        new_name: New project name.

    Raises:
        KeyError: If old_name is not found.
        ValueError: If new_name is invalid or already taken.
    """
    if not new_name or "/" in new_name or new_name.startswith("."):
        raise ValueError(f"Invalid project name: {new_name}")

    data = load_registry(config_dir)
    if old_name not in data["projects"]:
        raise KeyError(f"Project not found: {old_name}")
    if new_name in data["projects"]:
        raise ValueError(f"Project name already exists: {new_name}")

    data["projects"][new_name] = data["projects"].pop(old_name)
    save_registry(config_dir, data)
