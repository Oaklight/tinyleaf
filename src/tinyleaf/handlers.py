"""API request handlers for tinyleaf."""

import io
import json
import os
import re
import subprocess
import time
import zipfile

from tinyleaf import compiler, git_ops, registry, vendor
from tinyleaf._vendor import synctex

# Project config file name
CONFIG_FILE = ".tinyleaf.json"
SETTINGS_FILE = "settings.json"


def handle_request(handler, action, **kwargs):
    """Dispatch an API action to the appropriate handler function."""
    dispatch = {
        "get_mode": _get_mode,
        "list_docker_images": _list_docker_images,
        "docker_pull": _docker_pull,
        "docker_rmi": _docker_rmi,
        "cancel_docker_pull": _cancel_docker_pull,
        "list_projects": _list_projects,
        "create_project": _create_project,
        "register_project": _register_project,
        "delete_project": _delete_project,
        "rename_project": _rename_project,
        "browse_filesystem": _browse_filesystem,
        "vendor_status": _vendor_status,
        "update_vendor": _update_vendor,
        "get_settings": _get_settings,
        "put_settings": _put_settings,
        "list_files": _list_files,
        "read_file": _read_file,
        "check_file": _check_file,
        "write_file": _write_file,
        "delete_file": _delete_file,
        "mkdir": _mkdir,
        "rename_path": _rename_path,
        "upload": _upload,
        "get_config": _get_config,
        "put_config": _put_config,
        "compile": _compile,
        "cancel_compile": _cancel_compile,
        "compile_stream": _compile_stream,
        "get_output": _get_output,
        "synctex_query": _synctex_query,
        "synctex_forward": _synctex_forward,
        "clean": _clean,
        "search_files": _search_files,
        "git_status": _git_status,
        "git_diff": _git_diff,
        "git_diff_file": _git_diff_file,
        "git_commit": _git_commit,
        "git_push": _git_push,
        "git_pull": _git_pull,
        "git_log": _git_log,
        "word_count": _word_count,
        "export_zip": _export_zip,
    }
    fn = dispatch.get(action)
    if fn:
        fn(handler, **kwargs)
    else:
        handler.send_json({"error": f"Unknown action: {action}"}, status=400)


# ── Helpers ──


def _get_project_dir(handler, name):
    """Resolve project name to directory path.

    Returns:
        Absolute path or None (sends error response).
    """
    config = handler.config

    if config["mode"] == "single":
        return config["project_path"]

    # Multi-project mode: look up in registry
    project_dir = registry.get_project_path(config["config_dir"], name)
    if not project_dir:
        handler.send_json({"error": f"Project not found: {name}"}, status=404)
        return None
    if not os.path.isdir(project_dir):
        handler.send_json({"error": f"Project directory missing: {project_dir}"}, status=404)
        return None
    return project_dir


def _read_project_config(project_dir):
    """Read .tinyleaf.json from a project directory."""
    config_path = os.path.join(project_dir, CONFIG_FILE)
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return {}


def _write_project_config(project_dir, config_data):
    """Write .tinyleaf.json to a project directory."""
    config_path = os.path.join(project_dir, CONFIG_FILE)
    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=2, ensure_ascii=False)


def _detect_main_file(project_dir):
    """Auto-detect the main .tex file by looking for \\documentclass."""
    candidates = []
    for fname in os.listdir(project_dir):
        if not fname.endswith(".tex"):
            continue
        fpath = os.path.join(project_dir, fname)
        try:
            with open(fpath, encoding="utf-8", errors="ignore") as f:
                content = f.read(4096)
            if "\\documentclass" in content:
                candidates.append(fname)
        except OSError:
            continue

    if len(candidates) == 1:
        return candidates[0]
    if "main.tex" in candidates:
        return "main.tex"
    return candidates[0] if candidates else "main.tex"


# ── Mode ──


def _get_mode(handler):
    from tinyleaf import __version__

    config = handler.config
    handler.send_json(
        {
            "mode": config["mode"],
            "docker": config["use_docker"],
            "image": config["docker_image"],
            "version": __version__,
        }
    )


# Docker image name prefix for filtering
_DOCKER_IMAGE_PREFIX = "oaklight/texlive"

