# SecretScanner — Analizador de Secretos Multipropósito

**SecretScanner** es una suite de seguridad integral desarrollada en **Python 3.10+** diseñada para auditar, detectar y corregir **secretos y credenciales hardcodeadas** (API keys, tokens, contraseñas, claves privadas) en proyectos de desarrollo de software.

El sistema se compone de múltiples interfaces de uso (CLI, Extensión VSCode, Servidor MCP para Inteligencia Artificial y una consola Web interactiva) y está 100% preparado para ser empaquetado mediante **Docker** y desplegado automáticamente en la nube (PaaS).

---

## 🌟 Características Principales

* **Detección basada en 8 Patrones Regex**: Github Tokens, AWS Access Keys, API Keys genéricas, contraseñas quemadas, tokens JWT, tokens de Slack, claves privadas RSA y credenciales en URLs.
* **Enmascaramiento Inteligente**: Oculta el contenido crítico expuesto (`***`) al imprimir o exportar reportes para proteger el secreto real.
* **Múltiples Formatos de Salida**: CLI con colores por nivel de severidad y exportación nativa a formatos **JSON** y **CSV** en la carpeta `output/`.
* **Consola Web Interactiva**: Dashboard moderno en modo oscuro con glassmorphism y herramientas avanzadas de auditoría de seguridad.
* **Preparado para la Nube**: Configuración nativa para empaquetado Docker y despliegue rápido con un solo clic a través de Render Blueprints.

---

## 📁 Estructura del Ecosistema de SecretScanner

El proyecto está diseñado bajo un modelo modular que ofrece soporte en todas las etapas del desarrollo:

```
                  ┌──────────────────────────────────────────────┐
                  │              SecretScanner Core              │
                  │        (file_scanner.py & patterns.py)       │
                  └──────────────────────┬───────────────────────┘
                                         │
       ┌──────────────────┬──────────────┼──────────────┬──────────────────┐
       ▼                  ▼              ▼              ▼                  ▼
┌──────────────┐   ┌─────────────┐   ┌───────┐   ┌──────────────┐   ┌──────────────┐
│  Consola CLI │   │Servidor MCP │   │Extens.│   │Servidor Web  │   │  Imagen/App  │
│  (main.py)   │   │  (FastMCP)  │   │VSCode │   │  (FastAPI)   │   │ Contenedor   │
└──────────────┘   └─────────────┘   └───────┘   └──────────────┘   │   (Docker)   │
                                                                    └──────────────┘
```

1. **CLI (`main.py`)**: Utilidad de consola nativa para auditoría rápida local y automatización en pipelines de CI/CD.
2. **Servidor MCP (`mcp_server.py`)**: Puente compatible con el **Model Context Protocol (FastMCP)** para que agentes de IA (como Claude Desktop o Cursor) invoquen y consuman el scanner como una herramienta del sistema.
3. **Extensión VSCode (`vscode-extension/`)**: Extensión que analiza el archivo activo al guardarlo y subraya las claves inseguras directamente en tu editor de código.
4. **Consola Web (FastAPI + HTML5/CSS3/JS)**: Interfaz de usuario enriquecida que centraliza análisis locales, escaneo de repositorios externos y herramientas de remediación.
5. **Docker & Cloud Config**: Configuración lista de Dockerfile y Render Blueprint para albergar el scanner en producción.

---

## 💻 1. Uso de la Interfaz de Línea de Comandos (CLI)

### Instalación desde PyPI

```bash
pip install secret-scanner-cl
```

### Comandos y Parámetros

Ejecuta el analizador indicando la ruta del proyecto o archivo a auditar:

```bash
python -m secret_scanner.main --path <ruta-del-proyecto>
```

| Opción | Descripción |
|--------|-------------|
| `--path <ruta>` | **(Requerido)** Ruta al directorio o archivo local a analizar |
| `--output json` | Exporta los resultados detallados a `output/report.json` |
| `--output csv` | Exporta los resultados detallados a `output/report.csv` |
| `--verbose` | Modo informativo; imprime cada archivo conforme es procesado |

---

## 🌐 2. Interfaz Web de Seguridad y Auditoría

La interfaz web proporciona un panel visual interactivo con múltiples herramientas multipropósito integradas.

### Arrancar la Interfaz Web Localmente

Para instalar dependencias faltantes y abrir de forma automática la interfaz en tu navegador por defecto (`http://localhost:8080`), ejecuta:

```bash
python run_web.py
```

### Herramientas y Módulos de la Consola Web

* **Escáner Híbrido**:
  * *Ruta Local:* Escanea directorios de tu máquina de forma directa (oculta automáticamente cuando el sistema se aloja en la nube por seguridad).
  * *GitHub URL:* Introduce la dirección de cualquier repositorio público de GitHub. El sistema descarga el código temporalmente en memoria para auditarlo de forma remota.
  * *Subida ZIP:* Sube un archivo comprimido `.zip` de tus proyectos locales y analízalo de inmediato.
