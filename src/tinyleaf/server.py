"""HTTP server for tinyleaf, built on zerodep httpserver."""

import email.utils
import hmac
import logging
import os
import re
import ssl
import time
import uuid
from urllib.parse import urlsplit

from tinyleaf import __version__
from tinyleaf._vendor.httpserver import (
    App,
    HTTPException,
    JSONResponse,
    Response,
    StreamingResponse,
    abort,
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

logger = logging.getLogger(__name__)

app = App(
    max_body_size=50 * 1024 * 1024,
    keep_alive=True,
    keep_alive_timeout=30.0,
)

_config: dict = {}

_STARTED_AT = time.time()

# Request ids are echoed from the client only when they are safe to log and
# return unchanged.
_REQUEST_ID_RE = re.compile(r"[A-Za-z0-9._-]{1,64}")

_STATUS_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "method_not_allowed",
    408: "timeout",
    409: "conflict",
    413: "payload_too_large",
    415: "unsupported_media_type",
    422: "processing_failed",
    424: "dependency_missing",
    429: "rate_limited",
    500: "internal_error",
    502: "upstream_error",
    503: "dependency_missing",
    504: "timeout",
}

# The current UI uses inline handlers and style attributes, so the first CSP
# needs 'unsafe-inline'. Removing those is a separate follow-up.
_SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob:; "
        "font-src 'self' data:; "
        "connect-src 'self'; "
        "worker-src 'self' blob:; "
        "object-src 'none'; "
        "base-uri 'none'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    ),
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
}


class APIError(HTTPException):
    """HTTP error carrying a stable machine-readable code and detail.

    Handlers raise this for expected client and dependency failures so the
    error envelope can distinguish them from unexpected server errors.
    """

    __slots__ = ("code", "detail")

    def __init__(self, status_code, message, code=None, detail=None):
        super().__init__(status_code, message)
        self.code = code
        self.detail = detail


def _request_id(request):
    return getattr(request.state, "request_id", "")


def _error_envelope(request, status, error, code=None, detail=None):
    """Build the JSON error envelope shared by every API error."""
    return JSONResponse(
        {
            "error": error,
            "code": code or _STATUS_CODES.get(status, f"http_{status}"),
            "detail": detail,
            "request_id": _request_id(request),
        },
        status_code=status,
    )


@app.before_request
def assign_request_id(request):
    """Attach a request id to every request, reusing a valid client id."""
    candidate = request.headers.get("x-request-id", "")
    request.state.request_id = (
        candidate if _REQUEST_ID_RE.fullmatch(candidate) else uuid.uuid4().hex[:16]
    )


@app.on_response_started
def add_response_headers(request, response):
    """Add the request id and security headers to every response.

    ``on_response_started`` fires for static files, errors, and short-circuits;
    ``after_request`` does not.
    """
    request_id = _request_id(request)
    if request_id:
        response.headers.setdefault("X-Request-Id", request_id)
    for name, value in _SECURITY_HEADERS.items():
        response.headers.setdefault(name, value)


@app.errorhandler(HTTPException)
def handle_http_exception(request, exception):
    return _error_envelope(
        request,
        exception.status_code,
        exception.message,
        getattr(exception, "code", None),
        getattr(exception, "detail", None),
    )


@app.errorhandler(Exception)
def handle_unexpected_exception(request, exception):
    logger.error("Unhandled exception for request %s: %s", _request_id(request), exception)
    return _error_envelope(request, 500, "Internal Server Error")


# Paths reachable without a token; everything else under /api/ requires one.
_PUBLIC_API_PATHS = {"/api/health", "/api/version", "/api/auth/session"}

_SESSION_COOKIE = "tinyleaf_session"
_SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


def _normalize_host(name):
    return name.strip().lower().rstrip(".")


def _host_name(host_header):
    """Return the normalized hostname from a Host or Origin authority string."""
    if host_header.startswith("["):
        end = host_header.find("]")
        name = host_header[1:end] if end != -1 else host_header
    else:
        name = host_header.split(":", 1)[0]
    return _normalize_host(name)