# Known tags (stable list — update manually when new tags are added)
_KNOWN_TAGS = [
    "latest",
    "alpine-science",
    "alpine-science-cn",
    "alpine-science-jp",
    "alpine-science-kr",
    "alpine-base",
    "alpine-base-cn",
    "alpine-base-jp",
    "alpine-base-kr",
    "debian-science",
    "debian-science-cn",
    "debian-science-jp",
    "debian-science-kr",
    "debian-base",
    "debian-base-cn",
    "debian-base-jp",
    "debian-base-kr",
]


def _list_docker_images(handler):
    """List known oaklight/texlive tags with local availability status."""
    local_tags = set()
    try:
        result = subprocess.run(
            ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}", _DOCKER_IMAGE_PREFIX],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if line and "<none>" not in line:
                    local_tags.add(line)
    except Exception:
        pass

    all_tags = []
    for name in _KNOWN_TAGS:
        full = f"{_DOCKER_IMAGE_PREFIX}:{name}"
        all_tags.append({"tag": full, "name": name, "local": full in local_tags})
    handler.send_json(all_tags)


def _docker_pull(handler):
    """Pull a Docker image, optionally via registry mirror."""
    body = handler.read_json_body()
    image = body.get("image")
    if not image:
        handler.send_json({"error": "Missing image"}, status=400)
        return

    config_dir = handler.config.get("config_dir")
    registry_mirror = None
    if config_dir:
        settings = _read_settings(config_dir)
        registry_mirror = settings.get("registry_mirror") or None

    success, msg = compiler.docker_pull_image(image, registry_mirror=registry_mirror)
    handler.send_json({"success": success, "message": msg})


def _docker_rmi(handler):
    """Remove a local Docker image."""
    body = handler.read_json_body()
    image = body.get("image")
    if not image:
        handler.send_json({"error": "Missing image"}, status=400)
        return

    success, msg = compiler.docker_remove_image(image)
    handler.send_json({"success": success, "message": msg})


def _cancel_docker_pull(handler):
    """Cancel a running docker pull."""
    body = handler.read_json_body()
    image = body.get("image")
    if not image:
        handler.send_json({"error": "Missing image"}, status=400)
        return

    cancelled = compiler.cancel_docker_pull(image)
    handler.send_json({"cancelled": cancelled})


# ── Projects ──


def _list_projects(handler):
    config = handler.config
    if config["mode"] == "single":
        name = os.path.basename(config["project_path"])
        handler.send_json(
            [
                {
                    "name": name,
                    "path": config["project_path"],
                    "exists": True,
                    "git": git_ops.has_git(config["project_path"]),
                }
            ]
        )
        return

    projects = registry.list_projects(config["config_dir"])
    for p in projects:
        p["git"] = git_ops.has_git(p["path"]) if p["exists"] else False
    handler.send_json(projects)


def _create_project(handler):
    config = handler.config
    if config["mode"] == "single":
        handler.send_json({"error": "Cannot create projects in single mode"}, status=400)
        return

    body = handler.read_json_body()
    name = body.get("name", "").strip()
    path = body.get("path", "").strip()

    if not name or "/" in name or name.startswith("."):
        handler.send_json({"error": "Invalid project name"}, status=400)
        return
    if not path:
        handler.send_json({"error": "Project path required"}, status=400)
        return

    path = os.path.abspath(path)
    full_dir = os.path.join(path, name)

    if os.path.exists(full_dir):
        handler.send_json({"error": "Directory already exists"}, status=409)
        return

    os.makedirs(full_dir)
    # Create a default main.tex
    main_tex = os.path.join(full_dir, "main.tex")
    with open(main_tex, "w") as f:
        f.write(
            "\\documentclass{article}\n\n\\begin{document}\n\nHello, World!\n\n\\end{document}\n"
        )

    try:
        registry.register_project(config["config_dir"], name, full_dir)
    except ValueError as e:
        handler.send_json({"error": str(e)}, status=400)
        return

    handler.send_json({"name": name, "path": full_dir}, status=201)


def _register_project(handler):
    """Register an existing directory as a project."""
    config = handler.config
    if config["mode"] == "single":
        handler.send_json({"error": "Cannot register projects in single mode"}, status=400)
        return

    body = handler.read_json_body()
    path = body.get("path", "").strip()
    if not path:
        handler.send_json({"error": "Path required"}, status=400)
        return

    path = os.path.abspath(path)
    name = body.get("name", "").strip() or os.path.basename(path)

    try:
        entry = registry.register_project(config["config_dir"], name, path)
    except ValueError as e:
        handler.send_json({"error": str(e)}, status=400)
        return

    handler.send_json({"name": name, "path": path, "added_at": entry["added_at"]}, status=201)


