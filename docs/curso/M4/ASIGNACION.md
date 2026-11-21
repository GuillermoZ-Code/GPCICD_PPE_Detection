# Asignación del M4 — contrato de trabajo en paralelo

> **Qué es:** el reparto vigente de las 100 HU del M4. Es el contrato que cada
> agente lee antes de escribir código. Si una tarea no está aquí, no es tuya.
> **Fuente:** `docs/curso/M4/PLAN-M4-100-SPECS.md`, con la redistribución
> aprobada el 21/11/2026 (todo lo de GitLab pasa al Code Reviewer).
> **Cierre:** 26/11/2026. **Sustentación:** 28/11/2026.

## Reglas

1. **1 HU = 1 issue = 1 spec = 1 rama = 1 PR.** Nada de PR con dos HU.
2. **WIP 1:** reclama la HU en el tablero (*In progress*) antes del primer commit.
3. **Rutas:** el dueño de cada carpeta está en
   [`propiedad.toml`](../propiedad.toml). `make ownership-check` antes de cada push.
4. **Olas:** empieza por la Ola 1. La Ola 2 y 3 solo cuando la anterior esté
   fusionada o en revisión.
5. **Dependencias cruzadas:** si tu HU espera algo de otra persona, haz la parte
   que no depende y deja el AC pendiente para el final. Nunca esperes sentado.

## Resumen

| Persona | GitHub | HUs | SP | Pruebas | Foco |
|---|---|---:|---:|---:|---|
| Guillermo Zabala | `GuillermoZ-Code` | 24 | 50 | 192 | GitLab, despliegue, interfaz y gobierno técnico |
| Eliana Cardona | `ElianaCardona` | 26 | 50 | 192 | Servicio, MaaS, seguridad y operación |
| Hernán Estrada | `HestradaUAO` | 25 | 50 | 192 | Modelo, datos, evaluación y empaquetado |
| Jesús Riveros | `jesusriverosUAO` | 25 | 50 | 192 | Backlog, tablero, trazabilidad, MLflow y agentes |
| **Total** | | **100** | **200** | **768** | |

## Guillermo Zabala — GitLab, despliegue, interfaz y gobierno

| HU | Spec | Título | Épica | SP | Prio | Pruebas | Depende | Ola |
|---|---|---|---|---|---|---|---|---|
| HU-072 | 073 | SPA con API relativa detrás del proxy | ep-11 | 2 | P0 | 8 | — | 1 |
| HU-076 | 077 | Rediseño visual con `frontend-design` | ep-11 | 5 | P1 | 16 | HU-074 | 1 |
| HU-077 | 078 | Rediseño del flujo de carga y resultados | ep-11 | 2 | P1 | 8 | HU-076 | 1 |
| HU-081 | 082 | Estados de carga, error y reintento | ep-11 | 1 | P1 | 4 | — | 1 |
| HU-078 | 079 | Exportar resultados en CSV y JSON | ep-11 | 2 | P1 | 8 | — | 2 |
| HU-080 | 081 | Accesibilidad WCAG 2.2 AA | ep-11 | 2 | P1 | 8 | HU-076 | 2 |
| HU-088 | 089 | Historial de análisis de la sesión | ep-11 | 3 | P2 | 12 | HU-077 | 2 |
| HU-074 | 075 | Skills de GitLab y `frontend-design` | ep-12 | 1 | P0 | 4 | — | 2 |
| HU-085 | 086 | ADR de GitLab CI/CD, espejo y Droplet | ep-14 | 1 | P0 | 4 | — | 2 |
| HU-087 | 088 | Actualizar CONSTITUTION, AGENTS y README | ep-15 | 1 | P0 | 4 | — | 2 |
| HU-073 | 074 | MCP de GitLab y `glab` autenticado | ep-12 | 1 | P0 | 4 | HU-065 | 2 |
| **HU-065** | 066 | Proyecto GitLab y espejo GitHub → GitLab | ep-06 | 3 | P0 | 12 | — | 3 |
| **HU-066** | 067 | `.gitlab-ci.yml`: stages, cachés y reglas | ep-06 | 2 | P0 | 8 | HU-065 | 3 |
| **HU-067** | 068 | Job `build_image` con Docker-in-Docker | ep-06 | 3 | P0 | 12 | HU-066 | 3 |
| **HU-068** | 069 | Publicar imágenes en Registry y Docker Hub | ep-06 | 2 | P0 | 8 | HU-067 | 3 |
| **HU-069** | 070 | Aprovisionar el Droplet | ep-07 | 3 | P0 | 12 | — | 3 |
| **HU-070** | 071 | Job `deploy` por SSH con rollback | ep-06 | 5 | P0 | 16 | HU-068, HU-069 | 3 |
| **HU-071** | 072 | `compose.prod.yml` con healthchecks | ep-07 | 2 | P0 | 8 | HU-067 | 3 |
| **HU-042** | 043 | Variables CI enmascaradas y protegidas | ep-08 | 2 | P0 | 8 | HU-065 | 3 |
| **HU-043** | 044 | Escaneo de secretos con gitleaks | ep-08 | 1 | P0 | 4 | HU-014 | 3 |
| **HU-024** | 025 | Modelo en GitLab Generic Packages | ep-06 | 2 | P0 | 8 | HU-065 | 3 |
| **HU-046** | 047 | `HEALTHCHECK` en la imagen y compose | ep-13 | 1 | P0 | 4 | HU-045 | 3 |
| HU-014* | 015 | Pipeline CI/CD con compuertas | ep-05 | 2 | P0 | 8 | — | 3 |
| HU-015* | 016 | Comprobar el sistema desplegado | ep-05 | 1 | P0 | 4 | HU-070 | 3 |

