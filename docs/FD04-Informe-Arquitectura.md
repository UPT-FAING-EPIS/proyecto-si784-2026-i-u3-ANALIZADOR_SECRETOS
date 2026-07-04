# Documento de Arquitectura de Software (SAD) — SecretScanner

## Control de Versiones

| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1.0 | Kiara Holly Zapana Murillo | Mauricio Arian Choqueña Choque | Mg. Patrick Cuadros Quiroga | 04/07/2026 | Versión Original |

---

## 1. Propósito (Modelo 4+1 Vistas)

El propósito de este documento es describir la arquitectura del sistema **SecretScanner**, una herramienta especializada en el análisis estático de código para la detección de secretos, claves API y credenciales hardcodeadas. 

Para lograr una descripción clara y estructurada, se utiliza el **Modelo de 4+1 Vistas de Philippe Kruchten**, el cual permite capturar la arquitectura desde múltiples perspectivas alineadas a diferentes interesados:
* **Vista de Casos de Uso (Escenarios)**: Actúa como el elemento integrador (+1), relacionando los requerimientos funcionales con las decisiones de diseño mediante escenarios prácticos.
* **Vista Lógica**: Describe la estructura de diseño orientada a objetos, enfocándose en clases, subsistemas y flujos de colaboración internos.
* **Vista de Implementación (Desarrollo)**: Muestra la organización de los módulos físicos de software en el entorno de desarrollo (monorepo en Python).
* **Vista de Procesos**: Detalla el comportamiento dinámico y concurrente del sistema durante la ejecución del escaneo.
* **Vista de Despliegue (Física)**: Describe la topología física de ejecución, incluyendo el uso en terminal local, en pipelines CI/CD y mediante servidores MCP.

---

## 2. Alcance

El sistema **SecretScanner** está diseñado para ser integrado de tres formas distintas:
1. **Interfaz de Línea de Comandos (CLI)**: Ejecutada localmente por desarrolladores sobre carpetas de proyectos locales.
2. **Pipeline de Integración Continua (CI/CD)**: Integración en GitHub Actions para fallar de forma automática construcciones (builds) si se detectan secretos.
3. **Servidor Model Context Protocol (MCP)**: Expone herramientas de escaneo para que agentes de Inteligencia Artificial locales o remotos auditen el código y detecten secretos de manera autónoma.

El alcance de detección cubre **8 patrones de secretos definidos**, aplicados mediante expresiones regulares precompiladas sobre archivos de texto legibles, excluyendo archivos binarios o directorios del sistema de control de versiones y entornos virtuales.

---

## 3. Definición, Siglas y Abreviaturas

* **CLI**: *Command Line Interface* (Interfaz de Línea de Comandos).
* **SAD**: *Software Architecture Document* (Documento de Arquitectura de Software).
* **MCP**: *Model Context Protocol* (Protocolo de Contexto de Modelos). Protocolo para conectar modelos de lenguaje con herramientas locales.
* **Regex**: *Regular Expression* (Expresión Regular). Patrón que describe una secuencia de caracteres para su búsqueda.
* **Finding**: Hallazgo o coincidencia de secreto detectada por el sistema.
* **CI/CD**: *Continuous Integration / Continuous Delivery* (Integración y Despliegue Continuos).
* **Masking**: Enmascaramiento o censura de parte de un secreto expuesto para evitar doble exposición en los reportes generados.
* **UTF-8**: Formato de codificación de caracteres Unicode de ancho variable.

---

## 4. Organización del Documento

Este documento se estructura de la siguiente manera:
* **Secciones 1 a 6**: Detalle introductorio, alcance y especificaciones iniciales de requerimientos.
* **Sección 7 (Vista de Caso de Uso)**: Casos de uso e interacciones principales del sistema.
* **Sección 8 (Vista Lógica)**: Estructuras estáticas, interacciones dinámicas de diseño y esquema relacional de datos.
* **Sección 9 (Vista de Implementación)**: Estructura del monorepo y componentes del sistema.
* **Sección 10 (Vista de Procesos)**: Flujos dinámicos de ejecución y actividades internas del escaneo.
* **Sección 11 (Vista de Despliegue)**: Arquitectura física de hardware e infraestructura de red.
* **Secciones 12 a 18**: Escenarios detallados por atributos de calidad, limitaciones, fortalezas y roadmap técnico.

---

## 5. Requerimientos Funcionales