def _delete_project(handler, name):
    config = handler.config
    if config["mode"] == "single":
        handler.send_json({"error": "Cannot delete project in single mode"}, status=400)
        return

    body = handler.read_json_body()
    delete_files = body.get("delete_files", False)

    try:
        registry.unregister_project(config["config_dir"], name, delete_files=delete_files)
    except KeyError:
        handler.send_json({"error": f"Project not found: {name}"}, status=404)
        return

    handler.send_json({"deleted": name, "files_deleted": delete_files})


def _rename_project(handler, name):
    config = handler.config
    if config["mode"] == "single":
        handler.send_json({"error": "Cannot rename project in single mode"}, status=400)
        return

    body = handler.read_json_body()
    new_name = body.get("new_name", "").strip()
    if not new_name:
        handler.send_json({"error": "new_name is required"}, status=400)
        return

    try:
        registry.rename_project(config["config_dir"], name, new_name)
    except KeyError:
        handler.send_json({"error": f"Project not found: {name}"}, status=404)
        return
    except ValueError as e:
        handler.send_json({"error": str(e)}, status=400)
        return

    handler.send_json({"old_name": name, "new_name": new_name})


def _browse_filesystem(handler):
    """List subdirectories of a given path for the folder picker."""
    import urllib.parse

    parsed = urllib.parse.urlparse(handler.path)
    params = urllib.parse.parse_qs(parsed.query)
    path = params.get("path", [os.path.expanduser("~")])[0]
    path = os.path.expanduser(path)

    if not os.path.isdir(path):
        handler.send_json({"error": f"Not a directory: {path}"}, status=400)
        return

    entries = []
    try:
        for item in sorted(os.listdir(path)):
            if item.startswith("."):
                continue
            full = os.path.join(path, item)
            if os.path.isdir(full):
                entries.append(item)
    except PermissionError:
        handler.send_json({"error": "Permission denied"}, status=403)
        return

    handler.send_json({"path": path, "dirs": entries})


# ── Vendor ──


def _vendor_status(handler):
    config_dir = handler.config.get("config_dir")
    if not config_dir:
        handler.send_json({"ready": False, "reason": "single mode"})
        return
    vendor_dir = os.path.join(config_dir, "vendor")
    manifest = vendor.get_manifest(vendor_dir)
    proxy = vendor.load_proxy(config_dir) or ""
    if manifest:
        handler.send_json({"ready": True, "manifest": manifest, "proxy": proxy})
    else:
        handler.send_json({"ready": False, "proxy": proxy})


def _update_vendor(handler):
    config_dir = handler.config.get("config_dir")
    if not config_dir:
        handler.send_json({"error": "Not available in single mode"}, status=400)
        return
    body = handler.read_json_body()
    proxy = body.get("proxy", "").strip() if body else ""
    # Persist proxy setting
    vendor.save_proxy(config_dir, proxy)
    vendor_dir = os.path.join(config_dir, "vendor")
    try:
        manifest = vendor.download_vendor(vendor_dir, proxy=proxy or None)
        handler.send_json({"ok": True, "manifest": manifest})
    except Exception as e:
        handler.send_json({"error": str(e)}, status=500)


# ── Global Settings ──


def _read_settings(config_dir):
    """Read global settings from config_dir/settings.json."""
    path = os.path.join(config_dir, SETTINGS_FILE)
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _write_settings(config_dir, data):
    """Write global settings to config_dir/settings.json."""
    path = os.path.join(config_dir, SETTINGS_FILE)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _get_settings(handler):
    config_dir = handler.config.get("config_dir")
    if not config_dir:
        handler.send_json({})
        return
    handler.send_json(_read_settings(config_dir))


def _put_settings(handler):
    config_dir = handler.config.get("config_dir")
    if not config_dir:
        handler.send_json({"error": "Not available in single mode"}, status=400)
        return
    body = handler.read_json_body()
    existing = _read_settings(config_dir)
    existing.update(body)
    _write_settings(config_dir, existing)
    handler.send_json(existing)


# ── Files ──


def _list_files(handler, name):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    tree = _build_file_tree(project_dir, project_dir)
    handler.send_json(tree)


