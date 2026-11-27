# Implementation Plan: HU-037 — Evaluación por tamaño de objeto

**Branch**: `feature/038-hu-037-sesgo-tamano` | **Date**: 2026-11-26

**Spec**: [spec.md](spec.md)

**Input**: Issue #93 y `specs/038-hu-037-sesgo-tamano/spec.md`.

## Summary

Agregar `evaluation/size_bias.py` para clasificar cajas por área relativa y calcular
AP por clase y bucket. El cálculo es puro; la tabla real se produjo con YOLO26n sobre
las 1.095 imágenes de test y se documenta en `docs/evaluation/tamano.md`.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `contracts`, `evaluation.errors`,
`evaluation.metrics`; pytest

**Storage**: `docs/evaluation/tamano.md`; evidencia local en
`dist/analisis/tamano/summary.json`

**Testing**: pytest AAA con cajas sintéticas; sin YOLO, GPU ni dataset

**Target Platform**: CPU / CI

**Project Type**: biblioteca de evaluación

**Constraints**: no cargar el modelo en pruebas; no publicar imágenes

**Scale/Scope**: 6 clases, 3 buckets, 5 pruebas, 1.095 imágenes para la evidencia

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Pruebas en `tests/` y patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin GPU, dataset ni red en las pruebas.
- [x] La tabla reporta conteos y limitaciones.
- [x] No se versionan imágenes ni pesos.
- [x] No se cambia el contrato.

## Project Structure

```text
src/ppe_detection/evaluation/
├── size_bias.py
└── __init__.py
tests/
└── test_size_bias.py
docs/evaluation/
└── tamano.md
specs/038-hu-037-sesgo-tamano/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Clasificación

```text
small:  área / (ancho × alto) < 0,01
medium: 0,01 <= área / (ancho × alto) < 0,04
large:  área / (ancho × alto) >= 0,04
```

Las predicciones se asignan por su caja; las etiquetas por su caja anotada.

### AP

Para cada clase y bucket:

1. Se recolectan GT y predicciones del bucket.
2. Se ordenan predicciones por confianza.
3. Se emparejan con GT del mismo bucket a IoU 0,50; una predicción no se reutiliza.
4. Se calculan precision/recall y AP con `average_precision`.

### Evidencia real

Se ejecutó YOLO26n sobre el test completo con `conf=0.001`, `iou=0.7`, `imgsz=640`.
La tabla final está en `docs/evaluation/tamano.md`; el resumen local en
`dist/analisis/tamano/summary.json`.

## Phases

1. **Tests:** clasificación, errores, AP perfecto, AP cero y cobertura.
2. **Implementación:** `size_bias.py` y exports.
3. **Evidencia:** recolectar predicciones y generar la tabla.
4. **Cierre:** `make specs-check`, `make check`, `uv build`, PR `Closes #93`.

## Risks

| Riesgo | Mitigación |
|---|---|
| Umbral relativo distinto de COCO | Se documenta explícitamente |
| Clase sin GT | AP 0 y conteo 0 |
| Predicciones duplicadas | Emparejamiento greedy sin reutilizar |
| Sesgo por soporte | Se reportan conteos GT por bucket |
| Imágenes personales | Solo se publican conteos y métricas |

## Verification

```bash
uv run pytest tests/test_size_bias.py -q
make specs-check
make check
uv build
```
