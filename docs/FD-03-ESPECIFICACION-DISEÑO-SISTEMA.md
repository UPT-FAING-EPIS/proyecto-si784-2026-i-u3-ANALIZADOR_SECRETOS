<center>

![Logo UPT](./media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERÍA**

**Escuela Profesional de Ingeniería de Sistemas**

**Informe de Especificación de Requerimientos y Diseño**

**SecretScanner — Analizador de Secretos Multipropósito**

Curso: *Seguridad Informática / Base de Datos II*

Docente: *Mag. Patrick Cuadros Quiroga*

Integrantes:

***Kiara Z.***

***Mauricio C.***

**Tacna - Perú**

***2026***

</center>

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

Sistema *SecretScanner — Analizador de Secretos Multipropósito*

Informe de Especificación de Requerimientos (FD03)

Versión *2.0*

| CONTROL DE VERSIONES |           |              |               |            |                 |
|:--------------------:|:----------|:-------------|:--------------|:-----------|:----------------|
|       Versión        | Hecha por | Revisada por | Aprobada por  | Fecha      | Motivo          |
|         1.0          | Kiara Z., Mauricio C. | Kiara Z. | P. Cuadros Q. | 2026-07-07 | Versión inicial del documento FD03 |
|         2.0          | Kiara Z., Mauricio C. | Kiara Z. | P. Cuadros Q. | 2026-07-07 | Versión final del documento FD03 |

# ÍNDICE GENERAL

1. [Introducción](#1-introducción)
2. [Generalidades de la Empresa](#2-generalidades-de-la-empresa)
    1. [Nombre de la Empresa](#21-nombre-de-la-empresa)
    2. [Visión](#22-visión)
    3. [Misión](#23-misión)
    4. [Organigrama](#24-organigrama)
3. [Visionamiento de la Empresa](#3-visionamiento-de-la-empresa)
    1. [Descripcion del problema](#31-descripcion-del-problema)
    2. [Objetivo de Negocios](#32-objetivo-de-negocios)
    3. [Objetivo de diseño](#33-objetivo-de-diseño)
    4. [Alcance del proyecto](#34-alcance-del-proyecto)
    5. [Viabilidad del sistema](#35-viabilidad-del-sistema)
    6. [Informacion obtenida del Levantamiento de informacion](#36-informacion-obtenida-del-levantamiento-de-informacion)
4. [Analisis de procesos](#4-analisis-de-procesos)
    1. [Diagrama de Procesos Actual](#41-diagrama-de-procesos-actual)
    2. [Diagrama de Procesos Propuesto](#42-diagrama-de-procesos-propuesto)
5. [Especificacion de Requerimientos de Software](#5-especificacion-de-requerimientos-de-software)
    1. [Cuadro de Requerimientos funcionales Inicial](#51-cuadro-de-requerimientos-funcionales-inicial)
    2. [Cuadro de Requerimientos no funcionales](#52-cuadro-de-requerimientos-no-funcionales)
    3. [Cuadro de Requerimientos funcionales Final](#53-cuadro-de-requerimientos-funcionales-final)
    4. [Regla de Negocio](#54-regla-de-negocio)
6. [Fase de Desarrollo](#6-fase-de-desarrollo)
    1. [Perfil del Usuario](#61-perfil-del-usuario)
    2. [Modelo Conceptual](#62-modelo-conceptual)
        1. [Diagrama de paquetes](#621-diagrama-de-paquetes)
        2. [Diagrama de casos de uso](#622-diagrama-de-casos-de-uso)
        3. [Escenarios de casos de uso (narrativas)](#623-escenarios-de-casos-de-uso-narrativas)
    3. [Modelo Lógico](#63-modelo-lógico)
        1. [Analisis de Objetos](#631-analisis-de-objetos)
        2. [Diagrama de Actividades con objetos](#632-diagrama-de-actividades-con-objetos)
        3. [Diagrama de secuencia](#633-diagrama-de-secuencia)
        4. [Diagrama de clases](#634-diagrama-de-clases)
7. [Conclusiones](#7-conclusiones)
8. [Recomendaciones](#8-recomendaciones)
9. [Bibliografia](#9-bibliografia)
10. [Webgrafia](#10-webgrafia)
11. [Historias de Usuario, Criterios y Escenarios BDD](#11-historias-de-usuario-criterios-y-escenarios-bdd)

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

# 1. Introducción

El presente Informe de Especificación de Requerimientos y Diseño de Software (FD03) define las capacidades funcionales, no funcionales y la arquitectura general del sistema **SecretScanner**. 

**SecretScanner** es una suite de seguridad integral desarrollada en Python (3.10+) diseñada para auditar, detectar y corregir secretos y credenciales hardcodeadas (API keys, tokens, contraseñas, claves privadas) en proyectos de desarrollo de software. Este documento aborda el diseño de sus múltiples interfaces: la CLI, la Extensión de VSCode, el Servidor MCP para Inteligencia Artificial y la consola Web interactiva, así como su capacidad de despliegue automatizado en la nube (Docker).

# 2. Generalidades de la Empresa

## 2.1 Nombre de la Empresa

Universidad Privada de Tacna – Facultad de Ingeniería – Escuela Profesional de Ingeniería de Sistemas.

## 2.2 Visión

Formar profesionales líderes, innovadores y comprometidos con la calidad, capaces de desarrollar soluciones tecnológicas aplicadas a problemas reales del entorno.

## 2.3 Misión

Brindar formación integral en ingeniería de software, promoviendo investigación aplicada, ética profesional y producción de software de calidad con impacto académico y social.

## 2.4 Organigrama

```mermaid
flowchart TD
    UPT["Universidad Privada de Tacna"] --> FI["Facultad de Ingeniería"]
    FI --> EPIS["Escuela Profesional de Ingeniería de Sistemas"]
    EPIS --> CURSO["Curso: Seguridad Informática / Base de Datos II"]
    CURSO --> DOC["Docente Evaluador: Mag. Patrick Cuadros Quiroga"]
    CURSO --> EQ["Equipo del Proyecto SecretScanner (Kiara Z. y Mauricio C.)"]
```

# 3. Visionamiento de la Empresa

## 3.1 Descripcion del problema

En el ciclo de vida del desarrollo de software (SDLC), los programadores a menudo cometen el error crítico de dejar expuestas credenciales, tokens de acceso (AWS, GitHub, Slack) y claves privadas dentro del código fuente (hardcoding). Si este código se publica en repositorios públicos o es comprometido, los atacantes pueden acceder directamente a la infraestructura, bases de datos o servicios de pago de la empresa. Las herramientas existentes suelen ser complejas de integrar de manera local y carecen de una experiencia de usuario unificada que ofrezca opciones de mitigación (remediación) y conectividad con nuevas tecnologías (IA y MCP).

## 3.2 Objetivo de Negocios

Proveer a desarrolladores, auditores de seguridad (DevSecOps) y administradores de sistemas una herramienta rápida, extensible y multiplataforma que detecte secretos antes y después de que lleguen a producción. Esto reduce drásticamente el riesgo de brechas de datos, multas de cumplimiento (GDPR/PCI-DSS) y el daño a la reputación corporativa.

## 3.3 Objetivo de diseño

Diseñar un ecosistema modular basado en un motor core (`file_scanner.py` y `patterns.py`), rodeado de múltiples capas de presentación e integración:
- **CLI (`main.py`)**: Para uso en terminales y CI/CD pipelines.
- **Web App (FastAPI)**: Para un análisis visual interactivo, pruebas de entropía, laboratorio regex y generación de secretos.
- **VSCode Extension**: Para retroalimentación en tiempo real en el editor.
- **MCP Bridge (`mcp_server.py`)**: Para permitir a agentes de Inteligencia Artificial auditar proyectos usando SecretScanner como habilidad (tool).

## 3.4 Alcance del proyecto

**Incluido:**
- Detección basada en 8 patrones regex específicos.
- Consola Web moderna con UI reactiva.
- Extensión de VSCode funcional que subraya vulnerabilidades en el código al vuelo.
- Integración nativa a Docker y Render (PaaS) para despliegue Cloud.
- Exportación en múltiples formatos (JSON, CSV).
- Servidor FastMCP para agentes como Claude Desktop o Cursor.

**Fuera de alcance:**
- Eliminación automática de los secretos expuestos en repositorios remotos (solo sugiere la remediación).
- Análisis profundo de código compilado (.exe, .dll).

## 3.5 Viabilidad del sistema

El proyecto es altamente **viable**. Al estar construido principalmente sobre el ecosistema Python (FastAPI, pytest, expresiones regulares estándar), el mantenimiento de las reglas es sencillo. La arquitectura orientada a servicios para el front-end web, la CLI y la extensión de VSCode asegura un alto nivel de escalabilidad y desacoplamiento.

## 3.6 Informacion obtenida del Levantamiento de informacion

- Identificación de patrones más vulnerados (GitHub Tokens, AWS Access Keys, RSA Private Keys).
- Necesidad de enmascarar contraseñas encontradas en los reportes finales (principio de seguridad en profundidad).

# 4. Analisis de procesos

## 4.1 Diagrama de Procesos Actual

Proceso vulnerable actual en el desarrollo de software (Sin SecretScanner).

```mermaid
flowchart TD
    A["Desarrollador escribe código"] --> B["Usa temporalmente una API Key en texto plano"]
    B --> C["Olvida borrar el secreto y hace 'git commit'"]
    C --> D["Sube el código a GitHub Público"]
    D --> E["Atacante escanea repositorios con bots automatizados"]
    E --> F["Robo de credenciales en < 5 minutos"]
    F --> G["Compromiso de infraestructura de la empresa"]
```

## 4.2 Diagrama de Procesos Propuesto

Flujo seguro implementando SecretScanner en las estaciones de trabajo y CI/CD.

```mermaid
flowchart TD
    A["Desarrollador escribe código"] --> B["Usa temporalmente una API Key en texto plano"]
    B --> C["Extensión de VSCode detecta secreto y lo subraya (Opcional)"]
    C --> D["Pipeline CI o Hook pre-commit ejecuta SecretScanner CLI"]
    D --> E{"¿Hay secretos detectados?"}
    E -- "Sí" --> F["El Commit/Build falla. Se alerta al desarrollador"]
    F --> G["Desarrollador mueve secreto a variable de entorno (.env)"]
    G --> A
    E -- "No" --> H["Código seguro es subido al repositorio"]
```

# 5. Especificacion de Requerimientos de Software

## 5.1 Cuadro de Requerimientos funcionales Inicial

| ID     | Requerimiento funcional inicial             | Criterio general de aceptación                                                               |
|--------|---------------------------------------------|----------------------------------------------------------------------------------------------|
| RFI-01 | Detección mediante Regex                    | El sistema escanea archivos de texto plano buscando coincidencias con 8 expresiones regulares. |
| RFI-02 | Enmascaramiento de Secretos                 | Los resultados exportados muestran el valor censurado (ej. `AKIA_***`).                         |
| RFI-03 | Exportación JSON y CSV                      | Permite guardar los hallazgos en formatos estándar legibles por máquina.                     |
| RFI-04 | Interfaz de Línea de Comandos (CLI)         | Soporta ejecución desde terminal mediante argumentos (`--path`, `--output`).                   |

## 5.2 Cuadro de Requerimientos no funcionales

| ID     | Requerimiento no funcional | Métrica / Umbral                                               | Evidencia esperada                                              |
|--------|----------------------------|----------------------------------------------------------------|-----------------------------------------------------------------|
| RNF-01 | **Rendimiento**            | Analizar un directorio de 100 archivos fuente en < 5 segundos  | Pruebas de rendimiento (Benchmark CLI)                          |
| RNF-02 | **Cobertura de Pruebas**   | Cobertura de tests unitarios superior al 90% en el módulo base | Reporte de pytest-cov (`--cov=secret_scanner.scanner`)          |
| RNF-03 | **Portabilidad**           | Ejecutable y funcional en Windows, Linux, macOS y Docker       | Flujos de GitHub Actions exitosos; Dockerfile funcionando       |

## 5.3 Cuadro de Requerimientos funcionales Final

| ID    | Requerimiento funcional final                                                             | Prioridad | Trazabilidad técnica (módulo/código)                                    |
|-------|-------------------------------------------------------------------------------------------|-----------|-------------------------------------------------------------------------|
| RF-01 | Analizar código fuente local de forma recursiva ignorando binarios y archivos pesados     | Alta      | `secret_scanner/scanner/file_scanner.py`                                |
| RF-02 | Interfaz de consola web interactiva alojada por FastAPI                                   | Alta      | `run_web.py` / `fastapi`                                                |
| RF-03 | Análisis de código remoto desde repositorios de GitHub en memoria                         | Media     | `run_web.py` (Módulo de GitHub)                                         |
| RF-04 | Calculadora visual de entropía de contraseñas y tokens con base logarítmica               | Alta      | Frontend JS / API Endpoint de Entropía                                  |
| RF-05 | Integración continua mediante Extensión de VSCode y eventos `onDidSave`                   | Alta      | `vscode-extension/extension.js`                                         |
| RF-06 | Integración MCP para agentes LLM (Cursor, Claude) vía stdio                               | Media     | `mcp_server.py` (FastMCP)                                               |

## 5.4 Regla de Negocio

| ID    | Regla de negocio                                                                                               |
|-------|----------------------------------------------------------------------------------------------------------------|
| RN-01 | **Censura Obligatoria**: Nunca se debe imprimir o escribir en disco un secreto expuesto en su totalidad. Debe ser enmascarado al menos en un 50% de su longitud. |
| RN-02 | **Bloqueo Local en Cloud**: Cuando el sistema web está desplegado en la nube, la característica de "escanear ruta local" debe deshabilitarse para prevenir Directory Traversal. |

# 6. Fase de Desarrollo

## 6.1 Perfil del Usuario

| Perfil                      | Características                           | Necesidades principales                       |
|-----------------------------|-------------------------------------------|-----------------------------------------------|
| Desarrollador de Software   | Escribe código activamente                | Extensión de VSCode, alertas en tiempo real   |
| Ingeniero DevSecOps         | Configura pipelines de despliegue         | CLI rápida, integración con SonarQube o similar|
| Agente IA / LLM             | Audita código de manera autónoma          | Servidor MCP (FastMCP) para integración fluida|

## 6.2 Modelo Conceptual

### 6.2.1 Diagrama de paquetes

```mermaid
flowchart TD
    MAIN["CLI: main.py"]
    WEB["API Web: run_web.py / FastAPI"]
    VSCODE["Extensión VSCode: vscode-extension/"]
    MCP["Servidor MCP: mcp_server.py"]
    
    CORE["Motor Base: secret_scanner/scanner/"]
    PATTERNS["Reglas: patterns.py"]
    FILE_SCAN["Analizador: file_scanner.py"]
    
    MAIN --> CORE
    WEB --> CORE
    VSCODE -.->|Invoca| MAIN
    MCP --> CORE
    
    CORE --> PATTERNS
    CORE --> FILE_SCAN
```

### 6.2.2 Diagrama de casos de uso

A continuación, se presenta el diagrama de casos de uso general que muestra los 15 casos independientes interactuando con los distintos actores del sistema.

![Diagrama](./diagrams/diagram_1.png)

### 6.2.3 Escenarios de casos de uso (narrativas)

**Módulo CLI**

**CU-01: Escanear directorio local (CLI)**
- **Actor:** Desarrollador / DevSecOps
- **Descripción:** Ejecución rápida del scanner en terminal.
- **Flujo Principal:** 1) Usuario ejecuta `python -m secret_scanner.main --path src/`. 2) El motor itera sobre cada archivo de texto. 3) Evalúa cada línea usando regex. 4) Muestra resultados en consola con colores.

**CU-02: Exportar reporte JSON**
- **Actor:** DevSecOps
- **Descripción:** Guarda los hallazgos en un formato estructurado.
- **Flujo Principal:** 1) Ejecuta CLI con flag `--output json`. 2) El sistema procesa los archivos. 3) Censura los secretos (enmascaramiento). 4) Escribe `report.json`.

**CU-03: Exportar reporte CSV**
- **Actor:** DevSecOps
- **Descripción:** Guarda los hallazgos en formato tabular para auditorías.
- **Flujo Principal:** 1) Ejecuta CLI con flag `--output csv`. 2) El sistema consolida hallazgos. 3) Exporta a `report.csv`.

**Módulo Web App**

**CU-04: Escanear repositorio GitHub**
- **Actor:** DevSecOps
- **Descripción:** Análisis de un proyecto público directo desde la web.
- **Flujo Principal:** 1) Ingresa URL de GitHub. 2) FastAPI clona temporalmente el proyecto. 3) Escanea los archivos. 4) Muestra resultados visualmente.

**CU-05: Subir y escanear ZIP local**
- **Actor:** DevSecOps / QA
- **Descripción:** Escanea un paquete comprimido.
- **Flujo Principal:** 1) Sube `.zip`. 2) El backend extrae a temporal. 3) Escanea archivos. 4) Devuelve reporte interactivo.

**CU-06: Escanear fragmento de código (Copia/Pega)**
- **Actor:** Desarrollador
- **Descripción:** Analiza código sin guardar.
- **Flujo Principal:** 1) Pega el texto. 2) Procesado en RAM. 3) Muestra líneas vulnerables en rojo.

**CU-07: Evaluar entropía de contraseña o token**
- **Actor:** Desarrollador
- **Descripción:** Calcula la fuerza criptográfica.
- **Flujo Principal:** 1) Ingresa token. 2) Calcula entropía de Shannon. 3) Retorna nivel y tiempo de cracking.

**CU-08: Probar expresión regular personalizada**
- **Actor:** Desarrollador
- **Descripción:** Sandbox para escribir reglas.
- **Flujo Principal:** 1) Ingresa Regex y texto. 2) Evalúa en tiempo real. 3) Resalta coincidencias.

**CU-09: Generar clave segura**
- **Actor:** Desarrollador
- **Descripción:** Creación rápida de contraseñas.
- **Flujo Principal:** 1) Ajusta parámetros. 2) Produce clave y calcula entropía.

**CU-10: Consultar guía interactiva de remediación**
- **Actor:** DevSecOps / Desarrollador
- **Descripción:** Soluciones a problemas de hardcoding.
- **Flujo Principal:** 1) Clic en "Remediación". 2) Muestra guía de uso de `.env`.

**Módulo VSCode**

**CU-11: Instalar extensión**
- **Actor:** Desarrollador
- **Descripción:** Añade la funcionalidad al editor.
- **Flujo Principal:** 1) Carga archivo `.vsix`. 2) Verifica dependencia global de CLI.

**CU-12: Escanear archivo activo (onDidSave)**
- **Actor:** Desarrollador
- **Descripción:** Verificación en background.
- **Flujo Principal:** 1) Usuario presiona Ctrl+S. 2) Invoca CLI en la ruta actual. 3) Recibe JSON.

**CU-13: Visualizar vulnerabilidad subrayada (Squiggly)**
- **Actor:** Desarrollador
- **Descripción:** Interacción visual en el editor.
- **Flujo Principal:** 1) Extensión inyecta Diagnostic. 2) Subraya el secreto. 3) Tooltip indica el tipo de secreto.