| ID | Requerimiento | Descripción |
|:---|:---|:---|
| **RF-001** | Escaneo Recursivo | Recorrer recursivamente directorios desde un path raíz especificado. |
| **RF-002** | Detección de Secretos | Identificar tokens de GitHub, AWS Access Keys, API Keys genéricas, contraseñas hardcodeadas, tokens JWT, tokens de Slack, claves privadas RSA y URLs con credenciales embebidas usando expresiones regulares. |
| **RF-003** | Exclusión de Binarios | Omitir automáticamente archivos no textuales (imágenes, PDFs, ejecutables, archivos compilados como `.pyc`). |
| **RF-004** | Ignorar Carpetas | No descender en directorios del sistema (`.git`) o entornos virtuales (`.venv`, `node_modules`). |
| **RF-005** | Enmascarar Salida | Ocultar los caracteres centrales de los secretos identificados para prevenir la fuga accidental en reportes. |
| **RF-006** | Consola en Colores | Mostrar en la terminal los hallazgos coloreados por nivel de severidad (HIGH en Rojo, MEDIUM en Amarillo). |
| **RF-007** | Exportar Reportes | Generar salidas estructuradas en formatos CSV y JSON en el directorio `output/`. |
| **RF-008** | Interfaz CLI | Ofrecer argumentos configurables (`--path`, `--output`, `--verbose`) a través de la terminal. |
| **RF-009** | Códigos de Retorno | Retornar código de salida `1` cuando se encuentren secretos y `0` cuando no, para soporte de CI/CD. |
| **RF-010** | Servidor MCP | Proveer soporte de servidor de contexto para herramientas externas. |

---

## 6. Requerimientos No Funcionales – Atributos de Calidad

* **Mantenibilidad (RNF-01)**: Código modular escrito en Python 3.10+ estructurado en paquetes independientes para patrones, escaneo y generación de reportes.
* **Rendimiento (RNF-02)**: Capacidad para procesar un volumen de más de 1000 archivos en menos de 5 segundos.
* **Confiabilidad (RNF-03)**: Manejo graceful de archivos inaccesibles o codificaciones corruptas, logrando además una cobertura de pruebas unitarias superior al 80%.
* **Usabilidad (RNF-04)**: Ofrecer mensajes claros en terminal y salida estructurada autoexplicativa.
* **Portabilidad (RNF-05)**: Compatibilidad multiplataforma garantizada en sistemas operativos Windows, Linux y macOS.

---

## 7. Vista de Caso de Uso

La Vista de Caso de Uso representa el comportamiento externo del sistema desde el punto de vista de sus actores principales: Desarrolladores, Administradores de Seguridad, Motores CI/CD y Agentes de IA.

### Diagrama de Casos de Uso

```mermaid
flowchart LR

    %% Actores
    Dev["👨‍💻 Desarrollador"]
    Sec["🛡️ Administrador de Seguridad"]
    CI["⚙️ Pipeline CI/CD"]
    AI["🤖 Agente de IA"]

    %% Límite del sistema
    subgraph Sistema["SecretScanner"]
        direction TB

        UC1(["UC-01<br/>Escanear Path Local"])
        UC2(["UC-02<br/>Exportar Reportes"])
        UC3(["UC-03<br/>Bloquear Integración Insegura"])
        UC4(["UC-04<br/>Analizar mediante MCP"])
    end

    %% Relaciones
    Dev --> UC1
    Dev --> UC2

    Sec --> UC1
    Sec --> UC2

    CI --> UC1
    CI --> UC3

    AI --> UC4

    UC4 -. «include» .-> UC1
```

### Descripción de Casos de Uso Principales

#### UC-01: Escanear Path Local
* **Actores**: Desarrollador / Administrador de Seguridad.
* **Propósito**: Ejecutar un análisis estático recursivo sobre una ruta de archivos local.
* **Precondición**: El usuario especifica un path válido mediante el parámetro `--path`.
* **Flujo Principal**:
  1. El usuario invoca la herramienta en la terminal indicando la ruta.
  2. El sistema lee recursivamente todos los archivos de texto que no están en la lista de exclusiones.
  3. El sistema aplica las expresiones regulares compiladas sobre cada línea.
  4. Los secretos detectados se enmascaran.
  5. Se muestran los hallazgos en la terminal en tiempo real y coloreados por nivel de severidad.
* **Postcondición**: Consola muestra la cantidad total de archivos escaneados y hallazgos identificados.

#### UC-02: Exportar Reportes
* **Actores**: Desarrollador / Administrador de Seguridad.
* **Propósito**: Guardar los hallazgos encontrados en un formato estructurado para auditoría.
* **Precondición**: Se especifica el parámetro `--output` con el valor `json` o `csv` y el análisis genera al menos un hallazgo.
* **Flujo Principal**:
  1. Se ejecuta el escaneo básico.
  2. Al detectar hallazgos, el sistema crea la carpeta `output/` si no existe.
  3. Se serializan los datos al archivo correspondiente (`report.json` o `report.csv`).
  4. Se escribe la ruta de guardado en el resumen final de consola.
