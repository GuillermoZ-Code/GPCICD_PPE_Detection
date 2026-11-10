# Implementation Plan: HU-003 — Visualización de detecciones

**Branch**: `feature/004-hu-003-visualizacion` | **Date**: 2026-11-09 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/004-hu-003-visualizacion/spec.md` e issue #3.

## Summary

Dibujar las detecciones del contrato `ImageData → list[Detection]` sobre una copia de la
imagen y ofrecer un flag `--annotated` en la CLI de inferencia para guardar las imágenes
de evidencia. El módulo no conoce YOLO, la API ni la interfaz: solo el contrato.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `numpy`, `opencv-python-headless`

**Storage**: las imágenes anotadas van a `artifacts/predictions/<corrida>/annotated/`
(fuera de Git)

**Testing**: pytest (AAA) con imágenes sintéticas; sin GPU, dataset ni red

**Target Platform**: CPU

**Project Type**: library + CLI

**Performance Goals**: dibujo en milisegundos; no hay inferencia en este módulo

**Constraints**: no mutar la entrada; no cambiar el contrato

**Scale/Scope**: 1 módulo, 1 función pública, 1 flag de CLI, ~8 pruebas

## Constitution Check

- [x] `uv` como único gestor; sin dependencias nuevas.
- [x] src-layout y pruebas en `tests/`.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin datos ni pesos en Git.
- [x] Contract-first: `Detection` no cambia.
- [x] Sin LLM en inferencia.
- [x] Test-first y pruebas deterministas.

## Project Structure

```text
src/ppe_detection/
├── contracts.py
├── io/
│   └── images.py          # + write_image
├── detection/
│   └── predict.py         # + --annotated
└── visualization/
    ├── __init__.py
    └── overlay.py         # draw_detections, format_label

tests/
├── test_overlay.py
├── test_predict.py        # + prueba del flag
└── test_image_loader.py   # + pruebas de write_image
```

**Structure Decision**: `visualization/` depende solo de `contracts.py` e `io/`. La CLI
orquesta; la interfaz (HU-007) reutilizará `draw_detections` sin duplicar dibujo.

## Phase 0 — Investigación

- Los `bbox` de `Detection` están en píxeles de la imagen original y llevan
  `image_width`/`image_height`: la transformación es identidad y solo se escala cuando el
  lienzo tiene otro tamaño.
- OpenCV dibuja en BGR; la conversión se hace en los bordes del módulo.
- `cv2.getTextSize` permite reservar el fondo de la etiqueta.

## Phase 1 — Diseño

- `DISPLAY_NAMES` y `COLORS` por clase canónica.
- `format_label(detection) -> str` con `Casco 0.87`.
- `draw_detections(image, detections) -> ImageData`, sin mutar la entrada.
- Grosor `max(1, lado_mayor / 400)` y fuente `max(0.4, lado_mayor / 1600)`.
- Etiqueta encima de la caja; dentro si no hay espacio.
- `write_image(image, path)` en `io/` para guardar JPEG/PNG.
- `--annotated` guarda en `<salida>/annotated/` conservando el nombre del archivo.

## Complexity Tracking

No hay violaciones a la constitución. El módulo es pequeño y sin estado.