**Módulo MCP (IA)**

**CU-14: Iniciar servidor MCP local**
- **Actor:** Agente IA / Usuario
- **Descripción:** Levantar instancia FastMCP.
- **Flujo Principal:** 1) Claude inicializa el comando. 2) Escucha invocaciones.

**CU-15: Ejecutar scan_directory mediante IA**
- **Actor:** Agente IA
- **Descripción:** Auditar código vía prompt.
- **Flujo Principal:** 1) IA invoca `scan_directory`. 2) Servidor procesa. 3) Retorna hallazgos.

## 6.3 Modelo Lógico

### 6.3.1 Analisis de Objetos

En esta sección se presenta el desglose de Boundary-Control-Entity y el Diagrama de Objetos para **cada uno de los 15 Casos de Uso** independientes.

#### CU-01: Escanear directorio local

| Tipo     | Objeto              | Responsabilidad                                      |
|----------|----------------------|------------------------------------------------------|
| Boundary | CLITerminal          | Interfaz de entrada de comandos y salida formateada   |
| Control  | CoreScanner          | Ejecuta lógica de iteración y llamadas regex          |
| Entity   | ScannerResult        | Contiene los secretos detectados                      |

![Diagrama](./diagrams/diagram_2.png)

#### CU-02: Exportar reporte JSON

