# Backlog — espejo de las issues

> **Qué es:** espejo **1:1** de las issues del repositorio para el documento del
> curso. La redacción literal de cada HU, sus AC y su conversación viven en la issue;
> este archivo resume título, SP, dueño, ola y spec.
> **Fuente oficial:** GitHub Issues y [`M4/ASIGNACION.md`](M4/ASIGNACION.md).
> Si hay una diferencia, **avisa al equipo antes de continuar**.
>
> **No cambiar títulos, AC ni SP sin aprobación de Jesús** (dueño del backlog).
>
> **Generado:** 2026-11-23 · 113 HU · 219 SP. HU-014 y HU-015 se cuentan en el
> M4 porque su trabajo se ejecuta en ese sprint.

## Resumen

| Sprint | Fechas | HUs | SP |
|--------|--------|----:|---:|
| M3-S1 | 31/10–07/11/2026 | 7 | 11 |
| M3-S2 | 08/11–14/11/2026 | 6 | 8 |
| M4-S3 | 15/11–28/11/2026 | 100 | 200 |
| **Total** | | **113** | **219** |

## Reparto del M4 por integrante

| Persona | GitHub | HU | SP | Pruebas |
|---------|--------|----:|---:|--------:|
| Guillermo Zabala | `GuillermoZ-Code` | 24 | 50 | 192 |
| Eliana Cardona | `ElianaCardona` | 26 | 50 | 192 |
| Hernán Estrada | `HestradaUAO` | 25 | 50 | 192 |
| Jesús Riveros | `jesusriverosUAO` | 25 | 50 | 192 |
| **Total** | | **100** | **200** | **768** |

## M3 — HUs 001 a 013

### M3-S1 — 31/10 a 07/11 (11 SP)

