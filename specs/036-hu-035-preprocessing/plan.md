# Implementation Plan: HU-035 — Módulo de preprocesamiento con contrato numérico

**Branch**: `feature/036-hu-035-preprocessing` | **Date**: 2026-11-26

**Spec**: [spec.md](spec.md)

**Input**: Issue #91 y `specs/036-hu-035-preprocessing/spec.md`.

## Summary

Crear `src/ppe_detection/preprocessing/` con letterbox, normalización y
transformación inversa de cajas. El módulo es puro, usa OpenCV/NumPy y documenta el
contrato numérico para que las detecciones vuelvan a la imagen original.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: NumPy y OpenCV headless, ya presentes; pytest

**Storage**: ninguna; imágenes sintéticas en memoria

**Testing**: pytest AAA, sin GPU, dataset, red ni YOLO

**Target Platform**: CPU / CI

**Project Type**: biblioteca de preprocesamiento

**Constraints**: no cambiar el contrato de detección; no agregar dependencias

**Scale/Scope**: 8 pruebas; imágenes de 16×32 a 100×50; destinos 640 y 640×320

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Pruebas en `tests/` y patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin GPU, dataset completo ni red.
- [x] Test-first: primero las pruebas de letterbox e inversa.
- [x] No se cambia `ImageData → list[Detection]`.
- [x] No se versionan imágenes ni pesos.

## Project Structure

```text
src/ppe_detection/preprocessing/
├── __init__.py
└── letterbox.py
tests/
└── test_preprocessing.py
specs/036-hu-035-preprocessing/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Letterbox

1. Validar `uint8 HWC` y el destino.
2. Calcular `scale = min(ancho_destino/ancho, alto_destino/alto)`.
3. Si `scaleup=False`, limitar a 1.
4. Redimensionar con OpenCV.
5. Rellenar con `copyMakeBorder` y padding centrado.
6. Devolver `LetterboxResult` con escala, padding y dimensiones.

### Inversa

Para cada caja:

```text
x_original = (x_lienzo - pad_x) / scale
y_original = (y_lienzo - pad_y) / scale
```

Las coordenadas se recortan a `[0, ancho] × [0, alto]`.

### Normalización

`image.astype(float32) / 255.0`, conservando HWC RGB.

### Decisiones

- El orden de `new_shape` es `(alto, ancho)` para coincidir con NumPy.
- El padding se calcula con división entera; el residuo va al lado derecho/inferior.
- No se modifica `YoloDetector`; el módulo queda disponible para una integración
  posterior.

## Phases

1. **Tests:** 8 casos de forma, padding, inversa, normalización y bordes.
2. **Implementación:** `letterbox.py` y exports.
3. **Verificación:** pruebas focales, `make specs-check`, `make check`, `uv build`.
4. **Cierre:** PR con `Closes #91` cuando `develop` esté estable.

## Risks

| Riesgo | Mitigación |
|---|---|
| Cajas fuera de la imagen | Recorte explícito a dimensiones originales |
| Escala inconsistente | Se devuelve la escala usada en el resultado |
| Padding no centrado | Se prueban destinos no cuadrados |
| Imagen pequeña ampliada | `scaleup=False` probado |
| Dependencia de YOLO | No se importa Ultralytics |

## Verification

```bash
uv run pytest tests/test_preprocessing.py -q
make specs-check
make check
uv build
```
