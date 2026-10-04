#!/usr/bin/env python3
"""13002-dockmaster — NAS 导航页(配置驱动版:config.json 热加载,改配置刷新即生效)"""
import http.server
import json
import os
import socket
import socketserver

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(BASE, "config.json")


def load_config():
    """每次请求重新读配置 —— 改 config.json 无需重启容器。"""
    try:
        with open(CONFIG, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"title": "NAS 导航", "port": 13002, "services": [], "links": []}


def check(port) -> bool:
    try:
        s = socket.create_connection(("127.0.0.1", int(port)), timeout=1.5)
        s.close()
        return True
    except (OSError, ValueError, TypeError):
        return False


class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, body: bytes, ctype: str, code: int = 200):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/api/config"):
            cfg = load_config()
            self._send(json.dumps(cfg, ensure_ascii=False).encode(), "application/json; charset=utf-8")
        elif self.path.startswith("/api/status"):
            cfg = load_config()
            body = json.dumps(
                {s.get("key"): check(s.get("port")) for s in cfg.get("services", []) if s.get("key")}
            ).encode()
            self._send(body, "application/json")
        elif self.path in ("/", "/index.html"):
            try:
                self._send(open(os.path.join(BASE, "index.html"), "rb").read(), "text/html; charset=utf-8")
            except OSError:
                self.send_error(500)
        else:
            self.send_error(404)

    def log_message(self, *a):  # 静默访问日志
        pass


socketserver.ThreadingTCPServer.allow_reuse_address = True
cfg = load_config()
PORT = int(cfg.get("port", 13002))
with socketserver.ThreadingTCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"dockmaster serving on :{PORT} (config-driven)", flush=True)
    httpd.serve_forever()