| Tipo     | Objeto              | Responsabilidad                                      |
|----------|----------------------|------------------------------------------------------|
| Boundary | CLIParams            | Recibe el parámetro `--output json`                   |
| Control  | JSONReporter         | Formatea y censura datos para exportación             |
| Entity   | FileSystem           | Escribe el archivo en disco                           |

![Diagrama](./diagrams/diagram_3.png)

#### CU-03: Exportar reporte CSV

| Tipo     | Objeto              | Responsabilidad                                      |
|----------|----------------------|------------------------------------------------------|
| Boundary | CLIParams            | Recibe el parámetro `--output csv`                    |
| Control  | CSVReporter          | Mapea resultados a formato tabular                    |
| Entity   | FileSystem           | Escribe el archivo CSV                                |

![Diagrama](./diagrams/diagram_4.png)

#### CU-04: Escanear repo GitHub

| Tipo     | Objeto              | Responsabilidad                                      |
|----------|----------------------|------------------------------------------------------|
| Boundary | GitHubScanForm       | Formulario web para ingresar la URL                   |
| Control  | RepoClonerController | Descarga el repositorio en RAM temporal               |
| Entity   | TempDirectory        | Espacio donde se almacena el clon                     |

![Diagrama](./diagrams/diagram_5.png)

#### CU-05: Subir y escanear ZIP

