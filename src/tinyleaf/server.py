"""HTTP server for tinyleaf, built on zerodep httpserver."""

import email.utils
import os

from tinyleaf._vendor.httpserver import (
    App,
    Response,
    StreamingResponse,
    abort,
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

_CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

app = App(max_body_size=50 * 1024 * 1024)

_config: dict = {}


def _json_body(request):
    """Parse JSON body, returning {} for empty bodies."""
    return request.json() if request.body else {}


# Extension → MIME type mapping for static assets
_MIME_TYPES = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".json": "application/json",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".ico": "image/x-icon",
}


def _cache_control_for_static(filename):
    if filename == "index.html" or filename.endswith((".css", ".js")):
        return "no-cache"
    return "public, max-age=86400"


def _send_cached_response(filepath, content_type, cache_control, request, charset=True):
    """Build a Response with ETag/304 support for static files."""
    try:
        stat = os.stat(filepath)
    except FileNotFoundError:
        abort(404, "File not found")

    etag = f'"{stat.st_mtime_ns:x}-{stat.st_size:x}"'
    last_modified = email.utils.formatdate(stat.st_mtime, usegmt=True)

    if request.headers.get("if-none-match") == etag:
        return Response(
            status_code=304,
            headers={
                "ETag": etag,
                "Cache-Control": cache_control,
            },
        )

    with open(filepath, "rb") as f:
        content = f.read()

    ct = f"{content_type}; charset=utf-8" if charset else content_type
    return Response(
        body=content,
        status_code=200,
        content_type=ct,
        headers={
            "Cache-Control": cache_control,
            "ETag": etag,
            "Last-Modified": last_modified,
        },
    )


# ── Static file routes ──


@app.route("/", methods=["GET", "HEAD"])
@app.route("/index.html", methods=["GET", "HEAD"])
def serve_index(request):
    filepath = os.path.join(STATIC_DIR, "index.html")
    return _send_cached_response(filepath, "text/html", "no-cache", request)


@app.route("/static/<path:filepath>", methods=["GET", "HEAD"])
def serve_static(request, filepath):
    rel_path = os.path.normpath(filepath)
    if rel_path.startswith("..") or os.path.isabs(rel_path):
        abort(403, "Forbidden")

    ext = os.path.splitext(rel_path)[1].lower()
    ct = _MIME_TYPES.get(ext, "application/octet-stream")
    full_path = os.path.join(STATIC_DIR, rel_path)
    cache_control = _cache_control_for_static(rel_path)
    return _send_cached_response(full_path, ct, cache_control, request)


@app.route("/vendor/<path:filepath>", methods=["GET", "HEAD"])
def serve_vendor(request, filepath):
    config_dir = _config.get("config_dir")
    if not config_dir:
        abort(404, "Vendor not available in single mode")
    assert isinstance(config_dir, str)

    filename = os.path.basename(filepath)
    full_path = os.path.join(config_dir, "vendor", filename)
    if not os.path.isfile(full_path):
        abort(404, f"Vendor file not found: {filename}")

    ct = "application/javascript" if filename.endswith(".js") else "application/json"
    return _send_cached_response(
        full_path,
        ct,
        "public, max-age=31536000, immutable",
        request,
        charset=False,
    )


# ── Global API routes ──


@app.get("/api/mode")
def api_get_mode(request):
    from tinyleaf.handlers import handle_get_mode

    return handle_get_mode(_config)


@app.get("/api/docker/images")
def api_list_docker_images(request):
    from tinyleaf.handlers import handle_list_docker_images

    return handle_list_docker_images()


@app.post("/api/docker/pull")
async def api_docker_pull(request):
    from tinyleaf.handlers import handle_docker_pull

    return await handle_docker_pull(request.json(), _config)


@app.post("/api/docker/rmi")
async def api_docker_rmi(request):
    from tinyleaf.handlers import handle_docker_rmi

    return await handle_docker_rmi(request.json())


@app.post("/api/docker/cancel-pull")
async def api_cancel_docker_pull(request):
    from tinyleaf.handlers import handle_cancel_docker_pull

    return handle_cancel_docker_pull(request.json())


@app.get("/api/vendor/status")
def api_vendor_status(request):
    from tinyleaf.handlers import handle_vendor_status

    return handle_vendor_status(_config)


