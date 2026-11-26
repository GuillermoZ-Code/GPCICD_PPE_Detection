# Implementation Plan: HU-036 — Postprocesamiento con umbrales por clase

**Branch**: `feature/037-hu-036-postprocessing` | **Date**: 2026-11-24

**Spec**: [spec.md](spec.md)

**Input**: Issue #92 y `specs/037-hu-036-postprocessing/spec.md`.

## Summary

Agregar un módulo de postprocesamiento que cargue los umbrales calibrados de
`configs/thresholds.yaml` y filtre las detecciones por la clase de cada una. La
configuración inválida falla al cargar; la ausencia del archivo por defecto usa
0,25 como respaldo seguro.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `ppe_detection.contracts` y el lector de
`ppe_detection.evaluation.thresholds`; pytest

**Storage**: `configs/thresholds.yaml`; sin escritura

**Testing**: pytest AAA con YAML temporal y detecciones sintéticas

**Target Platform**: CPU / CI

**Project Type**: biblioteca de postprocesamiento

**Constraints**: no cargar YOLO, dataset, GPU ni red; no modificar el contrato

**Scale/Scope**: 6 clases, 10 pruebas, filtro lineal por lista de detecciones

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Pruebas en `tests/` y patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin GPU, dataset completo ni red.
- [x] Test-first: primero el YAML y el filtro.
- [x] No se cambia `ImageData → list[Detection]`.
- [x] Pesos y datasets fuera de Git.

## Project Structure

```text
src/ppe_detection/postprocessing/
├── __init__.py
└── thresholds.py
tests/
└── test_postprocessing_thresholds.py
specs/037-hu-036-postprocessing/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Configuración

`ThresholdConfig` contiene exactamente las seis clases y valida que cada valor esté en
`[0,1]`. `load_threshold_config(path=None)`:

- sin ruta: usa `configs/thresholds.yaml`; si no existe, 0,25 para todas;
- con ruta: debe existir;
- cualquier error de parseo o validación se envuelve en `ThresholdConfigError`.

### Filtro

`apply_thresholds(detections, config=None)` conserva las detecciones cuyo
`confidence >= config.thresholds[class_name]`. No reordena ni muta la secuencia. Si no
se pasa configuración, carga la del repositorio.

### Integración futura

La API y gRPC podrán llamar a `load_threshold_config()` en el arranque y a
`apply_thresholds()` después de `detector.detect()`. Esta HU no toca esos módulos.

## Phases

1. **Tests:** 10 casos de carga, respaldo, errores y filtro.
2. **Implementación:** `ThresholdConfig`, `load_threshold_config` y
   `apply_thresholds`.
3. **Verificación:** pruebas del módulo, `make specs-check`, lint y tipos; el
   `make check` completo queda bloqueado por los errores ajenos de API/frontend en
   `develop`.
4. **Cierre:** PR con `Closes #92` cuando `develop` vuelva a verde.

## Risks

| Riesgo | Mitigación |
|---|---|
| Archivo ausente en producción | Respaldo 0,25 solo para la ruta por defecto |
| YAML inválido silencioso | `ThresholdConfigError` con ruta y causa |
| Umbral global accidental | Cada detección usa su clase |
| Mutación de la lista | Se devuelve una lista nueva y se prueba el snapshot |
| Dependencia de FastAPI | El módulo es puro y no importa API/gRPC |

## Verification

```bash
uv run pytest tests/test_postprocessing_thresholds.py -q
make specs-check
uv run ruff check src/ppe_detection/postprocessing tests/test_postprocessing_thresholds.py
uv run ty check
```
