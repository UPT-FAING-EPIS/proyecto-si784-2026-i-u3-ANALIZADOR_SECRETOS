# Propuesta de Proyecto — SecretScanner

## Control de Versiones

| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1.0 | Kiara Holly Zapana Murillo | Mauricio Arian Choqueña Choque | Mg. Patrick Cuadros Quiroga | 04/07/2026 | Versión Original |

---

## Resumen Ejecutivo

El presente documento detalla la propuesta técnica y económica para la implementación de **SecretScanner**, una suite integral y automatizada para la detección de secretos, credenciales hardcodeadas y claves de acceso expuestas en código fuente (vulnerabilidad **CWE-798**). Desarrollado originalmente como una herramienta CLI y servidor MCP de consola, se ha expandido para incluir una consola web multipropósito (FastAPI + JS) y contenedores Docker listos para el despliegue automático en la nube a través de Render Blueprints. 

Con una inversión inicial de desarrollo de **S/. 120.00 PEN** (correspondiente a consumos básicos de internet y electricidad) y un retorno financiero medido en ahorros operativos proyectados de **S/. 5,402.40 PEN (VAN)** y una relación Beneficio/Costo de **52.00**, **SecretScanner** ofrece una suite completa de ciberseguridad preventiva. El proyecto cuenta con **80 pruebas unitarias automatizadas** con una cobertura de código superior al **93%**, garantizando la máxima confiabilidad técnica tanto en entornos de desarrollo local como en flujos automatizados de CI/CD.


---

# I. Propuesta Narrativa

## 1. Planteamiento del Problema
En el desarrollo de software actual, el uso constante de APIs, bases de datos y tokens de autenticación es indispensable. El problema reside en que los desarrolladores suelen incrustar estas claves directamente en el código fuente de forma temporal para realizar pruebas y, debido a descuidos u omisiones en el archivo `.gitignore`, estas credenciales terminan guardadas en el historial inmutable de Git y subidas a repositorios públicos o compartidos. Esto da lugar al compromiso inmediato de infraestructuras en la nube, secuestro de recursos, filtración de datos de usuarios y sanciones por incumplimiento de normativas de seguridad de datos.

## 2. Justificación del Proyecto
**SecretScanner** aborda este problema de manera preventiva (*Shift-Left Security*), impidiendo la exposición del secreto antes de que este abandone el entorno local del desarrollador o bloqueando automáticamente las integraciones continuas. Adicionalmente, el proyecto destaca por operar con **cero dependencias complejas** (eliminando riesgos de cadena de suministro) y funcionar localmente (preservando la confidencialidad absoluta del código fuente del usuario, el cual nunca es transmitido a la nube).

## 3. Objetivo General
Desarrollar una suite integral de análisis estático de código fuente que detecte secretos y credenciales hardcodeadas mediante expresiones regulares, con capacidad de presentación multiplataforma (CLI, extensión de VSCode, MCP y aplicación web) y despliegue automatizado en contenedores en la nube, logrando una cobertura de pruebas mínima del 90%.


## 4. Beneficios
* **Ahorro de Tiempo de Auditoría**: Automatiza en segundos un escaneo recursivo que a un ingeniero de seguridad le tomaría horas de revisión manual.
* **Cero Costos de Licencia**: Distribución bajo licencia MIT libre de regalías.
* **Integración Versátil**: Ejecutable por desarrolladores humanos mediante CLI, por flujos automáticos en CI/CD y por agentes virtuales autónomos mediante el estándar MCP.
* **Enmascaramiento Nativo**: Garantiza la seguridad de los reportes generados reemplazando los caracteres centrales de las claves detectadas por asteriscos (`***`).

## 5. Alcance
* Escaneo recursivo local omitiendo carpetas del control de versiones y entornos de desarrollo.
* Detección de 8 patrones principales de secretos y credenciales de alta y mediana severidad.
* Exportación estructurada a JSON y CSV.
* Servidor MCP integrado para comunicación JSON-RPC con agentes inteligentes de IA.
* Consola web multipropósito (FastAPI + Vanilla JS glassmorphism UI) con herramientas avanzadas: escáner remoto de repositorios de GitHub, cargador de archivos ZIP, cálculo de entropía de Shannon, generador criptográfico seguro de claves, laboratorio regex interactivo y guías de remediación dinámica.
* Containerización Docker y automatización de despliegue PaaS mediante Render Blueprints.


## 6. Requerimientos del Sistema
El sistema requiere para su ejecución:
* Intérprete Python 3.10 o superior instalado en el host de ejecución.
* Framework web FastAPI y servidor web Uvicorn (con dependencias como `python-multipart`).
* Librería de salida visual `colorama` (CLI local).
* Engine de contenedores Docker (despliegue en contenedor y Docker Compose).
* Cuenta de hosting en la nube de Render (para despliegue automatizado del Blueprint).