@app.post("/api/vendor/update")
def api_vendor_update(request):
    from tinyleaf.handlers import handle_update_vendor

    return handle_update_vendor(request.json(), _config)


@app.get("/api/settings")
def api_get_settings(request):
    from tinyleaf.handlers import handle_get_settings

    return handle_get_settings(_config)


@app.put("/api/settings")
def api_put_settings(request):
    from tinyleaf.handlers import handle_put_settings

    return handle_put_settings(request.json(), _config)


@app.get("/api/projects")
def api_list_projects(request):
    from tinyleaf.handlers import handle_list_projects

    return handle_list_projects(_config)


@app.post("/api/projects")
def api_create_project(request):
    from tinyleaf.handlers import handle_create_project

    return handle_create_project(request.json(), _config)


@app.post("/api/projects/register")
def api_register_project(request):
    from tinyleaf.handlers import handle_register_project

    return handle_register_project(request.json(), _config)


@app.get("/api/fs/browse")
def api_browse_filesystem(request):
    from tinyleaf.handlers import handle_browse_filesystem

    return handle_browse_filesystem(request.query_params)


# ── Project-scoped API routes ──


@app.get("/api/projects/<name>/files")
def api_list_files(request, name):
    from tinyleaf.handlers import handle_list_files

    return handle_list_files(_config, name)


@app.get("/api/projects/<name>/files/<path:file_path>")
def api_read_file(request, name, file_path):
    from tinyleaf.handlers import handle_read_file

    return handle_read_file(_config, name, file_path)


@app.put("/api/projects/<name>/files/<path:file_path>")
def api_write_file(request, name, file_path):
    from tinyleaf.handlers import handle_write_file

    return handle_write_file(request.json(), _config, name, file_path)


@app.delete("/api/projects/<name>/files/<path:file_path>")
def api_delete_file(request, name, file_path):
    from tinyleaf.handlers import handle_delete_file

    return handle_delete_file(_config, name, file_path)


@app.get("/api/projects/<name>/check/<path:file_path>")
def api_check_file(request, name, file_path):
    from tinyleaf.handlers import handle_check_file

    return handle_check_file(_config, name, file_path)


@app.get("/api/projects/<name>/config")
def api_get_config(request, name):
    from tinyleaf.handlers import handle_get_config

    return handle_get_config(_config, name)


@app.put("/api/projects/<name>/config")
def api_put_config(request, name):
    from tinyleaf.handlers import handle_put_config

    return handle_put_config(request.json(), _config, name)


@app.post("/api/projects/<name>/compile")
async def api_compile(request, name):
    from tinyleaf.handlers import handle_compile

    return await handle_compile(request.json(), _config, name)


@app.get("/api/projects/<name>/compile/<compile_id>/stream")
async def api_compile_stream(request, name, compile_id):
    from tinyleaf import compiler
    from tinyleaf.handlers import sse_compile_stream

    if not compiler.get_job(compile_id):
        abort(404, "Compile job not found")
    return StreamingResponse(
        sse_compile_stream(compile_id, name),
        content_type="text/event-stream",
        headers=_CORS_HEADERS.copy(),
    )


@app.post("/api/projects/<name>/compile/<compile_id>/cancel")
async def api_cancel_compile(request, name, compile_id):
    from tinyleaf.handlers import handle_cancel_compile

    return handle_cancel_compile(compile_id)


@app.get("/api/projects/<name>/output/<path:file_path>")
def api_get_output(request, name, file_path):
    from tinyleaf.handlers import handle_get_output

    return handle_get_output(_config, name, file_path)


@app.get("/api/projects/<name>/synctex")
def api_synctex_query(request, name):
    from tinyleaf.handlers import handle_synctex_query

    return handle_synctex_query(request.query_params, _config, name)


@app.get("/api/projects/<name>/synctex/forward")
def api_synctex_forward(request, name):
    from tinyleaf.handlers import handle_synctex_forward

    return handle_synctex_forward(request.query_params, _config, name)


@app.post("/api/projects/<name>/clean")
def api_clean(request, name):
    from tinyleaf.handlers import handle_clean

    return handle_clean(_config, name)


@app.get("/api/projects/<name>/wordcount")
def api_word_count(request, name):
    from tinyleaf.handlers import handle_word_count

    return handle_word_count(_config, name)


@app.get("/api/projects/<name>/export")
def api_export_zip(request, name):
    from tinyleaf.handlers import handle_export_zip

    return handle_export_zip(_config, name)


