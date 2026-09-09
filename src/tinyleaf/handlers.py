"""API request handlers for tinyleaf.

Handlers are pure functions: they receive parsed data (config, body, params)
and return dicts (auto-coerced to JSON by the server) or Response objects.
Errors are raised via abort() / HTTPException.
"""

import asyncio
import io
import json
import os
import re
import subprocess
import zipfile

from tinyleaf import compiler, git_ops, registry, vendor
from tinyleaf._vendor import synctex
from tinyleaf._vendor.httpserver import FileResponse, Response, abort

# Project config file name
CONFIG_FILE = ".tinyleaf.json"
SETTINGS_FILE = "settings.json"


# ── Helpers ──


def _get_project_dir(config, name):
    """Resolve project name to directory path. Raises on failure."""
    if config["mode"] == "single":
        return config["project_path"]

    project_dir = registry.get_project_path(config["config_dir"], name)
    if not project_dir:
        abort(404, f"Project not found: {name}")
    if not os.path.isdir(project_dir):
        abort(404, f"Project directory missing: {project_dir}")
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


def _ensure_within_project(project_dir, file_path):
    """Validate that file_path resolves inside project_dir."""
    full_path = os.path.join(project_dir, file_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(project_dir)):
        abort(403, "Access denied")
    return full_path


# ── Mode ──


def handle_get_mode(config):
    from tinyleaf import __version__

    return {
        "mode": config["mode"],
        "docker": config["use_docker"],
        "image": config["docker_image"],
        "version": __version__,
    }


# ── Docker ──

_DOCKER_IMAGE_PREFIX = "oaklight/texlive"

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


def handle_list_docker_images():
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
    return all_tags


def handle_docker_pull(body, config):
    image = body.get("image")
    if not image:
        abort(400, "Missing image")

    config_dir = config.get("config_dir")
    registry_mirror = None
    if config_dir:
        settings = _read_settings(config_dir)
        registry_mirror = settings.get("registry_mirror") or None

    success, msg = compiler.docker_pull_image(image, registry_mirror=registry_mirror)
    return {"success": success, "message": msg}


def handle_docker_rmi(body):
    image = body.get("image")
    if not image:
        abort(400, "Missing image")
    success, msg = compiler.docker_remove_image(image)
    return {"success": success, "message": msg}


def handle_cancel_docker_pull(body):
    image = body.get("image")
    if not image:
        abort(400, "Missing image")
    cancelled = compiler.cancel_docker_pull(image)
    return {"cancelled": cancelled}


# ── Projects ──


def handle_list_projects(config):
    if config["mode"] == "single":
        return [
            {
                "name": os.path.basename(config["project_path"]),
                "path": config["project_path"],
                "exists": True,
                "git": git_ops.has_git(config["project_path"]),
            }
        ]

    projects = registry.list_projects(config["config_dir"])
    for p in projects:
        p["git"] = git_ops.has_git(p["path"]) if p["exists"] else False
    return projects


def handle_create_project(body, config):
    if config["mode"] == "single":
        abort(400, "Cannot create projects in single mode")

    name = body.get("name", "").strip()
    path = body.get("path", "").strip()

    if not name or "/" in name or name.startswith("."):
        abort(400, "Invalid project name")
    if not path:
        abort(400, "Project path required")

    path = os.path.abspath(path)
    full_dir = os.path.join(path, name)

    if os.path.exists(full_dir):
        abort(409, "Directory already exists")

    os.makedirs(full_dir)
    main_tex = os.path.join(full_dir, "main.tex")
    with open(main_tex, "w") as f:
        f.write(
            "\\documentclass{article}\n\n\\begin{document}\n\nHello, World!\n\n\\end{document}\n"
        )

    try:
        registry.register_project(config["config_dir"], name, full_dir)
    except ValueError as e:
        abort(400, str(e))

    return {"name": name, "path": full_dir}, 201


def handle_register_project(body, config):
    if config["mode"] == "single":
        abort(400, "Cannot register projects in single mode")

    path = body.get("path", "").strip()
    if not path:
        abort(400, "Path required")

    path = os.path.abspath(path)
    name = body.get("name", "").strip() or os.path.basename(path)

    try:
        entry = registry.register_project(config["config_dir"], name, path)
    except ValueError as e:
        abort(400, str(e))

    return {"name": name, "path": path, "added_at": entry["added_at"]}, 201