| Tipo     | Objeto              | Responsabilidad                                      |
|----------|----------------------|------------------------------------------------------|
| Boundary | ZIPUploader          | Zona de arrastre de archivos en la Web App            |
| Control  | ExtractorController  | Descomprime el archivo y llama al CoreScanner         |
| Entity   | ScannerResult        | Almacena resultados del contenido del ZIP             |

![Diagrama](./diagrams/diagram_6.png)

#### CU-06: Escanear fragmento pegado

| Tipo     | Objeto              | Responsabilidad                                      |
|----------|----------------------|------------------------------------------------------|
| Boundary | CodeSandbox          | Textarea web para ingresar código                     |
| Control  | SandboxController    | Ejecuta motor regex en el buffer string               |
| Entity   | MemoryBuffer         | Almacena el texto temporalmente                       |

![Diagrama](./diagrams/diagram_7.png)

#### CU-07: Evaluar entropía de token

| Tipo     | Objeto              | Responsabilidad                                      |
|----------|----------------------|------------------------------------------------------|
| Boundary | EntropyForm          | Interfaz visual para medir seguridad                  |
| Control  | MathController       | Calcula algoritmo de Shannon                          |
| Entity   | EntropyMetrics       | Objeto con bits y tiempo de crack                     |

![Diagrama](./diagrams/diagram_8.png)

