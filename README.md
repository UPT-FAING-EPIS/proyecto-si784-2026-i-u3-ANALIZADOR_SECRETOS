[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/MQUb8mG3)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=23328920)

# SecretScanner — Analizador de Secretos


Herramienta de código abierto desarrollada en **Python 3.10** que analiza proyectos de software y detecta **secretos y credenciales hardcodeadas** (API keys, tokens, contraseñas, claves privadas) mediante expresiones regulares.

## Características

- Soporte para cualquier directorio o archivo de texto.
- Detección automática del tipo de secreto encontrado.
- Recorrido recursivo de directorios con `os.walk`.
- Análisis basado en **8 patrones regex** documentados: GitHub Token, AWS Access Key, API Key genérica, contraseña hardcodeada, JWT Token, Slack Token, clave privada RSA y URL con credenciales.
- Salida en consola con colores diferenciados por severidad.
- Exportación de reportes a **JSON** y **CSV** en la carpeta `output/`.
- Interfaz de línea de comandos (CLI) con `--path`, `--output` y `--verbose`.

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

```bash
git clone https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-i-u1-analizador-de-secretos.git
cd proyecto-si784-2026-i-u1-analizador-de-secretos
pip install -r requirements.txt
```

## Uso de la CLI

Una vez instaladas las dependencias, ejecuta la herramienta con:

```bash
python main.py --path <ruta-del-proyecto>
```

## Parámetros y opciones

| Opción | Descripción |
|--------|-------------|
| `--path <ruta>` | **(Requerido)** Ruta al directorio o archivo a analizar |
| `--output json` | Exporta el reporte a `output/report.json` |
| `--output csv` | Exporta el reporte a `output/report.csv` |
| `--verbose` | Muestra cada archivo procesado durante el escaneo |

## Ejemplos

```bash
# Analizar el directorio actual
python main.py --path .

# Analizar una ruta específica y exportar JSON
python main.py --path ./mi_proyecto --output json

# Analizar y exportar CSV
python main.py --path ./mi_proyecto --output csv

# Modo verbose — muestra cada archivo procesado
python main.py --path ./mi_proyecto --verbose

# Verbose + exportar JSON
python main.py --path ./mi_proyecto --verbose --output json
```

## Ejemplo de salida
🔍 Analizando: ./mi_proyecto

[ALERTA] GitHub Token encontrado
Archivo : mi_proyecto/config.py
Línea : 12
Contenido: token = "ghp_1234...****"

[ALERTA] Contraseña hardcodeada encontrada
Archivo : mi_proyecto/db.py
Línea : 8
Contenido: password = "****"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Análisis completado
Archivos analizados : 24
Secretos encontrados : 2
Reporte exportado : output/report.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

text

## Tipos de secretos detectados

| Tipo | Patrón detectado |
|------|-----------------|
| GitHub Token | `ghp_`, `gho_`, `ghu_`, `ghs_` |
| AWS Access Key | `AKIA[0-9A-Z]{16}` |
| API Key genérica | `api_key = "..."` |
| Contraseña hardcodeada | `password = "..."` |
| JWT Token | `eyJ...` (header base64) |
| Slack Token | `xox[baprs]-...` |
| Clave privada RSA | `-----BEGIN RSA PRIVATE KEY-----` |
| URL con credenciales | `http://user:pass@host` |

## Archivos ignorados

El escáner omite automáticamente extensiones binarias (`.png`, `.jpg`, `.gif`, `.exe`, `.zip`, `.pdf`) y directorios no relevantes (`.git`, `__pycache__`, `node_modules`, `output`).

## Desarrollo y tests

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar todos los tests
pytest

# Ver cobertura por módulo
pytest --cov=scanner --cov-report=term-missing

# Tests de un módulo específico
pytest tests/test_patterns.py -v
```

La cobertura mínima requerida es **80%** sobre el paquete `scanner/`.

## CI/CD

El proyecto cuenta con un pipeline de **GitHub Actions** (`.github/workflows/ci.yml`) que se activa en cada `push` y `pull_request` hacia `main`, instala dependencias, ejecuta los tests con cobertura y falla el build si algún test no pasa.

