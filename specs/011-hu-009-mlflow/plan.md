# Implementation Plan: HU-009 — MLflow para experimentos

**Branch**: `feature/011-hu-009-mlflow` | **Date**: 2026-11-11 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/011-hu-009-mlflow/spec.md` e issue #9.

## Summary

Instrumentar la evaluación de HU-008 para registrar cada corrida en MLflow y ofrecer
una comparación legible de dos o más runs. La integración con MLflow es opcional
(extra `tracking`) y perezosa; las pruebas usan un tracker falso y no requieren MLflow,
GPU, dataset ni red.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `mlflow>=3,<4` como extra `tracking`; sin dependencias nuevas
en el paquete base

**Storage**: backend local de MLflow (`sqlite:///mlflow.db` o `file:./mlruns`), fuera
de Git; artefactos de evaluación en `artifacts/eval/`

**Testing**: pytest (AAA) con `FakeTracker`, sin MLflow instalado

**Target Platform**: CPU, local

**Project Type**: library + CLI

**Performance Goals**: registrar y comparar decenas de runs en segundos; no aplica
latencia de inferencia

**Constraints**: no versionar pesos, datasets ni `mlruns/`; no servidor remoto; no
entrenar ni descargar pesos

**Scale/Scope**: un run por evaluación de HU-008; comparación de 2+ runs

## Constitution Check

- [x] `uv` como único gestor; MLflow entra con `uv add --optional tracking`.
- [x] src-layout y pruebas en `tests/`.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin datos ni pesos en Git.
- [x] Contract-first: el payload se define sobre el `summary.json` de HU-008.
- [x] Sin LLM en inferencia.
- [x] Test-first: cada AC tiene una prueba que lo referencia.

## Project Structure

```text
src/ppe_detection/tracking/
├── __init__.py           # API pública del paquete
├── __main__.py           # python -m ppe_detection.tracking
└── mlflow_tracker.py     # payload, tracker MLflow y CLI log/compare

tests/
└── test_tracking.py      # pruebas con FakeTracker y summary de HU-008

docs/operacion/
└── mlflow.md             # procedimiento local, UI y comparación
```

## Phases

1. **Tests first**: payload, registro, rechazo de pesos, comparación y nombres.
2. **Implementación**: `build_run_payload`, `log_evaluation_run`, `compare_runs`,
   `render_comparison`, `MlflowTracker` y CLI.
3. **Dependencia**: extra `tracking` con MLflow y `uv.lock`.
4. **Evidencia**: registrar dos evaluaciones reales (492 y 1.094) en un backend local,
   compararlas y documentar los `run_id`.
5. **Cierre**: `make check`, `uv build`, docs, backlog y estado.

## Risks

- **MLflow 3.x es pesado** (>150 dependencias resueltas): por eso es un extra opcional y
  las pruebas no lo importan.
- **El backend local cambia entre versiones**: se documenta SQLite como opción principal
  y archivo como alternativa.
- **Los `run_id` son locales**: la evidencia se guarda con el nombre del run y los IDs;
  no se versiona el almacén de MLflow.
- **Acoplamiento con HU-008**: si el `summary.json` cambia, el payload debe fallar con un
  mensaje claro; la spec fija las claves mínimas.
