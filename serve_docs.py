"""
serve_docs.py — Servidor HTTP local para visualizar la documentación de SecretScanner.

Ejecución:
    python serve_docs.py
"""

import http.server
import socketserver
import webbrowser
import threading
import sys
import os

PORT = 8000

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Desactivar caché del navegador para cargar los MD actualizados al instante
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def start_server():
    # Asegura que corremos desde el directorio raíz del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    Handler = NoCacheHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"\n============================================================")
            print(f"  Servidor de Documentación de SecretScanner Iniciado")
            print(f"  Visualizar en: http://localhost:{PORT}/docs/viewer/index.html")
            print(f"============================================================")
            print("  Presiona Ctrl+C para detener el servidor.\n")
            httpd.serve_forever()
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    url = f"http://localhost:{PORT}/docs/viewer/index.html"
    
    # Abrir el navegador por defecto tras un retardo de 1 segundo
    timer = threading.Timer(1.0, lambda: webbrowser.open(url))
    timer.start()
    
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n[+] Servidor finalizado por el usuario.")
        sys.exit(0)
