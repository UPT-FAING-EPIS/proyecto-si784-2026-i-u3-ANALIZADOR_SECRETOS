"""
run_web.py — Servidor y lanzador de la interfaz web multipropósito de SecretScanner.

Ejecución:
    python run_web.py
"""

import sys
import os
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

PORT = 8080
HOST = "127.0.0.1"

def install_dependencies():
    """Instala dependencias si no se encuentran en el entorno local."""
    try:
        import fastapi
        import uvicorn
    except ImportError:
        print("[*] Dependencias web faltantes detectadas (fastapi, uvicorn).")
        print("[*] Instalando dependencias necesarias a través de pip...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"])
            print("[+] Dependencias instaladas con éxito.\n")
        except subprocess.CalledProcessError as e:
            print(f"[-] Error al instalar las dependencias: {e}")
            sys.exit(1)

def open_browser():
    """Espera un momento a que el servidor web se active y abre la página."""
    time.sleep(1.5)
    url = f"http://{HOST}:{PORT}"
    print(f"[*] Abriendo navegador web en: {url}")
    webbrowser.open(url)

def main():
    # Asegura que corremos desde el directorio raíz del proyecto
    script_dir = Path(__file__).resolve().parent
    os.chdir(script_dir)
    
    # Agregar 'src' al path de python para que secret_scanner sea importable
    src_dir = str(script_dir / "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    
    # Verificar e instalar dependencias si faltan
    install_dependencies()
    
    # Importar uvicorn de manera diferida
    import uvicorn
    
    print("\n============================================================")
    print("  Sistema Web de SecretScanner Iniciado")
    print(f"  Visualizar en: http://{HOST}:{PORT}")
    print("============================================================")
    print("  Módulos Integrados:")
    print("   1. Dashboard & Estadísticas en tiempo real")
    print("   2. Escáner de Rutas/Directorios Locales")
    print("   3. Escáner Interactivo de Código (Copia y Pega)")
    print("   4. Laboratorio Regex para prototipado rápido")
    print("   5. Analizador de Entropía de Shannon para Contraseñas")
    print("   6. Generador de Secretos Seguros Criptográficos")
    print("   7. Sandbox y Guía Educativa de Remediación")
    print("============================================================")
    print("  Presiona Ctrl+C para detener el servidor.\n")
    
    # Hilo para abrir el navegador web automáticamente
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Iniciar servidor Uvicorn
    try:
        # Pasamos la app directamente o por string importable con path añadido
        uvicorn.run("secret_scanner.web.app:app", host=HOST, port=PORT, reload=False, log_level="info")
    except KeyboardInterrupt:
        print("\n[+] Servidor web finalizado por el usuario.")
        sys.exit(0)

if __name__ == "__main__":
    main()