def _allowed_host_names(config):
    names = {"localhost", "127.0.0.1", "::1"}
    if config.get("host"):
        names.add(_normalize_host(config["host"]))
    names.update(_normalize_host(host) for host in (config.get("allowed_hosts") or []))
    return names


def _host_allowed(host_header, config):
    name = _host_name(host_header)
    return bool(name) and name in _allowed_host_names(config)


def _token_matches(candidate, token):
    """Constant-time token comparison that never raises on odd input."""
    return (
        isinstance(candidate, str)
        and candidate.isascii()
        and token.isascii()
        and hmac.compare_digest(candidate, token)
    )


def _has_valid_token(request, token):
    header = request.headers.get("authorization", "")
    if header[:7].lower() == "bearer ":
        if _token_matches(header[7:].strip(), token):
            return True
    return _token_matches(request.cookies.get(_SESSION_COOKIE, ""), token)


def _origin_allowed(request, config):
    if request.headers.get("sec-fetch-site") == "cross-site":
        return False
    origin = request.headers.get("origin")
    if not origin:
        return True
    try:
        authority = urlsplit(origin).netloc
    except ValueError:
        return False
    return _host_allowed(authority, config)


@app.before_request
def enforce_access(request):
    """Enforce Host, token, read-only, and Origin policy."""
    if not _host_allowed(request.headers.get("host", ""), _config):
        return _error_envelope(request, 400, "Host not allowed", "host_not_allowed")

    token = _config.get("token")
    if (
        token
        and request.path.startswith("/api/")
        and request.path not in _PUBLIC_API_PATHS
        and not _has_valid_token(request, token)
    ):
        response = _error_envelope(request, 401, "Authentication required", "unauthorized")
        response.headers["WWW-Authenticate"] = "Bearer"
        return response

    if (
        _config.get("read_only")
        and request.method not in _SAFE_METHODS
        and request.path != "/api/auth/session"
    ):
        return _error_envelope(request, 403, "Server is read-only", "read_only")

    if request.method not in _SAFE_METHODS and not _origin_allowed(request, _config):
        return _error_envelope(request, 403, "Origin not allowed", "origin_not_allowed")

    return None


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
    token = _config.get("token")
    candidate = request.query_params.get("token", [None])[0]
    if token and candidate is not None:
        if not _token_matches(candidate, token):
            response = _error_envelope(request, 401, "Invalid token", "unauthorized")
            response.headers["WWW-Authenticate"] = "Bearer"
            response.headers["Cache-Control"] = "no-store"
            return response
        response = Response(
            status_code=302,
            headers={"Location": "/", "Cache-Control": "no-store"},
        )
        response.set_cookie(
            _SESSION_COOKIE,
            token,
            httponly=True,
            samesite="Strict",
            secure=bool(_config.get("ssl_cert")),
            path="/",
        )
        return response
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


# ── API metadata ──


def _route_template(route):
    """Render a compiled route regex back as a ``{param}`` path template."""
    body = route.pattern.pattern
    if body.startswith("^"):
        body = body[1:]
    if body.endswith("$"):
        body = body[:-1]
    parts = re.split(r"(\([^()]*\))", body)
    names = iter(route.param_names)
    rendered = []
    for part in parts:
        if re.fullmatch(r"\([^()]*\)", part):
            name = next(names, None)
            rendered.append("{" + name + "}" if name else part)
        else:
            rendered.append(part)
    return "".join(rendered)


def _schema_payload():
    routes = []
    for route in app._routes:
        path = _route_template(route)
        if not path.startswith("/api/"):
            continue
        for method in route.methods:
            if method != "*":
                routes.append({"method": method, "path": path})
    routes.sort(key=lambda item: (item["path"], item["method"]))
    return {
        "name": "tinyleaf",
        "version": __version__,
        "auth_required": bool(_config.get("token")),
        "routes": routes,
    }


@app.get("/api/health")
def api_health(request):
    return {
        "status": "ok",
        "version": __version__,
        "mode": _config.get("mode", ""),
        "uptime_seconds": int(time.time() - _STARTED_AT),
    }


