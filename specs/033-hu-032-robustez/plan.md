# Implementation Plan: HU-032 — Robustez ante luz, ruido y escala

**Branch**: `feature/033-hu-032-robustez` | **Date**: 2026-11-27

**Spec**: [spec.md](./spec.md)

**Input**: Issue #88 y `specs/033-hu-032-robustez/spec.md`.

## Summary

Agregar funciones puras de perturbación en `evaluation/robustness.py` y generar una
tabla real de mAP sobre una muestra fija de 100 imágenes de test. El cálculo de mAP
se delega en `YOLO.val`; el módulo nuevo no carga el modelo.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: NumPy, OpenCV; Ultralytics solo para la evidencia

**Testing**: pytest AAA con arreglos sintéticos; sin YOLO, GPU ni dataset

**Target Platform**: CPU / CI

**Project Type**: biblioteca de evaluación

**Constraints**: perturbaciones deterministas; sin imágenes ni pesos en Git

**Scale/Scope**: 4 variantes, 5 pruebas, muestra fija de 100 imágenes

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Pruebas en `tests/` con patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin GPU, dataset ni red en las pruebas.
- [x] La evidencia declara muestra, semilla e intensidades.
- [x] No se versionan imágenes ni pesos.
- [x] No se cambia el contrato del detector.

## Project Structure

```text
src/ppe_detection/evaluation/
├── robustness.py       # nuevo
└── __init__.py         # exports
tests/
└── test_robustness.py
docs/evaluation/
└── robustez.md
specs/033-hu-032-robustez/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Perturbaciones

| Variante | Operación | Parámetro |
|---|---|---|
| `clean` | copia sin cambios | — |
| `brightness` | multiplica canales y recorta | factor 0,7 |
| `noise` | gaussiano con semilla | sigma 12, seed 42 |
| `scale` | redimensiona con OpenCV | factor 0,75 |

La imagen se valida antes de operar: `uint8`, tres canales y dimensiones no vacías.
Las cajas normalizadas de YOLO se conservan al cambiar la resolución.

### Evidencia

Se preparan cuatro carpetas temporales con las primeras 100 imágenes de test y sus
etiquetas. Para cada variante se ejecuta:

```text
YOLO.val(data=..., split="val", imgsz=640, conf=0.001, iou=0.7, device="cpu")
```

La tabla reporta mAP@0.5 y mAP@0.5:0.95; el resumen local queda en
`dist/robustez/summary.json`, fuera de Git.

## Phases

1. **Tests:** brillo, ruido determinista, escala, parámetros inválidos y nombres.
2. **Implementación:** `robustness.py` y exports.
3. **Evidencia:** generar las cuatro variantes y validar con YOLO26n.
4. **Cierre:** `make specs-check`, `make check`, `uv build`, PR `Closes #88`.

## Risks

| Riesgo | Mitigación |
|---|---|
| Muestra pequeña | Se declara y no sustituye la evaluación completa |
| Una sola intensidad | Se documenta como limitación |
| Ruido no reproducible | Semilla explícita y prueba de igualdad |
| Imágenes en Git | Carpetas temporales en `dist/`, ignorado |
| Escala con cajas incorrectas | Se conservan las cajas normalizadas |

## Verification

```bash
uv run pytest tests/test_robustness.py -q
make specs-check
make check
uv build
```
