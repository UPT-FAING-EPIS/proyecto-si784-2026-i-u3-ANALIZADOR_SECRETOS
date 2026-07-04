<center>

[comment]: <img src="./media/media/image1.png" style="width:1.088in;height:1.46256in" alt="escudo.png" />

![./media/media/image1.png](./media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERÍA**

**Escuela Profesional de Ingeniería de Sistemas**

**Proyecto *Analizador de Secretos — SecretScanner***

Curso: *Calidad y Pruebas de Software*

Docente: *Patrick Cuadros Quiroga*

Integrantes:

***Zapana Murillo, Kiara Holly (2023077087)***

***Choqueña Choque, Mauricio Arian (2023076799)***

**Tacna – Perú**

***2026***

</center>

---

Sistema *Analizador de Secretos (SecretScanner)*

Informe de Factibilidad

Versión *1.0*

| CONTROL DE VERSIONES |             |                        |                        |            |                  |
|:--------------------:|:------------|:-----------------------|:-----------------------|:-----------|:-----------------|
| Versión              | Hecha por   | Revisada por           | Aprobada por           | Fecha      | Motivo           |
| 1.0                  | KHZM / MACC | KHZM  | MACC  | 2026-03-29 | Versión Original |

---

# ÍNDICE GENERAL

1. [Descripción del Proyecto](#1-descripción-del-proyecto)
2. [Riesgos](#2-riesgos)
3. [Análisis de la Situación Actual](#3-análisis-de-la-situación-actual)
4. [Estudio de Factibilidad](#4-estudio-de-factibilidad)
   - 4.1 [Factibilidad Técnica](#41-factibilidad-técnica)
   - 4.2 [Factibilidad Económica](#42-factibilidad-económica)
   - 4.3 [Factibilidad Operativa](#43-factibilidad-operativa)
   - 4.4 [Factibilidad Legal](#44-factibilidad-legal)
   - 4.5 [Factibilidad Social](#45-factibilidad-social)
   - 4.6 [Factibilidad Ambiental](#46-factibilidad-ambiental)
5. [Análisis Financiero](#5-análisis-financiero)
6. [Conclusiones](#6-conclusiones)

---

# Informe de Factibilidad

## 1. Descripción del Proyecto

### 1.1. Nombre del proyecto

**Analizador de Secretos — SecretScanner**

### 1.2. Duración del proyecto

El proyecto tiene una duración estimada de **4 semanas (≈30 días)**, distribuidas
en cuatro fases: configuración del entorno, desarrollo del núcleo funcional,
pruebas y aseguramiento de calidad, e integración final con métricas y entrega.

| Fase | Días | Issues |
|------|------|--------|
| Fase 1 — Configuración del proyecto | Días 1–5 | #1, #2, #3, #4 |
| Fase 2 — Desarrollo del núcleo del analizador | Días 6–14 | #5, #6, #7, #8 |
| Fase 3 — Pruebas y aseguramiento de calidad | Días 15–22 | #9, #10, #11, #12 |
| Fase 4 — Integración final, métricas y entrega | Días 23–30 | #13, #14, #15 |

### 1.3. Descripción

SecretScanner es una herramienta de código abierto desarrollada en **Python 3.10+**,
organizada como un **monorepo**, cuyo propósito es detectar automáticamente
secretos y credenciales sensibles hardcodeadas en repositorios de código fuente.
La herramienta analiza archivos de texto en directorios usando expresiones regulares
(regex) para identificar patrones de secretos conocidos: GitHub Tokens, AWS Access
Keys, Claves API genéricas, Contraseñas hardcodeadas, JWT Tokens, Tokens de Slack,
Claves Privadas RSA y URLs con credenciales embebidas.

La importancia del proyecto radica en que la exposición accidental de secretos en
repositorios de código es una de las principales causas de brechas de seguridad en
organizaciones de software. Según estudios del sector, miles de secretos son
expuestos públicamente en GitHub cada día. SecretScanner cubre una necesidad real
en el flujo de trabajo del desarrollador al proveer una herramienta local, gratuita
y extensible que analiza el código antes de que llegue a un repositorio remoto,
generando reportes en consola, JSON y CSV.

El proyecto se desarrolla como trabajo de la asignatura **Calidad y Pruebas de
Software** en la Escuela Profesional de Ingeniería de Sistemas de la Universidad
Privada de Tacna.

### 1.4. Objetivos

#### 1.4.1. Objetivo general

Desarrollar una herramienta de análisis estático de código fuente que detecte
secretos y credenciales hardcodeadas en proyectos de software mediante expresiones
regulares, con capacidad de reporte en múltiples formatos (consola, JSON, CSV) y
distribución como interfaz de línea de comandos (CLI), logrando una cobertura de
pruebas mínima del 80%.

#### 1.4.2. Objetivos específicos

1. **Implementar un módulo de patrones regex (`patterns.py`)** que contenga al
menos 8 tipos de secretos documentados (GitHub Token, AWS Access Key, API Key
genérica, contraseña hardcodeada, JWT Token, Slack Token, clave privada RSA y URL
con credenciales), con el fin de cubrir los tipos de secretos más frecuentes en
repositorios públicos.

2. **Desarrollar un módulo de escaneo de archivos (`file_scanner.py`)** que recorra
directorios de forma recursiva con `os.walk()`, aplique los patrones regex sobre
cada archivo de texto, retorne hallazgos estructurados con campos `file`,
`line_number`, `secret_type` y `content`, e ignore extensiones y directorios no
relevantes (`.png`, `.jpg`, `.git/`, `__pycache__/`).

3. **Construir un módulo de reportes (`reporter.py`)** que presente los hallazgos
en consola con colores (colorama) diferenciando hallazgos críticos de advertencias,
y que exporte los resultados a archivos `.json` y `.csv` en la carpeta `output/`,
para facilitar la trazabilidad y el análisis posterior.

4. **Implementar una interfaz de línea de comandos (`main.py`)** basada en
`argparse` con los argumentos `--path`, `--output` y `--verbose`, de modo que
cualquier usuario pueda ejecutar la herramienta sobre un directorio o archivo con
un único comando desde la terminal.

5. **Crear un conjunto de archivos de muestra (`tests/sample_files/`)** con
secretos falsos y no funcionales, y escribir pruebas unitarias y de integración con
`pytest` y `pytest-cov`, alcanzando una cobertura mínima del 80% en todos los
módulos del paquete `scanner/`.

6. **Calcular y documentar métricas de calidad del analizador** (Precisión, Recall,
Verdaderos Positivos, Falsos Positivos y Falsos Negativos) sobre el dataset de
prueba, registrando los resultados en un archivo `METRICS.md` para evidenciar la
efectividad de la herramienta.

---

## 2. Riesgos

| # | Riesgo | Probabilidad | Impacto | Mitigación |
|---|--------|:---:|:---:|-----------|
| R1 | **Falsos positivos excesivos:** los patrones regex pueden marcar como secretos textos que no lo son (comentarios educativos, ejemplos de documentación). | Alta | Medio | Diseño cuidadoso de los patrones con anclas y contexto; archivo de prueba `falsos_positivos.py` dedicado a validar el comportamiento. |
| R2 | **Falsos negativos por ofuscación:** secretos con codificación no estándar (base64, variables de entorno concatenadas) podrían no ser detectados. | Media | Alto | Documentar explícitamente en el README el alcance de detección; incluir métricas de Recall en METRICS.md para transparentar las limitaciones. |
| R3 | **Archivos binarios o encoding especial:** el escáner podría fallar al procesar archivos con encoding distinto a UTF-8 o archivos binarios. | Alta | Medio | Usar `errors="ignore"` al abrir archivos; implementar lista de extensiones a ignorar; prueba de integración específica para archivos binarios. |
| R4 | **Tiempo insuficiente para alcanzar 80% de cobertura:** la fase de pruebas podría quedar corta si el desarrollo del núcleo se extiende. | Media | Alto | Escribir pruebas en paralelo al desarrollo desde la Fase 2; monitorizar cobertura en cada PR con `pytest-cov`. |
| R5 | **Conflictos de merge en el monorepo:** trabajo simultáneo de dos personas sobre los mismos archivos puede generar conflictos en Git. | Media | Bajo | Protección de rama `main` con pull requests obligatorios y al menos 1 aprobación; separación clara de responsabilidades por módulo. |
| R6 | **Secretos reales expuestos accidentalmente en el repositorio:** existe la paradoja de que una herramienta anti-secretos filtre secretos propios. | Baja | Alto | `.gitignore` configurado para excluir `.env` y `output/`; revisión manual antes de cada push a `main`; Issue #15 incluye este check explícitamente. |
| R7 | **Dependencia de colorama en entornos CI/CD:** la librería de colores puede generar caracteres ANSI no deseados en entornos sin soporte de color. | Baja | Bajo | Detectar si la salida es un TTY antes de activar colorama; documentar la opción de desactivar colores. |

---

## 3. Análisis de la Situación Actual

### 3.1. Planteamiento del problema

El desarrollo de software moderno implica el uso constante de credenciales: tokens
de acceso a APIs, claves privadas, contraseñas de base de datos y tokens de
autenticación. Estos secretos deben mantenerse fuera del código fuente y de los
repositorios de control de versiones; sin embargo, por error humano, descuido o
falta de herramientas adecuadas, es frecuente que sean incluidos directamente en
archivos de código, configuración o scripts.

**El problema de los secretos hardcodeados.** Cuando un desarrollador incluye una
clave de API directamente en el código (`api_key = "sk-1234abcd..."`) o sube un
archivo `.env` con credenciales reales al repositorio, esas credenciales quedan
expuestas permanentemente en el historial de Git, incluso si el archivo es
eliminado posteriormente. Según el informe de GitGuardian de 2023, se detectaron
más de 10 millones de secretos expuestos en repositorios públicos de GitHub en un
solo año, con un tiempo medio de exposición de más de 300 días antes de ser
revocados.

**Herramientas existentes y sus limitaciones.** Soluciones como GitGuardian,
TruffleHog o detect-secrets abordan este problema, pero presentan barreras de
adopción: GitGuardian es un servicio SaaS con planes de pago para equipos privados;
TruffleHog requiere configuración avanzada e integración con el historial completo
de Git; detect-secrets necesita una fase de inicialización previa y no genera
reportes en múltiples formatos de forma nativa. Ninguna de estas herramientas
ofrece simultáneamente ejecución local sin dependencias externas, patrones
configurables con un diccionario Python claro, y exportación directa a JSON/CSV
para integración con otras herramientas del equipo.

**SecretScanner** busca cubrir este nicho: una herramienta minimalista, de código
abierto, escrita en Python sin dependencias complejas, que cualquier desarrollador
pueda instalar con `pip install -r requirements.txt` y ejecutar en segundos sobre
cualquier directorio de proyecto.

### 3.2. Consideraciones de hardware y software

**Hardware disponible para el desarrollo:**

| Recurso | Especificación mínima | Disponibilidad |
|---------|----------------------|----------------|
| Computadora de desarrollo | CPU 2 núcleos, 4 GB RAM, 20 GB almacenamiento | Disponible (equipo personal de cada integrante) |
| Servidor de CI/CD | GitHub Actions (runners gratuitos para repos públicos) | Disponible (plan gratuito de GitHub) |

**Software requerido:**

| Software | Versión | Propósito | Licencia |
|----------|---------|-----------|----------|
| Python | 3.10+ | Lenguaje de desarrollo y ejecución | PSF License (gratuita) |
| pytest | 7.x+ | Framework de pruebas unitarias e integración | MIT |
| pytest-cov | 4.x+ | Medición de cobertura de código | MIT |
| colorama | 0.4.x+ | Salida con colores en consola (multiplataforma) | BSD |
| Git | 2.x | Control de versiones | GPL v2 |
| GitHub (repositorio) | — | Gestión del proyecto, PRs y CI/CD | Gratuito (plan público) |
| VS Code / PyCharm CE | Última | IDE de desarrollo | MIT / Apache 2.0 |

**Estructura del monorepo:**

```

secret-scanner/
├── scanner/
│   ├── __init__.py
│   ├── patterns.py         \# Diccionario de patrones regex
│   ├── file_scanner.py     \# Lógica de escaneo de archivos
│   └── reporter.py         \# Generación de reportes
├── tests/
│   ├── __init__.py
│   ├── sample_files/       \# Archivos de prueba con secretos falsos
│   ├── test_patterns.py
│   └── test_file_scanner.py
├── output/                 \# Reportes generados (ignorado en .gitignore)
├── main.py                 \# CLI principal (argparse)
├── requirements.txt
├── requirements-dev.txt
├── METRICS.md
└── README.md

```

---

## 4. Estudio de Factibilidad

El estudio de factibilidad fue preparado para evaluar la viabilidad del proyecto
desde las dimensiones técnica, económica, operativa, legal, social y ambiental. Los
resultados determinan si el proyecto puede ejecutarse con los recursos disponibles
y si sus beneficios justifican la inversión en tiempo y esfuerzo.

### 4.1. Factibilidad Técnica

El proyecto es técnicamente factible. Todos los componentes tecnológicos requeridos
son de código abierto, ampliamente documentados y con soporte activo.

**Lenguaje y entorno.** Python 3.10+ es una elección natural para herramientas de
análisis de texto: su módulo estándar `re` provee soporte completo de expresiones
regulares, `os.walk()` permite recorrido recursivo de directorios, y `argparse`
facilita la construcción de CLIs sin dependencias externas. La curva de aprendizaje
es baja y los integrantes del equipo tienen experiencia previa con el lenguaje.

**Detección de patrones.** Las expresiones regulares son la tecnología estándar
para este tipo de detección. Los patrones objetivo (GitHub tokens, AWS keys, JWT,
etc.) tienen formatos públicamente documentados y son detectables con precisión
aceptable mediante regex. El módulo `patterns.py` centraliza todos los patrones
en un diccionario, facilitando su extensión y prueba independiente.

**Pruebas y cobertura.** `pytest` y `pytest-cov` son las herramientas de facto
para pruebas en Python. La arquitectura modular del proyecto (patrones, escáner,
reportes separados) facilita alcanzar el umbral del 80% de cobertura mediante
pruebas unitarias parametrizadas con `pytest.mark.parametrize` y pruebas de
integración sobre archivos de muestra controlados.

**CI/CD.** GitHub Actions provee runners gratuitos para repositorios públicos,
suficientes para ejecutar la suite de pruebas en cada PR. No se requiere
infraestructura adicional ni servidores propios.

**Evaluación:** No se requiere inversión en infraestructura adicional. El equipo
de cómputo disponible es suficiente para el desarrollo, las pruebas y la entrega.
**La factibilidad técnica es ALTA.**

### 4.2. Factibilidad Económica

El proyecto es de naturaleza académica y open-source. No contempla ingresos ni
retorno financiero directo; sin embargo, sí presenta costos reales de operación
(internet y energía eléctrica). Todo el software necesario es gratuito o de código
abierto, por lo que los costos se limitan a los servicios básicos durante el período
de desarrollo (1 mes).

#### 4.2.1. Costos Generales

No se registran gastos significativos en materiales físicos durante el desarrollo
del proyecto. El trabajo es íntegramente digital.

| Ítem | Costo (S/.) |
|------|:---:|
| Material de oficina (papel, impresión de entregas) | 10.00 |
| **Total Costos Generales** | **10.00** |

#### 4.2.2. Costos Operativos Durante el Desarrollo

| Ítem | Cantidad (meses) | Costo Mensual (S/.) | Costo Total (S/.) |
|------|:---:|:---:|:---:|
| Servicio de internet (parte proporcional del costo doméstico, por integrante) | 1 × 2 | 40.00 | 80.00 |
| Energía eléctrica (consumo del equipo de desarrollo, estimado, por integrante) | 1 × 2 | 15.00 | 30.00 |
| **Total Costos Operativos** | | | **110.00** |

#### 4.2.3. Costos del Ambiente

| Ítem | Costo (S/.) |
|------|:---:|
| GitHub (plan gratuito para repositorios públicos) | 0.00 |
| GitHub Actions (plan gratuito: 2000 min/mes para repos públicos) | 0.00 |
| Python 3.10+ (licencia gratuita PSF) | 0.00 |
| pytest / pytest-cov / colorama (librerías open-source) | 0.00 |
| VS Code / PyCharm Community Edition (gratuitos) | 0.00 |
| Gemini / Claude (planes gratuitos para apoyo académico) | 0.00 |
| **Total Costos del Ambiente** | **0.00** |

#### 4.2.4. Costos de Personal

El trabajo del equipo se realiza como parte de la formación académica en la
asignatura de Calidad y Pruebas de Software y no contempla remuneración económica.

#### 4.2.5. Costos Totales del Desarrollo del Sistema

| Categoría | Costo (S/.) |
|-----------|:---:|
| Costos Generales | 10.00 |
| Costos Operativos durante el desarrollo | 110.00 |
| Costos del Ambiente | 0.00 |
| Costos de Personal | 0.00 |
| **TOTAL** | **120.00** |

### 4.3. Factibilidad Operativa

**Beneficios para los usuarios finales.** SecretScanner está orientado a
desarrolladores individuales y equipos pequeños que deseen auditar su código antes
de hacer push a un repositorio remoto. La herramienta reduce a segundos una
revisión que manualmente podría tomar horas en proyectos medianos, y elimina la
dependencia de servicios SaaS externos o configuraciones complejas.

**Facilidad de uso.** La interfaz CLI con `argparse` hace que la herramienta sea
accesible para cualquier desarrollador con conocimientos básicos de terminal. Un
único comando (`python main.py --path ./mi_proyecto --output json`) es suficiente
para obtener un reporte completo, sin necesidad de configuración previa ni cuentas
en servicios externos.

**Capacidad de mantenimiento.** La arquitectura modular (patrones, escáner,
reportes y CLI en módulos separados) facilita la adición de nuevos tipos de
secretos sin modificar el núcleo del sistema. El archivo `patterns.py` actúa como
único punto de extensión para nuevos patrones.

**Lista de interesados:**

| Interesado | Rol | Interés |
|------------|-----|---------|
| Zapana Murillo, Kiara Holly | Desarrolladora y responsable del proyecto | Completar el proyecto académico y desarrollar una herramienta funcional |
| Choqueña Choque, Mauricio Arian | Desarrollador y responsable del proyecto | Completar el proyecto académico y desarrollar una herramienta funcional |
| Patrick Cuadros Quiroga | Evaluador académico (docente) | Verificar el cumplimiento de criterios de calidad, pruebas y documentación |
| Comunidad de desarrolladores Python | Usuarios potenciales | Disponer de una herramienta open-source ligera para detección de secretos |
| Equipos de desarrollo universitario | Usuarios potenciales | Integrar la herramienta en flujos de trabajo de proyectos académicos y de tesis |
| Universidad Privada de Tacna | Institución académica | Promover la producción de software de calidad como resultado de la formación universitaria |

**Evaluación:** El producto es operativamente viable. No requiere personal
adicional para su funcionamiento y su uso es inmediato tras la instalación.
**La factibilidad operativa es ALTA.**

### 4.4. Factibilidad Legal

**Licencias de software.** Todo el stack tecnológico del proyecto usa licencias
permisivas: Python bajo PSF License, pytest bajo MIT, colorama bajo BSD,
pytest-cov bajo MIT. No existe conflicto de licencias para la publicación del
proyecto bajo una licencia open-source (MIT o Apache 2.0).

**Protección de datos.** La herramienta opera exclusivamente de forma local sobre
los archivos del sistema analizado. No transmite ningún dato a servidores externos,
no requiere conexión a internet para su funcionamiento principal y no recopila ni
almacena información del usuario ni del código analizado más allá del reporte local
generado en `output/`.

**Propiedad intelectual.** El software constituye una contribución académica
original del equipo. Los patrones regex utilizados describen formatos públicamente
documentados por los proveedores de los servicios correspondientes (GitHub, AWS,
Slack, etc.) y no reproducen código de herramientas comerciales existentes.

**Uso ético.** La herramienta está diseñada para ser usada exclusivamente sobre
código propio o código para el que el usuario tiene autorización de análisis. El
README incluirá una nota explícita sobre uso responsable.

**Evaluación:** No existen impedimentos legales para el desarrollo, distribución
ni uso de la herramienta. **La factibilidad legal es ALTA.**

### 4.5. Factibilidad Social

El proyecto tiene un impacto social positivo directo en la cultura de seguridad del
desarrollo de software. Al ser una herramienta gratuita y de código abierto,
cualquier desarrollador puede adoptarla sin costo, reduciendo la probabilidad de
exposición accidental de credenciales que pueden comprometer sistemas de producción,
datos de usuarios o infraestructura cloud.

En el contexto local universitario, el proyecto sirve como ejemplo práctico de
aplicación de buenas prácticas de ingeniería de software (modularidad, pruebas
automatizadas, métricas de calidad, documentación técnica) que pueden ser
referenciadas por futuros estudiantes de la Escuela de Ingeniería de Sistemas de la
Universidad Privada de Tacna.

No se identifican impactos negativos de índole social, cultural o ético. La
herramienta no recopila datos personales, no facilita actividades maliciosas (su
propósito es defensivo, no ofensivo) y no genera discriminación de ningún tipo.

**Evaluación:** El proyecto tiene un impacto social positivo en la seguridad del
software y no presenta conflictos éticos. **La factibilidad social es ALTA.**

### 4.6. Factibilidad Ambiental

El proyecto es una herramienta de software puro, sin componentes físicos ni
procesos industriales asociados. Su impacto ambiental es mínimo:

- **Consumo energético:** el desarrollo se realiza en equipos de cómputo personales
  de uso doméstico. El consumo adicional atribuible al proyecto es marginal respecto
  al uso habitual de los equipos.
- **Infraestructura en la nube:** los servicios de CI/CD (GitHub Actions) utilizan
  infraestructura de Microsoft/GitHub que, según sus informes de sostenibilidad,
  opera con objetivos de neutralidad de carbono para 2030.
- **Distribución digital:** la herramienta se distribuye exclusivamente en formato
  digital (repositorio GitHub), sin componentes físicos que generen residuos
  electrónicos.
- **Sin dependencias de hardware especializado:** no requiere servidores propios,
  GPUs ni equipos de cómputo de alta demanda energética.

**Evaluación:** El impacto ambiental del proyecto es despreciable y no presenta
conflictos ambientales. **La factibilidad ambiental es ALTA.**

---

## 5. Análisis Financiero

### 5.1. Justificación de la Inversión

#### 5.1.1. Beneficios del Proyecto

Dado que SecretScanner es una herramienta open-source de uso libre, el retorno de
la inversión no se mide en ingresos económicos directos, sino en beneficios
tangibles e intangibles para sus usuarios y para la comunidad académica.

**Beneficios tangibles:**

| Beneficio | Estimación |
|-----------|-----------|
| Reducción del tiempo de revisión manual de secretos en un repositorio | De 2–4 horas a menos de 30 segundos por análisis |
| Eliminación del costo de herramientas SaaS equivalentes (GitGuardian, etc.) | Ahorro de USD 20–40/mes por desarrollador en planes equivalentes |
| Detección temprana de secretos antes del push: evita el costo de rotación de credenciales comprometidas | Rotación manual de credenciales: 2–8 horas por incidente |
| Exportación a JSON/CSV: integración directa con pipelines de auditoría | Eliminación del tiempo de reformateo manual de reportes |

**Beneficios intangibles:**

- Mejora de la cultura de seguridad en equipos de desarrollo que adopten la
  herramienta en su flujo de trabajo diario.
- Contribución de la Universidad Privada de Tacna al ecosistema open-source de
  seguridad en Python.
- Desarrollo de competencias avanzadas del equipo en testing, métricas de calidad,
  expresiones regulares y arquitectura modular de herramientas CLI.
- Material de referencia reutilizable para futuros proyectos académicos de la
  asignatura de Calidad y Pruebas de Software.

#### 5.1.2. Criterios de Inversión

Dado el carácter académico del proyecto, el análisis financiero se realiza desde la
perspectiva del **ahorro generado** para un equipo de desarrollo que adopte la
herramienta, comparado con alternativas de pago. Se considera como escenario de
referencia un equipo de 2 desarrolladores que actualmente no utilizan ninguna
herramienta de detección de secretos y deben rotar credenciales comprometidas al
menos una vez cada 3 meses.

**Parámetros del análisis:**

| Parámetro | Valor |
|-----------|-------|
| Inversión total del proyecto (costo de desarrollo) | S/. 120.00 |
| Ahorro mensual estimado (2 devs × S/. 130/mes en licencias SaaS equivalentes + tiempo ahorrado) | S/. 260.00 |
| Tasa de descuento mensual (COK referencial: 12% anual) | 1% mensual |
| Horizonte de evaluación | 24 meses |

##### 5.1.2.1. Relación Beneficio/Costo (B/C)

Los beneficios totales a 24 meses (ahorro acumulado) ascienden a
S/. 6,240.00 (S/. 260 × 24 meses).

```

B/C = Beneficios Totales / Costo Total de Inversión
B/C = 6,240.00 / 120.00
B/C = 52.00

```

Como el B/C = **52.00 > 1**, el proyecto **se acepta**. Por cada sol invertido
en el desarrollo, se generan S/. 52.00 en valor para los equipos que adoptan la
herramienta.

##### 5.1.2.2. Valor Actual Neto (VAN)

El VAN se calcula descontando el flujo de beneficios mensuales (S/. 260) a una
tasa mensual del 1%, durante 24 meses:

```

VAN = -120.00 + Σ [260 / (1 + 0.01)^t]  para t = 1..24
VAN = -120.00 + 260 × [(1 - (1.01)^-24) / 0.01]
VAN = -120.00 + 260 × 21.24
VAN = -120.00 + 5,522.40
VAN = S/. 5,402.40

```

Como el VAN = **S/. 5,402.40 > 0**, el proyecto **se acepta**.

##### 5.1.2.3. Tasa Interna de Retorno (TIR)

La TIR es la tasa a la que el VAN = 0:

```

0 = -120.00 + 260 × [(1 - (1 + TIR)^-24) / TIR]

```

Con una inversión inicial muy baja frente al flujo mensual de beneficios estimados,
la TIR resultante es extraordinariamente alta y pierde valor interpretativo
práctico. Por ello, para este caso se prioriza la evaluación con B/C y VAN, ambos
claramente favorables.

**Resumen del análisis financiero:**

| Indicador | Resultado | Decisión |
|-----------|:---------:|:--------:|
| Relación B/C | 52.00 | ✅ Aceptado |
| VAN | S/. 5,402.40 | ✅ Aceptado |
| TIR | No representativa por inversión mínima | Referencial |

---

## 6. Conclusiones

El análisis de factibilidad realizado sobre el proyecto
**Analizador de Secretos — SecretScanner** arroja resultados positivos en todas
las dimensiones evaluadas:

1. **Factibilidad Técnica:** El proyecto es técnicamente viable. Python 3.10+,
pytest, colorama y el módulo estándar `re` son tecnologías maduras, gratuitas y
ampliamente documentadas. La arquitectura modular del monorepo facilita el
desarrollo paralelo entre Kiara y Mauricio, y el mantenimiento futuro de la
herramienta. No se requiere inversión en infraestructura adicional.

2. **Factibilidad Económica:** El costo total del proyecto asciende a **S/. 120.00**,
correspondiente a costos operativos básicos (internet y energía eléctrica de ambos
integrantes durante el mes de desarrollo). No existe costo de personal remunerado
ni de licencias de software.

3. **Factibilidad Operativa:** La herramienta cubre una necesidad real y frecuente
en los equipos de desarrollo. Su interfaz CLI minimalista garantiza una curva de
adopción baja. La arquitectura modular facilita la extensión con nuevos patrones
sin modificar el núcleo del sistema.

4. **Factibilidad Legal:** No existen impedimentos legales. Todo el stack usa
licencias permisivas (MIT, BSD, PSF). La herramienta opera exclusivamente de forma
local y no transmite datos a servicios externos.

5. **Factibilidad Social y Ambiental:** El proyecto contribuye positivamente a la
cultura de seguridad en el desarrollo de software. El impacto ambiental es
despreciable al tratarse de software puro distribuido digitalmente.

6. **Análisis Financiero:** Los indicadores evaluados (B/C = 52.00 y
VAN = S/. 5,402.40) superan ampliamente los umbrales de aceptación, validando la
inversión desde una perspectiva de valor generado para los equipos que adopten la
herramienta.