#### CU-08: Probar Regex personalizado

| Tipo     | Objeto              | Responsabilidad                                      |
|----------|----------------------|------------------------------------------------------|
| Boundary | RegexLabForm         | Campos de input para Regex y Texto de prueba          |
| Control  | PatternTester        | Ejecuta el test de coincidencia                       |
| Entity   | MatchResult          | Arreglo de coincidencias                              |

![Diagrama](./diagrams/diagram_9.png)

#### CU-09: Generar clave segura

| Tipo     | Objeto              | Responsabilidad                                      |
|----------|----------------------|------------------------------------------------------|
| Boundary | GeneratorForm        | Deslizadores de longitud y opciones                   |
| Control  | CryptoGenerator      | Crea secuencias aleatorias seguras                    |
| Entity   | SecureKey            | La cadena generada                                    |

![Diagrama](./diagrams/diagram_10.png)

#### CU-10: Guía de remediación

| Tipo     | Objeto              | Responsabilidad                                      |
|----------|----------------------|------------------------------------------------------|
| Boundary | RemediationModal     | Ventana emergente con la documentación                |
| Control  | ContentManager       | Selecciona guía acorde al lenguaje de programación    |
| Entity   | DocSnippet           | Fragmentos de Markdown o HTML                         |

![Diagrama](./diagrams/diagram_11.png)

#### CU-11: Instalar extensión

| Tipo     | Objeto              | Responsabilidad                                      |
|----------|----------------------|------------------------------------------------------|
| Boundary | VSCodeMarketplace    | Panel de extensiones del IDE                          |
| Control  | ExtensionActivator   | Registra comandos y verifica dependencias locales     |
| Entity   | ExtensionState       | Estado local habilitado/deshabilitado                 |

![Diagrama](./diagrams/diagram_12.png)

#### CU-12: Escanear archivo activo

