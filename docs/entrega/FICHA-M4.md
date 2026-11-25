# Ficha de entrega — Módulo 4 — Grupo 4

> Guion de 15 minutos para la sustentación M4 y checklist previo del entorno.
> **Fecha de corte:** 2026-11-24. Esta ficha no sustituye la ejecución en vivo: los
> resultados de detección se muestran con el artefacto versionado, sin afirmar
> cumplimiento normativo.

## 1. Datos rápidos

| Dato | Valor |
|---|---|
| Repositorio | <https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection> |
| Rama de entrega | `develop` |
| Tablero Kanban | <https://github.com/users/GuillermoZ-Code/projects/1> |
| Columnas | Backlog → Ready → In progress → In review → Done |
| API local | `uv run --extra inference python -m ppe_detection.api` (puerto 8000) |
| SPA local | `make frontend-dev` (puerto 5173) |
| Modelo | variable `$env:PPE_MODEL_PATH`; pesos fuera de Git, identificados por SHA256 |
| Runbook | [`docs/operacion/fallos.md`](../operacion/fallos.md) |
| Rúbrica | [`RUBRICA-M4.md`](./RUBRICA-M4.md) |

## Guion de la sustentación

Regla: hablar solo de evidencia que esté en `develop` o en la carpeta `docs/`; cuando
un ítem esté pendiente, decirlo explícitamente. Tiempo total: 15:00.

### 0:00–2:00 — Apertura y alcance

- **Responsable:** Eliana.
- **Mensaje:** presentamos el sistema de detección de seis clases de EPP en imágenes
  estáticas, sobre CPU, con API REST, gRPC y SPA; no certificamos cumplimiento ni
  detectamos personas.
- **Evidencia:** este documento, [`docs/README.md`](../README.md) y el tablero del
  proyecto.

### 2:00–5:00 — Arquitectura y contratos

- **Responsable:** Guillermo.
- **Mensaje:** el contrato `ImageData`/`Detection` separa ingesta, detector,
  postprocesamiento y API; Docker y `compose.yml` sirven el mismo artefacto en local
  y en despliegue.
- **Evidencia:** [`docs/architecture/arquitectura.html`](../architecture/arquitectura.html),
  [`docs/architecture/contracts.md`](../architecture/contracts.md) y `Dockerfile`.

### 5:00–8:00 — Modelo y evaluación

- **Responsable:** Hernán.
- **Mensaje:** se usa YOLO26n + ONNX 640; se reportan mAP@0.5, precisión y recall por
  clase, con umbrales y semilla registrados. Los pesos no se versionan.
- **Evidencia:** [`docs/evaluation/YOLO26.md`](../evaluation/YOLO26.md),
  [`docs/model-card.md`](../model-card.md) y `docs/adr/0009-modelo-productivo.md`.

### 8:00–11:00 — Demo de inferencia

- **Responsable:** Eliana.
- **Mensaje:** una imagen PNG sube por `POST /predict`; la respuesta enumera EPP con
  confianza y coordenadas. `GET /health` confirma que el modelo cargó.
- **Evidencia:** [`docs/operacion/demo-local.md`](../operacion/demo-local.md),
  `src/ppe_detection/api/app.py` y `tests/test_docs_runbook_fallos.py` como apoyo del
  escenario de fallo. Sin red: `FakeDetector` en pruebas.

### 11:00–13:30 — Calidad, CI/CD y operación

- **Responsable:** Guillermo, con Hernán para la compuerta de métricas.
- **Mensaje:** las PRs pasan Ruff, formato, `ty`, pytest, propiedad y Spec Kit; el
  pipeline y el contenedor se verifican con CI/CD. El runbook organiza el diagnóstico
  de fallos del despliegue.
- **Evidencia:** `.github/workflows/ci.yml`, `docs/curso/TRAZABILIDAD.md` y el runbook
  de fallos. Se muestra un `glab ci status` y un `docker logs` de ejemplo.

### 13:30–15:00 — Cierre: trazabilidad, riesgos y retro

- **Responsable:** Jesús, con Eliana para el cierre.
- **Mensaje:** cada HU enlaza issue, spec, PR y pruebas; quedan registrados los riesgos
  y las acciones de la retrospectiva. Si un ítem de la rúbrica está pendiente, se dice
  en voz alta y se indica la HU que lo completa.
- **Evidencia:** [`docs/curso/M4/RIESGOS.md`](../curso/M4/RIESGOS.md),
  [`docs/curso/M4/RETRO.md`](../curso/M4/RETRO.md) y `RUBRICA-M4.md`.

> Si sobra tiempo, no ampliar la demo: responder preguntas usando el runbook y la
> matriz de trazabilidad.

## Checklist del entorno (§5.4)

Revisar en este orden antes de iniciar la sustentación. Marcar ✅ solo si el criterio
se verificó en la sesión; lo pendiente se reporta al inicio del bloque 13:30.

| Ítem | Comando | Criterio | Responsable |
|---|---|---|---|
| Rama `develop` actualizada | `git status && git log -1 origin/develop` | sin cambios locales y PRs de la HU en revisión | Guillermo |
| tablero visible | abrir <https://github.com/users/GuillermoZ-Code/projects/1> | columnas y tarjetas de M4 visibles | Jesús |
| Entorno Python con `uv` | `uv sync && uv run python --version` | Python 3.13 y dependencias resueltas | Guillermo |
| Pesos del modelo disponibles | `$env:PPE_MODEL_PATH = "<ruta local>"` | archivo legible y SHA256 comparado con `models.lock` | Hernán |
| API y contrato | `uv run pytest tests/test_api*.py` | healthcheck y `/predict` en verde | Eliana |
| Docker CPU | `make docker-build` | imagen construida sin CUDA | Guillermo |
| SPA React | `make frontend-check` | ESLint y Vitest en verde | Guillermo |
| CI de la rama | `glab ci status` | compuertas verdes o declarar la excepción | Jesús |
| Runbook a mano | abrir `docs/operacion/fallos.md` | seis etapas y tres fallos simulados | Eliana |

## Ensayo cronometrado

Duración objetivo acordada para cada bloque. La columna `Real` se completa durante
el ensayo con el equipo; mientras tanto se deja `—` para no inventar tiempos.

| Bloque | Objetivo | Real | Estado |
|---|---|---|---|
| 0:00–2:00 | 2:00 | — | Pendiente |
| 2:00–5:00 | 3:00 | — | Pendiente |
| 5:00–8:00 | 3:00 | — | Pendiente |
| 8:00–11:00 | 3:00 | — | Pendiente |
| 11:00–13:30 | 2:30 | — | Pendiente |
| 13:30–15:00 | 1:30 | — | Pendiente |

- **Validación estática:** revisión del documento y 9 pruebas automatizadas en
  `tests/test_docs_ficha_m4.py`, ejecutadas por Eliana el 2026-11-24.
- **Ensayo del equipo:** **Pendiente** — requiere sala, los cuatro responsables y el
  entorno de despliegue. Completar fecha, participantes y tiempos reales antes de la
  sustentación. No se afirma que el ensayo cronometrado ya se realizó.

## Referencias

- [`FICHA-M3.md`](./FICHA-M3.md) — datos de la entrega anterior.
- [`docs/operacion/fallos.md`](../operacion/fallos.md) — árbol de decisión y fallos simulados.
- [`docs/curso/PLAN-PRUEBAS.md`](../curso/PLAN-PRUEBAS.md) — reparto de pruebas.
