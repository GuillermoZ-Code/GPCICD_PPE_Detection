# Implementation Plan: HU-005 — Validación de imágenes recibidas

**Branch**: `feature/007-hu-005-validacion-imagenes` | **Date**: 2026-11-10 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/006-hu-005-validacion-imagenes/spec.md`
e issue #5.

## Summary

Agregar una capa de validación reutilizable para las imágenes que entran al sistema:
rechaza archivos vacíos, corruptos, de formato no admitido y mayores de 10 MB antes de
tocar el detector. `load_image` y `load_image_bytes` comparten las mismas reglas para
que la CLI, la API (HU-006) y la interfaz (HU-007) no dupliquen criterios.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `numpy`, `opencv-python-headless` (ya existentes); sin
dependencias nuevas.

**Storage**: n/a (sin datos ni pesos).

**Testing**: pytest (AAA), imágenes sintéticas en memoria; sin GPU, sin red y sin
dataset.

**Target Platform**: CPU

**Project Type**: library

**Performance Goals**: la validación de tamaño y formato debe ser O(1) sobre los bytes
de cabecera; la decodificación ya existe en HU-001.

**Constraints**: mensajes en español; formatos JPEG/PNG por contenido; límite alineado
con el frontend (`10 MB`); no importar `ultralytics` ni el detector.

**Scale/Scope**: 1 módulo existente (`io/images.py`), 1 archivo de pruebas nuevo
(~6 pruebas), documentación de contrato y enlaces del backlog.

## Constitution Check

- [x] `uv` como único gestor; no hay dependencias nuevas.
- [x] src-layout y pruebas en `tests/` con patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin datos ni pesos en Git.
- [x] Contract-first: devuelve `ImageData` del contrato existente.
- [x] Sin LLM en inferencia.
- [x] Test-first: pruebas antes de la implementación.
- [x] Uso responsable: un rechazo no afirma nada sobre el cumplimiento de EPP.

## Project Structure

### Documentation

```text
specs/006-hu-005-validacion-imagenes/
├── spec.md
├── plan.md
└── tasks.md
```

### Source Code

```text
src/ppe_detection/io/
├── __init__.py          # exporta MAX_IMAGE_BYTES y validate_image_bytes
└── images.py            # validación de tamaño, formato y decodificación
tests/
└── test_image_validation.py
```

## Design

1. `MAX_IMAGE_BYTES = 10 * 1024 * 1024` como constante pública.
2. `validate_image_bytes(data, source="upload", max_bytes=MAX_IMAGE_BYTES) -> ImageData`:
   - rechaza `len(data) == 0` con «El archivo está vacío»;
   - rechaza `len(data) > max_bytes` con el límite en MB;
   - delega en `_decode` para validar la cabecera JPEG/PNG y decodificar.
3. `load_image_bytes` delega en `validate_image_bytes`.
4. `load_image` verifica el tamaño del archivo antes de leerlo y luego decodifica.
5. La API de HU-006 capturará `InvalidImageError` y devolverá un 4xx con el mensaje.

## Risks

- **Límite duplicado con el frontend:** se documenta la constante y se prueba el
  límite; si cambia, se actualizan ambos lados.
- **Imágenes grandes:** el límite se valida antes de `cv2.imdecode` para no cargar
  archivos desproporcionados.
- **Falso positivo de formato:** se usa la cabecera mágica, no la extensión.

## Verification

- `uv run pytest tests/test_image_validation.py`
- `make check`
- `uv build`