* **Postcondición**: El archivo físico se escribe correctamente en disco con codificación UTF-8.

---

## 8. Vista Lógica

La **Vista Lógica** describe la organización estructural del sistema, mostrando los principales subsistemas (paquetes) y las dependencias entre ellos. Cada capa agrupa componentes con responsabilidades específicas, favoreciendo la separación de responsabilidades y la mantenibilidad del software.

### Diagrama de Subsistemas (Paquetes)

```mermaid
graph TD

    subgraph Presentacion["Capa de Presentación (CLI)"]
        main["main.py<br/>(Punto de entrada)"]
    end

    subgraph Core["Capa de Lógica de Negocio"]
        scanner["file_scanner.py<br/>(Motor de escaneo)"]
        patterns["patterns.py<br/>(Catálogo de patrones)"]
    end

    subgraph Persistencia["Capa de Reportes"]
        reporter["reporter.py<br/>(Generación y exportación de reportes)"]
    end

    subgraph Agente["Capa MCP"]
        mcp["mcp_server.py<br/>(Servidor FastMCP)"]
    end

    %% Dependencias
    main --> scanner
    main --> reporter

    scanner --> patterns

    mcp --> scanner
    mcp --> reporter
```

### Descripción de los subsistemas

- **Capa de Presentación (CLI):** Contiene el punto de entrada de la aplicación (`main.py`), encargado de recibir los parámetros del usuario e iniciar el proceso de análisis.

- **Capa de Lógica de Negocio:** Implementa el funcionamiento principal del sistema. El módulo `file_scanner.py` realiza el análisis de archivos fuente utilizando los patrones definidos en `patterns.py`.

- **Capa de Reportes:** Responsable de generar y exportar los resultados del análisis en diferentes formatos, como JSON, CSV o Markdown.

- **Capa MCP:** Expone las funcionalidades del sistema mediante un servidor FastMCP, permitiendo que clientes compatibles invoquen el escáner y obtengan reportes de forma programática.

### Diagrama de Secuencia (Vista de Diseño)

El siguiente diagrama ilustra el flujo dinámico de llamadas a funciones al escanear un directorio local y exportar los reportes:

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Desarrollador
    participant Main as main.py
    participant Scanner as file_scanner.py
    participant Patterns as patterns.py
    participant Reporter as reporter.py

    Dev->>Main: Ejecuta CLI (path, output="json")
    Main->>Scanner: scan_path(target_path, verbose)
    activate Scanner
    Scanner->>Scanner: _walk_directory(root)
    loop Para cada archivo encontrado
        Scanner->>Scanner: _is_text_file(filepath)
        alt Es archivo de texto válido
            Scanner->>Scanner: _scan_file(filepath, findings)
            activate Scanner
            loop Para cada línea y cada patrón en PATTERNS
                Scanner->>Patterns: Match regex
                Patterns-->>Scanner: Match detectado
                Scanner->>Scanner: _mask_secret(line)
                Scanner->>Scanner: Append a findings list
            end
            deactivate Scanner
        end
    end
    Scanner-->>Main: Retorna lista findings
    deactivate Scanner

    alt Hay findings y output == "json"
        Main->>Reporter: export_json(findings, "output/report.json")
        activate Reporter
        Reporter->>Reporter: _ensure_output_dir()
        Reporter-->>Main: Archivo guardado con éxito
        deactivate Reporter
    end

    Main-->>Dev: Imprime resumen y retorna código de salida
```

### Diagrama de Colaboración (Vista de Diseño)

El diagrama de colaboración destaca las relaciones estructurales entre los objetos de software que participan en el proceso de escaneo:

```mermaid
graph TD
    Main["1: Main Loop (main.py)"]
    Scanner["2: Path Scanner (file_scanner.py)"]
    Patterns["3: Patterns Database (patterns.py)"]
    Reporter["4: Data Exporter (reporter.py)"]

    Main -- "Llama a scan_path()" --> Scanner
    Scanner -- "Itera sobre regex en" --> Patterns
    Main -- "Llama a export_json()/export_csv()" --> Reporter