def _build_file_tree(base_dir, current_dir):
    """Build a nested file tree structure.

    Returns:
        List of {name, path, type} where type is "file" or "dir".
        Dirs have a "children" key.
    """
    entries = []
    try:
        items = sorted(os.listdir(current_dir))
    except OSError:
        return entries

    dirs_list = []
    files_list = []

    for item in items:
        if item in (".git", "__pycache__"):
            continue

        full = os.path.join(current_dir, item)
        rel = os.path.relpath(full, base_dir)

        if os.path.isdir(full):
            children = _build_file_tree(base_dir, full)
            dirs_list.append({"name": item, "path": rel, "type": "dir", "children": children})
        else:
            files_list.append(
                {"name": item, "path": rel, "type": "file", "mtime": os.path.getmtime(full)}
            )

    return dirs_list + files_list


def _read_file(handler, name, file_path):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    full_path = os.path.join(project_dir, file_path)
    # Security: ensure file is within project
    if not os.path.abspath(full_path).startswith(os.path.abspath(project_dir)):
        handler.send_json({"error": "Access denied"}, status=403)
        return

    if not os.path.exists(full_path):
        handler.send_json({"error": "File not found"}, status=404)
        return

    try:
        with open(full_path, encoding="utf-8") as f:
            content = f.read()
        handler.send_json(
            {"path": file_path, "content": content, "mtime": os.path.getmtime(full_path)}
        )
    except UnicodeDecodeError:
        handler.send_json({"error": "Binary file, cannot read as text"}, status=400)


def _check_file(handler, name, file_path):
    """Return mtime of a file without reading its content."""
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    full_path = os.path.join(project_dir, file_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(project_dir)):
        handler.send_json({"error": "Access denied"}, status=403)
        return

    if not os.path.exists(full_path):
        handler.send_json({"exists": False})
        return

    handler.send_json({"path": file_path, "mtime": os.path.getmtime(full_path)})


def _write_file(handler, name, file_path):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    full_path = os.path.join(project_dir, file_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(project_dir)):
        handler.send_json({"error": "Access denied"}, status=403)
        return

    body = handler.read_json_body()
    content = body.get("content", "")

    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

    handler.send_json({"path": file_path, "saved": True})


def _delete_file(handler, name, file_path):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    full_path = os.path.join(project_dir, file_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(project_dir)):
        handler.send_json({"error": "Access denied"}, status=403)
        return

    if not os.path.exists(full_path):
        handler.send_json({"error": "File not found"}, status=404)
        return

    import shutil

    if os.path.isdir(full_path):
        shutil.rmtree(full_path)
    else:
        os.remove(full_path)
    handler.send_json({"path": file_path, "deleted": True})


def _mkdir(handler, name):
    """Create a directory inside a project."""
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    body = handler.read_json_body()
    dir_path = body.get("path", "").strip()
    if not dir_path:
        handler.send_json({"error": "Directory path required"}, status=400)
        return

    full_path = os.path.join(project_dir, dir_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(project_dir)):
        handler.send_json({"error": "Access denied"}, status=403)
        return

    if os.path.exists(full_path):
        handler.send_json({"error": "Path already exists"}, status=409)
        return

    os.makedirs(full_path, exist_ok=True)
    handler.send_json({"path": dir_path, "created": True})


def _rename_path(handler, name):
    """Rename a file or directory inside a project."""
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    body = handler.read_json_body()
    old_path = body.get("old_path", "").strip()
    new_path = body.get("new_path", "").strip()
    if not old_path or not new_path:
        handler.send_json({"error": "old_path and new_path required"}, status=400)
        return

    old_full = os.path.join(project_dir, old_path)
    new_full = os.path.join(project_dir, new_path)
    abs_project = os.path.abspath(project_dir)
    if not os.path.abspath(old_full).startswith(abs_project) or not os.path.abspath(
        new_full
    ).startswith(abs_project):
        handler.send_json({"error": "Access denied"}, status=403)
        return

    if not os.path.exists(old_full):
        handler.send_json({"error": "Source not found"}, status=404)
        return

    if os.path.exists(new_full):
        handler.send_json({"error": "Destination already exists"}, status=409)
        return

    os.makedirs(os.path.dirname(new_full), exist_ok=True)
    os.rename(old_full, new_full)
    handler.send_json({"old_path": old_path, "new_path": new_path, "renamed": True})


