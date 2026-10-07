"""
MANOS QUE HABLAN - Lanzador en Python
Proyecto sociotecnológico Trayecto II - UPT de Aragua "Federico Brito Figueroa"

Este programa en Python abre un servidor local y ejecuta el juego web (index.html)
que está en la misma carpeta. No necesita internet ni instalar nada extra.

Uso:  python servidor_lsv.py
Luego se abre en el navegador:  http://localhost:8000
Otros dispositivos de la misma red Wi-Fi pueden abrir la dirección que aparece en pantalla.
"""
import http.server
import os
import socket
import socketserver
import threading
import webbrowser

PUERTO = 8000
CARPETA = os.path.dirname(os.path.abspath(__file__))


class Manejador(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=CARPETA, **kwargs)

    def log_message(self, *args):
        pass  # no llenar la pantalla de mensajes


def ip_local():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"


if not os.path.exists(os.path.join(CARPETA, "index.html")):
    raise SystemExit("No se encontró index.html. Ponlo en la misma carpeta que este archivo.")

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PUERTO), Manejador) as servidor:
    print("🤟 Manos que hablan está funcionando")
    print(f"   En este aparato:   http://localhost:{PUERTO}")
    print(f"   Otros aparatos Wi-Fi: http://{ip_local()}:{PUERTO}")
    print("   Para cerrar, presiona Ctrl+C (o detén el programa).")
    threading.Timer(1, lambda: webbrowser.open(f"http://localhost:{PUERTO}")).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