> **Ruta crítica del proyecto.** Las HU en negrita son el 40 % (pipeline) y el
> 30 % (Droplet) de la rúbrica. HU-014 actúa como paraguas: se cierra cuando
> 066-068 y 070 estén fusionadas.

## Eliana Cardona — servicio, MaaS, seguridad y operación

| HU | Spec | Título | Épica | SP | Prio | Pruebas | Depende | Ola |
|---|---|---|---|---|---|---|---|---|
| HU-044 | 045 | Configuración por entorno validada al arrancar | ep-10 | 2 | P0 | 8 | — | 1 |
| HU-045 | 046 | Healthcheck de liveness y readiness | ep-13 | 2 | P0 | 8 | — | 1 |
| HU-047 | 048 | Logs estructurados JSON con `request_id` | ep-13 | 3 | P1 | 12 | — | 1 |
| HU-048 | 049 | Límites de tamaño y tipo en REST | ep-08 | 2 | P1 | 8 | — | 2 |
| HU-050 | 051 | Cliente de verificación remota REST y gRPC | ep-13 | 2 | P0 | 8 | HU-045 | 2 |
| HU-056 | 057 | Runbook de diagnóstico de fallos | ep-15 | 1 | P0 | 4 | — | 2 |
| HU-057 | 058 | Guion de la sustentación y checklist | ep-15 | 2 | P0 | 8 | — | 2 |
| HU-082 | 083 | CODEOWNERS y checks obligatorios | ep-14 | 1 | P1 | 4 | — | 2 |
| HU-083 | 084 | CI GitHub: Docker, smoke y Trivy | ep-08 | 2 | P1 | 8 | — | 2 |
| HU-084 | 085 | Optimizar la imagen Docker | ep-07 | 1 | P2 | 4 | — | 2 |
| HU-079 | 080 | Página 'Acerca del modelo' desde `/health` | ep-11 | 1 | P1 | 4 | HU-045 | 2 |
| HU-041 | 042 | Caddy con HTTPS automático | ep-07 | 3 | P0 | 12 | HU-071 | 3 |
| HU-049 | 050 | Exposición de gRPC | ep-07 | 1 | P1 | 4 | HU-041 | 3 |
| HU-051 | 052 | MaaS: clave de API opcional | ep-10 | 3 | P1 | 12 | HU-044 | 3 |
| HU-052 | 053 | MaaS: documentación pública de la API | ep-10 | 2 | P1 | 8 | HU-045 | 3 |
| HU-053 | 054 | MaaS: segunda URL pública | ep-10 | 5 | P1 | 16 | HU-026 | 3 |
| HU-054 | 055 | CORS de producción y rate limit | ep-08 | 1 | P1 | 4 | HU-041 | 3 |
| HU-060 | 061 | Cumplimiento AGPL y CC-BY en el despliegue | ep-08 | 1 | P1 | 4 | HU-045 | 3 |
| HU-086 | 087 | Diagrama de arquitectura de despliegue | ep-15 | 1 | P1 | 4 | HU-070 | 3 |
| HU-055 | 056 | Runbook de despliegue y rollback | ep-15 | 2 | P0 | 8 | HU-070 | 3 |
| HU-061 | 062 | README con badges y enlaces públicos | ep-15 | 1 | P0 | 4 | HU-065 | 3 |
| HU-062 | 063 | Paridad REST/gRPC con el modelo productivo | ep-10 | 3 | P1 | 12 | — | 3 |
| HU-063 | 064 | Prueba de carga ligera | ep-13 | 5 | P2 | 16 | HU-070 | 3 |
| HU-058 | 059 | Manual de usuario de la SPA | ep-15 | 1 | P2 | 4 | HU-077 | 3 |
| HU-059 | 060 | Catálogo de errores de API e interfaz | ep-15 | 1 | P2 | 4 | HU-048 | 3 |
| HU-064 | 065 | Notas de versión v1.0.0 y CHANGELOG | ep-15 | 1 | P2 | 4 | — | 3 |

