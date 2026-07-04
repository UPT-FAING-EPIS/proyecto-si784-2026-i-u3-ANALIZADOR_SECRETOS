# Integración de SecretScanner como Skill (MCP)

Este documento detalla la integración de **SecretScanner** como una "Skill" (habilidad) compatible con agentes de Inteligencia Artificial mediante el estándar **Model Context Protocol (MCP)**. 

## ¿Qué es MCP?

El **Model Context Protocol (MCP)** es un estándar abierto que facilita la comunicación entre modelos de Inteligencia Artificial (como Claude, Cursor, o agentes personalizados) y herramientas de software locales o remotas. Permite que la IA interactúe directamente con tu entorno, ejecutando acciones o leyendo datos de manera segura.

## La Skill de SecretScanner

La integración de SecretScanner expone su motor principal de escaneo de secretos para que pueda ser utilizado de forma autónoma por una IA. 

En lugar de que un desarrollador tenga que ejecutar el comando manualmente en la terminal para revisar si hay tokens o contraseñas hardcodeadas, la IA puede llamar a la herramienta en tiempo real mientras ayuda a escribir código, revisar PRs o analizar directorios.

### ¿Cómo funciona a nivel técnico?

1. **Implementación:** 
   El servidor está implementado en `src/secret_scanner/mcp_server.py` utilizando la clase `FastMCP` de la librería oficial `mcp`.

2. **Herramienta Expuesta (`@mcp.tool()`):**
   El servidor expone la función `scan_secrets(target_path: str)`. Cuando la IA decide ejecutar un escaneo, le pasa a esta función la ruta (ej. `./mi_proyecto`).
   
3. **Ejecución Lógica:**
   La función toma esa ruta, ejecuta internamente el analizador de `secret_scanner.scanner.file_scanner`, recopila los resultados (contraseñas, API keys, tokens) y se los devuelve a la IA en un formato de texto plano estructurado.

4. **Comunicación por `stdio`:**
   Al ser ejecutado por el agente IA, el servidor se comunica usando la entrada y salida estándar (`stdin`/`stdout`). Envía y recibe mensajes JSON según la especificación del protocolo MCP, de manera invisible para el usuario humano.

## Configuración e Instalación

Al instalar el paquete (con `pip install .`), se registra un comando de consola o *entry point* llamado `secret-scanner-mcp`. Este comando es el que los agentes IA utilizarán para arrancar el servidor en segundo plano.

### Integración en Agentes Compatibles (Ej. Claude Desktop)

Para que el agente reconozca tu Skill, es necesario añadir la configuración en el archivo correspondiente de tu cliente IA (por ejemplo, `claude_desktop_config.json`):

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

Al reiniciar el Agente, este detectará la herramienta "SecretScanner" y sabrá que puede usarla para buscar secretos o vulnerabilidades en el código que está analizando.

## Extensibilidad

La arquitectura actual está diseñada para escalar. Si en un futuro deseas que la IA pueda realizar más acciones (por ejemplo, leer el último reporte CSV generado, o añadir una regla de excepción temporal), simplemente puedes agregar nuevas funciones en el archivo `mcp_server.py` y decorarlas con `@mcp.tool()`. El protocolo MCP se encargará automáticamente de notificar a la IA sobre las nuevas capacidades disponibles.