def handle_delete_project(body, config, name):
    if config["mode"] == "single":
        abort(400, "Cannot delete project in single mode")

    delete_files = body.get("delete_files", False)

    try:
        registry.unregister_project(config["config_dir"], name, delete_files=delete_files)
    except KeyError:
        abort(404, f"Project not found: {name}")

    return {"deleted": name, "files_deleted": delete_files}


def handle_rename_project(body, config, name):
    if config["mode"] == "single":
        abort(400, "Cannot rename project in single mode")

    new_name = body.get("new_name", "").strip()
    if not new_name:
        abort(400, "new_name is required")

    try:
        registry.rename_project(config["config_dir"], name, new_name)
    except KeyError:
        abort(404, f"Project not found: {name}")
    except ValueError as e:
        abort(400, str(e))

    return {"old_name": name, "new_name": new_name}


def handle_browse_filesystem(query_params):
    path = query_params.get("path", [os.path.expanduser("~")])[0]
    path = os.path.expanduser(path)

    if not os.path.isdir(path):
        abort(400, f"Not a directory: {path}")

    entries = []
    try:
        for item in sorted(os.listdir(path)):
            if item.startswith("."):
                continue
            full = os.path.join(path, item)
            if os.path.isdir(full):
                entries.append(item)
    except PermissionError:
        abort(403, "Permission denied")

    return {"path": path, "dirs": entries}


# ── Vendor ──


def handle_vendor_status(config):
    config_dir = config.get("config_dir")
    if not config_dir:
        return {"ready": False, "reason": "single mode"}
    vendor_dir = os.path.join(config_dir, "vendor")
    manifest = vendor.get_manifest(vendor_dir)
    proxy = vendor.load_proxy(config_dir) or ""
    if manifest:
        return {"ready": True, "manifest": manifest, "proxy": proxy}
    return {"ready": False, "proxy": proxy}


def handle_update_vendor(body, config):
    config_dir = config.get("config_dir")
    if not config_dir:
        abort(400, "Not available in single mode")
    proxy = body.get("proxy", "").strip() if body else ""
    vendor.save_proxy(config_dir, proxy)
    vendor_dir = os.path.join(config_dir, "vendor")
    try:
        manifest = vendor.download_vendor(vendor_dir, proxy=proxy or None)
        return {"ok": True, "manifest": manifest}
    except Exception as e:
        abort(500, str(e))


# ── Global Settings ──


def handle_get_settings(config):
    config_dir = config.get("config_dir")
    if not config_dir:
        return {}
    return _read_settings(config_dir)


def handle_put_settings(body, config):
    config_dir = config.get("config_dir")
    if not config_dir:
        abort(400, "Not available in single mode")
    existing = _read_settings(config_dir)
    existing.update(body)
    _write_settings(config_dir, existing)
    return existing


# ── Files ──


def handle_list_files(config, name):
    project_dir = _get_project_dir(config, name)
    return _build_file_tree(project_dir, project_dir)


def _build_file_tree(base_dir, current_dir):
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


def handle_read_file(config, name, file_path):
    project_dir = _get_project_dir(config, name)
    full_path = _ensure_within_project(project_dir, file_path)

    if not os.path.exists(full_path):
        abort(404, "File not found")

    try:
        with open(full_path, encoding="utf-8") as f:
            content = f.read()
        return {"path": file_path, "content": content, "mtime": os.path.getmtime(full_path)}
    except UnicodeDecodeError:
        abort(400, "Binary file, cannot read as text")


def handle_check_file(config, name, file_path):
    project_dir = _get_project_dir(config, name)
    full_path = _ensure_within_project(project_dir, file_path)

    if not os.path.exists(full_path):
        return {"exists": False}

    return {"path": file_path, "mtime": os.path.getmtime(full_path)}


def handle_write_file(body, config, name, file_path):
    project_dir = _get_project_dir(config, name)
    full_path = _ensure_within_project(project_dir, file_path)

    content = body.get("content", "")
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

    return {"path": file_path, "saved": True}


def handle_delete_file(config, name, file_path):
    project_dir = _get_project_dir(config, name)
    full_path = _ensure_within_project(project_dir, file_path)

    if not os.path.exists(full_path):
        abort(404, "File not found")

    import shutil

    if os.path.isdir(full_path):
        shutil.rmtree(full_path)
    else:
        os.remove(full_path)
    return {"path": file_path, "deleted": True}


def handle_mkdir(body, config, name):
    project_dir = _get_project_dir(config, name)

    dir_path = body.get("path", "").strip()
    if not dir_path:
        abort(400, "Directory path required")

    full_path = _ensure_within_project(project_dir, dir_path)

    if os.path.exists(full_path):
        abort(409, "Path already exists")

    os.makedirs(full_path, exist_ok=True)
    return {"path": dir_path, "created": True}