@app.get("/api/projects/<name>/search")
def api_search_files(request, name):
    from tinyleaf.handlers import handle_search_files

    return handle_search_files(request.query_params, _config, name)


@app.get("/api/projects/<name>/symbols")
def api_project_symbols(request, name):
    from tinyleaf.handlers import handle_project_symbols

    return handle_project_symbols(_config, name)


@app.delete("/api/projects/<name>")
def api_delete_project(request, name):
    from tinyleaf.handlers import handle_delete_project

    return handle_delete_project(_json_body(request), _config, name)


@app.post("/api/projects/<name>/rename-project")
def api_rename_project(request, name):
    from tinyleaf.handlers import handle_rename_project

    return handle_rename_project(request.json(), _config, name)


@app.post("/api/projects/<name>/mkdir")
def api_mkdir(request, name):
    from tinyleaf.handlers import handle_mkdir

    return handle_mkdir(request.json(), _config, name)


@app.post("/api/projects/<name>/rename")
def api_rename_path(request, name):
    from tinyleaf.handlers import handle_rename_path

    return handle_rename_path(request.json(), _config, name)


@app.post("/api/projects/<name>/upload")
def api_upload(request, name):
    from tinyleaf.handlers import handle_upload

    return handle_upload(request, _config, name)


# ── Git routes ──


@app.get("/api/projects/<name>/git/branches")
def api_git_branches(request, name):
    from tinyleaf.handlers import handle_git_branches

    return handle_git_branches(request.query_params, _config, name)


@app.get("/api/projects/<name>/git/status")
def api_git_status(request, name):
    from tinyleaf.handlers import handle_git_status

    return handle_git_status(_config, name)


@app.get("/api/projects/<name>/git/diff")
def api_git_diff(request, name):
    from tinyleaf.handlers import handle_git_diff

    return handle_git_diff(request.query_params, _config, name)


@app.get("/api/projects/<name>/git/diff/<path:file_path>")
def api_git_diff_file(request, name, file_path):
    from tinyleaf.handlers import handle_git_diff_file

    return handle_git_diff_file(request.query_params, _config, name, file_path)


@app.get("/api/projects/<name>/git/log")
def api_git_log(request, name):
    from tinyleaf.handlers import handle_git_log

    return handle_git_log(_config, name)


@app.post("/api/projects/<name>/git/commit")
def api_git_commit(request, name):
    from tinyleaf.handlers import handle_git_commit

    return handle_git_commit(request.json(), _config, name)


@app.post("/api/projects/<name>/git/push")
def api_git_push(request, name):
    from tinyleaf.handlers import handle_git_push

    return handle_git_push(_config, name)


@app.post("/api/projects/<name>/git/pull")
def api_git_pull(request, name):
    from tinyleaf.handlers import handle_git_pull

    return handle_git_pull(_config, name)


@app.get("/api/projects/<name>/git/worktrees")
def api_git_worktree_list(request, name):
    from tinyleaf.handlers import handle_git_worktree_list

    return handle_git_worktree_list(_config, name)


@app.post("/api/projects/<name>/git/worktrees")
def api_git_worktree_add(request, name):
    from tinyleaf.handlers import handle_git_worktree_add

    return handle_git_worktree_add(request.json(), _config, name)


@app.delete("/api/projects/<name>/git/worktrees")
def api_git_worktree_remove(request, name):
    from tinyleaf.handlers import handle_git_worktree_remove

    return handle_git_worktree_remove(request.json(), _config, name)


@app.post("/api/projects/<name>/git/worktrees/switch")
def api_git_worktree_switch(request, name):
    from tinyleaf.handlers import handle_git_worktree_switch

    return handle_git_worktree_switch(request.json(), _config, name)


# ── CORS middleware ──


@app.before_request
def handle_cors_preflight(request):
    if request.method == "OPTIONS":
        return Response(status_code=204, headers=_CORS_HEADERS)


@app.after_request
def add_cors_headers(request, response):
    if isinstance(response, Response) and not isinstance(response, StreamingResponse):
        for k, v in _CORS_HEADERS.items():
            response.headers.setdefault(k, v)
    return response


def run_server(config: dict):
    """Start the HTTP server (blocking)."""
    global _config
    _config = config
    host = config["host"]
    port = config["port"]
    app.run(host=host, port=port)
