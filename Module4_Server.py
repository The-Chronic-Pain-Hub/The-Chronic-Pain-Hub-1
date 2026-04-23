from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import ProxyHandler, Request, build_opener
import json
import mimetypes
import os
import sys


HOST = "127.0.0.1"
PORT = int(os.environ.get("PCILAB_PORT", "3000"))
CMS_NPPES_API = "https://npiregistry.cms.hhs.gov/api/"
BACKEND_API = "http://localhost:8000"  # Backend FastAPI server
PROJECT_ROOT = Path(__file__).resolve().parent
DIRECT_OPENER = build_opener(ProxyHandler({}))


class AppHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path_only = urlparse(path).path.lstrip("/")
        target = (PROJECT_ROOT / path_only).resolve()
        try:
            target.relative_to(PROJECT_ROOT)
        except ValueError:
            return str(PROJECT_ROOT / "index.html")
        return str(target)

    def do_GET(self):
        parsed = urlparse(self.path)

        # Proxy NPPES API requests (specific endpoint)
        if parsed.path == "/api/nppes":
            self.handle_nppes_proxy(parsed)
            return

        # Proxy all other Backend API requests (pain-mapping, analyze-text, analyze-audio, etc.)
        if parsed.path.startswith("/api/"):
            self.handle_backend_proxy(parsed, "GET")
            return

        if parsed.path == "/":
            self.path = "/index.html"

        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        # Proxy all Backend API POST requests (except NPPES which only uses GET)
        if parsed.path.startswith("/api/") and parsed.path != "/api/nppes":
            self.handle_backend_proxy(parsed, "POST")
            return

        self.send_error(405, "Method Not Allowed")

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def handle_nppes_proxy(self, parsed):
        query = parse_qs(parsed.query, keep_blank_values=False)
        flat_query = {key: values[-1] for key, values in query.items() if values}

        if "version" not in flat_query:
            flat_query["version"] = "2.1"

        url = CMS_NPPES_API + "?" + urlencode(flat_query)
        request = Request(
            url,
            headers={
                "User-Agent": "Chronic-Pain-Hub-Module4/1.0",
                "Accept": "application/json",
            },
        )

        try:
            with DIRECT_OPENER.open(request, timeout=20) as response:
                payload = response.read()
                content_type = response.headers.get("Content-Type", "application/json")
                self.send_response(response.status)
                self.send_header("Content-Type", content_type)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(payload)
        except (ConnectionAbortedError, BrokenPipeError):
            # Client closed connection - this is normal, just log and continue
            print(f"[NPPES] Client disconnected during request")
            return
        except HTTPError as error:
            try:
                error_body = error.read()
                self.send_response(error.code)
                self.send_header("Content-Type", error.headers.get("Content-Type", "application/json"))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(error_body)
            except (ConnectionAbortedError, BrokenPipeError):
                print(f"[NPPES] Client disconnected during error response")
                return
        except URLError as error:
            try:
                self.send_json(
                    502,
                    {
                        "error": "Unable to reach the CMS NPPES service from the local proxy.",
                        "details": str(error.reason),
                    },
                )
            except (ConnectionAbortedError, BrokenPipeError):
                print(f"[NPPES] Client disconnected during error response")
                return
        except Exception as error:
            try:
                self.send_json(
                    500,
                    {
                        "error": "Unexpected proxy failure.",
                        "details": str(error),
                    },
                )
            except (ConnectionAbortedError, BrokenPipeError):
                print(f"[NPPES] Client disconnected during error response")
                return

    def handle_backend_proxy(self, parsed, method):
        """Proxy requests to the Backend FastAPI server"""
        url = BACKEND_API + parsed.path
        if parsed.query:
            url += "?" + parsed.query

        try:
            # Read request body for POST requests
            content_length = 0
            request_body = b""
            if method == "POST":
                content_length = int(self.headers.get("Content-Length", 0))
                if content_length > 0:
                    request_body = self.rfile.read(content_length)

            # Create request
            request = Request(
                url,
                data=request_body if method == "POST" else None,
                headers={
                    "User-Agent": "Chronic-Pain-Hub-Proxy/1.0",
                    "Accept": "application/json",
                    "Content-Type": self.headers.get("Content-Type", "application/json"),
                },
                method=method,
            )

            # Forward request to backend
            with DIRECT_OPENER.open(request, timeout=30) as response:
                payload = response.read()
                content_type = response.headers.get("Content-Type", "application/json")
                self.send_response(response.status)
                self.send_header("Content-Type", content_type)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(payload)

        except (ConnectionAbortedError, BrokenPipeError):
            # Client closed connection - this is normal, just log and continue
            print(f"[Backend] Client disconnected during request to {parsed.path}")
            return
        except HTTPError as error:
            try:
                error_body = error.read()
                self.send_response(error.code)
                self.send_header("Content-Type", error.headers.get("Content-Type", "application/json"))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(error_body)
            except (ConnectionAbortedError, BrokenPipeError):
                print(f"[Backend] Client disconnected during error response")
                return
        except URLError as error:
            try:
                self.send_json(
                    502,
                    {
                        "error": "Unable to reach the Backend API server.",
                        "details": str(error.reason),
                        "hint": "Make sure the Backend server is running on port 8000",
                    },
                )
            except (ConnectionAbortedError, BrokenPipeError):
                print(f"[Backend] Client disconnected during error response")
                return
        except Exception as error:
            try:
                self.send_json(
                    500,
                    {
                        "error": "Backend proxy failure.",
                        "details": str(error),
                    },
                )
            except (ConnectionAbortedError, BrokenPipeError):
                print(f"[Backend] Client disconnected during error response")
                return

    def send_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)


def run():
    mimetypes.add_type("application/javascript", ".js")
    port = PORT

    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    server = ThreadingHTTPServer((HOST, port), AppHandler)
    print(f"Serving The Chronic Pain Hub at http://{HOST}:{port}/")
    print("Proxying NPPES requests through /api/nppes")
    print("Proxying Backend API requests through /api/pain-mapping/*")
    print("(Backend should be running on port 8000)")
    server.serve_forever()


if __name__ == "__main__":
    run()