| Tipo     | Objeto              | Responsabilidad                                      |
|----------|----------------------|------------------------------------------------------|
| Boundary | VSCodeEditor         | El archivo abierto actual                             |
| Control  | SaveEventHandler     | Lanza un proceso hijo CLI (`subprocess`)              |
| Entity   | JSONBuffer           | Recepción del reporte en STDOUT                       |

![Diagrama](./diagrams/diagram_13.png)

#### CU-13: Visualizar vulnerabilidad

| Tipo     | Objeto              | Responsabilidad                                      |
|----------|----------------------|------------------------------------------------------|
| Boundary | DiagnosticPanel      | Interfaz nativa de problemas de VSCode                |
| Control  | DiagnosticMapper     | Convierte JSONBuffer a rangos de texto (Squiggly)     |
| Entity   | VSCodeDiagnostic     | Objeto nativo de advertencia del IDE                  |

![Diagrama](./diagrams/diagram_14.png)

#### CU-14: Iniciar servidor MCP

| Tipo     | Objeto              | Responsabilidad                                      |
|----------|----------------------|------------------------------------------------------|
| Boundary | ClaudeConfig         | Archivo de configuración del cliente LLM              |
| Control  | FastMCPServer        | Escucha en canal Standard Input/Output                |
| Entity   | ToolRegistry         | Catálogo de herramientas expuestas (scan_directory)   |

![Diagrama](./diagrams/diagram_15.png)

#### CU-15: Ejecutar scan_directory

| Tipo     | Objeto              | Responsabilidad                                      |
|----------|----------------------|------------------------------------------------------|
| Boundary | LLMPrompt            | Mensaje del usuario solicitando auditoría             |
| Control  | FastMCPHandler       | Ejecuta el scanner core mediante la herramienta       |
| Entity   | ScannerResult        | Lista de vulnerabilidades halladas                    |

![Diagrama](./diagrams/diagram_16.png)

### 6.3.2 Diagrama de Actividades con objetos

Ejemplo del flujo de actividad integral para el caso de uso principal (Escaneo en Terminal):

![Diagrama](./diagrams/diagram_17.png)

### 6.3.3 Diagrama de secuencia

A continuación se presentan los diagramas de secuencia para cada uno de los 15 Casos de Uso del sistema.

#### CU-01: Escanear directorio local

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Desarrollador
    participant CLI as Terminal CLI
    participant Core as CoreScanner
    participant FS as FileSystem
    
    Dev->>CLI: Ejecuta 'secret_scanner --path src'
    activate CLI
    CLI->>Core: Inicia escaneo
    activate Core
    Core->>FS: Itera y lee archivos de texto
    FS-->>Core: Contenido de archivos
    Core->>Core: Aplica expresiones regulares
    Core-->>CLI: Resultados (ScannerResult)
    deactivate Core
    CLI-->>Dev: Muestra hallazgos en consola
    deactivate CLI
```

#### CU-02: Exportar reporte JSON

```mermaid
sequenceDiagram
    autonumber
    actor Sec as DevSecOps
    participant CLI as Terminal CLI
    participant Reporter as JSONReporter
    participant FS as FileSystem
    
    Sec->>CLI: Ejecuta con '--output json'
    activate CLI
    CLI->>Reporter: Generar reporte JSON
    activate Reporter
    Reporter->>Reporter: Censura valores de los secretos
    Reporter->>FS: Escribe 'report.json'
    FS-->>Reporter: Confirmación de guardado
    Reporter-->>CLI: Éxito
    deactivate Reporter
    CLI-->>Sec: Muestra mensaje de completado
    deactivate CLI
```

#### CU-03: Exportar reporte CSV

```mermaid
sequenceDiagram
    autonumber
    actor Sec as DevSecOps
    participant CLI as Terminal CLI
    participant Reporter as CSVReporter
    participant FS as FileSystem
    
    Sec->>CLI: Ejecuta con '--output csv'
    activate CLI
    CLI->>Reporter: Generar reporte tabular
    activate Reporter
    Reporter->>Reporter: Mapea entidades a filas
    Reporter->>FS: Escribe 'report.csv'
    FS-->>Reporter: Confirmación de guardado
    Reporter-->>CLI: Éxito
    deactivate Reporter
    CLI-->>Sec: Muestra mensaje de completado
    deactivate CLI
```

#### CU-04: Escanear repo GitHub

```mermaid
sequenceDiagram
    autonumber
    actor Sec as DevSecOps
    participant Web as Web UI
    participant API as FastAPI
    participant Git as Git Subsystem
    participant Core as CoreScanner
    
    Sec->>Web: Ingresa URL de GitHub
    activate Web
    Web->>API: POST /scan/github
    activate API
    API->>Git: git clone en /tmp
    Git-->>API: Clonado exitoso
    API->>Core: Inicia escaneo en /tmp
    Core-->>API: Hallazgos encontrados
    API->>Git: Limpia directorio /tmp
    API-->>Web: JSON de resultados
    deactivate API
    Web-->>Sec: Renderiza reporte visual
    deactivate Web
