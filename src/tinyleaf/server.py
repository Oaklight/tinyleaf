"""HTTP server wrapper for tinyleaf."""

import json
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


class TexliveHandler(BaseHTTPRequestHandler):
    """Request handler with routing to API handlers."""

    # Injected by run_server()
    config: dict = {}

    def log_message(self, format, *args):
        """Suppress default request logging for cleaner output."""
        pass

    # ── HTTP method dispatchers ──

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"

        if path == "/" or path == "/index.html":
            self._serve_static("index.html", "text/html")
        elif path.startswith("/vendor/"):
            self._serve_vendor(path[8:])
        elif path == "/api/mode":
            self._handle_api("get_mode")
        elif path == "/api/docker/images":
            self._handle_api("list_docker_images")
        elif path == "/api/vendor/status":
            self._handle_api("vendor_status")
        elif path == "/api/settings":
            self._handle_api("get_settings")
        elif path == "/api/projects":
            self._handle_api("list_projects")
        elif path.startswith("/api/fs/browse"):
            self._handle_api("browse_filesystem")
        elif path.startswith("/api/projects/"):
            self._route_project_get(path, parsed.query)
        else:
            self._send_error(404, "Not found")

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path.rstrip("/")

        if path == "/api/projects":
            self._handle_api("create_project")
        elif path == "/api/projects/register":
            self._handle_api("register_project")
        elif path == "/api/vendor/update":
            self._handle_api("update_vendor")
        elif path == "/api/docker/pull":
            self._handle_api("docker_pull")
        elif path == "/api/docker/rmi":
            self._handle_api("docker_rmi")
        elif path == "/api/docker/cancel-pull":
            self._handle_api("cancel_docker_pull")
        elif path.startswith("/api/projects/"):
            self._route_project_post(path)
        else:
            self._send_error(404, "Not found")

    def do_PUT(self):
        path = urllib.parse.urlparse(self.path).path.rstrip("/")

        if path == "/api/settings":
            self._handle_api("put_settings")
        elif path.startswith("/api/projects/"):
            self._route_project_put(path)
        else:
            self._send_error(404, "Not found")

    def do_DELETE(self):
        path = urllib.parse.urlparse(self.path).path.rstrip("/")

        if path.startswith("/api/projects/"):
            self._route_project_delete(path)
        else:
            self._send_error(404, "Not found")

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_HEAD(self):
        """Handle HEAD requests (same routing as GET, no body)."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"

        if path.startswith("/vendor/"):
            filename = os.path.basename(path[8:])
            config_dir = self.config.get("config_dir")
            if config_dir:
                filepath = os.path.join(config_dir, "vendor", filename)
                if os.path.isfile(filepath):
                    ct = (
                        "application/javascript" if filename.endswith(".js") else "application/json"
                    )
                    self.send_response(200)
                    self.send_header("Content-Type", ct)
                    self.send_header("Content-Length", str(os.path.getsize(filepath)))
                    self._send_cors_headers()
                    self.end_headers()
                    return
        self._send_error(404, "Not found")

    # ── Project route parsing ──

    def _parse_project_route(self, path):
        """Parse /api/projects/{name}/... into (name, rest).

        Returns:
            Tuple of (project_name, remaining_path) or None if invalid.
        """
        prefix = "/api/projects/"
        rest = path[len(prefix) :]
        parts = rest.split("/", 1)
        name = urllib.parse.unquote(parts[0])
        sub = parts[1] if len(parts) > 1 else ""
        return name, sub

    def _route_project_get(self, path, query_string=""):
        name, sub = self._parse_project_route(path)

        if not sub:
            # GET /api/projects/{name} — not used, but could return project info
            self._send_error(404, "Not found")
        elif sub == "files":
            self._handle_api("list_files", name=name)
        elif sub.startswith("files/"):
            file_path = urllib.parse.unquote(sub[6:])
            self._handle_api("read_file", name=name, file_path=file_path)
        elif sub.startswith("check/"):
            file_path = urllib.parse.unquote(sub[6:])
            self._handle_api("check_file", name=name, file_path=file_path)
        elif sub == "config":
            self._handle_api("get_config", name=name)
        elif sub.startswith("compile/") and sub.endswith("/stream"):
            compile_id = sub[8:-7]
            self._handle_api("compile_stream", name=name, compile_id=compile_id)
        elif sub.startswith("output/"):
            file_path = urllib.parse.unquote(sub[7:])
            self._handle_api("get_output", name=name, file_path=file_path)
        elif sub == "synctex/forward":
            qs = urllib.parse.parse_qs(query_string)
            self._handle_api("synctex_forward", name=name, qs=qs)
        elif sub == "synctex":
            qs = urllib.parse.parse_qs(query_string)
            self._handle_api("synctex_query", name=name, qs=qs)
        elif sub == "git/status":
            self._handle_api("git_status", name=name)
        elif sub == "git/diff":
            qs = urllib.parse.parse_qs(query_string)
            self._handle_api("git_diff", name=name, qs=qs)
        elif sub.startswith("git/diff/"):
            file_path = urllib.parse.unquote(sub[9:])
            qs = urllib.parse.parse_qs(query_string)
            self._handle_api("git_diff_file", name=name, file_path=file_path, qs=qs)
        elif sub == "git/log":
            self._handle_api("git_log", name=name)
        elif sub == "wordcount":
            self._handle_api("word_count", name=name)
        elif sub == "export":
            self._handle_api("export_zip", name=name)
        elif sub == "search":
            qs = urllib.parse.parse_qs(query_string)
            self._handle_api("search_files", name=name, qs=qs)
        else:
            self._send_error(404, "Not found")

    def _route_project_post(self, path):
        name, sub = self._parse_project_route(path)

        if sub == "compile":
            self._handle_api("compile", name=name)
        elif sub.startswith("compile/") and sub.endswith("/cancel"):
            compile_id = sub[8:-7]
            self._handle_api("cancel_compile", name=name, compile_id=compile_id)
        elif sub == "clean":
            self._handle_api("clean", name=name)
        elif sub == "mkdir":
            self._handle_api("mkdir", name=name)
        elif sub == "rename":
            self._handle_api("rename_path", name=name)
        elif sub == "upload":
            self._handle_api("upload", name=name)
        elif sub == "git/commit":
            self._handle_api("git_commit", name=name)
        elif sub == "git/push":
            self._handle_api("git_push", name=name)
        elif sub == "git/pull":
            self._handle_api("git_pull", name=name)
        elif sub == "rename-project":
            self._handle_api("rename_project", name=name)
        else:
            self._send_error(404, "Not found")

    def _route_project_put(self, path):
        name, sub = self._parse_project_route(path)

        if sub.startswith("files/"):
            file_path = urllib.parse.unquote(sub[6:])
            self._handle_api("write_file", name=name, file_path=file_path)
        elif sub == "config":
            self._handle_api("put_config", name=name)
        else:
            self._send_error(404, "Not found")

    def _route_project_delete(self, path):
        name, sub = self._parse_project_route(path)

        if not sub:
            self._handle_api("delete_project", name=name)
        elif sub.startswith("files/"):
            file_path = urllib.parse.unquote(sub[6:])
            self._handle_api("delete_file", name=name, file_path=file_path)
        else:
            self._send_error(404, "Not found")

    # ── Dispatch to handlers ──

    def _handle_api(self, action, **kwargs):
        from tinyleaf.handlers import handle_request

        handle_request(self, action, **kwargs)

    # ── Response helpers ──

    def _serve_static(self, filename, content_type):
        filepath = os.path.join(STATIC_DIR, filename)
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", f"{content_type}; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self._send_error(404, f"Static file not found: {filename}")

    def _serve_vendor(self, filename):
        """Serve a file from the vendor directory."""
        config_dir = self.config.get("config_dir")
        if not config_dir:
            self._send_error(404, "Vendor not available in single mode")
            return
        # Sanitize filename to prevent path traversal
        filename = os.path.basename(filename)
        filepath = os.path.join(config_dir, "vendor", filename)
        if not os.path.isfile(filepath):
            self._send_error(404, f"Vendor file not found: {filename}")
            return
        ct = "application/javascript" if filename.endswith(".js") else "application/json"
        self.send_file(filepath, content_type=ct)

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._send_cors_headers()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_text(self, text, status=200, content_type="text/plain"):
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self._send_cors_headers()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, filepath, content_type="application/octet-stream"):
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self._send_cors_headers()
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self._send_error(404, "File not found")

    def start_sse(self):
        """Begin an SSE response. Caller must write events via send_sse_event()."""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self._send_cors_headers()
        self.end_headers()

    def send_sse_event(self, data, event=None):
        """Send a single SSE event."""
        lines = []
        if event:
            lines.append(f"event: {event}")
        if isinstance(data, dict):
            lines.append(f"data: {json.dumps(data, ensure_ascii=False)}")
        else:
            lines.append(f"data: {data}")
        lines.append("")
        lines.append("")
        self.wfile.write("\n".join(lines).encode("utf-8"))
        self.wfile.flush()

    def read_json_body(self):
        """Read and parse JSON request body. Returns dict or None."""
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length)
        return json.loads(body)

    def _send_error(self, status, message):
        self.send_json({"error": message}, status=status)

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")


def run_server(config: dict):
    """Start the HTTP server (blocking)."""
    TexliveHandler.config = config
    host = config["host"]
    port = config["port"]
    server = ThreadingHTTPServer((host, port), TexliveHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()