def handle_rename_path(body, config, name):
    project_dir = _get_project_dir(config, name)

    old_path = body.get("old_path", "").strip()
    new_path = body.get("new_path", "").strip()
    if not old_path or not new_path:
        abort(400, "old_path and new_path required")

    old_full = _ensure_within_project(project_dir, old_path)
    new_full = _ensure_within_project(project_dir, new_path)

    if not os.path.exists(old_full):
        abort(404, "Source not found")

    if os.path.exists(new_full):
        abort(409, "Destination already exists")

    os.makedirs(os.path.dirname(new_full), exist_ok=True)
    os.rename(old_full, new_full)
    return {"old_path": old_path, "new_path": new_path, "renamed": True}


def handle_upload(request, config, name):
    """Handle multipart file upload.

    This handler receives the raw Request object because it needs
    direct access to the request body and headers for multipart parsing.
    """
    project_dir = _get_project_dir(config, name)

    content_type = request.headers.get("content-type", "")
    if "multipart/form-data" not in content_type:
        abort(400, "Expected multipart/form-data")

    boundary = None
    for part in content_type.split(";"):
        part = part.strip()
        if part.startswith("boundary="):
            boundary = part[9:].strip('"')
            break

    if not boundary:
        abort(400, "Missing boundary")
    assert boundary is not None

    body = request.body

    boundary_bytes = ("--" + boundary).encode()
    parts = body.split(boundary_bytes)

    uploaded = []
    target_dir = ""

    for part in parts:
        if not part or part == b"--\r\n" or part == b"--":
            continue
        if b"Content-Disposition:" not in part:
            continue

        header_end = part.find(b"\r\n\r\n")
        if header_end < 0:
            continue
        headers_raw = part[:header_end].decode("utf-8", errors="replace")
        file_data = part[header_end + 4 :]
        if file_data.endswith(b"\r\n"):
            file_data = file_data[:-2]

        if 'name="target_dir"' in headers_raw:
            target_dir = file_data.decode("utf-8", errors="replace").strip()
            continue

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

    return {"uploaded": uploaded, "count": len(uploaded)}


# ── Config ──


def handle_get_config(config, name):
    project_dir = _get_project_dir(config, name)

    if config["mode"] == "multi":
        registry.touch_project(config["config_dir"], name)

    config_data = _read_project_config(project_dir)
    if "main_file" not in config_data:
        config_data["main_file"] = _detect_main_file(project_dir)
    if "engine" not in config_data:
        config_data["engine"] = "pdflatex"

    return config_data


def handle_put_config(body, config, name):
    project_dir = _get_project_dir(config, name)

    existing = _read_project_config(project_dir)
    existing.update(body)
    _write_project_config(project_dir, existing)
    return existing


# ── Compile ──


def handle_compile(body, config, name):
    project_dir = _get_project_dir(config, name)

    config_data = _read_project_config(project_dir)

    main_file = (
        body.get("main_file") or config_data.get("main_file") or _detect_main_file(project_dir)
    )
    engine = body.get("engine") or config_data.get("engine", "pdflatex")

    use_docker = body.get("use_docker", config_data.get("use_docker", config["use_docker"]))
    docker_image = (
        body.get("docker_image") or config_data.get("docker_image") or config["docker_image"]
    )
    config_dir = config.get("config_dir")
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

    return {"compile_id": compile_id, "main_file": main_file, "engine": engine}


def handle_cancel_compile(compile_id):
    cancelled = compiler.cancel_compile(compile_id)
    return {"cancelled": cancelled}


async def sse_compile_stream(compile_id, name):
    """Async generator that yields SSE events for a compile job.

    Caller must verify the job exists before invoking this generator.
    """
    job = compiler.get_job(compile_id)

    sent_index = 0
    while True:
        new_logs = job.get_logs_from(sent_index)
        for entry in new_logs:
            yield _sse_frame(entry, event="log")
            sent_index += 1

        if job.is_done:
            remaining = job.get_logs_from(sent_index)
            for entry in remaining:
                yield _sse_frame(entry, event="log")

            done_data = {"status": job.status}
            if job.pdf_path:
                done_data["pdf_url"] = f"/api/projects/{name}/output/{job.pdf_path}"
            yield _sse_frame(done_data, event="done")
            return

        await asyncio.sleep(0.1)