```

### Diagrama de Objetos

El siguiente diagrama de objetos representa una instantánea del estado del sistema durante la ejecución, mostrando un hallazgo (`Finding`) generado al detectar un token de GitHub en el archivo `config.py`. Asimismo, se ilustra la relación entre el hallazgo y el patrón (`Pattern`) utilizado para identificar la credencial.

```mermaid
graph LR

    subgraph Runtime["Instancias en tiempo de ejecución"]

        Finding["<b>f1 : Finding</b><br/><br/>
        Tipo: GitHub Token<br/>
        Severidad: HIGH<br/>
        Archivo: src/config.py<br/>
        Línea: 12<br/>
        Valor: ghp_abc123***xyz"]

    end

    subgraph Catalogo["Catálogo de Patrones"]

        Pattern["<b>p1 : Pattern</b><br/><br/>
        Nombre: GitHub Token<br/>
        Severidad: HIGH<br/>
        Expresión Regular"]

    end

    Finding -->|coincide con| Pattern
```

**Descripción de los objetos**

- **`f1 : Finding`** representa una instancia concreta de un hallazgo generado durante el proceso de escaneo. Contiene información como el tipo de secreto detectado, el nivel de severidad, la ubicación del archivo y la línea donde fue encontrado.

- **`p1 : Pattern`** representa el patrón de búsqueda utilizado por el motor de escaneo para identificar tokens de GitHub mediante una expresión regular.

- La relación **"instancia detectada mediante"** indica que el objeto `Finding` fue generado al coincidir el contenido del archivo con el patrón definido en `Pattern`.

### Diagrama de Clases

Las clases principales y sus relaciones de dependencia estructural en el monorepo son las siguientes:

```mermaid
classDiagram
    class Main {
        +main() int
        +_print_findings(findings: list) None
        +_print_summary(total: int, findings: list, path: str) None
        +_count_files(path: str) int
    }

    class FileScanner {
        +BINARY_EXTENSIONS: set~str~
        +IGNORED_DIRS: set~str~
        +scan_path(path: str, verbose: bool) List~Dict~
        +_walk_directory(root: Path) List~Path~
        +_scan_file(filepath: Path, findings: List) None
        +_is_text_file(filepath: Path) bool
        +_mask_secret(text: str) str
    }

    class Patterns {
        +PATTERNS: List~Dict~
    }

    class Reporter {
        +OUTPUT_DIR: str
        +export_json(findings: List, output_path: str) None
        +export_csv(findings: List, output_path: str) None
        +_ensure_output_dir(output_path: str) None
    }

    class MCPServer {
        +mcp: FastMCP
        +scan_secrets(target_path: str) str
        +main() None
    }

    Main ..> FileScanner : utiliza
    Main ..> Reporter : utiliza
    MCPServer ..> FileScanner : utiliza
    FileScanner ..> Patterns : lee
```

### Diagrama de Base de Datos (Relacional o No Relacional)

Aunque la Fase 1 del sistema **SecretScanner** opera sin base de datos persistente (orientada a archivos), una futura migración a base de datos relacional para soportar un panel multiusuario e histórico de auditoría requerirá el siguiente diseño lógico relacional:

```mermaid
erDiagram
    PROYECTO {
        int id PK
        string nombre
        string ruta_local
        datetime fecha_creacion
    }
    ESCANEADO {
        int id PK
        int proyecto_id FK
        datetime fecha_ejecucion
        int total_archivos
        int total_hallazgos
        string exit_code
    }
    HALLAZGO {
        int id PK
        int escaneado_id FK
        string tipo_secreto
        string severidad
        string ruta_archivo
        int numero_linea
        string contenido_enmascarado
    }
    PATRON_DETECCION {
        int id PK
        string nombre_patron
        string expresion_regular
        string severidad_defecto
        boolean activo
    }

    PROYECTO ||--o{ ESCANEADO : "registra"
    ESCANEADO ||--o{ HALLAZGO : "contiene"
    HALLAZGO }o--|| PATRON_DETECCION : "clasificado por"
```

---

## 9. Vista de Implementación (Vista de Desarrollo)

La Vista de Implementación organiza el código fuente físico del monorepo en subsistemas y componentes de desarrollo.

### Diagrama de Arquitectura de Software (Paquetes)

El siguiente diagrama detalla la estructura física del proyecto en disco y sus dependencias de importación:

```mermaid
graph TD
    subgraph Root ["secret-scanner (Monorepo)"]
        pyproject["pyproject.toml (Setuptools)"]
        reqs["requirements.txt"]
        
        subgraph Source ["src/secret_scanner/"]
            main_py["main.py (CLI)"]
            mcp_py["mcp_server.py (MCP)"]
            
            subgraph ScannerPkg ["scanner/"]
                init_scanner["__init__.py"]
                file_scanner_py["file_scanner.py"]
                patterns_py["patterns.py"]
                reporter_py["reporter.py"]
            end
        end

        subgraph Tests ["tests/"]
            test_patterns["test_patterns.py"]
            test_scanner["test_file_scanner.py"]
        end
    end

    main_py --> file_scanner_py
    main_py --> reporter_py
    mcp_py --> file_scanner_py
    file_scanner_py --> patterns_py
    test_patterns --> patterns_py
    test_scanner --> file_scanner_py
```

### Diagrama de Arquitectura del Sistema (Diagrama de Componentes)

El siguiente diagrama muestra los principales componentes lógicos del sistema y las dependencias entre ellos durante la ejecución.

```mermaid
graph LR

    CLI["Interfaz CLI"]
    MCP["Servidor MCP"]
    Controller["Controlador del Scanner"]
    Extractor["Extractor de Archivos"]
    Filter["Filtro de Exclusiones"]
    Regex["Motor de Expresiones Regulares"]
    Patterns["Base de Patrones"]
    Masker["Enmascarador de Datos"]
    Reporter["Generador de Reportes"]

    CLI --> Controller
    MCP --> Controller

    Controller --> Extractor
    Controller --> Filter
    Controller --> Regex
    Controller --> Masker
    Controller --> Reporter

    Regex --> Patterns
```

## 10. Vista de Procesos

La Vista de Procesos explica el comportamiento del flujo de control de un hilo del sistema al ejecutarse el escaneo.

### Diagrama de Procesos del Sistema (Diagrama de Actividad)

```mermaid
stateDiagram-v2
    [*] --> Iniciar_Proceso
    Iniciar_Proceso --> Parsear_Argumentos
    Parsear_Argumentos --> Validar_Ruta
    
    state Validar_Ruta <<choice>>
    Validar_Ruta --> Ruta_Invalida : Si no existe
    Validar_Ruta --> Listar_Archivos : Si existe

    Ruta_Invalida --> Imprimir_Error
    Imprimir_Error --> Finalizar_Con_Error

    state Listar_Archivos {
        [*] --> Recorrer_Directorios
        Recorrer_Directorios --> Filtrar_Directorios_Ignorados
        Filtrar_Directorios_Ignorados --> Retornar_Rutas
    }

    Listar_Archivos --> Analizar_Archivos

    state Analizar_Archivos {
        [*] --> Verificar_Tipo_Texto
        Verificar_Tipo_Texto --> Excluir_Binario : Si es binario
        Verificar_Tipo_Texto --> Leer_Lineas : Si es texto
        Leer_Lineas --> Buscar_Coincidencias_Regex
        Buscar_Coincidencias_Regex --> Enmascarar_Secretos : Si hay coincidencia
        Enmascarar_Secretos --> Guardar_Findings
    }

    Analizar_Archivos --> Exportar_Resultados

    state Exportar_Resultados <<choice>>
    Exportar_Resultados --> Generar_Reporte : Si se solicitó --output
    Exportar_Resultados --> Mostrar_Resultados_Consola : Si no

    Generar_Reporte --> Escribir_Disco
    Escribir_Disco --> Mostrar_Resultados_Consola

    Mostrar_Resultados_Consola --> Verificar_Exit_Code

    state Verificar_Exit_Code <<choice>>
    Verificar_Exit_Code --> Finalizar_Con_1 : Si hay findings
    Verificar_Exit_Code --> Finalizar_Con_0 : Si no hay findings

    Finalizar_Con_Error --> [*]
    Finalizar_Con_1 --> [*]
    Finalizar_Con_0 --> [*]
```

---

## 11. Vista de Despliegue (Vista Física)

La Vista de Despliegue muestra la asignación física de los módulos de software en los diferentes nodos y entornos de ejecución.

### Diagrama de Despliegue

```mermaid
graph TD
    subgraph Estacion_Desarrollo ["Entorno Local del Desarrollador (PC)"]
        direction TB
        cli_process["Proceso Python: secret-scanner CLI"]
        mcp_process["Proceso Python: secret-scanner-mcp"]
        disk_files["Almacenamiento Local (Código Fuente & output/ report.json/csv)"]
        cli_process -.->|Lectura / Escritura| disk_files
        mcp_process -.->|Lectura| disk_files
    end

    subgraph CI_CD ["Entorno de Integración Continua (GitHub Actions Runner)"]
        actions_runner["Contenedor Virtual de Ejecución (Ubuntu Runner)"]
        actions_script["GitHub Actions Workflow (python -m secret_scanner.main)"]
        git_workspace["Espacio de Trabajo Git Clonado"]
        actions_runner --> actions_script
        actions_script -.->|Escanea| git_workspace
    end

    subgraph Cliente_Externo ["Estación de IA del Agente"]
        agent_client["Cliente MCP (ej. Cursor IDE, Claude Desktop)"]
    end

    agent_client -->|Llamadas JSON-RPC sobre Stdio| mcp_process
```

---

## 12. Escenario de Funcionalidad

### Escenario 1: Detección Correcta de GitHub Token
* **Descripción**: El analizador detecta un token de GitHub activo en el código fuente.
* **Entrada**: Un archivo de configuración que contiene: `token = "ghp_abcdefghijklmnopqrstuvwxyz0123456789"`
* **Procesamiento**: El módulo `file_scanner` procesa la línea, la valida contra el patrón `(ghp_|gho_|ghu_|ghs_)[A-Za-z0-9_]{36,}` en `patterns.py`, la marca con severidad **HIGH** y enmascara el secreto a `ghp_abc***789`.
* **Salida**: Hallazgo registrado y mostrado en consola: `[HIGH] GitHub Token`.

### Escenario 2: Exclusión de Archivos Binarios
* **Descripción**: Se evita el análisis de un archivo de imagen en el repositorio para prevenir bloqueos o falsos positivos.
* **Entrada**: Archivo `docs/media/logo-upt.png`.
* **Procesamiento**: Al validar la ruta, el analizador verifica la extensión contra la lista `BINARY_EXTENSIONS` o lee los primeros 1024 bytes buscando bytes nulos (`\x00`). 
* **Salida**: El archivo se omite del análisis de forma segura y transparente.

### Escenario 3: Generación de Reportes en Múltiples Formatos
* **Descripción**: Exportación simultánea a archivos de análisis posterior.
* **Entrada**: `--path src --output json` con hallazgos detectados.
* **Procesamiento**: El sistema ejecuta el escaneo e invoca a `export_json()` en `reporter.py` para escribir en `output/report.json`.
* **Salida**: El archivo se escribe en disco en formato JSON indentado.

---

## 13. Escenario de Usabilidad

### Escenario 1: Interfaz CLI Intuitiva
* **Descripción**: Ayuda en terminal clara para usuarios novatos.
* **Entrada**: El usuario ejecuta `secret-scanner --help`.
* **Procesamiento**: El módulo `argparse` procesa la instrucción y autogenera el menú explicativo.
* **Salida**: Se despliega en consola las opciones `--path`, `--output` y `--verbose` de manera interactiva.

### Escenario 2: Mensajes de Error Claros
* **Descripción**: El usuario proporciona una ruta no existente para el escaneo.
* **Entrada**: `secret-scanner --path ./no_existe`.
* **Procesamiento**: El sistema valida la ruta física con `target.exists()`.
* **Salida**: Mensaje en terminal: `ERROR: Path not found: ./no_existe` con código de retorno `1`.

### Escenario 3: Salida Coloreada por Severidad
* **Descripción**: Visualización diferenciada según la gravedad de los hallazgos en terminal local.
* **Entrada**: Hallazgos de severidad `HIGH` y `MEDIUM` en el mismo análisis.
* **Procesamiento**: El módulo `main.py` lee la severidad de cada hallazgo y aplica colores utilizando la librería `colorama`.
* **Salida**: El token de GitHub se muestra en rojo brillante (`HIGH`) y la API key genérica se muestra en amarillo brillante (`MEDIUM`).

### Escenario 4: Modo Verbose para Debugging
* **Descripción**: Un desarrollador desea ver exactamente qué archivos se están procesando.
* **Entrada**: Ejecución del comando con la bandera `--verbose`.
* **Procesamiento**: En cada iteración del bucle de archivos, `file_scanner` imprime el path del archivo procesado si `verbose` está en `True`.
* **Salida**: Consola muestra la traza de archivos antes de listar los hallazgos.

---

## 14. Escenario de Confiabilidad

### Escenario 1: Manejo de Archivos Sin Permisos de Lectura
* **Descripción**: Un archivo del proyecto local está bloqueado por el sistema operativo.
* **Entrada**: Archivo `src/locked_config.py` con permisos de lectura revocados.
* **Procesamiento**: La instrucción `open()` lanza una excepción de tipo `PermissionError`. El bloque `try-except` en `_scan_file` captura el error `OSError` y ejecuta un `pass`.
* **Salida**: El analizador continúa escaneando los archivos restantes sin abortar la ejecución del proceso general.

### Escenario 2: Manejo de Encoding Inválido
* **Descripción**: Archivos guardados con formatos de codificación no Unicode.
* **Entrada**: Archivo con caracteres codificados en Windows-1252 o binarios corruptos.
* **Procesamiento**: El archivo se abre con la configuración `encoding="utf-8", errors="replace"`.
* **Salida**: Los caracteres inválidos se sustituyen por el carácter de reemplazo Unicode `` y el análisis de la expresión regular se completa correctamente.

### Escenario 3: Manejo de Directorios Muy Profundos
* **Descripción**: Análisis de estructuras anidadas de alta complejidad.
* **Entrada**: Un directorio de pruebas con más de 20 niveles de subcarpetas.
* **Procesamiento**: La función `os.walk()` recorre el árbol de directorios de manera iterativa sin generar desbordamiento de pila (*Stack Overflow*).
* **Salida**: Detección y listado correcto de hallazgos en la profundidad máxima.

### Escenario 4: Cobertura de Pruebas
* **Descripción**: Garantía de correcto funcionamiento ante refactorizaciones de código.
* **Entrada**: Comando `pytest --cov=secret_scanner.scanner`.
* **Procesamiento**: Ejecución de las pruebas unitarias y de integración sobre mockups y archivos de prueba controlados.
* **Salida**: Generación del reporte de cobertura mostrando un porcentaje superior al 80% del código central.

---

## 15. Escenario de Rendimiento

### Escenario 1: Escaneo de 1000 Archivos
* **Descripción**: Comportamiento ante repositorios medianos.
* **Entrada**: Un repositorio local que contiene 1000 archivos de código fuente.
* **Procesamiento**: Recorrido iterativo de los paths y precompilación de las expresiones regulares para evitar compilaciones redundantes en bucle.
* **Salida**: Análisis completado y reporte mostrado en menos de 5 segundos.

### Escenario 2: Uso de Memoria
* **Descripción**: Optimización de recursos de hardware en la máquina del desarrollador.
* **Entrada**: Un archivo de código de gran tamaño (por ejemplo, 100 MB).
* **Procesamiento**: En lugar de cargar todo el archivo a memoria con `read()`, el sistema utiliza un bucle iterativo de lectura línea por línea (`for line in fh`).
* **Salida**: El consumo de memoria RAM se mantiene constante e independiente del tamaño del archivo.

### Escenario 3: Latencia de Exportación
* **Descripción**: Impacto de la escritura de archivos en disco.
* **Entrada**: 500 hallazgos detectados para guardar en un reporte JSON.
* **Procesamiento**: Uso del módulo optimizado en C `json.dump()` en disco.
* **Salida**: Escritura completada en menos de 100 ms.

### Escenario 4: Escalabilidad Horizontal (Futuro)
* **Descripción**: Planificación para análisis de monorepos corporativos gigantes.
* **Entrada**: Repositorios de tamaño superior a 10 GB.
* **Procesamiento**: Migración de la lógica de procesamiento secuencial a hilos de ejecución paralelos mediante `concurrent.futures.ThreadPoolExecutor` o `ProcessPoolExecutor` para procesar archivos de manera simultánea en arquitecturas multi-core.

---

## 16. Escenario de Mantenibilidad

### Escenario 1: Adición de Nuevo Patrón de Detección
* **Descripción**: Se publica una nueva API y es necesario detectar sus credenciales.
* **Entrada**: Nueva expresión regular para tokens de servicio de OpenAI.
* **Procesamiento**: Se añade una nueva estructura de diccionario en la lista `PATTERNS` en `src/secret_scanner/scanner/patterns.py`.
* **Salida**: El sistema incorpora la detección de forma inmediata sin necesidad de alterar el motor de escaneo de archivos.

### Escenario 2: Refactorización de CLI
* **Descripción**: Modificación de argumentos de terminal.
* **Entrada**: Adición de una nueva bandera `--ignore-path`.
* **Procesamiento**: Modificación en el objeto `argparse` en `main.py` y pase del argumento a la función de escaneo.
* **Salida**: Incorporación del requerimiento sin modificar las librerías de reporte o patrones.

### Escenario 3: Migración a Base de Datos
* **Descripción**: Almacenamiento histórico para panel de administración.
* **Entrada**: Cambiar la escritura en archivos por base de datos SQLite local.
* **Procesamiento**: Reemplazar las funciones de `reporter.py` por llamadas a un adaptador de base de datos SQL sin alterar la lógica de escaneo.
* **Salida**: Hallazgos guardados en tablas relacionales persistentes.

### Escenario 4: Integración con Sistema Externo
* **Descripción**: Uso del escáner en herramientas de análisis empresariales.
* **Entrada**: Integración con un orquestador corporativo mediante API HTTP.
* **Procesamiento**: Exposición de los métodos a través de un servidor FastAPI o usando el servidor MCP implementado.
* **Salida**: Los hallazgos se retornan en formato JSON-RPC estructurado.

---

## 17. Otros Escenarios

### Escenario: Seguridad - Prevención de Exposición de Secretos en Reportes
* **Descripción**: Evitar la paradoja de exponer secretos en un reporte de seguridad.
* **Entrada**: Hallazgo de una clave de base de datos crítica.
* **Procesamiento**: Procesamiento de la cadena mediante la función `_mask_secret()` que reemplaza los caracteres centrales del token detectado.
* **Salida**: El reporte físico en disco solo almacena la firma parcial segura: `admin:123***890`.

### Escenario: Compatibilidad Multiplataforma
* **Descripción**: Ejecución de la misma herramienta por desarrolladores de Windows y Linux.
* **Entrada**: Rutas de archivos con delimitadores de sistema operativo (`\` vs `/`).
* **Procesamiento**: Uso exclusivo de la librería estándar `pathlib.Path` para normalizar las rutas de acceso en disco.
* **Salida**: Ejecución transparente sin fallos de ruta sin importar el sistema operativo.

### Escenario: Integración CI/CD - Exit Codes
* **Descripción**: Bloqueo automático de construcciones inseguras.
* **Entrada**: Ejecución en un contenedor de GitHub Actions sobre un pull request con secretos hardcodeados.
* **Procesamiento**: El proceso finaliza con código de retorno `1`.
* **Salida**: El runner de CI/CD detecta el retorno distinto de cero y marca la tarea como fallida, notificando al autor del commit.

---

## 18. Resumen de Atributos de Calidad

| Atributo de Calidad | Criterio de Aceptación | Método de Medición | Estado |
|:---|:---|:---|:---:|
| **Funcionalidad** | Detección de los 8 patrones objetivo sin falsos positivos en comentarios estándar. | Ejecución sobre repositorio de test `tests/sample_files/`. | ✅ Cumplido |
| **Usabilidad** | Ejecución simple con un comando y visualización formateada por severidades. | Validación con usuarios desarrolladores mediante CLI. | ✅ Cumplido |
| **Rendimiento** | Escaneo de 1000 archivos en menos de 5 segundos. | Medición de tiempo de ejecución de la suite de pruebas. | ✅ Cumplido |
| **Confiabilidad** | Tolerancia a fallos por permisos y encodings con cobertura de tests ≥ 80%. | Cobertura validada mediante `pytest-cov`. | ✅ Cumplido |
| **Mantenibilidad** | Arquitectura modular que permite agregar patrones en menos de 5 líneas de código. | Inspección de código y revisión de `patterns.py`. | ✅ Cumplido |

---

## 19. Fortalezas

1. **Arquitectura Altamente Desacoplada**: La separación estricta entre patrones, motor de escaneo de archivos, generador de reportes y clientes de interfaz (CLI/MCP) facilita actualizaciones seguras sin riesgos de regresión.
2. **Cero Dependencias Complejas**: Excluyendo la librería visual `colorama` y el conector `mcp` para integraciones de agentes de IA, el sistema utiliza únicamente la librería estándar de Python, minimizando vectores de ataque en la cadena de suministro.
3. **Mapeo Integrado para Agentes de IA (MCP)**: La inclusión de un servidor de contexto nativo posiciona a **SecretScanner** como una herramienta de vanguardia lista para interactuar directamente en ecosistemas modernos de desarrollo asistido por IA.

---

## 20. Limitaciones Conocidas

1. **Dependencia de Expresiones Regulares**: Al basarse en regex determinísticas, el analizador carece de capacidad de análisis semántico avanzado, lo que puede derivar en falsos positivos en variables simuladas de prueba o ejemplos educativos.
2. **Falta de Análisis de Historial Completo Git en Modo Local**: El CLI escanea el estado de los archivos físicos actuales, omitiendo secretos antiguos eliminados en commits históricos anteriores si no se implementa una integración directa con Git local.

---

## 21. Roadmap - Fase 2 (Futuro)

```mermaid
gantt
    title Plan de Ruta Técnica - SecretScanner Fase 2
    dateFormat  YYYY-MM-DD
    section Detección Avanzada
    Integración de GitPython (Historial completo Git) :active, 2026-08-01, 15d
    Análisis Semántico Avanzado por Machine Learning  : 2026-08-16, 20d
    section Persistencia y UI
    Migración a SQLite Local e Historial               : 2026-09-05, 10d
    Desarrollo de Panel Web de Gestión (React/FastAPI) : 2026-09-15, 25d
    section Integraciones
    Plugins IDE (VS Code & JetBrains)                  : 2026-10-10, 20d
```
