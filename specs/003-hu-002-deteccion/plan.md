# Implementation Plan: HU-002 — Detección de EPP

**Branch**: `feature/003-hu-002-deteccion` | **Date**: 2026-11-04 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/003-hu-002-deteccion/spec.md` e issue #2.

## Summary

Adaptar el artefacto YOLO entrenado al protocolo `Detector` del contrato TA-11 y
ofrecer una CLI que cargue imágenes con HU-001, ejecute inferencia y exporte las
detecciones a CSV. `ultralytics` se importa perezosamente para que las pruebas
unitarias corran sin torch.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `numpy`, `opencv-python-headless`; `ultralytics` opcional
(extra `inference`)

**Storage**: pesos fuera de Git, ruta configurable

**Testing**: pytest (AAA), modelo falso inyectado; prueba real opcional con
`pytest.importorskip("ultralytics")`

**Target Platform**: CPU

**Project Type**: library + CLI

**Performance Goals**: medir latencia en HU-008; SPI-01 reporta 136–158 ms a 640 px

**Constraints**: sin GPU, sin red, sin pesos en las pruebas unitarias

**Scale/Scope**: 1 adaptador, 1 CLI, ~15 pruebas

## Constitution Check

- [x] `uv` como único gestor; `ultralytics` como extra opcional.
- [x] src-layout y pruebas en `tests/`.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin datos ni pesos en Git.
- [x] Contract-first: `YoloDetector` cumple `Detector`.
- [x] Sin LLM en inferencia.
- [x] Test-first y modelo falso determinista.

## Project Structure

```text
src/ppe_detection/
├── contracts.py
├── io/
└── detection/
    ├── __init__.py
    ├── yolo.py           # YoloDetector
    └── predict.py        # CLI de inferencia y CSV

tests/
├── test_yolo_detector.py
└── test_predict.py

specs/003-hu-002-deteccion/
├── spec.md
├── plan.md
└── tasks.md
```

**Structure Decision**: el adaptador vive en `detection/` y depende del contrato, no al
contrario. La CLI reutiliza `load_image` de HU-001 y no dibuja cajas (eso es HU-003).

## Phase 0 — Investigación

- SPI-01: YOLOv8n + Python 3.13 + torch CPU funciona; latencia 136–158 ms a 640 px.
- SPI-02: baseline reproducible y catálogo real del `data.yaml`.
- Los pesos disponibles son `yolo11s_clean` y `yolov8n_clean`; el adaptador no fija
  una variante, recibe la ruta.

## Phase 1 — Diseño

- `YoloDetector(model_path, conf, iou, imgsz, device, model=None)`.
- Conversión RGB→BGR antes de `predict` (Ultralytics asume BGR en arrays NumPy).
- Recorte de cajas y descarte de cajas degeneradas antes de construir `Detection`.
- Validación estricta del catálogo del modelo contra `CLASSES`.
- `importlib` perezoso de `ultralytics` con mensaje accionable.

## Complexity Tracking

No hay violaciones a la constitución. La dependencia pesada queda como extra para no
obligar a torch en CI.