def _sse_frame(data, event=None):
    """Format a single SSE frame as bytes."""
    lines = []
    if event:
        lines.append(f"event: {event}")
    if isinstance(data, dict):
        lines.append(f"data: {json.dumps(data, ensure_ascii=False)}")
    else:
        lines.append(f"data: {data}")
    lines.append("")
    lines.append("")
    return "\n".join(lines)


# ── Output ──

_OUTPUT_MIME_MAP = {
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


def handle_get_output(config, name, file_path):
    project_dir = _get_project_dir(config, name)
    full_path = _ensure_within_project(project_dir, file_path)

    ext = os.path.splitext(file_path)[1].lower()
    content_type = _OUTPUT_MIME_MAP.get(ext, "application/octet-stream")

    from pathlib import Path

    return FileResponse(Path(full_path), content_type=content_type)


# ── SyncTeX ──


def _find_synctex_file(project_dir):
    """Find the .synctex.gz or .synctex file for a project."""
    config_data = _read_project_config(project_dir)
    main_file = config_data.get("main_file") or _detect_main_file(project_dir)
    if not main_file:
        abort(404, "No main file found")

    base = os.path.splitext(main_file)[0]
    synctex_gz = os.path.join(project_dir, base + ".synctex.gz")
    synctex_plain = os.path.join(project_dir, base + ".synctex")

    if os.path.exists(synctex_gz):
        return synctex_gz
    if os.path.exists(synctex_plain):
        return synctex_plain

    abort(404, "SyncTeX file not found. Compile with -synctex=1")


def handle_synctex_query(query_params, config, name):
    project_dir = _get_project_dir(config, name)

    try:
        page = int(query_params.get("page", [None])[0])
        x = float(query_params.get("x", [None])[0])
        y = float(query_params.get("y", [None])[0])
    except (TypeError, ValueError, IndexError):
        abort(400, "Missing or invalid page/x/y parameters")

    synctex_path = _find_synctex_file(project_dir)

    try:
        data = synctex.parse_synctex(synctex_path, strip_prefix="/workspace/")
        result = synctex.inverse_search(data, page, x, y)
    except Exception as exc:
        abort(500, f"SyncTeX parse error: {exc}")

    if result is None:
        abort(404, "No match found")

    return result


def handle_synctex_forward(query_params, config, name):
    project_dir = _get_project_dir(config, name)

    file_param = query_params.get("file", [None])[0]
    line_param = query_params.get("line", [None])[0]

    if not file_param or not line_param:
        abort(400, "Missing file or line parameter")

    try:
        line_num = int(line_param)
    except ValueError:
        abort(400, "Invalid line parameter")

    synctex_path = _find_synctex_file(project_dir)

    try:
        data = synctex.parse_synctex(synctex_path, strip_prefix="/workspace/")
        result = synctex.forward_search(data, file_param, line_num)
    except Exception as exc:
        abort(500, f"SyncTeX parse error: {exc}")

    if result is None:
        abort(404, "No match found")

    return result


# ── Clean ──

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


def handle_clean(config, name):
    project_dir = _get_project_dir(config, name)

    removed = []
    for root, dirs, filenames in os.walk(project_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in filenames:
            _, ext = os.path.splitext(fname)
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

    return {"removed": removed, "count": len(removed)}


# ── Word Count ──


def handle_word_count(config, name):
    project_dir = _get_project_dir(config, name)

    config_data = _read_project_config(project_dir)
    main_file = config_data.get("main_file") or _detect_main_file(project_dir)

    use_docker = config_data.get("use_docker", config["use_docker"])
    docker_image = config_data.get("docker_image") or config["docker_image"]

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
        abort(500, "texcount not found. Enable Docker or install texcount locally.")
    except subprocess.TimeoutExpired:
        abort(500, "texcount timed out")

    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        abort(500, f"texcount failed: {stderr}")

    return _parse_texcount_output(result.stdout)


def _parse_texcount_output(output):
    stats = {
        "words_in_text": 0,
        "words_in_headers": 0,
        "words_outside_text": 0,
        "words_in_captions": 0,
        "math_inline": 0,
        "math_display": 0,
    }

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

    stats["total"] = (
        stats["words_in_text"] + stats["words_in_headers"] + stats["words_outside_text"]
    )

    return stats


# ── Export ──

_EXPORT_SKIP_DIRS = {".git", "__pycache__", ".tinyleaf"}

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


def handle_export_zip(config, name):
    project_dir = _get_project_dir(config, name)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(project_dir):
            dirs[:] = [d for d in dirs if d not in _EXPORT_SKIP_DIRS]
            for fname in files:
                if fname == CONFIG_FILE:
                    continue
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
    return Response(
        body=data,
        status_code=200,
        content_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{safe_name}.zip"',
        },
    )


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


def handle_search_files(query_params, config, name):
    project_dir = _get_project_dir(config, name)

    query = query_params.get("q", [None])[0]
    if not query:
        abort(400, "Missing search query")

    case_sensitive = query_params.get("case", ["0"])[0] == "1"
    max_results = 500

    flags = 0 if case_sensitive else re.IGNORECASE
    try:
        pattern = re.compile(re.escape(query), flags)
    except re.error:
        abort(400, "Invalid search pattern")

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

    return {
        "query": query,
        "case_sensitive": case_sensitive,
        "results": results,
        "total": total,
        "truncated": total >= max_results,
    }


# ── Symbols (labels & citations) ──

_SYMBOLS_SKIP_DIRS = {".git", "__pycache__", ".ruff_cache", "node_modules"}


def handle_project_symbols(config, name):
    project_dir = _get_project_dir(config, name)

    labels = []
    citations = []

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in _SYMBOLS_SKIP_DIRS]
        for fname in files:
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, project_dir)

            if fname.endswith(".tex"):
                try:
                    with open(full, encoding="utf-8", errors="replace") as fh:
                        for i, line in enumerate(fh, 1):
                            for m in re.finditer(r"\\label\{([^}]+)\}", line):
                                labels.append(
                                    {
                                        "key": m.group(1),
                                        "file": rel,
                                        "line": i,
                                        "context": line.strip()[:80],
                                    }
                                )
                except OSError:
                    continue

            elif fname.endswith(".bib"):
                try:
                    with open(full, encoding="utf-8", errors="replace") as fh:
                        content = fh.read()
                except OSError:
                    continue

                for m in re.finditer(r"@\w+\{([^,\s]+),", content):
                    key = m.group(1)
                    pos = m.end()
                    window = content[pos : pos + 500]
                    title_m = re.search(r"title\s*=\s*[{\"]([^}\"]+)", window)
                    author_m = re.search(r"author\s*=\s*[{\"]([^}\"]+)", window)
                    year_m = re.search(r"year\s*=\s*[{\"](\d{4})", window)
                    citations.append(
                        {
                            "key": key,
                            "title": title_m.group(1).strip() if title_m else "",
                            "author": author_m.group(1).strip()[:50] if author_m else "",
                            "year": year_m.group(1) if year_m else "",
                            "file": rel,
                        }
                    )

    return {"labels": labels, "citations": citations}


