# Informe del Proyecto Final — SecretScanner

## Control de Versiones

| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1.0 | Kiara Holly Zapana Murillo | Mauricio Arian Choqueña Choque | Mg. Patrick Cuadros Quiroga | 04/07/2026 | Versión Original |

---

## 1. Antecedentes

El incremento exponencial en el desarrollo de software y la adopción de arquitecturas basadas en microservicios, APIs y servicios en la nube han traído consigo un reto crítico: la gestión de credenciales y secretos de acceso. Tradicionalmente, los sistemas se desarrollaban en entornos aislados donde las contraseñas e identificadores se configuraban de forma local. Sin embargo, en el ecosistema moderno de desarrollo distribuido (utilizando repositorios públicos y colaborativos como GitHub, GitLab o Bitbucket), el riesgo de filtrar credenciales por error humano es elevado.

En este contexto, la asignatura de **Calidad y Pruebas de Software** de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna ha propiciado el desarrollo del proyecto **SecretScanner** como una respuesta académica y técnica a este problema. A lo largo del ciclo de desarrollo, el equipo integrado por Kiara Zapana y Mauricio Choqueña diseñó e implementó un analizador estático capaz de auditar repositorios de manera local y en procesos de CI/CD para impedir la fuga de información sensible, validando su comportamiento con pruebas automáticas rigurosas.

---

## 2. Planteamiento del Problema

### a. Problema
El problema central abordado es la **exposición accidental de credenciales y secretos hardcodeados en el código fuente de los proyectos**. Este incidente, comúnmente provocado por descuidos en la configuración de archivos de entorno (`.env`) o por escribir contraseñas directamente en variables durante fases de prueba rápidas, deja un registro permanente en el historial de control de versiones. Debido a que el historial de Git es inmutable por diseño (y reescribirlo es complejo e interrumpe el flujo del equipo), un secreto que se sube una sola vez a un repositorio público o compartido queda expuesto a ataques de automatización (*scanners* maliciosos) en cuestión de segundos, comprometiendo bases de datos corporativas e infraestructuras en la nube.

### b. Justificación
La implementación de **SecretScanner** se justifica en los siguientes pilares:
* **Seguridad Preventiva (Shift-Left Security)**: Detectar los secretos en la máquina del desarrollador antes de que realice el envío de cambios (*push*) al servidor remoto.
* **Reducción del Costo de Remediación**: Modificar una credencial expuesta en producción requiere la rotación del secreto, actualización de dependencias, auditoría de logs de acceso y, potencialmente, gestión de incidentes legales. Realizar la detección a tiempo evita por completo este coste financiero y operativo.
* **Código Abierto y Privacidad**: A diferencia de plataformas comerciales de alto costo (como GitGuardian o TruffleHog Enterprise), **SecretScanner** es de código abierto y funciona al 100% de manera local, garantizando que el código de la organización nunca sea transmitido a servidores de terceros para su análisis.

### c. Alcance
El proyecto incluye:
* Un motor recursivo de escaneo en Python que filtra archivos binarios y directorios de sistema de forma automática.
* Detección activa de 8 patrones críticos de secretos mediante expresiones regulares.
* Visualización coloreada en consola basada en niveles de severidad y exportación estructurada en JSON y CSV.
* Un servidor Model Context Protocol (MCP) para la automatización e integración con agentes de Inteligencia Artificial locales y remotos.

Quedan fuera del alcance del proyecto actual la modificación directa o eliminación (redacción) de secretos detectados en los archivos originales y la limpieza automatizada del historial de Git.

---

## 3. Objetivos

### Objetivo General
Desarrollar una herramienta de análisis estático de código fuente que detecte secretos y credenciales hardcodeadas en proyectos de software mediante expresiones regulares, con capacidad de reporte en múltiples formatos (consola, JSON, CSV) y distribución como interfaz de línea de comandos (CLI), logrando una cobertura de pruebas mínima del 80%.

### Objetivos Específicos
1. **Módulo de Detección**: Diseñar y compilar 8 expresiones regulares optimizadas para identificar tokens de GitHub, AWS Access Keys, API Keys genéricas, contraseñas, JWT, tokens de Slack, claves privadas RSA y URLs con credenciales.
2. **Escáner Eficiente**: Implementar un motor en `file_scanner.py` que recorra estructuras de directorios de forma iterativa y descarte tipos de archivos no textuales.
3. **Reportes Robustos**: Codificar un formateador en terminal con soporte de colores para severidades y exportadores de disco estables.
4. **Control de Calidad**: Construir una suite de pruebas automatizadas parametrizadas con `pytest` y `pytest-cov` que garantice la estabilidad del sistema y supere la cobertura del 80%.
5. **Integración Moderna**: Proveer conectores de automatización (CLI e integración MCP) para facilitar la ejecución del sistema de manera transparente por usuarios humanos o agentes virtuales.

---

## 4. Marco Teórico