| HU | Issue | Título | SP | Spec | Estado |
|---|---|---|---:|---|---|
| HU-001 | [#1](../../issues/1) | Cargar una imagen para su análisis | 1 | [002-hu-001-carga-imagen](../../specs/002-hu-001-carga-imagen/) | cerrada |
| HU-002 | [#2](../../issues/2) | Detectar las seis categorías de EPP en una imagen | 3 | [003-hu-002-deteccion](../../specs/003-hu-002-deteccion/) | cerrada |
| HU-003 | [#3](../../issues/3) | Visualizar las detecciones sobre la imagen | 1 | [004-hu-003-visualizacion](../../specs/004-hu-003-visualizacion/) | cerrada |
| HU-004 | [#4](../../issues/4) | Informar cuando no se detectan elementos de protección personal | 1 | [006-hu-004-informe-sin-detecciones](../../specs/006-hu-004-informe-sin-detecciones/) | cerrada |
| HU-005 | [#5](../../issues/5) | Validar las imágenes recibidas | 1 | [007-hu-005-validacion-imagenes](../../specs/007-hu-005-validacion-imagenes/) | cerrada |
| HU-006 | [#6](../../issues/6) | Consultar inferencias mediante una API REST con FastAPI | 2 | [008-hu-006-api-rest](../../specs/008-hu-006-api-rest/) | cerrada |
| HU-007 | [#7](../../issues/7) | Utilizar el detector desde una interfaz gráfica | 2 | [005-hu-007-interfaz](../../specs/005-hu-007-interfaz/) | cerrada |

### M3-S2 — 08/11 a 14/11 (8 SP)

| HU | Issue | Título | SP | Spec | Estado |
|---|---|---|---:|---|---|
| HU-008 | [#8](../../issues/8) | Evaluar el desempeño del modelo de detección | 2 | [009-hu-008-evaluacion](../../specs/009-hu-008-evaluacion/) | cerrada |
| HU-009 | [#9](../../issues/9) | Consultar y comparar experimentos en MLflow | 1 | [012-hu-009-mlflow](../../specs/012-hu-009-mlflow/) | cerrada |
| HU-010 | [#10](../../issues/10) | Consumir inferencias mediante gRPC | 1 | [010-hu-010-consumo-grpc](../../specs/010-hu-010-consumo-grpc/) | cerrada |
| HU-011 | [#11](../../issues/11) | Ejecutar el sistema en un contenedor Docker CPU | 2 | [013-hu-011-docker-cpu](../../specs/013-hu-011-docker-cpu/) | cerrada |
| HU-012 | [#12](../../issues/12) | Ejecutar verificaciones automatizadas de calidad | 1 | [011-hu-012-calidad](../../specs/011-hu-012-calidad/) | cerrada |
| HU-013 | [#13](../../issues/13) | Consultar la versión del modelo utilizado | 1 | [014-hu-013-version-modelo](../../specs/014-hu-013-version-modelo/) | cerrada |

## M4 — HUs 014 a 113

El reparto, las dependencias y las olas son los de
[`M4/ASIGNACION.md`](M4/ASIGNACION.md). Las 100 HU tienen la misma milestone
(`M4-S3`) y se agrupan aquí por integrante.

### Guillermo Zabala (`GuillermoZ-Code`) — 24 HU · 50 SP · 192 pruebas

| HU | Issue | Título | Épica | SP | Prio | Ola | Spec | Estado |
|---|---|---|---|---:|---|---:|---|---|
| HU-072 | [#128](../../issues/128) | SPA con API relativa detrás del proxy | `ep-11` | 2 | P0 | 1 | 073 | abierta |
| HU-076 | [#132](../../issues/132) | Rediseño visual con `frontend-design` | `ep-11` | 5 | P1 | 1 | 077 | abierta |
| HU-077 | [#133](../../issues/133) | Rediseño del flujo de carga y resultados | `ep-11` | 2 | P1 | 1 | 078 | abierta |
| HU-081 | [#137](../../issues/137) | Estados de carga, error y reintento | `ep-11` | 1 | P1 | 1 | 082 | abierta |
| HU-078 | [#134](../../issues/134) | Exportar resultados en CSV y JSON | `ep-11` | 2 | P1 | 2 | 079 | abierta |
| HU-080 | [#136](../../issues/136) | Accesibilidad WCAG 2.2 AA | `ep-11` | 2 | P1 | 2 | 081 | abierta |
| HU-088 | [#144](../../issues/144) | Historial de análisis de la sesión | `ep-11` | 3 | P2 | 2 | 089 | abierta |
| HU-074 | [#130](../../issues/130) | Skills de GitLab y `frontend-design` | `ep-12` | 1 | P0 | 2 | 075 | abierta |
| HU-085 | [#141](../../issues/141) | ADR de GitLab CI/CD, espejo y Droplet | `ep-14` | 1 | P0 | 2 | 086 | abierta |
| HU-087 | [#143](../../issues/143) | Actualizar CONSTITUTION, AGENTS y README | `ep-15` | 1 | P0 | 2 | 088 | abierta |
| HU-073 | [#129](../../issues/129) | MCP de GitLab y `glab` autenticado | `ep-12` | 1 | P0 | 2 | 074 | abierta |
| HU-065 | [#121](../../issues/121) | Proyecto GitLab y espejo GitHub → GitLab | `ep-06` | 3 | P0 | 3 | 066 | abierta |
| HU-066 | [#122](../../issues/122) | `.gitlab-ci.yml`: stages, cachés y reglas | `ep-06` | 2 | P0 | 3 | 067 | abierta |
| HU-067 | [#123](../../issues/123) | Job `build_image` con Docker-in-Docker | `ep-06` | 3 | P0 | 3 | 068 | abierta |
| HU-068 | [#124](../../issues/124) | Publicar imágenes en Registry y Docker Hub | `ep-06` | 2 | P0 | 3 | 069 | abierta |
| HU-069 | [#125](../../issues/125) | Aprovisionar el Droplet | `ep-07` | 3 | P0 | 3 | 070 | abierta |
| HU-070 | [#126](../../issues/126) | Job `deploy` por SSH con rollback | `ep-06` | 5 | P0 | 3 | 071 | abierta |
| HU-071 | [#127](../../issues/127) | `compose.prod.yml` con healthchecks | `ep-07` | 2 | P0 | 3 | 072 | abierta |
| HU-042 | [#98](../../issues/98) | Variables CI enmascaradas y protegidas | `ep-08` | 2 | P0 | 3 | 043 | abierta |
| HU-043 | [#99](../../issues/99) | Escaneo de secretos con gitleaks | `ep-08` | 1 | P0 | 3 | 044 | abierta |
| HU-024 | [#80](../../issues/80) | Modelo en GitLab Generic Packages | `ep-06` | 2 | P0 | 3 | 025 | abierta |
| HU-046 | [#102](../../issues/102) | `HEALTHCHECK` en la imagen y compose | `ep-13` | 1 | P0 | 3 | 047 | abierta |
| HU-014 | [#14](../../issues/14) | Pipeline CI/CD con compuertas | `ep-05` | 2 | P0 | 3 | 015 | abierta |
| HU-015 | [#15](../../issues/15) | Comprobar el sistema desplegado | `ep-05` | 1 | P0 | 3 | 016 | abierta |

### Eliana Cardona (`ElianaCardona`) — 26 HU · 50 SP · 192 pruebas

| HU | Issue | Título | Épica | SP | Prio | Ola | Spec | Estado |
|---|---|---|---|---:|---|---:|---|---|
| HU-044 | [#100](../../issues/100) | Configuración por entorno validada al arrancar | `ep-10` | 2 | P0 | 1 | 045 | abierta |
| HU-045 | [#101](../../issues/101) | Healthcheck de liveness y readiness | `ep-13` | 2 | P0 | 1 | 046 | abierta |
| HU-047 | [#103](../../issues/103) | Logs estructurados JSON con `request_id` | `ep-13` | 3 | P1 | 1 | 048 | abierta |
| HU-048 | [#104](../../issues/104) | Límites de tamaño y tipo en REST | `ep-08` | 2 | P1 | 2 | 049 | abierta |
| HU-050 | [#106](../../issues/106) | Cliente de verificación remota REST y gRPC | `ep-13` | 2 | P0 | 2 | 051 | abierta |
| HU-056 | [#112](../../issues/112) | Runbook de diagnóstico de fallos | `ep-15` | 1 | P0 | 2 | 057 | abierta |
| HU-057 | [#113](../../issues/113) | Guion de la sustentación y checklist | `ep-15` | 2 | P0 | 2 | 058 | abierta |
| HU-082 | [#138](../../issues/138) | CODEOWNERS y checks obligatorios | `ep-14` | 1 | P1 | 2 | 083 | abierta |
| HU-083 | [#139](../../issues/139) | CI GitHub: Docker, smoke y Trivy | `ep-08` | 2 | P1 | 2 | 084 | abierta |
| HU-084 | [#140](../../issues/140) | Optimizar la imagen Docker | `ep-07` | 1 | P2 | 2 | 085 | abierta |
| HU-079 | [#135](../../issues/135) | Página 'Acerca del modelo' desde `/health` | `ep-11` | 1 | P1 | 2 | 080 | abierta |
| HU-041 | [#97](../../issues/97) | Caddy con HTTPS automático | `ep-07` | 3 | P0 | 3 | 042 | abierta |
| HU-049 | [#105](../../issues/105) | Exposición de gRPC | `ep-07` | 1 | P1 | 3 | 050 | abierta |
| HU-051 | [#107](../../issues/107) | MaaS: clave de API opcional | `ep-10` | 3 | P1 | 3 | 052 | abierta |
| HU-052 | [#108](../../issues/108) | MaaS: documentación pública de la API | `ep-10` | 2 | P1 | 3 | 053 | abierta |
| HU-053 | [#109](../../issues/109) | MaaS: segunda URL pública | `ep-10` | 5 | P1 | 3 | 054 | abierta |
| HU-054 | [#110](../../issues/110) | CORS de producción y rate limit | `ep-08` | 1 | P1 | 3 | 055 | abierta |
| HU-060 | [#116](../../issues/116) | Cumplimiento AGPL y CC-BY en el despliegue | `ep-08` | 1 | P1 | 3 | 061 | abierta |
| HU-086 | [#142](../../issues/142) | Diagrama de arquitectura de despliegue | `ep-15` | 1 | P1 | 3 | 087 | abierta |
| HU-055 | [#111](../../issues/111) | Runbook de despliegue y rollback | `ep-15` | 2 | P0 | 3 | 056 | abierta |
| HU-061 | [#117](../../issues/117) | README con badges y enlaces públicos | `ep-15` | 1 | P0 | 3 | 062 | abierta |
| HU-062 | [#118](../../issues/118) | Paridad REST/gRPC con el modelo productivo | `ep-10` | 3 | P1 | 3 | 063 | abierta |
| HU-063 | [#119](../../issues/119) | Prueba de carga ligera | `ep-13` | 5 | P2 | 3 | 064 | abierta |
| HU-058 | [#114](../../issues/114) | Manual de usuario de la SPA | `ep-15` | 1 | P2 | 3 | 059 | abierta |
| HU-059 | [#115](../../issues/115) | Catálogo de errores de API e interfaz | `ep-15` | 1 | P2 | 3 | 060 | abierta |
| HU-064 | [#120](../../issues/120) | Notas de versión v1.0.0 y CHANGELOG | `ep-15` | 1 | P2 | 3 | 065 | abierta |

### Hernán Estrada (`HestradaUAO`) — 25 HU · 50 SP · 192 pruebas

| HU | Issue | Título | Épica | SP | Prio | Ola | Spec | Estado |
|---|---|---|---|---:|---|---:|---|---|
| HU-025 | [#81](../../issues/81) | Manifiesto canónico `models.lock` | `ep-14` | 1 | P0 | 1 | [026](../../specs/026-hu-025-models-lock/) | cerrada |
| HU-026 | [#82](../../issues/82) | Descarga y verificación del modelo por SHA256 | `ep-06` | 2 | P0 | 1 | [027](../../specs/027-hu-026-fetch-model/) | cerrada |
| HU-033 | [#89](../../issues/89) | Pruebas de regresión de métricas | `ep-09` | 2 | P1 | 1 | [034](../../specs/034-hu-033-regresion-metricas/) | cerrada |
| HU-034 | [#90](../../issues/90) | Contrato del detector con YOLO26 | `ep-09` | 1 | P0 | 1 | 035 | abierta |
| HU-016 | [#72](../../issues/72) | Spike: YOLO26 en CPU | `ep-09` | 2 | P0 | 2 | [017](../../specs/017-hu-016-spike-yolo26/) | cerrada |
| HU-035 | [#91](../../issues/91) | Preprocesamiento con contrato numérico | `ep-09` | 2 | P2 | 2 | 036 | abierta |
| HU-036 | [#92](../../issues/92) | Postprocesamiento con umbrales por clase | `ep-09` | 2 | P1 | 2 | 037 | abierta |
| HU-027 | [#83](../../issues/83) | Model Card v2 | `ep-15` | 2 | P1 | 2 | 028 | abierta |
| HU-028 | [#84](../../issues/84) | Dataset Card y atribución CC-BY-4.0 | `ep-15` | 1 | P1 | 2 | 029 | abierta |
| HU-075 | [#131](../../issues/131) | GGA: revisión con IA en pre-commit | `ep-12` | 2 | P0 | 2 | 076 | abierta |
| HU-017 | [#73](../../issues/73) | Script de entrenamiento parametrizable | `ep-09` | 3 | P0 | 3 | [018](../../specs/018-hu-017-train-yolo26/) | cerrada |
| HU-018 | [#74](../../issues/74) | Entrenar YOLO26n y YOLO26s en GPU | `ep-09` | 5 | P0 | 3 | [019](../../specs/019-hu-018-entrenar-yolo26/) | cerrada |
| HU-019 | [#75](../../issues/75) | Evaluación YOLO26 vs. YOLO11s | `ep-09` | 3 | P0 | 3 | [020](../../specs/020-hu-019-comparar-yolo26-yolo11/) | cerrada |
| HU-020 | [#76](../../issues/76) | Benchmark de latencia por resolución | `ep-09` | 3 | P1 | 3 | [021](../../specs/021-hu-020-benchmark-latencia/) | cerrada |
| HU-021 | [#77](../../issues/77) | Adaptar el detector a YOLO26 | `ep-09` | 3 | P0 | 3 | [022](../../specs/022-hu-021-detector-nms-free/) | cerrada |
| HU-022 | [#78](../../issues/78) | Exportación ONNX y backend opcional | `ep-09` | 5 | P2 | 3 | [023](../../specs/023-hu-022-export-onnx/) | abierta |
| HU-023 | [#79](../../issues/79) | ADR: modelo productivo | `ep-09` | 1 | P0 | 3 | [024](../../specs/024-hu-023-adr-modelo-productivo/) | cerrada |
| HU-029 | [#85](../../issues/85) | Calibración de umbrales por clase | `ep-09` | 2 | P1 | 3 | 030 | abierta |
| HU-030 | [#86](../../issues/86) | Análisis de falsos positivos y negativos | `ep-09` | 2 | P1 | 3 | 031 | abierta |
| HU-031 | [#87](../../issues/87) | Matriz de confusión y curvas PR | `ep-14` | 1 | P1 | 3 | 032 | abierta |
| HU-032 | [#88](../../issues/88) | Robustez ante luz, ruido y escala | `ep-09` | 1 | P2 | 3 | 033 | abierta |
| HU-037 | [#93](../../issues/93) | Evaluación por tamaño de objeto | `ep-09` | 1 | P2 | 3 | 038 | abierta |
| HU-038 | [#94](../../issues/94) | Estadísticas de entrada para deriva | `ep-13` | 1 | P2 | 3 | 039 | abierta |
| HU-039 | [#95](../../issues/95) | Inferencia por lotes desde CLI | `ep-09` | 1 | P2 | 3 | 040 | abierta |
| HU-040 | [#96](../../issues/96) | Guía de reproducibilidad del entrenamiento | `ep-15` | 1 | P1 | 3 | 041 | abierta |

### Jesús Riveros (`jesusriverosUAO`) — 25 HU · 50 SP · 192 pruebas

| HU | Issue | Título | Épica | SP | Prio | Ola | Spec | Estado |
|---|---|---|---|---:|---|---:|---|---|
| HU-091 | [#147](../../issues/147) | Plantilla de issue HU con AC y DoR/DoD | `ep-14` | 1 | P0 | 1 | [092](../../specs/092-hu-091-plantilla-hu/) | cerrada |
| HU-094 | [#150](../../issues/150) | Conteo reproducible de pruebas | `ep-14` | 2 | P0 | 1 | [095](../../specs/095-hu-094-conteo-pruebas/) | cerrada |
| HU-095 | [#151](../../issues/151) | Corregir PRUEBAS.md y plan a 1.200 | `ep-14` | 1 | P0 | 1 | [096](../../specs/096-hu-095-corregir-pruebas-md/) | cerrada |
| HU-105 | [#161](../../issues/161) | Milestones y labels de las épicas | `ep-14` | 1 | P0 | 1 | [106](../../specs/106-hu-105-milestones-labels/) | cerrada |
| HU-107 | [#163](../../issues/163) | Definición de Ready y Done del M4 | `ep-14` | 1 | P0 | 1 | [108](../../specs/108-hu-107-dor-dod/) | cerrada |
| HU-089 | [#145](../../issues/145) | Crear las 100 issues | `ep-14` | 3 | P0 | 2 | 090 | cerrada |
| HU-090 | [#146](../../issues/146) | Tablero con Fibonacci y olas | `ep-14` | 2 | P0 | 2 | 091 | abierta |
| HU-092 | [#148](../../issues/148) | Sincronizar `backlog.md` con las 113 HU | `ep-14` | 2 | P0 | 2 | [093](../../specs/093-hu-092-backlog-espejo/) | abierta |
| HU-093 | [#149](../../issues/149) | Matriz de trazabilidad HU → issue → spec → PR | `ep-14` | 5 | P0 | 2 | [094](../../specs/094-hu-093-matriz-trazabilidad/) | abierta |
| HU-096 | [#152](../../issues/152) | Validador de specs SDD | `ep-14` | 3 | P1 | 2 | [097](../../specs/097-hu-096-validador-specs/) | abierta |
| HU-101 | [#157](../../issues/157) | Engram: memoria de los agentes | `ep-12` | 2 | P0 | 2 | [102](../../specs/102-hu-101-engram/) | abierta |
| HU-104 | [#160](../../issues/160) | Registro de riesgos del M4 | `ep-14` | 1 | P1 | 2 | [105](../../specs/105-hu-104-riesgos/) | abierta |
| HU-097 | [#153](../../issues/153) | Runs de YOLO26 y YOLO11s en MLflow | `ep-14` | 2 | P0 | 3 | [098](../../specs/098-hu-097-runs-mlflow/) | abierta |
| HU-098 | [#154](../../issues/154) | Model Registry con champion/challenger | `ep-14` | 2 | P1 | 3 | 099 | abierta |
| HU-099 | [#155](../../issues/155) | Informe comparativo de runs | `ep-14` | 1 | P1 | 3 | [100](../../specs/100-hu-099-informe-runs/) | abierta |
| HU-100 | [#156](../../issues/156) | Latencia del benchmark en MLflow | `ep-14` | 1 | P2 | 3 | [101](../../specs/101-hu-100-latencia-mlflow/) | abierta |
| HU-102 | [#158](../../issues/158) | Protocolo de Engram y ADR | `ep-12` | 2 | P1 | 3 | [103](../../specs/103-hu-102-protocolo-engram/) | abierta |
| HU-103 | [#159](../../issues/159) | Informe de sprint y burndown | `ep-14` | 2 | P1 | 3 | 104 | abierta |
| HU-106 | [#162](../../issues/162) | `make estado` con el pipeline de GitLab | `ep-14` | 3 | P2 | 3 | 107 | abierta |
| HU-108 | [#164](../../issues/164) | Retrospectiva y lecciones | `ep-15` | 1 | P2 | 3 | [109](../../specs/109-hu-108-retrospectiva/) | abierta |
| HU-109 | [#165](../../issues/165) | Capacidad y velocidad real | `ep-14` | 1 | P2 | 3 | 110 | abierta |
| HU-110 | [#166](../../issues/166) | MLflow en el Droplet con autenticación | `ep-14` | 5 | P2 | 3 | 111 | abierta |
| HU-111 | [#167](../../issues/167) | Release v1.0.0 `develop → main` | `ep-15` | 2 | P0 | 3 | 112 | abierta |
| HU-112 | [#168](../../issues/168) | Glosario y mapa de documentación | `ep-15` | 1 | P2 | 3 | 113 | abierta |
| HU-113 | [#169](../../issues/169) | Informe de cumplimiento de la rúbrica | `ep-15` | 3 | P0 | 3 | [114](../../specs/114-hu-113-rubrica/) | abierta |

## Dependencias entre integrantes

| HU | Espera a | De |
|---|---|---|
| HU-041 | HU-071 `compose.prod.yml` | Guillermo |
| HU-046 | HU-045 healthcheck | Eliana |
| HU-053 | HU-026 fetch verificado | Hernán |
| HU-055, HU-063, HU-086, HU-111 | HU-070 deploy | Guillermo |
| HU-058 | HU-077 flujo rediseñado | Guillermo |
| HU-097, HU-100 | HU-019 / HU-020 evaluación | Hernán |
| HU-110 | HU-071 compose de producción | Guillermo |

## Decisiones de planificación

- **Reestimación del M3 (04/11/2026):** las 15 HU del M3 pasaron de 67 a 22 SP,
  alineadas con el documento del M2. El M3 cerró con 13 HU y 19 SP; HU-014 y HU-015
  (3 SP) se arrastraron al M4.
- **M4 (21/11/2026):** 100 HU nuevas y 200 SP, 50 por integrante, repartidas en tres
  olas. La reasignación del 21/11 pasó todo lo de GitLab al Code Reviewer.
- **TA/SPI:** TA-04, TA-11, SPI-01, TA-02, TA-09, SPI-02, TA-10 y TA-EDA quedaron
  absorbidas en las actividades de preparación P1–P4; no son issues.
- **Pruebas:** el conteo vigente y el plan hacia 1.200 viven en
  [`PRUEBAS.md`](PRUEBAS.md) y [`PLAN-PRUEBAS.md`](PLAN-PRUEBAS.md).
