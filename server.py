#!/usr/bin/env python3
"""Marcador de Parejas: serves the scoreboard and relays an iPhone remote over the local Wi-Fi.

Run:  python3 server.py   (or double-click "Iniciar marcador.command")
TV:   http://localhost:8000/marcador.html  (opens automatically)
Phone: scan the QR code shown in the scoreboard's control panel (key C).
"""
import json
import os
import queue
import random
import socket
import subprocess
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", 8000))
ROOT = os.path.dirname(os.path.abspath(__file__))


def load_pin():
    # Keep the same code across restarts so phones don't need to rescan.
    path = os.path.join(ROOT, ".codigo")
    try:
        pin = open(path).read().strip()
        if len(pin) == 4 and pin.isdigit():
            return pin
    except OSError:
        pass
    pin = f"{random.randint(0, 9999):04d}"
    try:
        with open(path, "w") as f:
            f.write(pin)
    except OSError:
        pass
    return pin


PIN = load_pin()

clients = set()
lock = threading.Lock()
last_state = None

# Trivia buzzer. The server decides who pressed first: the first /buzz request to arrive wins.
buzz_lock = threading.Lock()
buzz = {"mode": "off", "winner": None, "wrong": None, "locked": [], "q": 0, "pts": 1, "event": "init", "seq": 0}


def lan_ip():
    # Prefer the Mac's Wi-Fi/Ethernet address; the default route may point at a VPN.
    # Windows also has an ipconfig, with a different syntax, so only ask on macOS.
    for iface in ("en0", "en1") if sys.platform == "darwin" else ():
        try:
            ip = subprocess.run(["ipconfig", "getifaddr", iface], capture_output=True, text=True, timeout=2).stdout.strip()
            if ip:
                return ip
        except Exception:
            pass
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def remote_url():
    return f"http://{lan_ip()}:{PORT}/remote.html?k={PIN}"


def buzzer_url(team):
    return f"http://{lan_ip()}:{PORT}/buzzer.html?k={PIN}&t={team}"


def buzz_changed(event):
    # call with buzz_lock held
    buzz["event"] = event
    buzz["seq"] += 1
    broadcast("buzzer", dict(buzz))


def buzz_command(action, data):
    with buzz_lock:
        mode = buzz["mode"]
        if action == "buzz_open":
            buzz.update(mode="armed", winner=None, wrong=None, locked=[])
            buzz["q"] += 1
            buzz_changed("open")
        elif action == "buzz_right" and mode == "buzzed":
            team = buzz["winner"]
            broadcast("cmd", {"action": "add", "team": team, "n": buzz["pts"], "via": "trivia"})
            buzz.update(mode="done", wrong=None)
            buzz_changed("right")
        elif action == "buzz_wrong" and mode == "buzzed":
            team = buzz["winner"]
            buzz["locked"].append(team)
            other = 1 - team
            buzz.update(winner=None, wrong=team, mode="armed" if other not in buzz["locked"] else "done")
            buzz_changed("wrong")
        elif action == "buzz_pts":
            try:
                buzz["pts"] = max(1, min(100, int(data.get("n", 1))))
            except (TypeError, ValueError):
                return
            buzz_changed("pts")
        elif action == "buzz_off":
            buzz.update(mode="off", winner=None, wrong=None, locked=[])
            buzz_changed("off")


def sse(event, data):
    return f"event: {event}\ndata: {json.dumps(data)}\n\n".encode()


def broadcast(event, data):
    msg = sse(event, data)
    with lock:
        for q in list(clients):
            q.put(msg)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def log_message(self, *a):
        pass

    def is_local(self):
        return self.client_address[0] in ("127.0.0.1", "::1")

    def send_json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        if self.path.endswith(".html"):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/":
            self.send_response(302)
            self.send_header("Location", "/marcador.html")
            self.end_headers()
        elif path == "/info":
            # Only the laptop itself may read the PIN.
            if not self.is_local():
                return self.send_json({"error": "forbidden"}, 403)
            self.send_json({"url": remote_url(), "pin": PIN, "buzzers": [buzzer_url(0), buzzer_url(1)]})
        elif path == "/events":
            self.stream()
        else:
            super().do_GET()

    def do_POST(self):
        path = self.path.split("?")[0]
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            return self.send_json({"error": "bad json"}, 400)
        global last_state
        if path == "/cmd":
            if str(data.get("k")) != PIN and not self.is_local():
                return self.send_json({"error": "pin"}, 403)
            data.pop("k", None)
            action = str(data.get("action", ""))
            if action.startswith("buzz_"):
                buzz_command(action, data)
            else:
                broadcast("cmd", data)
            self.send_json({"ok": True})
        elif path == "/buzz":
            if str(data.get("k")) != PIN:
                return self.send_json({"error": "pin"}, 403)
            team = data.get("team")
            if team not in (0, 1):
                return self.send_json({"error": "team"}, 400)
            with buzz_lock:
                if buzz["mode"] == "armed" and team not in buzz["locked"]:
                    buzz.update(mode="buzzed", winner=team, wrong=None)
                    buzz_changed("buzz")
                    result = "first"
                elif buzz["mode"] == "buzzed":
                    result = "first" if buzz["winner"] == team else "late"
                elif buzz["mode"] == "armed":
                    result = "locked"
                else:
                    result = "closed"
            self.send_json({"result": result})
        elif path == "/state":
            if not self.is_local():
                return self.send_json({"error": "forbidden"}, 403)
            last_state = data
            broadcast("state", data)
            self.send_json({"ok": True})
        else:
            self.send_json({"error": "not found"}, 404)

    def stream(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        q = queue.Queue()
        with lock:
            clients.add(q)
        if last_state is not None:
            q.put(sse("state", last_state))
        with buzz_lock:
            q.put(sse("buzzer", dict(buzz)))
        try:
            self.wfile.write(b": hola\n\n")
            self.wfile.flush()
            while True:
                try:
                    msg = q.get(timeout=15)
                except queue.Empty:
                    msg = b": ping\n\n"
                self.wfile.write(msg)
                self.wfile.flush()
        except Exception:
            pass
        finally:
            with lock:
                clients.discard(q)


def main():
    ThreadingHTTPServer.daemon_threads = True
    try:
        server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    except OSError:
        print(f"\n  El puerto {PORT} ya está en uso. ¿Ya está abierto el marcador en otra ventana?\n")
        return
    print("\n  ✦ Marcador de Parejas ✦\n")
    print(f"  Pantalla (TV):   http://localhost:{PORT}/marcador.html")
    print(f"  Control iPhone:  {remote_url()}")
    print(f"  Código:          {PIN}\n")
    print(f"  Timbre Hombres:  {buzzer_url(0)}")
    print(f"  Timbre Mujeres:  {buzzer_url(1)}\n")
    print("  En el marcador presiona C para ver los códigos QR.")
    print("  Deja esta ventana abierta. Ctrl+C para terminar.\n")
    if not os.environ.get("NO_BROWSER"):
        threading.Timer(.6, lambda: webbrowser.open(f"http://localhost:{PORT}/marcador.html")).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Marcador cerrado. ¡Gracias por jugar!\n")


if __name__ == "__main__":
    main()