### Análisis Estático de Código
El análisis estático de código consiste en la inspección de programas informáticos sin ejecutar los mismos. Es una técnica fundamental de aseguramiento de calidad (QA) y seguridad de software (SAST - *Static Application Security Testing*). Permite identificar debilidades en fases tempranas del ciclo de vida del software.

### Expresiones Regulares (Regex)
Una expresión regular es un método de emparejamiento de patrones que describe un conjunto de cadenas de caracteres según reglas sintácticas específicas. En la detección de secretos, las expresiones regulares representan el estándar industrial para identificar tokens estructurados que poseen firmas predecibles (por ejemplo, el prefijo `ghp_` en tokens de GitHub).

### Vulnerabilidad CWE-798
La clasificación CWE (*Common Weakness Enumeration*) cataloga el "Uso de Credenciales Hardcodeadas" bajo el identificador **CWE-798**. Esta debilidad se define como la inclusión de datos confidenciales directamente en el código de la aplicación, facilitando a los atacantes el bypass de la autenticación del sistema.

---

## 5. Desarrollo de la Solución

### a. Análisis de Factibilidad

#### Factibilidad Técnica
**Alta**. El sistema se desarrolla en **Python 3.10+** utilizando la biblioteca estándar (`re`, `pathlib`, `json`, `csv`, `argparse`). Para las pruebas, se usan herramientas consolidadas del ecosistema como `pytest` y `pytest-cov`. La compatibilidad multiplataforma y la baja demanda de memoria están garantizadas por la arquitectura modular y la lectura secuencial de los archivos.

#### Factibilidad Económica
**Alta**. El costo del software del entorno es nulo debido al uso de herramientas y lenguajes bajo licencias permisivas de código abierto (MIT, BSD, PSF). Los costos operativos acumulados correspondientes a energía eléctrica y servicio de internet del equipo de desarrollo durante un mes de trabajo se calculan en **S/. 120.00 PEN**.

##### Evaluación Financiera (Ahorro Estimado a 24 Meses)
* **Inversión Inicial**: S/. 120.00
* **Flujo Mensual de Ahorro Estimado**: S/. 260.00 (equivalente a prescindir de licencias SaaS corporativas y tiempo ahorrado en auditorías y rotación de credenciales).
* **Tasa de Descuento (COK)**: 1% mensual (≈12% anual).
* **Valor Actual Neto (VAN)**: 
  $$\text{VAN} = -120.00 + \sum_{t=1}^{24} \frac{260.00}{(1 + 0.01)^t} = S/. 5,402.40\text{ PEN}$$
* **Relación Beneficio / Costo (B/C)**: 
  $$\text{B/C} = \frac{\text{Beneficios Totales Descontados}}{\text{Costo Inicial}} = \frac{6,240.00}{120.00} = 52.00$$
Dado que el $\text{VAN} > 0$ y la relación $\text{B/C} = 52.00 > 1$, la inversión del proyecto es financieramente excelente.

#### Factibilidad Operativa
**Alta**. La curva de aprendizaje del CLI es mínima gracias al menú de ayuda autogenerado. Su uso no requiere de infraestructura ni configuraciones previas de cuentas externas, y se integra de forma transparente en flujos DevSecOps mediante los códigos de retorno en terminal.

#### Factibilidad Social
**Alta**. Contribuye positivamente a la concientización sobre la seguridad del software en el ámbito estudiantil y profesional de Tacna, promoviendo el desarrollo de aplicaciones seguras.

#### Factibilidad Legal
**Alta**. El código desarrollado utiliza licencias libres y respeta los estándares internacionales de protección de datos, operando localmente sin transferir información sensible fuera del equipo local.

#### Factibilidad Ambiental
**Alta**. Al ser software puro distribuido digitalmente a través de Git, no genera residuos electrónicos ni consume recursos materiales significativos.

### b. Tecnología de Desarrollo
* **Lenguaje**: Python 3.10+
* **Framework de Pruebas**: pytest 8.x
* **Librería de Cobertura**: pytest-cov 5.x
* **Librería Gráfica de Consola**: colorama 0.4.6
* **Integración MCP**: FastMCP (SDK de Contexto de Modelos en Python)
* **Entornos**: Visual Studio Code, Git, GitHub Actions (CI)

### c. Metodología de Implementación
El desarrollo se estructuró siguiendo la metodología ágil XP (Programación Extrema), fundamentada en entregables correlativos:
1. **Documento de Visión (FD02)**: Definición del alcance inicial, posicionamiento del producto e identificación de interesados.
2. **Especificación de Requerimientos - SRS (FD03)**: Levantamiento de necesidades funcionales, no funcionales y reglas de negocio.
3. **Diseño de Arquitectura - SAD (FD04)**: Mapeo técnico detallado utilizando el modelo de vistas 4+1 e integración del diagrama de secuencia, clases y procesos.
4. **Implementación y Pruebas**: Programación modular en monorepo, desarrollo de suite de test y publicación en repositorio seguro.

---

## 6. Cronograma

La duración total del proyecto fue de **4 semanas (30 días)** estructurada en los siguientes hitos temporales:

| Hito | Fase | Duración | Fecha de Inicio | Fecha de Fin | Entregable Principal |
|:---:|:---|:---:|:---:|:---:|:---|
| **H1** | Configuración del Entorno | 5 días | 2026-03-01 | 2026-03-05 | Repositorio Git inicializado y CI configurado. |
| **H2** | Desarrollo del Núcleo Core | 9 días | 2026-03-06 | 2026-03-14 | Motores de escaneo, patrones regex y CLI. |
| **H3** | QA, Pruebas y Cobertura | 8 días | 2026-03-15 | 2026-03-22 | Suite de tests con pytest y cobertura del 80%. |
| **H4** | Servidor MCP e Integración | 8 días | 2026-03-23 | 2026-03-30 | Servidor MCP habilitado y documentación final. |

---

## 7. Presupuesto

| Categoría | Descripción del Recurso | Costo Unitario (S/.) | Cantidad | Costo Total (S/.) |
|:---|:---|:---:|:---:|:---:|
| **Generales** | Materiales de oficina e impresiones de control | 10.00 | 1 | 10.00 |
| **Operativos** | Servicio de internet doméstico (proporcional) | 40.00 | 2 personas | 80.00 |
| **Operativos** | Energía eléctrica consumida por PCs (estimado) | 15.00 | 2 personas | 30.00 |
| **Software** | Licencias de IDEs, Python, pytest y GitHub | Gratis | - | 0.00 |
| **Personal** | Desarrollo y control de QA (académico) | 0.00 | 2 personas | 0.00 |
| **TOTAL** | | | | **120.00** |

---

## 8. Conclusiones

1. Se cumplieron todos los requerimientos funcionales, logrando detectar de manera precisa los **8 patrones de secretos** requeridos por las especificaciones de seguridad.
2. La arquitectura modular adoptada en la especificación **SAD (FD04)** demostró su valor al permitir un desarrollo paralelo y sin conflictos en el repositorio entre los desarrolladores.
3. El sistema cuenta con una cobertura de pruebas unitarias superior al **80%**, asegurando la estabilidad del analizador estático ante futuras modificaciones del código fuente.
4. La integración innovadora con el protocolo **MCP** abre oportunidades clave para automatizar revisiones de seguridad en el ciclo DevSecOps mediante agentes autónomos de Inteligencia Artificial.

---

## Recomendaciones

1. **Integración con Hooks**: Configurar **SecretScanner** como un hook pre-commit de Git local para forzar automáticamente la auditoría de código antes de registrar cualquier cambio de manera física.
2. **Actualización de Patrones**: Auditar semestralmente el archivo `patterns.py` para adaptar los patrones de detección a nuevos formatos de proveedores de servicios cloud que surjan en el mercado.
3. **Escalabilidad Paralela**: Para grandes organizaciones con repositorios de tamaño extremo, implementar el motor concurrente sugerido en la Fase 2 para reducir los tiempos de escaneo en procesadores de múltiples núcleos.

---

## Bibliografía

* **OWASP Foundation (2023)**. *OWASP Top 10: The Ten Most Critical Web Application Security Risks*.
* **CWE Database (2024)**. *CWE-798: Use of Hard-Coded Credentials*. MITRE Corporation.
* **Kruchten, P. (1995)**. *Architectural Blueprints—The “4+1” View Model of Software Architecture*. IEEE Software, 12(6), 42-50.
* **Chacon, S., & Straub, B. (2014)**. *Pro Git*. Apress (2da Edición).

---

## Anexos

* **Anexo 01**: [FD01-Informe-Factibilidad.md](file:///c:/Users/HP/Desktop/asjee/proyecto-si784-2026-i-u3-ANALIZADOR_SECRETOS/docs/FD01-Informe-Factibilidad.md)
* **Anexo 02**: [FD02-Informe-Vision.md](file:///c:/Users/HP/Desktop/asjee/proyecto-si784-2026-i-u3-ANALIZADOR_SECRETOS/docs/FD02-Informe-Vision.md)
* **Anexo 03**: [FD-03-ESPECIFICACION-DISEÑO-SISTEMA.md](file:///c:/Users/HP/Desktop/asjee/proyecto-si784-2026-i-u3-ANALIZADOR_SECRETOS/docs/FD-03-ESPECIFICACION-DISE%C3%91O-SISTEMA.md)
* **Anexo 04**: [FD04-Informe-Arquitectura.md](file:///c:/Users/HP/Desktop/asjee/proyecto-si784-2026-i-u3-ANALIZADOR_SECRETOS/docs/FD04-Informe-Arquitectura.md)
* **Anexo 05**: [README.md](file:///c:/Users/HP/Desktop/asjee/proyecto-si784-2026-i-u3-ANALIZADOR_SECRETOS/README.md) y [MCP_SKILL_INTEGRATION.md](file:///c:/Users/HP/Desktop/asjee/proyecto-si784-2026-i-u3-ANALIZADOR_SECRETOS/MCP_SKILL_INTEGRATION.md)