```

#### CU-05: Subir y escanear ZIP

```mermaid
sequenceDiagram
    autonumber
    actor QA as DevSecOps / QA
    participant Web as Web UI
    participant API as FastAPI
    participant Extractor as ExtractorController
    participant Core as CoreScanner
    
    QA->>Web: Sube archivo .zip
    activate Web
    Web->>API: POST /scan/zip (multipart/form-data)
    activate API
    API->>Extractor: Extrae .zip en /tmp
    Extractor-->>API: Extracción exitosa
    API->>Core: Inicia escaneo
    Core-->>API: Hallazgos encontrados
    API->>Extractor: Elimina archivos temporales
    API-->>Web: JSON de resultados
    deactivate API
    Web-->>QA: Renderiza reporte visual
    deactivate Web
```

#### CU-06: Escanear fragmento pegado

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Desarrollador
    participant Sandbox as Web Sandbox
    participant API as FastAPI
    participant Core as CoreScanner
    
    Dev->>Sandbox: Pega texto fuente
    activate Sandbox
    Sandbox->>API: POST /scan/text
    activate API
    API->>Core: scan_string(buffer)
    Core-->>API: Hallazgos (líneas y matches)
    API-->>Sandbox: Resultados
    deactivate API
    Sandbox-->>Dev: Subraya problemas en rojo
    deactivate Sandbox
```

#### CU-07: Evaluar entropía de token

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Desarrollador
    participant Web as Web UI
    participant API as FastAPI
    participant Math as MathController
    
    Dev->>Web: Ingresa token secreto
    activate Web
    Web->>API: GET /entropy?token=...
    activate API
    API->>Math: calculate_shannon(token)
    Math-->>API: {bits, tiempo_cracking}
    API-->>Web: Métricas de seguridad
    deactivate API
    Web-->>Dev: Muestra barra de fortaleza (Débil/Fuerte)
    deactivate Web
```

#### CU-08: Probar Regex personalizado

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Desarrollador
    participant RegexLab as Web Regex Lab
    participant API as FastAPI
    participant Tester as PatternTester
    
    Dev->>RegexLab: Ingresa patrón y texto
    activate RegexLab
    RegexLab->>API: POST /regex/test
    activate API
    API->>Tester: match(regex, text)
    Tester-->>API: Grupos capturados y tiempos
    API-->>RegexLab: MatchResult
    deactivate API
    RegexLab-->>Dev: Resalta coincidencias en la UI
    deactivate RegexLab
```

#### CU-09: Generar clave segura

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Desarrollador
    participant Web as GeneratorForm
    participant API as FastAPI
    participant Crypto as CryptoGenerator
    
    Dev->>Web: Ajusta longitud y caracteres
    activate Web
    Web->>API: GET /generate?len=32...
    activate API
    API->>Crypto: Genera cadena aleatoria
    Crypto-->>API: SecureKey (string)
    API-->>Web: Resultado
    deactivate API
    Web-->>Dev: Retorna clave y su entropía
    deactivate Web
```

#### CU-10: Guía de remediación

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Desarrollador
    participant Web as UI Modal
    participant API as FastAPI
    participant Docs as ContentManager
    
    Dev->>Web: Clic en botón "Ayuda"
    activate Web
    Web->>API: GET /docs/remediation?lang=python
    activate API
    API->>Docs: Fetch markdown snippet
    Docs-->>API: Fragmento de código seguro (.env)
    API-->>Web: HTML renderizado
    deactivate API
    Web-->>Dev: Muestra la guía paso a paso
    deactivate Web
```

#### CU-11: Instalar extensión

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Desarrollador
    participant VSCode as Editor IDE
    participant Ext as Extension Activator
    participant OS as Sistema Operativo
    
    Dev->>VSCode: Instala y habilita .vsix
    activate VSCode
    VSCode->>Ext: activate()
    activate Ext
    Ext->>OS: Verifica si 'secret-scanner-cl' existe en PATH
    OS-->>Ext: true (binario encontrado)
    Ext-->>VSCode: Extensión lista
    deactivate Ext
    VSCode-->>Dev: Habilita funcionalidades
    deactivate VSCode
```

#### CU-12: Escanear archivo activo

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Desarrollador
    participant VSCode as Editor IDE
    participant Ext as VSCode Extension
    participant CLI as CLI Subprocess
    
    Dev->>VSCode: Ctrl+S (Guardar)
    activate VSCode
    VSCode->>Ext: onDidSaveTextDocument(file)
    activate Ext
    Ext->>CLI: Ejecuta 'secret_scanner --path file --output json'
    activate CLI
    CLI-->>Ext: JSONBuffer en STDOUT
    deactivate CLI
    Ext-->>VSCode: Diagnósticos analizados
    deactivate Ext
    VSCode-->>Dev: Actualiza el estado visual
    deactivate VSCode
```

#### CU-13: Visualizar vulnerabilidad

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Desarrollador
    participant Ext as VSCode Extension
    participant IDE as Diagnostic API
    
    Ext->>Ext: Procesa el JSON de hallazgos
    activate Ext
    Ext->>IDE: Mapea {línea, mensaje} a VSCodeDiagnostic
    activate IDE
    IDE-->>Ext: Registra Squiggly line
    deactivate IDE
    deactivate Ext
    Dev->>IDE: Hover sobre el texto subrayado
    activate IDE
    IDE-->>Dev: Muestra Tooltip ("AWS Key detectada")
    deactivate IDE
