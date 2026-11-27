# Implementation Plan: HU-039 — Inferencia por lotes desde CLI

**Branch**: `feature/040-hu-039-predict-lotes` | **Date**: 2026-11-26

**Spec**: [spec.md](spec.md)

**Input**: Issue #95 y `specs/040-hu-039-predict-lotes/spec.md`.

## Summary

Extender la CLI `ppe-predict` para aceptar `--dir`, generar un JSON por imagen y
conservar el CSV/manifiesto actuales. Cada JSON registra identidad del modelo,
parámetros y detecciones, y funciona con un detector simulado.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: las existentes (`contracts`, `io`, `detection`); pytest

**Storage**: `<salida>/json/<nombre-completo>.json`

**Testing**: pytest AAA con imágenes PNG/JPEG temporales y detector simulado

**Target Platform**: CPU / CLI

**Project Type**: herramienta de evaluación

**Constraints**: no cargar Ultralytics en pruebas; no cambiar el contrato; no añadir
dependencias

**Scale/Scope**: 4 pruebas; 2 imágenes en la suite; 1 JSON por imagen

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Pruebas en `tests/` y patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin GPU, dataset completo ni red en las pruebas.
- [x] No se cambia `ImageData → list[Detection]`.
- [x] No se versionan imágenes ni pesos.

## Project Structure

```text
src/ppe_detection/detection/predict.py   # CLI extendida
tests/test_predict_batch.py              # 4 pruebas de lote
specs/040-hu-039-predict-lotes/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Entrada

`--source` y `--dir` son alias en un grupo mutuamente excluyente. `--dir` apunta a una
carpeta; `--source` acepta archivo o carpeta. Ambos terminan en `args.source`.

### Salida

Por cada imagen se escribe:

```text
<salida>/json/<nombre-completo>.json
```

El nombre completo evita colisiones entre `a.png` y `a.jpg`. El payload incluye:

- imagen, ancho, alto y formato;
- `model.path`, `model.version` y `model.sha256`;
- `parameters.conf`, `iou`, `imgsz`, `device`, `seed`;
- `detections` con class_id, class_name, confidence, bbox y dimensiones;
- `message` vacío de HU-004 cuando no hay detecciones.

El CSV y `run.json` se siguen generando.

### Pruebas

Se usa un detector falso que implementa `detect()` y devuelve una caja o una lista
vacía. Se comprueba el alias `--dir`, el payload y los archivos por imagen.

## Phases

1. **Tests:** alias, payload, lote con detección y lote vacío.
2. **Implementación:** `--dir`, `image_json_payload`, `write_image_json` y salida.
3. **Verificación:** pruebas focales, `make specs-check`, `make check`, `uv build`.
4. **Cierre:** PR con `Closes #95`.

## Risks

| Riesgo | Mitigación |
|---|---|
| Romper `--source` | Grupo mutuamente excluyente y pruebas existentes |
| Colisión de nombres | Se usa el nombre completo de la imagen |
| JSON sin identidad | Se registra modelo, SHA256 y parámetros |
| Detector vacío | Se prueba el mensaje de HU-004 |
| Ultralytics en pruebas | Se inyecta un detector simulado |

## Verification

```bash
uv run pytest tests/test_predict_batch.py tests/test_predict.py -q
make specs-check
make check
uv build
```