## Hernán Estrada — modelo, datos y evaluación

| HU | Spec | Título | Épica | SP | Prio | Pruebas | Depende | Ola |
|---|---|---|---|---|---|---|---|---|
| HU-025 | 026 | Manifiesto canónico `models.lock` | ep-14 | 1 | P0 | 4 | — | 1 |
| HU-026 | 027 | Descarga y verificación del modelo por SHA256 | ep-06 | 2 | P0 | 8 | HU-025 | 1 |
| HU-033 | 034 | Pruebas de regresión de métricas | ep-09 | 2 | P1 | 8 | — | 1 |
| HU-034 | 035 | Contrato del detector con YOLO26 | ep-09 | 1 | P0 | 4 | HU-021 | 1 |
| HU-016 | 017 | Spike: YOLO26 en CPU | ep-09 | 2 | P0 | 8 | — | 2 |
| HU-035 | 036 | Preprocesamiento con contrato numérico | ep-09 | 2 | P2 | 8 | — | 2 |
| HU-036 | 037 | Postprocesamiento con umbrales por clase | ep-09 | 2 | P1 | 8 | HU-029 | 2 |
| HU-027 | 028 | Model Card v2 | ep-15 | 2 | P1 | 8 | HU-023 | 2 |
| HU-028 | 029 | Dataset Card y atribución CC-BY-4.0 | ep-15 | 1 | P1 | 4 | — | 2 |
| HU-075 | 076 | GGA: revisión con IA en pre-commit | ep-12 | 2 | P0 | 8 | — | 2 |
| HU-017 | 018 | Script de entrenamiento parametrizable | ep-09 | 3 | P0 | 12 | HU-016 | 3 |
| HU-018 | 019 | Entrenar YOLO26n y YOLO26s en GPU | ep-09 | 5 | P0 | 16 | HU-017 | 3 |
| HU-019 | 020 | Evaluación YOLO26 vs. YOLO11s | ep-09 | 3 | P0 | 12 | HU-018 | 3 |
| HU-020 | 021 | Benchmark de latencia por resolución | ep-09 | 3 | P1 | 12 | HU-018 | 3 |
| HU-021 | 022 | Adaptar el detector a YOLO26 | ep-09 | 3 | P0 | 12 | HU-016 | 3 |
| HU-022 | 023 | Exportación ONNX y backend opcional | ep-09 | 5 | P2 | 16 | HU-020 | 3 |
| HU-023 | 024 | ADR: modelo productivo | ep-09 | 1 | P0 | 4 | HU-019 | 3 |
| HU-029 | 030 | Calibración de umbrales por clase | ep-09 | 2 | P1 | 8 | HU-019 | 3 |
| HU-030 | 031 | Análisis de falsos positivos y negativos | ep-09 | 2 | P1 | 8 | HU-019 | 3 |
| HU-031 | 032 | Matriz de confusión y curvas PR | ep-14 | 1 | P1 | 4 | HU-019 | 3 |
| HU-032 | 033 | Robustez ante luz, ruido y escala | ep-09 | 1 | P2 | 4 | HU-019 | 3 |
| HU-037 | 038 | Evaluación por tamaño de objeto | ep-09 | 1 | P2 | 4 | HU-019 | 3 |
| HU-038 | 039 | Estadísticas de entrada para deriva | ep-13 | 1 | P2 | 4 | — | 3 |
| HU-039 | 040 | Inferencia por lotes desde CLI | ep-09 | 1 | P2 | 4 | — | 3 |
| HU-040 | 041 | Guía de reproducibilidad del entrenamiento | ep-15 | 1 | P1 | 4 | HU-018 | 3 |

## Jesús Riveros — backlog, tablero, trazabilidad y agentes