# ── Git ──


def handle_git_status(config, name):
    project_dir = _get_project_dir(config, name)
    return git_ops.status(project_dir)


def _parse_diff_qs(query_params):
    staged_raw = query_params.get("staged", ["both"])[0]
    staged = staged_raw if staged_raw in ("both", "staged", "unstaged") else "both"
    fmt_raw = query_params.get("format", ["text"])[0]
    fmt = "json" if fmt_raw == "json" else "text"
    return staged, fmt


def handle_git_diff(query_params, config, name):
    project_dir = _get_project_dir(config, name)
    staged, fmt = _parse_diff_qs(query_params)
    result = git_ops.diff(project_dir, staged=staged, fmt=fmt)
    if fmt == "json":
        return result
    return Response(
        body=result.encode("utf-8"),
        content_type="text/plain; charset=utf-8",
    )


def handle_git_diff_file(query_params, config, name, file_path):
    project_dir = _get_project_dir(config, name)
    staged, fmt = _parse_diff_qs(query_params)
    result = git_ops.diff(project_dir, file_path=file_path, staged=staged, fmt=fmt)
    if fmt == "json":
        return result
    return Response(
        body=result.encode("utf-8"),
        content_type="text/plain; charset=utf-8",
    )


def handle_git_commit(body, config, name):
    project_dir = _get_project_dir(config, name)

    message = body.get("message", "").strip()
    if not message:
        abort(400, "Commit message required")

    files = body.get("files")
    return git_ops.commit(project_dir, message, files=files)


def handle_git_push(config, name):
    project_dir = _get_project_dir(config, name)
    return git_ops.push(project_dir)


def handle_git_pull(config, name):
    project_dir = _get_project_dir(config, name)
    return git_ops.pull(project_dir)


def handle_git_log(config, name):
    project_dir = _get_project_dir(config, name)
    return git_ops.log(project_dir)