```

#### CU-14: Iniciar servidor MCP

```mermaid
sequenceDiagram
    autonumber
    actor AI as Agente IA
    participant Claude as Claude Desktop
    participant MCP as FastMCP Server
    
    AI->>Claude: Inicializa la aplicación
    activate Claude
    Claude->>MCP: Lanza subproceso 'secret-scanner-mcp'
    activate MCP
    MCP->>MCP: Registra Tool 'scan_directory'
    MCP-->>Claude: Listo (Stdio Listening)
    deactivate MCP
    Claude-->>AI: Herramientas habilitadas en el contexto
    deactivate Claude
```

#### CU-15: Ejecutar scan_directory mediante IA

```mermaid
sequenceDiagram
    autonumber
    actor AI as Agente IA (Claude)
    participant Client as Cliente MCP (Stdio)
    participant Server as Servidor FastMCP
    participant Core as Scanner Core
    
    AI->>Client: "Analiza el directorio actual"
    activate Client
    Client->>Server: JSON-RPC call_tool("scan_directory")
    activate Server
    Server->>Core: scanner.scan_directory(".")
    activate Core
    Core-->>Server: [Lista de Secretos Hallados]
    deactivate Core
    Server-->>Client: Respuesta JSON-RPC
    deactivate Server
    Client-->>AI: Inyecta JSON en el contexto de IA
    deactivate Client
    AI->>AI: Analiza resultados
    AI-->>AI: "Te sugiero que borres la AWS Key..."
```

### 6.3.4 Diagrama de clases

![Diagrama](./diagrams/diagram_18.png)

# 7. Conclusiones

1. SecretScanner se posiciona como una herramienta versátil para resolver el problema de credenciales expuestas en múltiples frentes (Web, CLI, IDE y LLM).
2. El análisis minucioso de 15 casos de uso con sus respectivos diagramas BCE demuestra un diseño arquitectónico modular altamente desacoplado.

# 8. Recomendaciones

1. Adoptar un pipeline DevSecOps institucional obligando a que la ejecución del CLI de SecretScanner pase exitosamente antes de cada Merge Request.
2. Mantener actualizadas las expresiones regulares de `patterns.py` conforme los proveedores Cloud (como AWS o Azure) modifiquen sus formatos de tokens.

# 9. Bibliografia

1. OWASP Top 10 (2021). *A07:2021-Identification and Authentication Failures*.
2. Cuadros Quiroga, P. (2026). *Material de Cátedra: Seguridad Informática y Base de Datos II*. Universidad Privada de Tacna.

# 10. Webgrafia

1. FastAPI Framework Documentation. https://fastapi.tiangolo.com/
2. Model Context Protocol Specification. https://modelcontextprotocol.io/
3. PlantUML Use Case Diagrams. https://plantuml.com/use-case-diagram

# 11. Historias de Usuario, Criterios y Escenarios BDD

**Issue 1: Escaneo Multi-Patrón por Expresiones Regulares**
* **Historia de Usuario:** COMO Analista de Seguridad QUIERO que el analizador detecte tokens comunes (AWS, JWT, Slack, RSA) PARA evitar subir credenciales a producción.
* **Criterios de Aceptación:** Todas las 8 Regex definidas deben detectar correctamente coincidencias positivas sin generar altos falsos positivos.
* **Escenario de Prueba BDD:**
  * **DADO** que hay un archivo que contiene `AKIA_FAKE_KEY_FOR_DOCS`
  * **CUANDO** el analizador procesa este archivo
  * **ENTONCES** debe identificar y marcar la cadena como vulnerabilidad de `AWS Access Key`.

**Issue 2: Exportación de Resultados Seguros**
* **Historia de Usuario:** COMO Administrador DevOps QUIERO exportar los hallazgos en CSV o JSON PARA integrarlos con otras herramientas.
* **Criterios de Aceptación:** El reporte exportado debe tener todas las credenciales censuradas a la mitad.
* **Escenario de Prueba BDD:**
  * **DADO** que el scanner halla un token de Slack: `xoxb-FAKE-TOKEN-FOR-DOCS`
  * **CUANDO** se genera el archivo `report.json`
  * **ENTONCES** el campo de valor del secreto debe registrarse como `xoxb-1234***`.

**Issue 3: Extensión VSCode Nativa**
* **Historia de Usuario:** COMO Desarrollador QUIERO ver los problemas de seguridad marcados directamente en mi editor PARA corregirlos al momento.
* **Criterios de Aceptación:** La extensión debe inyectar diagnósticos en la línea exacta.
* **Escenario de Prueba BDD:**
  * **DADO** que un usuario guarda un archivo con una clave quemada
  * **CUANDO** la extensión intercepta el evento de guardado
  * **ENTONCES** VSCode mostrará una alerta subrayada en amarillo indicando la exposición.