* **Escáner por Copia y Pega**: Caja de arena interactiva para pegar fragmentos de código sensibles y visualizar alertas de secretos resaltadas por colores.
* **Analizador de Robustez y Entropía**: Mide de forma gráfica la complejidad de contraseñas y tokens calculando su **Entropía de Shannon** en bits, determinando su nivel de fuerza (Muy Débil, Débil, Medio, Fuerte, Muy Fuerte) y calculando el tiempo estimado necesario para descifrarlo por fuerza bruta.
* **Generador de Secretos Seguros**: Generador criptográfico local con barras de longitud deslizantes y selectores de caracteres (mayúsculas, números, símbolos) para crear claves API y contraseñas de alta complejidad.
* **Laboratorio Regex**: Permite a administradores escribir expresiones regulares personalizadas y probarlas contra texto de prueba para experimentar antes de añadirlas al núcleo.
* **Guía Interactiva de Remediación**: Ejemplos de código y guías paso a paso para migrar secretos hardcodeados a variables de entorno en lenguajes como **Python**, **JavaScript (Node)**, **Go** y **Java**.

---

## ☁️ 3. Despliegue en la Nube con Render Blueprint

Este repositorio incluye una configuración de infraestructura como código lista para ser desplegada en **Render** usando contenedores **Docker**.

### Archivos de Configuración Incluidos

* **`Dockerfile`**: Compila una imagen ligera basada en `python:3.10-slim`, instala dependencias y expone el puerto `8080` de FastAPI.
* **`.dockerignore`**: Excluye los directorios de pruebas, entornos virtuales y código fuente innecesario para optimizar la compilación.
* **`render.yaml`**: Archivo Blueprint que automatiza el aprovisionamiento de un servicio web gratuito en Render.
* **`docker-compose.yml`**: Configuración para compilar y probar el contenedor de manera local ejecutando `docker compose up --build`.

### Pasos para Desplegar en la Nube

1. Realiza un `git push` de tu repositorio a GitHub o GitLab.
2. Inicia sesión en [Render.com](https://render.com).
3. Haz clic en **Blueprints** en la barra superior de la consola y presiona **New Blueprint Instance**.
4. Vincula tu repositorio de GitHub.
5. Render leerá el archivo `render.yaml` y creará automáticamente el servicio web. Haz clic en **Apply**.
6. Render desplegará tu app en una URL pública segura tipo `https://secret-scanner-web-xxxx.onrender.com`.

*Nota: Al desplegarse en la nube, el sistema ocultará automáticamente el escáner de "Ruta Local" para evitar errores del sistema de archivos, manteniendo activos los escáneres de GitHub y Cargas ZIP.*

---

## 🤖 4. Integración con Agentes de IA (MCP Skill)

SecretScanner incluye un servidor compatible con el estándar **Model Context Protocol (MCP)** para que herramientas como Claude Desktop o Cursor puedan interactuar nativamente con el analizador de secretos.

Para registrar el servidor de forma global:
```bash
secret-scanner-mcp
```

### Configuración en Claude Desktop

Agrega la siguiente clave al archivo de configuración de tu agente (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "secret-scanner": {
      "command": "secret-scanner-mcp",
      "args": []
    }
  }
}
```

---

## 🔌 5. Extensión de Visual Studio Code

### Instalación

1. Dirígete a la carpeta `vscode-extension/` del repositorio.
2. Abre VS Code, navega a Extensiones (Ctrl+Shift+X), haz clic en el menú de tres puntos `...` y selecciona **Install from VSIX...**.
3. Selecciona el archivo compilado `secret-scanner-vscode-1.0.0.vsix`.

*(Nota: Asegúrate de tener instalado globalmente `secret-scanner-cl` en tu máquina a través de `pip` para que la extensión de VSCode pueda invocar al motor).*

---

## 🧪 6. Desarrollo, Cobertura y Pipeline de CI/CD

El proyecto mantiene un alto estándar de calidad de código verificado mediante un pipeline de **GitHub Actions** (`.github/workflows/ci.yml`).

### Ejecución de Pruebas Unitarias

Para ejecutar el suite completo de 80 pruebas de seguridad, establece la variable de entorno de path y lanza pytest:

```bash
# En Windows (PowerShell)
$env:PYTHONPATH="src"; python -m pytest

# En Linux o macOS
PYTHONPATH=src pytest
```

Para auditar la cobertura de código (mantiene una cobertura superior al 90% en el core del scanner):
```bash
$env:PYTHONPATH="src"; python -m pytest --cov=secret_scanner.scanner --cov-report=term-missing
```

---

## 🤝 Créditos y Desarrollo

Herramienta educativa y de auditoría desarrollada por:
* **Kiara Z.** & **Mauricio C.**
* Escuela Profesional de Ingeniería en Informática y Sistemas (**EPIS**) - **Universidad Privada de Tacna**.