def _upload(handler, name):
    """Handle multipart file upload."""
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    content_type = handler.headers.get("Content-Type", "")
    if "multipart/form-data" not in content_type:
        handler.send_json({"error": "Expected multipart/form-data"}, status=400)
        return

    # Parse boundary from content-type
    boundary = None
    for part in content_type.split(";"):
        part = part.strip()
        if part.startswith("boundary="):
            boundary = part[9:].strip('"')
            break

    if not boundary:
        handler.send_json({"error": "Missing boundary"}, status=400)
        return

    content_length = int(handler.headers.get("Content-Length", 0))
    body = handler.rfile.read(content_length)

    boundary_bytes = ("--" + boundary).encode()
    parts = body.split(boundary_bytes)

    uploaded = []
    # Get target directory from query or default to root
    target_dir = ""

    for part in parts:
        if not part or part == b"--\r\n" or part == b"--":
            continue
        if b"Content-Disposition:" not in part:
            continue

        # Parse headers and content
        header_end = part.find(b"\r\n\r\n")
        if header_end < 0:
            continue
        headers_raw = part[:header_end].decode("utf-8", errors="replace")
        file_data = part[header_end + 4 :]
        # Strip trailing \r\n
        if file_data.endswith(b"\r\n"):
            file_data = file_data[:-2]

        # Check for target_dir field
        if 'name="target_dir"' in headers_raw:
            target_dir = file_data.decode("utf-8", errors="replace").strip()
            continue

        # Extract filename
        filename = None
        for line in headers_raw.split("\r\n"):
            if "filename=" in line:
                idx = line.index("filename=")
                fname_raw = line[idx + 9 :].split(";")[0].strip('" ')
                if fname_raw:
                    filename = os.path.basename(fname_raw)
                break

        if not filename:
            continue

        rel_path = os.path.join(target_dir, filename) if target_dir else filename
        full_path = os.path.join(project_dir, rel_path)
        if not os.path.abspath(full_path).startswith(os.path.abspath(project_dir)):
            continue

        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(file_data)
        uploaded.append(rel_path)

    handler.send_json({"uploaded": uploaded, "count": len(uploaded)})


# ── Config ──


def _get_config(handler, name):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    config_data = _read_project_config(project_dir)
    # Auto-detect main file if not configured
    if "main_file" not in config_data:
        config_data["main_file"] = _detect_main_file(project_dir)
    if "engine" not in config_data:
        config_data["engine"] = "pdflatex"

    handler.send_json(config_data)


def _put_config(handler, name):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    body = handler.read_json_body()
    existing = _read_project_config(project_dir)
    existing.update(body)
    _write_project_config(project_dir, existing)
    handler.send_json(existing)


# ── Compile ──


def _compile(handler, name):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    body = handler.read_json_body()
    config_data = _read_project_config(project_dir)

    main_file = (
        body.get("main_file") or config_data.get("main_file") or _detect_main_file(project_dir)
    )
    engine = body.get("engine") or config_data.get("engine", "pdflatex")

    server_config = handler.config
    # Allow overriding docker settings from request or project config
    use_docker = body.get("use_docker", config_data.get("use_docker", server_config["use_docker"]))
    docker_image = (
        body.get("docker_image") or config_data.get("docker_image") or server_config["docker_image"]
    )
    # Read registry mirror from global settings
    config_dir = handler.config.get("config_dir")
    registry_mirror = None
    if config_dir:
        settings = _read_settings(config_dir)
        registry_mirror = settings.get("registry_mirror") or None

    compile_id = compiler.start_compile(
        project_dir=project_dir,
        main_file=main_file,
        engine=engine,
        use_docker=use_docker,
        docker_image=docker_image,
        registry_mirror=registry_mirror,
    )

    handler.send_json({"compile_id": compile_id, "main_file": main_file, "engine": engine})


def _cancel_compile(handler, name, compile_id):
    """Cancel a running compilation."""
    cancelled = compiler.cancel_compile(compile_id)
    handler.send_json({"cancelled": cancelled})