| HU | Spec | Título | Épica | SP | Prio | Pruebas | Depende | Ola |
|---|---|---|---|---|---|---|---|---|
| HU-091 | 092 | Plantilla de issue HU con AC y DoR/DoD | ep-14 | 1 | P0 | 4 | — | 1 |
| HU-094 | 095 | Conteo reproducible de pruebas | ep-14 | 2 | P0 | 8 | — | 1 |
| HU-095 | 096 | Corregir PRUEBAS.md y plan a 1.200 | ep-14 | 1 | P0 | 4 | — | 1 |
| HU-105 | 106 | Milestones y labels de las épicas | ep-14 | 1 | P0 | 4 | — | 1 |
| HU-107 | 108 | Definición de Ready y Done del M4 | ep-14 | 1 | P0 | 4 | — | 1 |
| HU-089 | 090 | Crear las 100 issues | ep-14 | 3 | P0 | 12 | HU-091 | 2 |
| HU-090 | 091 | Tablero con Fibonacci y olas | ep-14 | 2 | P0 | 8 | HU-089 | 2 |
| HU-092 | 093 | Sincronizar `backlog.md` con las 113 HU | ep-14 | 2 | P0 | 8 | HU-089 | 2 |
| HU-093 | 094 | Matriz de trazabilidad HU → issue → spec → PR | ep-14 | 5 | P0 | 16 | HU-089 | 2 |
| HU-096 | 097 | Validador de specs SDD | ep-14 | 3 | P1 | 12 | — | 2 |
| HU-101 | 102 | Engram: memoria de los agentes | ep-12 | 2 | P0 | 8 | — | 2 |
| HU-104 | 105 | Registro de riesgos del M4 | ep-14 | 1 | P1 | 4 | — | 2 |
| HU-097 | 098 | Runs de YOLO26 y YOLO11s en MLflow | ep-14 | 2 | P0 | 8 | HU-019 | 3 |
| HU-098 | 099 | Model Registry con champion/challenger | ep-14 | 2 | P1 | 8 | HU-097 | 3 |
| HU-099 | 100 | Informe comparativo de runs | ep-14 | 1 | P1 | 4 | HU-097 | 3 |
| HU-100 | 101 | Latencia del benchmark en MLflow | ep-14 | 1 | P2 | 4 | HU-020 | 3 |
| HU-102 | 103 | Protocolo de Engram y ADR | ep-12 | 2 | P1 | 8 | HU-101 | 3 |
| HU-103 | 104 | Informe de sprint y burndown | ep-14 | 2 | P1 | 8 | HU-090 | 3 |
| HU-106 | 107 | `make estado` con el pipeline de GitLab | ep-14 | 3 | P2 | 12 | HU-073 | 3 |
| HU-108 | 109 | Retrospectiva y lecciones | ep-15 | 1 | P2 | 4 | — | 3 |
| HU-109 | 110 | Capacidad y velocidad real | ep-14 | 1 | P2 | 4 | HU-103 | 3 |
| HU-110 | 111 | MLflow en el Droplet con autenticación | ep-14 | 5 | P2 | 16 | HU-071 | 3 |
| HU-111 | 112 | Release v1.0.0 `develop → main` | ep-15 | 2 | P0 | 8 | HU-070 | 3 |
| HU-112 | 113 | Glosario y mapa de documentación | ep-15 | 1 | P2 | 4 | — | 3 |
| HU-113 | 114 | Informe de cumplimiento de la rúbrica | ep-15 | 3 | P0 | 12 | — | 3 |

## Dependencias entre personas

Solo estas cruzan de dueño. Si tu HU está aquí, adelanta la parte que no depende.

| HU | Espera a | De |
|---|---|---|
| HU-041 | HU-071 `compose.prod.yml` | Guillermo |
| HU-046 | HU-045 healthcheck | Eliana |
| HU-053 | HU-026 fetch verificado | Hernán |
| HU-055, HU-063, HU-086, HU-111 | HU-070 deploy | Guillermo |
| HU-058 | HU-077 flujo rediseñado | Guillermo |
| HU-097, HU-100 | HU-019 / HU-020 evaluación | Hernán |
| HU-110 | HU-071 compose de producción | Guillermo |

## Estado de partida (21/11/2026)

- **HU-073** está operativa: MCP de GitLab conectado y `glab` autenticado.
- **HU-065** está a medias: existe el proyecto y un espejo *pull* roto
  (`Could not update main`); falta decidir push o pull y añadir el workflow.
- **Blindaje** ya en el repo: `propiedad.toml`, `make ownership-check`,
  `.github/CODEOWNERS`, job `Propiedad` y `.opencode/rules/propiedad.md`.
