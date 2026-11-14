# Ficha de entrega — Módulo 3 — Grupo 4

> Datos para que el docente abra el proyecto en menos de un minuto. Este documento es
> la versión versionada del mensaje enviado por el canal del curso; **no sustituye la
> sustentación en vivo**.
>
> **Sustentación:** sábado 14/11/2026 · 12:30–12:45 · Salón 2103 (A2).

## 1. Repositorio y tablero

| Dato | Valor |
|---|---|
| Repositorio | <https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection> |
| Visibilidad | Público (no requiere invitación) |
| Rama de la entrega | `develop` |
| Tablero Kanban | <https://github.com/users/GuillermoZ-Code/projects/1> |
| Columnas | Backlog · Ready · In Progress · In Review · Done |

## 2. Frontend desacoplado

| Dato | Valor |
|---|---|
| Stack | React 19 + Vite + TypeScript (`frontend/`) |
| Comando | `make app` (API + SPA) o `make frontend-dev` |
| URL local | <http://localhost:5173> |
| Contrato | `POST /predict` por HTTP/JSON; estados `idle` / `loading` / `success` / `error` |
| Pruebas | Vitest + Testing Library (76 pruebas) |

## 3. Backend

| Dato | Valor |
|---|---|
| Stack | FastAPI (REST) + gRPC |
| Comando REST | `uv run --extra inference python -m ppe_detection.api` |
| Puerto REST | 8000 |
| OpenAPI | <http://127.0.0.1:8000/docs> |
| Healthcheck | <http://127.0.0.1:8000/health> |
| Puerto gRPC | 9000 |
| Contrato gRPC | `src/ppe_detection/grpc/ppe.proto` |
| Modelo | se carga una sola vez con `PPE_MODEL_PATH` |

## 4. MLflow

| Dato | Valor |
|---|---|
| Comando | `make mlflow-ui` |
| Puerto | 5000 |
| `MLFLOW_TRACKING_URI` | `sqlite:///mlflow.db` |
| Experimento | `ppe-detection-inference` (3 runs comparables) |
| Model Registry | `ppe-detection`, versión 1, alias `production` |
| Artefactos | `latency_samples.csv`, `summary.md`, paquete del modelo |

## 5. Modelo y Model Card

| Dato | Valor |
|---|---|
| Modelo base | Ultralytics YOLO11s (`yolo11s.pt`) + fine-tuning propio |
| Licencia | AGPL-3.0 |
| Artefacto | `artifacts/drive/yolo11s_clean/weights/best.pt` (fuera de Git) |
| SHA256 | `E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959` |
| Model Card del equipo | [`docs/model-card.md`](../model-card.md) |
| Model Card en Hugging Face | No aplica: el artefacto es un fine-tune local identificado por SHA256 |

## 6. Diagrama de arquitectura

| Dato | Valor |
|---|---|
| Archivo | [`docs/architecture/arquitectura.html`](../architecture/arquitectura.html) |
| Fuente | [`docs/architecture/arquitectura.json`](../architecture/arquitectura.json) |
| Tipo | Architecture (Archify) |

## 7. Trazabilidad

| Dato | Valor |
|---|---|
| PRs fusionadas | 52 (48 humanas + 4 Dependabot) |
| Reparto | Guillermo 26 · Hernán 11 · Jesús 7 · Eliana 4 |
| PRs con issue cerrada | 15 (`Closes #N`) |
| Especificaciones SDD | 14 en [`specs/`](../../specs/) |
| Ejemplos | `001-ta-contract-first`, `002-hu-001-carga-imagen` |
| Formato de cada spec | `spec.md` + `plan.md` + `tasks.md` |

## 8. Notas de cumplimiento

Se declaran para que la sustentación no afirme como cumplido algo que no lo está:

- El piso de **40 PRs** y **40 specs** de la rúbrica **no se alcanzó**. El repositorio
  tiene 52 PRs fusionadas, de las cuales 15 cierran una historia, y 14 especificaciones
  SDD completas.
- Las cuatro PRs del cierre de la rúbrica (healthcheck, MLflow, Model Card y README)
  se fusionaron sin una revisión registrada de otro integrante.
- El piso de **120 pruebas pytest** sí se supera: 375 pytest + 76 Vitest = **451**.
- El modelo se sirve en CPU y la latencia medida en el equipo de desarrollo es de
  **82 ms** a 640 px y **41 ms** a 416 px.

## 9. Cómo se levanta la demo

```bash
uv sync
export PPE_MODEL_PATH=artifacts/drive/yolo11s_clean/weights/best.pt   # PowerShell: $env:PPE_MODEL_PATH = "..."
make app       # API :8000 + SPA :5173
make mlflow-ui # MLflow :5000
```

Paso a paso completo en [`docs/operacion/demo-local.md`](../operacion/demo-local.md).