## 7. Restricciones
* **Análisis No Semántico**: El motor se basa en patrones Regex compilados; no realiza interpretaciones semánticas avanzadas, por lo que nombres de variables coincidentes con las expresiones de búsqueda (como `password = "test"`) serán detectados.
* **Codificación**: Optimizado principalmente para analizar archivos de texto con codificación UTF-8 o compatibles.
* **Tamaño**: El análisis de repositorios de tamaño masivo (superior a 10 GB) de forma secuencial puede requerir segmentación.

## 8. Supuestos
* Los archivos analizados que contienen secretos están estructurados en formato de texto plano legible.
* Los desarrolladores disponen de acceso a terminal en sus estaciones de trabajo locales.
* El entorno de CI/CD posee soporte para ejecución de procesos Python básicos.

## 9. Resultados Esperados
* Detección y reporte exitoso de secretos válidos en el repositorio de test.
* Integración limpia de la suite de ciberseguridad a entornos locales y cloud.
* Cobertura de pruebas superior al 93% con un suite automatizada de 80 tests unitarios y de integración.


## 10. Metodología de Implementación
El proyecto se implementa empleando prácticas ágiles de desarrollo de software con ciclos de realimentación cortos:
1. **Fase de Planeación**: Definición y estimación de historias de usuario y diagramación de casos de uso iniciales.
2. **Fase de Diseño**: Modelado de diagramas estructurales y de comportamiento (clases, secuencia, actividad) descritos en el SAD.
3. **Fase de Codificación**: Desarrollo iterativo de módulos en Python siguiendo lineamientos de modularidad.
4. **Fase de Pruebas**: Programación de tests de validación automatizados de regresión en entornos de desarrollo local e integración continua de GitHub Actions.

## 11. Actores Claves

![Diagrama de Actores](./media/actores.png)


* **Mg. Patrick Cuadros Quiroga**: Evaluador académico y responsable de la dirección del curso de Calidad y Pruebas de Software.
* **Kiara Holly Zapana Murillo**: Desarrolladora principal, encargada del diseño de la lógica del escáner y la definición de patrones regex de secretos.
* **Mauricio Arian Choqueña Choque**: Ingeniero DevOps y QA, responsable de la suite de pruebas automatizadas y de la integración de CI/CD y MCP.

## 12. Papel y Responsabilidades del Personal
* **Kiara Zapana (Desarrollo y Patrones)**:
  * Diseñar y optimizar expresiones regulares en `patterns.py`.
  * Desarrollar lógica del motor de escaneo de archivos y filtros de exclusión en `file_scanner.py`.
  * Diseñar las interfaces de presentación y visualización de reportes.
* **Mauricio Choqueña (DevOps, QA y MCP)**:
  * Codificar la suite de pruebas de validación con `pytest`.
  * Configurar las tareas del pipeline en GitHub Actions.
  * Implementar el servidor MCP en `mcp_server.py`.
  * Documentar métricas de cobertura y rendimiento del sistema.

## 13. Plan de Monitoreo y Evaluación
El monitoreo del avance del proyecto se ejecuta mediante:
* **Métricas de Cobertura**: Ejecución semanal de `pytest-cov` garantizando el umbral del 80%.
* **Revisión de Issues en GitHub**: Registro, asignación y cierre de las 15 tareas (issues) del monorepo.
* **Pruebas de Integración Continua**: Ejecución automatizada de la suite de pruebas en la infraestructura de GitHub Actions ante cada *pull request* en la rama `main`.

## 14. Cronograma del Proyecto
El proyecto se completó en un período de 5 semanas según el siguiente desglose:

```
Semanas:      [Semana 1]      [Semana 2]      [Semana 3]      [Semana 4]      [Semana 5]
Fase 1:   ===========(Configuración)
Fase 2:               ===============(Desarrollo Core)
Fase 3:                               ===========(Pruebas y QA)
Fase 4:                                           ===========(Integración y MCP)
Fase 5:                                                       =================(Web & Cloud)
```

## 15. Hitos de Entregables
* **Hito 1 (Día 5)**: Configuración e inicialización del monorepo y entorno de pruebas básico.
* **Hito 2 (Día 14)**: Motor core del analizador estático completado e interfaz CLI funcional.
* **Hito 3 (Día 22)**: Suite de tests finalizada alcanzando el 80% de cobertura y reportes JSON/CSV estables.
* **Hito 4 (Día 30)**: Integración de servidor MCP completada y documentación de cierre generada.
* **Hito 5 (Día 35)**: Suite web FastAPI, containerización Docker, render.yaml y 80 tests pasando.


