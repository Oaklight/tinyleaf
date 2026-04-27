"""API request handlers for texlive-web."""

import json
import os
import subprocess
import time

from texlive_web import compiler, git_ops

# Project config file name
CONFIG_FILE = ".texlive-web.json"


def handle_request(handler, action, **kwargs):
    """Dispatch an API action to the appropriate handler function."""
    dispatch = {
        "get_mode": _get_mode,
        "list_docker_images": _list_docker_images,
        "list_projects": _list_projects,
        "create_project": _create_project,
        "delete_project": _delete_project,
        "list_files": _list_files,
        "read_file": _read_file,
        "write_file": _write_file,
        "delete_file": _delete_file,
        "get_config": _get_config,
        "put_config": _put_config,
        "compile": _compile,
        "compile_stream": _compile_stream,
        "get_output": _get_output,
        "clean": _clean,
        "git_status": _git_status,
        "git_diff": _git_diff,
        "git_commit": _git_commit,
        "git_push": _git_push,
        "git_pull": _git_pull,
        "git_log": _git_log,
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

    # Multi-project mode
    project_dir = os.path.join(config["projects_dir"], name)
    if not os.path.isdir(project_dir):
        handler.send_json({"error": f"Project not found: {name}"}, status=404)
        return None
    return project_dir


def _read_project_config(project_dir):
    """Read .texlive-web.json from a project directory."""
    config_path = os.path.join(project_dir, CONFIG_FILE)
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return {}


def _write_project_config(project_dir, config_data):
    """Write .texlive-web.json to a project directory."""
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
    config = handler.config
    handler.send_json(
        {
            "mode": config["mode"],
            "docker": config["use_docker"],
            "image": config["docker_image"],
        }
    )


# Docker image name prefix for filtering
_DOCKER_IMAGE_PREFIX = "oaklight/texlive"


def _list_docker_images(handler):
    """List locally available oaklight/texlive Docker images."""
    try:
        result = subprocess.run(
            ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}", _DOCKER_IMAGE_PREFIX],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            handler.send_json([])
            return

        tags = []
        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if line and "<none>" not in line:
                tags.append(line)
        # Sort: latest first, then alphabetical
        tags.sort(key=lambda t: (0 if t.endswith(":latest") else 1, t))
        handler.send_json(tags)
    except Exception:
        handler.send_json([])


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
                    "git": git_ops.has_git(config["project_path"]),
                }
            ]
        )
        return

    projects_dir = config["projects_dir"]
    projects = []
    for entry in sorted(os.listdir(projects_dir)):
        full = os.path.join(projects_dir, entry)
        if os.path.isdir(full) and not entry.startswith("."):
            projects.append(
                {
                    "name": entry,
                    "git": git_ops.has_git(full),
                }
            )
    handler.send_json(projects)


def _create_project(handler):
    config = handler.config
    if config["mode"] == "single":
        handler.send_json({"error": "Cannot create projects in single mode"}, status=400)
        return

    body = handler.read_json_body()
    name = body.get("name", "").strip()
    if not name or "/" in name or name.startswith("."):
        handler.send_json({"error": "Invalid project name"}, status=400)
        return

    project_dir = os.path.join(config["projects_dir"], name)
    if os.path.exists(project_dir):
        handler.send_json({"error": "Project already exists"}, status=409)
        return

    os.makedirs(project_dir)
    # Create a default main.tex
    main_tex = os.path.join(project_dir, "main.tex")
    with open(main_tex, "w") as f:
        f.write(
            "\\documentclass{article}\n\n\\begin{document}\n\nHello, World!\n\n\\end{document}\n"
        )

    handler.send_json({"name": name}, status=201)


def _delete_project(handler, name):
    config = handler.config
    if config["mode"] == "single":
        handler.send_json({"error": "Cannot delete project in single mode"}, status=400)
        return

    project_dir = os.path.join(config["projects_dir"], name)
    if not os.path.isdir(project_dir):
        handler.send_json({"error": "Project not found"}, status=404)
        return

    import shutil

    shutil.rmtree(project_dir)
    handler.send_json({"deleted": name})


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
        if item.startswith(".") and item != CONFIG_FILE:
            continue
        if item == "__pycache__":
            continue

        full = os.path.join(current_dir, item)
        rel = os.path.relpath(full, base_dir)

        if os.path.isdir(full):
            children = _build_file_tree(base_dir, full)
            dirs_list.append({"name": item, "path": rel, "type": "dir", "children": children})
        else:
            files_list.append({"name": item, "path": rel, "type": "file"})

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
        handler.send_json({"path": file_path, "content": content})
    except UnicodeDecodeError:
        handler.send_json({"error": "Binary file, cannot read as text"}, status=400)


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

    os.remove(full_path)
    handler.send_json({"path": file_path, "deleted": True})


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
    # Allow overriding docker image from request or project config
    docker_image = (
        body.get("docker_image") or config_data.get("docker_image") or server_config["docker_image"]
    )
    compile_id = compiler.start_compile(
        project_dir=project_dir,
        main_file=main_file,
        engine=engine,
        use_docker=server_config["use_docker"],
        docker_image=docker_image,
    )

    handler.send_json({"compile_id": compile_id, "main_file": main_file, "engine": engine})


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

    content_type = "application/pdf" if file_path.endswith(".pdf") else "application/octet-stream"
    handler.send_file(full_path, content_type=content_type)


# LaTeX build artifacts to clean
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


# ── Git ──


def _git_status(handler, name):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return
    handler.send_json(git_ops.status(project_dir))


def _git_diff(handler, name):
    project_dir = _get_project_dir(handler, name)
    if not project_dir:
        return
    handler.send_text(git_ops.diff(project_dir))


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
