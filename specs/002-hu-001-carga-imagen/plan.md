# Implementation Plan: HU-001 — Carga de imágenes

**Branch**: `feature/002-hu-001-carga-imagen` | **Date**: 2026-11-04 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/002-hu-001-carga-imagen/spec.md` e
issue #1.

## Summary

Definir el contrato `ImageData` (prerrequisito TA-11) y un cargador que decodifique
JPEG/PNG desde ruta o bytes, conserve las dimensiones originales y rechace entradas
inválidas sin ejecutar inferencia. La salida alimenta el preprocesamiento y el
detector de HU-002.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `numpy`, `opencv-python-headless` (decodificación)

**Storage**: N/A

**Testing**: pytest (patrón AAA), `make check`

**Target Platform**: Linux/Windows; CPU

**Project Type**: library (`ppe_detection`)

**Performance Goals**: carga de una imagen en menos de 100 ms en CPU para 1280×720

**Constraints**: sin GPU, sin dataset, sin pesos, sin red en las pruebas

**Scale/Scope**: 1 contrato (`ImageData`), 2 funciones públicas, ~9 pruebas

## Constitution Check

- [x] `uv` como único gestor; dependencias con `uv add`.
- [x] src-layout y pruebas en `tests/`.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin datos ni pesos en Git; imágenes sintéticas en pruebas.
- [x] Contract-first y AGPL-3.0-only.
- [x] Sin LLM en inferencia.
- [x] Test-first: cada AC tiene prueba antes de la implementación.

## Project Structure

### Documentation (this feature)

```text
specs/002-hu-001-carga-imagen/
├── spec.md
├── plan.md
└── tasks.md
```

### Source Code (repository root)

```text
src/ppe_detection/
├── contracts.py          # CLASSES, ImageData (prerrequisito TA-11)
├── io/
│   ├── __init__.py
│   └── images.py         # load_image, load_image_bytes, InvalidImageError

tests/
├── test_contracts.py
└── test_image_loader.py
```

**Structure Decision**: el contrato vive en `contracts.py` para que el detector, la API
y la interfaz lo importen sin acoplarse a OpenCV. La carga queda aislada en `io/`.

## Phase 0 — Investigación

- Decodificación con `cv2.imdecode` sobre bytes; conversión BGR→RGB.
- Detección de formato por magic bytes (`\xff\xd8\xff`, `\x89PNG\r\n\x1a\n`).
- Confirmado: Python 3.13 + OpenCV headless no requieren GPU.

## Phase 1 — Diseño

- `ImageData` inmutable (`frozen dataclass`) con validación de forma, `dtype` y
  dimensiones en `__post_init__`.
- `InvalidImageError(ValueError)` para entradas vacías, corruptas o no admitidas.
- `load_image(path)` y `load_image_bytes(data, source)` comparten la decodificación.
- Sin importar `ultralytics` ni `ppe_detection.detection` desde `io`.

## Complexity Tracking

No hay violaciones a la constitución. El contrato se adelanta desde TA-11 porque
HU-001 lo exige; se documenta en el PR y en `specs/001-ta-contract-first`.
