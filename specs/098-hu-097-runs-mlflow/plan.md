# Implementation Plan: HU-097 — Runs comparables en MLflow

**Branch**: `feature/098-hu-097-runs-mlflow` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #153 y `specs/098-hu-097-runs-mlflow/spec.md`.

## Summary

Añadir `build_comparison_payloads` a `tracking/mlflow_tracker.py`: recibe dos o más
resúmenes de evaluación, reutiliza `build_run_payload` y valida que compartan `imgsz`,
`conf`, `iou`, `seed` y partición. Devuelve pares `(nombre, payload)` con el modelo
referenciado por SHA256 y las métricas por clase.

## Technical Context

**Python 3.13, biblioteca estándar; sin dependencias nuevas.**

## Constitution Check

- [x] Sin dependencias nuevas; sin pesos en Git.
- [x] Cada AC tiene prueba.
- [x] `tracking/` y `tests/test_tracking*.py` son del autor.

## Project Structure

```text
src/ppe_detection/tracking/mlflow_tracker.py   # + build_comparison_payloads
src/ppe_detection/tracking/__init__.py         # exporta la funcion
tests/test_tracking_comparison.py              # nuevo: 8 pruebas
specs/098-hu-097-runs-mlflow/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

- `COMPARISON_KEYS = ("imgsz", "conf", "iou", "seed", "dataset_split")`.
- Se construye cada payload con `build_run_payload`; el primero fija los parámetros
  compartidos y los demás se comparan contra ellos.
- Nombre del run: `default_run_name(summary)` → `eval-<split>-<sha12>`.

## Phases

1. Tests first (8 pruebas).
2. Implementación y export.
3. `make check`, ownership y PR.

## Risks

- **Resúmenes incompletos**: `build_run_payload` ya los rechaza.
- **Tres modelos**: la función no impone el número; exige al menos dos.
