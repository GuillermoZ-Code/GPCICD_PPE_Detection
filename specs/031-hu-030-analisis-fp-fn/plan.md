# Implementation Plan: HU-030 — Análisis de falsos positivos y negativos

**Branch**: `feature/031-hu-030-analisis-fp-fn` | **Date**: 2026-11-24

**Spec**: [spec.md](spec.md)

**Input**: Issue #86 y `specs/031-hu-030-analisis-fp-fn/spec.md`.

## Summary

Agregar un analizador puro de FP/FN que recibe etiquetas y predicciones ya
convertidas a píxeles. El analizador empareja por clase y IoU, cuenta TP/FP/FN y
clasifica cada error con una causa geométrica. Con esa salida se genera
`docs/evaluation/errores.md` sin publicar imágenes.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `ppe_detection.contracts`, `ppe_detection.evaluation.metrics`;
pytest

**Storage**: `docs/evaluation/errores.md`; evidencia local en
`dist/analisis/errores/summary.json` (fuera de Git)

**Testing**: pytest AAA con cajas sintéticas; sin YOLO, GPU, dataset ni red

**Target Platform**: CPU / CI

**Project Type**: biblioteca de evaluación

**Constraints**: no cargar imágenes en pruebas; no publicar recortes; no cambiar el
contrato ni el modelo

**Scale/Scope**: 6 clases, 8 pruebas, 1.095 imágenes de test para la evidencia real

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Pruebas en `tests/` y patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin GPU, dataset completo ni red en las pruebas.
- [x] Test-first: primero el analizador y sus categorías.
- [x] No se cambia `ImageData → list[Detection]`.
- [x] Pesos y dataset fuera de Git.

## Project Structure

```text
src/ppe_detection/evaluation/
├── errors.py                 # análisis puro y render del informe
└── __init__.py               # exports
tests/
└── test_evaluation_errors.py
docs/evaluation/
└── errores.md                # informe real de YOLO26n en test
specs/031-hu-030-analisis-fp-fn/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Emparejamiento

Para cada clase se filtran las predicciones con `confidence >= 0,25` y se llama
`match_detections` con IoU 0,50. Las cajas no emparejadas se convierten en FP o FN.
Los pares emparejados son TP.

### Categorías

**FP:**

1. `class_confusion`: IoU >= 0,50 con un GT de otra clase.
2. `duplicate`: IoU >= 0,50 con un GT de la misma clase ya emparejado.
3. `localization`: IoU >= 0,10 con cualquier GT.
4. `small_object`: área relativa < 1 %.
5. `background`: sin solapamiento relevante.

**FN:**

1. `class_confusion`: una predicción de otra clase con IoU >= 0,50.
2. `localization`: una predicción de la misma clase con IoU >= 0,10.
3. `small_object`: área relativa < 1 %.
4. `occlusion_or_missed`: sin predicción cercana.

### Informe

`render_error_report` produce tablas de configuración, resumen, categorías, errores
por clase y hasta 10 ejemplos por tipo. No incrusta imágenes ni recortes.

### Evidencia real

Se ejecutó YOLO26n sobre las 1.095 imágenes de test con `imgsz=640`, `conf=0.001`
para recolectar candidatos, y se analizó con `confidence=0.25`, `iou=0.5`.
El resultado local quedó en `dist/analisis/errores/summary.json`.

## Phases

1. **Tests:** 8 casos de TP, categorías, umbral y reporte.
2. **Implementación:** `errors.py` y exports.
3. **Evidencia:** recolectar predicciones de YOLO26n y escribir `errores.md`.
4. **Cierre:** `make specs-check`, `make check`, `uv build`, PR `Closes #86`.

## Risks

| Riesgo | Mitigación |
|---|---|
| Categoría geométrica no equivale a oclusión real | Se declara en limitaciones |
| Reescalar cajas cambia los conteos | Se documentan IoU y confianza |
| Imágenes con personas | Solo se publican nombres y geometría; no recortes |
| Duplicados por NMS | Se cuentan como `duplicate` y se reportan |
| Datos fuera de Git | La evidencia pesada queda en `dist/` y el informe es reproducible |

## Verification

```bash
uv run pytest tests/test_evaluation_errors.py -q
make specs-check
make check
uv build
```
