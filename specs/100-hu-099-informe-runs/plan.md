# Implementation Plan: HU-099 — Informe comparativo de runs de MLflow

**Branch**: `feature/100-hu-099-informe-runs` | **Date**: 2026-11-24

**Spec**: [spec.md](spec.md)

**Input**: Issue #155 y `specs/100-hu-099-informe-runs/spec.md`.

## Summary

Añadir `render_comparison_report(runs, tracking_uri, generated_at)` a
`tracking/mlflow_tracker.py`: tabla con métricas, ruta del artefacto con `sha256:` y
enlace a `#/runs/<run_id>`. Generar `docs/evaluation/mlflow-comparacion.md` con los
resúmenes de HU-019 y dejar el comando de regeneración.

## Technical Context

**Python 3.13, biblioteca estándar; sin dependencias nuevas.**

## Constitution Check

- [x] Sin dependencias nuevas; sin pesos en Git.
- [x] Cada AC tiene prueba.
- [x] `tracking/` es del autor; `docs/evaluation/` genera aviso.

## Project Structure

```text
src/ppe_detection/tracking/mlflow_tracker.py   # + render_comparison_report
tests/test_tracking_report.py                  # nuevo: 7 pruebas
docs/evaluation/mlflow-comparacion.md          # generado
specs/100-hu-099-informe-runs/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

- Tabla `| Run | mAP50 | mAP50-95 | Precision | Recall | Artefacto | Enlace |`.
- Enlace: `<tracking_uri>/#/runs/<run_id>`; artefacto: `model_path` + `model_reference`.
- `_format_metric` muestra «—» si falta la métrica.

## Phases

1. Tests first (7 pruebas).
2. Implementación y export.
3. Generar el informe y `make check`.

## Risks

- **Muestra**: el informe del repo se construye con los resúmenes de HU-019; se regenera
  contra MLflow cuando los runs estén en el Droplet.