@app.get("/api/version")
def api_version(request):
    return {"name": "tinyleaf", "version": __version__}


@app.get("/api/schema")
def api_schema(request):
    return _schema_payload()


@app.post("/api/auth/session")
def api_auth_session(request):
    """Exchange a valid token for an HttpOnly session cookie."""
    token = _config.get("token")
    try:
        payload = _json_body(request)
    except ValueError:
        return _error_envelope(request, 400, "Invalid JSON body", "bad_request")
    if not isinstance(payload, dict):
        return _error_envelope(request, 400, "Request body must be a JSON object", "bad_request")
    candidate = payload.get("token", "")
    if not token:
        return {"authenticated": False, "auth_required": False}
    if not _token_matches(candidate, token):
        response = _error_envelope(request, 401, "Invalid token", "unauthorized")
        response.headers["WWW-Authenticate"] = "Bearer"
        response.headers["Cache-Control"] = "no-store"
        return response
    response = JSONResponse({"authenticated": True})
    response.headers["Cache-Control"] = "no-store"
    response.set_cookie(
        _SESSION_COOKIE,
        token,
        httponly=True,
        samesite="Strict",
        secure=bool(_config.get("ssl_cert")),
        path="/",
    )
    return response


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

    return await handle_docker_rmi(request.json(), _config)


@app.post("/api/docker/cancel-pull")
async def api_cancel_docker_pull(request):
    from tinyleaf.handlers import handle_cancel_docker_pull

    return handle_cancel_docker_pull(request.json())


@app.get("/api/docker/pull/status")
def api_docker_pull_status(request):
    from tinyleaf.handlers import handle_docker_pull_status

    return handle_docker_pull_status(request.query_params, _config)


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

    return handle_browse_filesystem(request.query_params, _config)


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


@app.post("/api/projects/<name>/git/branches/switch")
def api_git_switch_branch(request, name):
    from tinyleaf.handlers import handle_git_switch_branch

    return handle_git_switch_branch(request.json(), _config, name)


@app.post("/api/projects/<name>/git/branches")
def api_git_create_branch(request, name):
    from tinyleaf.handlers import handle_git_create_branch

    return handle_git_create_branch(request.json(), _config, name)


@app.delete("/api/projects/<name>/git/branches/<path:branch_name>")
def api_git_delete_branch(request, name, branch_name):
    from tinyleaf.handlers import handle_git_delete_branch

    return handle_git_delete_branch(_json_body(request), _config, name, branch_name)


@app.post("/api/projects/<name>/git/stash")
def api_git_stash(request, name):
    from tinyleaf.handlers import handle_git_stash

    return handle_git_stash(_config, name)


@app.post("/api/projects/<name>/git/stash/pop")
def api_git_stash_pop(request, name):
    from tinyleaf.handlers import handle_git_stash_pop

    return handle_git_stash_pop(_config, name)


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


# ── Lifecycle hooks ──


@app.on_request_rejected
async def log_rejected_request(rejection):
    """Log requests rejected while being read (malformed, too large, timeout)."""
    logger.warning(
        "Rejected request %s id=%s reason=%s client=%s",
        rejection.status_code,
        rejection.request_id,
        rejection.reason,
        rejection.client_addr,
    )


@app.on_client_disconnect
def log_client_disconnect(request):
    """Log a client that dropped while a response was being written."""
    logger.debug(
        "Client disconnected: %s %s from %s",
        request.method,
        request.path,
        request.client_addr,
    )


@app.on_shutdown
def shutdown_running_jobs():
    """Stop compile jobs and image pulls when the server exits."""
    from tinyleaf import compiler

    compiler.shutdown_all()


def run_server(config: dict):
    """Start the HTTP server (blocking)."""
    global _config
    _config = config
    host = config["host"]
    port = config["port"]

    ssl_context = None
    if config.get("ssl_cert"):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(
            certfile=config["ssl_cert"],
            keyfile=config.get("ssl_key") or None,
        )
        logger.info("TLS enabled with certificate %s", config["ssl_cert"])

    app.run(host=host, port=port, ssl_context=ssl_context)
