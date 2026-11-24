# Implementation Plan: HU-100 — Latencia del benchmark en MLflow

**Branch**: `feature/101-hu-100-latencia-mlflow` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #156 y `specs/101-hu-100-latencia-mlflow/spec.md`.

## Summary

Añadir `ResolutionLatency` y `build_latency_payload` a `tracking/mlflow_tracker.py`, y
extender `LatencyStats`/`latency_stats` con el p50. El payload registra p50, p95, media y
fps por resolución, y el hardware, la versión y el SHA256 como parámetros.

## Technical Context

**Python 3.13, biblioteca estándar; sin dependencias nuevas.**

## Constitution Check

- [x] Sin dependencias nuevas; sin pesos en Git.
- [x] Cada AC tiene prueba.
- [x] `tracking/` y `tests/test_tracking*.py` son del autor.

## Project Structure

```text
src/ppe_detection/tracking/mlflow_tracker.py   # + ResolutionLatency y payload
src/ppe_detection/tracking/__init__.py         # exporta
tests/test_tracking_latency_run.py             # nuevo: 8 pruebas
specs/101-hu-100-latencia-mlflow/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

- `LatencyStats` gana `p50_ms`; se calcula con `ceil(0.50 * n) - 1`.
- `build_latency_payload(measurements, hardware, model_version, model_sha256)`:
  - métricas `p50_ms_<imgsz>`, `p95_ms_<imgsz>`, `mean_ms_<imgsz>`, `fps_<imgsz>`;
  - parámetros `hardware`, `model_version`, `model_sha256`, `resolutions`;
  - etiqueta `model_reference = sha256:<hash>`.

## Phases

1. Tests first (8 pruebas).
2. Implementación y export.
3. `make check`, ownership y PR.

## Risks

- **Compatibilidad**: añadir `p50_ms` al dataclass; las pruebas existentes usan sus
  campos, no una tupla posicional.
- **Resoluciones**: el orden de `resolutions` refleja el de las mediciones.