---

# II. Presupuesto

## 1. Planteamiento de Aplicación del Presupuesto
El presupuesto se aplica exclusivamente al financiamiento de los recursos operativos indispensables para el desarrollo y validación de la herramienta digital durante el mes de desarrollo, ya que el personal y el licenciamiento de software no suponen un desembolso financiero directo en el contexto académico del proyecto.

## 2. Presupuesto Detallado

| Descripción del Gasto | Categoría | Costo (S/.) |
|:---|:---|:---:|
| Materiales de oficina y papelería para entregas físicas | Costo General | 10.00 |
| Energía eléctrica de computadoras de desarrollo (2 personas) | Costo Operativo | 30.00 |
| Conexión a internet banda ancha (2 personas) | Costo Operativo | 80.00 |
| Licencias de software y frameworks de desarrollo | Costo del Ambiente | 0.00 |
| **TOTAL** | | **120.00** |

## 3. Análisis de Factibilidad
La factibilidad del proyecto es **Alta** en todas sus dimensiones (Técnica, Económica, Operativa, Social, Legal, Ambiental), al emplear un conjunto tecnológico estándar de fácil mantenimiento local y gratuito.

## 4. Evaluación Financiera
El análisis a un horizonte de 24 meses evidencia un **Valor Actual Neto (VAN) de S/. 5,402.40 PEN** (calculado con una tasa de descuento mensual de 1% y un flujo de ahorro mensual de S/. 260.00 PEN) y una relación **Beneficio/Costo de 52.00**, lo que cataloga el proyecto como sumamente rentable desde la perspectiva del valor y protección generados.

---

# Anexo 01 – Requerimientos del Sistema SecretScanner

A continuación se listan los requerimientos técnicos y funcionales detallados que componen la base del sistema **SecretScanner**:

```
[CLI CLIENT] <---> [CORE SCANNER] <---> [REGEX PATTERNS]
                         |
[WEB CLIENT] <---> [WEB APP (FASTAPI)]
                         |
                         +---> [REPORTER] (JSON / CSV)
                         |
[AGENT CLIENT] <--> [MCP SERVER]
```


### 1. Requerimientos del Motor de Escaneo
* El sistema debe realizar un escaneo en profundidad (recursivo) de la ruta de entrada provista.
* Debe ignorar de manera automática directorios que contengan dependencias pesadas o metadatos de Git (`.git`, `node_modules`, `venv`, `.venv`).
* Debe filtrar archivos binarios conocidos para omitir su lectura, validándolos por extensión (`.png`, `.exe`, `.zip`) o por la presencia de bytes nulos en los primeros 1024 bytes del archivo.
* Ante problemas de lectura o codificación corrupta en archivos de texto, debe sustituir los caracteres inválidos y continuar con el análisis sin abortar el flujo global.

### 2. Requerimientos de Detección (Patrones)
El motor de detección debe identificar con exactitud los siguientes patrones estructurados de secretos:
1. **GitHub Token**: Patrón regex que coincide con tokens que poseen los prefijos oficiales `ghp_`, `gho_`, `ghu_` o `ghs_` seguidos de al menos 36 caracteres alfanuméricos.
2. **AWS Access Key**: Identificación de cadenas alfanuméricas de 20 caracteres que inicien con el prefijo `AKIA`.
3. **Generic API Key**: Patrones que definan asignaciones de claves API en formato `api_key = "..."` de forma insensible a mayúsculas.
4. **Hardcoded Password**: Asignaciones directas del tipo `password = "..."` de al menos 4 caracteres de longitud.
5. **JWT Token**: Cadenas estructuradas en base64 de tres partes separadas por puntos que inicien con `eyJ`.
6. **Slack Token**: Tokens que inicien con el prefijo `xoxb-`, `xoxa-`, `xoxp-`, `xoxr-` o `xoxs-`.
7. **RSA Private Key**: Detección de bloques de cabecera de certificados que inicien con `-----BEGIN RSA PRIVATE KEY-----`.
8. **URL con Credenciales**: Cadenas de conexión de red que expongan usuario y contraseña embebidos en el formato `protocolo://usuario:contraseña@servidor`.

### 3. Requerimientos de Enmascaramiento y Salida
* El sistema debe enmascarar los secretos identificados mostrando únicamente los caracteres extremos (aproximadamente el 20% inicial y final) y reemplazando los caracteres intermedios por `***`.
* La salida de consola debe formatearse con colores diferenciadores de severidad utilizando estilos de terminal estándar.
* El sistema debe retornar un código de estado `1` cuando existan hallazgos para integrarse de forma nativa con herramientas de automatización de control de calidad.
