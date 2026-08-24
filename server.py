#!/usr/bin/env python3
"""X1Ninja Mon — local server. Keeps the API key off the page."""

from __future__ import annotations

import json
import os
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
BRAND = ROOT / "brand"
API_BASE = "https://api.x1.ninja"
PAGE_SIZE = 500
CACHE_SECONDS = 20
PORT = int(os.environ.get("PORT", "3000"))

_cache: dict = {"expires": 0.0, "payload": None, "error": None}
_lock = threading.Lock()


def load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def api_key() -> str:
    return os.environ.get("x1_api") or os.environ.get("X1_API_KEY") or ""


def fetch_pools_page(offset: int) -> dict:
    query = urllib.parse.urlencode(
        {"minLiquidity": 0, "limit": PAGE_SIZE, "offset": offset}
    )
    req = urllib.request.Request(
        f"{API_BASE}/v1/pools?{query}",
        headers={
            "Authorization": f"Bearer {api_key()}",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.loads(res.read().decode("utf-8"))


def newest_launches() -> dict:
    now = time.time()
    with _lock:
        if _cache["payload"] and now < _cache["expires"]:
            return _cache["payload"]

    if not api_key():
        raise RuntimeError("Missing x1_api in .env")

    first = fetch_pools_page(0)
    pools = list(first.get("pools") or [])
    total = int(first.get("total") or first.get("totalCount") or len(pools))
    offset = PAGE_SIZE
    while offset < total:
        page = fetch_pools_page(offset)
        chunk = page.get("pools") or []
        pools.extend(chunk)
        if not chunk:
            break
        offset += PAGE_SIZE

    pools.sort(key=lambda p: p.get("createdAt") or "", reverse=True)
    newest = pools[:40]
    payload = {
        "xntPriceUsd": first.get("xntPriceUsd"),
        "lastUpdated": first.get("lastUpdated"),
        "totalPools": total,
        "launches": newest,
    }
    with _lock:
        _cache["payload"] = payload
        _cache["expires"] = time.time() + CACHE_SECONDS
        _cache["error"] = None
    return payload


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC), **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        print(f"[{self.log_date_time_string()}] {fmt % args}")

    def do_GET(self) -> None:
        path = urllib.parse.urlparse(self.path).path
        if path == "/api/launches":
            self.handle_launches()
            return
        if path.startswith("/brand/"):
            self.serve_brand(path)
            return
        if path in ("/", "/index.html"):
            self.path = "/index.html"
        super().do_GET()

    def serve_brand(self, url_path: str) -> None:
        rel = url_path[len("/brand/") :]
        if not rel or ".." in Path(rel).parts:
            self.send_error(404)
            return
        target = (BRAND / rel).resolve()
        brand_root = BRAND.resolve()
        if target != brand_root and brand_root not in target.parents:
            self.send_error(404)
            return
        if not target.is_file():
            self.send_error(404)
            return
        data = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", self.guess_type(str(target)))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def handle_launches(self) -> None:
        try:
            payload = newest_launches()
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            self.send_json_error(exc.code, detail or exc.reason)
        except Exception as exc:
            self.send_json_error(500, str(exc))

    def send_json_error(self, code: int, message: str) -> None:
        body = json.dumps({"error": message}).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    load_env()
    if not api_key():
        raise SystemExit("Add x1_api to .env (see .env.example)")
    PUBLIC.mkdir(exist_ok=True)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"X1Ninja Mon → http://localhost:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
