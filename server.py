"""
自我介绍网站 — 本地 / 局域网预览服务器

用法：
    python server.py

本机访问：  http://localhost:8000
局域网访问：http://<你的IP>:8000   （同 WiFi 下的手机/平板可用）
按 Ctrl+C 停止服务器
"""

import http.server
import socketserver
import webbrowser
import socket
import threading

PORT = 8000
DIRECTORY = "."


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        print(f"  ➜  {args[0]} {args[1]} {args[2]}")


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "未知"


def open_browser():
    import time
    time.sleep(0.5)
    webbrowser.open(f"http://localhost:{PORT}")


if __name__ == "__main__":
    local_ip = get_local_ip()

    print(f"\n  🌐 自我介绍网站已启动！")
    print(f"  ─────────────────────────────")
    print(f"  本机访问:   http://localhost:{PORT}")
    if local_ip != "未知":
        print(f"  局域网访问: http://{local_ip}:{PORT}")
        print(f"  （手机/平板连同一个 WiFi 后输入上方地址）")
    print(f"  ─────────────────────────────")
    print(f"  按 Ctrl+C 停止服务器\n")
    print(f"  ⚠️  注意：服务器停止后网址就打不开了！")
    print(f"      要让别人随时能访问，建议部署到线上。\n")

    threading.Thread(target=open_browser, daemon=True).start()

    # "" 表示监听所有网络接口，允许局域网其他设备访问
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  👋 服务器已关闭\n")