def _compile_stream(handler, name, compile_id):
    job = compiler.get_job(compile_id)
    if not job:
        handler.send_json({"error": "Compile job not found"}, status=404)
        return

    handler.start_sse()

    sent_index = 0
    while True:
        new_logs = job.get_logs_from(sent_index)
        for entry in new_logs:
            handler.send_sse_event(entry, event="log")
            sent_index += 1

        if job.is_done:
            # Send any remaining logs
            remaining = job.get_logs_from(sent_index)
            for entry in remaining:
                handler.send_sse_event(entry, event="log")

            done_data = {"status": job.status}
            if job.pdf_path:
                project_name = name
                done_data["pdf_url"] = f"/api/projects/{project_name}/output/{job.pdf_path}"
            handler.send_sse_event(done_data, event="done")
            break

        time.sleep(0.1)


def _get_output(handler, name, file_path):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    full_path = os.path.join(project_dir, file_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(project_dir)):
        handler.send_json({"error": "Access denied"}, status=403)
        return

    _MIME_MAP = {
        ".pdf": "application/pdf",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
        ".ico": "image/x-icon",
    }
    ext = os.path.splitext(file_path)[1].lower()
    content_type = _MIME_MAP.get(ext, "application/octet-stream")
    handler.send_file(full_path, content_type=content_type)


def _find_synctex_file(handler, project_dir):
    """Find the .synctex.gz or .synctex file for a project.

    Returns the path on success, or None after sending an error response.
    """
    config_data = _read_project_config(project_dir)
    main_file = config_data.get("main_file") or _detect_main_file(project_dir)
    if not main_file:
        handler.send_json({"error": "No main file found"}, status=404)
        return None

    base = os.path.splitext(main_file)[0]
    synctex_gz = os.path.join(project_dir, base + ".synctex.gz")
    synctex_plain = os.path.join(project_dir, base + ".synctex")

    if os.path.exists(synctex_gz):
        return synctex_gz
    if os.path.exists(synctex_plain):
        return synctex_plain

    handler.send_json(
        {"error": "SyncTeX file not found. Compile with -synctex=1"},
        status=404,
    )
    return None


def _synctex_query(handler, name, qs=None):
    """Handle SyncTeX inverse search: PDF click → source location."""
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    qs = qs or {}
    try:
        page = int(qs.get("page", [None])[0])
        x = float(qs.get("x", [None])[0])
        y = float(qs.get("y", [None])[0])
    except (TypeError, ValueError, IndexError):
        handler.send_json({"error": "Missing or invalid page/x/y parameters"}, status=400)
        return

    synctex_path = _find_synctex_file(handler, project_dir)
    if not synctex_path:
        return

    try:
        data = synctex.parse_synctex(synctex_path, strip_prefix="/workspace/")
        result = synctex.inverse_search(data, page, x, y)
    except Exception as exc:
        handler.send_json({"error": f"SyncTeX parse error: {exc}"}, status=500)
        return

    if result is None:
        handler.send_json({"error": "No match found"}, status=404)
        return

    handler.send_json(result)


def _synctex_forward(handler, name, qs=None):
    """Handle SyncTeX forward search: source location → PDF position."""
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    qs = qs or {}
    file_param = qs.get("file", [None])[0]
    line_param = qs.get("line", [None])[0]

    if not file_param or not line_param:
        handler.send_json({"error": "Missing file or line parameter"}, status=400)
        return

    try:
        line_num = int(line_param)
    except ValueError:
        handler.send_json({"error": "Invalid line parameter"}, status=400)
        return

    synctex_path = _find_synctex_file(handler, project_dir)
    if not synctex_path:
        return

    try:
        data = synctex.parse_synctex(synctex_path, strip_prefix="/workspace/")
        result = synctex.forward_search(data, file_param, line_num)
    except Exception as exc:
        handler.send_json({"error": f"SyncTeX parse error: {exc}"}, status=500)
        return

    if result is None:
        handler.send_json({"error": "No match found"}, status=404)
        return

    handler.send_json(result)


_CLEAN_EXTENSIONS = {
    ".aux",
    ".bbl",
    ".bcf",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".log",
    ".out",
    ".run.xml",
    ".synctex.gz",
    ".toc",
    ".lof",
    ".lot",
    ".nav",
    ".snm",
    ".vrb",
    ".xdv",
}


