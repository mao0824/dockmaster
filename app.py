#!/usr/bin/env python3
"""13002-nas-nav — Niven 的 NAS 导航页(静态页面 + 服务状态 API)"""
import http.server
import json
import socket
import socketserver

SERVICES = [
    {"key": "mp", "port": 3000},
    {"key": "qbt", "port": 8085},
    {"key": "qbt_send", "port": 8086},
    {"key": "emby", "port": 8096},
    {"key": "dsm", "port": 5000},
]


def check(port: int) -> bool:
    try:
        s = socket.create_connection(("127.0.0.1", port), timeout=1.5)
        s.close()
        return True
    except OSError:
        return False


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/status"):
            body = json.dumps({s["key"]: check(s["port"]) for s in SERVICES}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        elif self.path in ("/", "/index.html"):
            try:
                body = open("index.html", "rb").read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(body)
            except OSError:
                self.send_error(500)
        else:
            self.send_error(404)

    def log_message(self, *a):  # 静默访问日志,避免刷容器日志
        pass


socketserver.ThreadingTCPServer.allow_reuse_address = True
with socketserver.ThreadingTCPServer(("0.0.0.0", 13002), Handler) as httpd:
    print("nas-nav serving on :13002", flush=True)
    httpd.serve_forever()