def _clean(handler, name):
    """Remove LaTeX compilation artifacts from the project directory."""
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    removed = []
    for root, dirs, filenames in os.walk(project_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in filenames:
            _, ext = os.path.splitext(fname)
            # Handle .synctex.gz (compound extension)
            if fname.endswith(".synctex.gz"):
                ext = ".synctex.gz"
            if ext in _CLEAN_EXTENSIONS:
                full = os.path.join(root, fname)
                rel = os.path.relpath(full, project_dir)
                try:
                    os.remove(full)
                    removed.append(rel)
                except OSError:
                    pass

    handler.send_json({"removed": removed, "count": len(removed)})


# ── Word Count ──


def _word_count(handler, name=""):
    """Run texcount on the project's main file and return word statistics.

    Tries to run texcount via Docker (same pattern as compilation) if Docker
    is enabled, otherwise falls back to a local texcount binary.
    """
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    config_data = _read_project_config(project_dir)
    main_file = config_data.get("main_file") or _detect_main_file(project_dir)

    server_config = handler.config
    use_docker = config_data.get("use_docker", server_config["use_docker"])
    docker_image = config_data.get("docker_image") or server_config["docker_image"]

    texcount_cmd = ["texcount", "-inc", "-sum", "-merge", main_file]

    if use_docker:
        cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{project_dir}:/workspace",
            "-w",
            "/workspace",
            docker_image,
        ] + texcount_cmd
        cwd = None
    else:
        cmd = texcount_cmd
        cwd = project_dir

    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except FileNotFoundError:
        handler.send_json(
            {"error": "texcount not found. Enable Docker or install texcount locally."},
            status=500,
        )
        return
    except subprocess.TimeoutExpired:
        handler.send_json({"error": "texcount timed out"}, status=500)
        return

    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        handler.send_json({"error": f"texcount failed: {stderr}"}, status=500)
        return

    stats = _parse_texcount_output(result.stdout)
    handler.send_json(stats)


def _parse_texcount_output(output):
    """Parse texcount output into a structured dict.

    Args:
        output: Raw stdout from texcount with -sum -merge flags.

    Returns:
        Dict with word/count statistics.
    """
    stats = {
        "words_in_text": 0,
        "words_in_headers": 0,
        "words_outside_text": 0,
        "words_in_captions": 0,
        "math_inline": 0,
        "math_display": 0,
    }

    # texcount -sum -merge output lines look like:
    #   Words in text: 1234
    #   Words in headers: 56
    #   Words outside text (captions, etc.): 78
    #   Number of headers: 12
    #   Number of floats/tables/figures: 3
    #   Number of math inlines: 45
    #   Number of math displayed: 6
    patterns = {
        "words_in_text": r"Words in text:\s*(\d+)",
        "words_in_headers": r"Words in headers:\s*(\d+)",
        "words_outside_text": r"Words outside text.*?:\s*(\d+)",
        "words_in_captions": r"Words in float captions:\s*(\d+)",
        "math_inline": r"Number of math inlines:\s*(\d+)",
        "math_display": r"Number of math displayed:\s*(\d+)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, output)
        if match:
            stats[key] = int(match.group(1))

    # Total = text + headers + captions (outside text)
    stats["total"] = (
        stats["words_in_text"] + stats["words_in_headers"] + stats["words_outside_text"]
    )

    return stats


# ── Export ──

# Directories to skip when building the export zip
_EXPORT_SKIP_DIRS = {".git", "__pycache__", ".tinyleaf"}

# File extensions for LaTeX build artifacts to exclude from export
_EXPORT_SKIP_EXTS = {
    ".aux",
    ".log",
    ".out",
    ".bbl",
    ".blg",
    ".fls",
    ".fdb_latexmk",
    ".synctex.gz",
    ".toc",
    ".lof",
    ".lot",
}


def _export_zip(handler, name=""):
    """Export a project directory as a downloadable zip file.

    Creates an in-memory zip archive of the project, excluding version control
    directories, build artifacts, and the internal config file. The compiled
    PDF is included if present.

    Args:
        handler: The HTTP request handler.
        name: Project name.
    """
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(project_dir):
            # Skip excluded directories in-place
            dirs[:] = [d for d in dirs if d not in _EXPORT_SKIP_DIRS]
            for fname in files:
                # Skip internal config
                if fname == CONFIG_FILE:
                    continue
                # Skip build artifacts (handle compound .synctex.gz extension)
                if fname.endswith(".synctex.gz"):
                    continue
                ext = os.path.splitext(fname)[1].lower()
                if ext in _EXPORT_SKIP_EXTS:
                    continue
                full = os.path.join(root, fname)
                arcname = os.path.relpath(full, project_dir)
                zf.write(full, arcname)

    data = buf.getvalue()
    safe_name = name.replace(" ", "_") if name else "project"
    handler.send_response(200)
    handler.send_header("Content-Type", "application/zip")
    handler.send_header("Content-Disposition", f'attachment; filename="{safe_name}.zip"')
    handler.send_header("Content-Length", str(len(data)))
    handler._send_cors_headers()
    handler.end_headers()
    handler.wfile.write(data)


# ── Search ──

_SEARCH_SKIP_DIRS = {".git", "__pycache__", ".ruff_cache", "node_modules"}
_SEARCH_BINARY_EXTS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".bmp",
    ".ico",
    ".zip",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
    ".7z",
    ".rar",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".o",
    ".a",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".eot",
    ".mp3",
    ".mp4",
    ".avi",
    ".mov",
    ".wav",
    ".flac",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
}


def _search_files(handler, name, qs=None):
    """Search for text across all project files (grep-style)."""
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    qs = qs or {}
    query = qs.get("q", [None])[0]
    if not query:
        handler.send_json({"error": "Missing search query"}, status=400)
        return

    case_sensitive = qs.get("case", ["0"])[0] == "1"
    max_results = 500

    flags = 0 if case_sensitive else re.IGNORECASE
    try:
        pattern = re.compile(re.escape(query), flags)
    except re.error:
        handler.send_json({"error": "Invalid search pattern"}, status=400)
        return

    results = {}
    total = 0

    for root, dirs, filenames in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in _SEARCH_SKIP_DIRS]
        for fname in sorted(filenames):
            if fname.endswith(".synctex.gz"):
                continue
            ext = os.path.splitext(fname)[1].lower()
            if ext in _SEARCH_BINARY_EXTS:
                continue

            full = os.path.join(root, fname)
            rel = os.path.relpath(full, project_dir)

            try:
                with open(full, encoding="utf-8") as f:
                    for line_num, line_text in enumerate(f, 1):
                        if pattern.search(line_text):
                            if rel not in results:
                                results[rel] = []
                            results[rel].append(
                                {
                                    "line": line_num,
                                    "text": line_text.rstrip("\n\r")[:300],
                                }
                            )
                            total += 1
                            if total >= max_results:
                                break
            except (UnicodeDecodeError, OSError):
                continue

            if total >= max_results:
                break
        if total >= max_results:
            break

    handler.send_json(
        {
            "query": query,
            "case_sensitive": case_sensitive,
            "results": results,
            "total": total,
            "truncated": total >= max_results,
        }
    )


# ── Git ──


def _git_status(handler, name):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return
    handler.send_json(git_ops.status(project_dir))


def _parse_diff_qs(qs):
    """Extract diff query-string parameters.

    Args:
        qs: Parsed query string dict (values are lists).

    Returns:
        Tuple of (staged, fmt) where staged is one of ``"both"``,
        ``"staged"``, ``"unstaged"`` and fmt is ``"text"`` or ``"json"``.
    """
    staged_raw = (qs or {}).get("staged", ["both"])[0]
    staged = staged_raw if staged_raw in ("both", "staged", "unstaged") else "both"
    fmt_raw = (qs or {}).get("format", ["text"])[0]
    fmt = "json" if fmt_raw == "json" else "text"
    return staged, fmt


def _git_diff(handler, name, qs=None):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return
    staged, fmt = _parse_diff_qs(qs)
    result = git_ops.diff(project_dir, staged=staged, fmt=fmt)
    if fmt == "json":
        handler.send_json(result)
    else:
        handler.send_text(result)


def _git_diff_file(handler, name, file_path, qs=None):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return
    staged, fmt = _parse_diff_qs(qs)
    result = git_ops.diff(project_dir, file_path=file_path, staged=staged, fmt=fmt)
    if fmt == "json":
        handler.send_json(result)
    else:
        handler.send_text(result)


def _git_commit(handler, name):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return

    body = handler.read_json_body()
    message = body.get("message", "").strip()
    if not message:
        handler.send_json({"error": "Commit message required"}, status=400)
        return

    files = body.get("files")
    result = git_ops.commit(project_dir, message, files=files)
    handler.send_json(result)


def _git_push(handler, name):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return
    handler.send_json(git_ops.push(project_dir))


def _git_pull(handler, name):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return
    handler.send_json(git_ops.pull(project_dir))


def _git_log(handler, name):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return
    handler.send_json(git_ops.log(project_dir))
