# Implementation Plan: HU-021 — Adaptar el detector a YOLO26

**Branch**: `feature/022-hu-021-detector-nms-free` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #77 y `specs/022-hu-021-detector-nms-free/spec.md`.

## Summary

Ampliar `YoloDetector` con un modo `nms` opcional y una propiedad `model_version`.
La salida sigue siendo `list[Detection]`; REST, gRPC y la SPA no cambian. La versión
de `/health` se infiere del artefacto cuando `PPE_MODEL_PATH` está definido.

## Technical Context

**Python**: 3.13

**Dependencias**: Ultralytics ya existente; sin dependencias nuevas.

**Contrato**: `ImageData → list[Detection]` (sin cambios).

**Testing**: modelos falsos que reproducen `Results.boxes` de YOLO11/YOLO26; sin GPU
ni pesos.

## Design

### `YoloDetector`

- Nuevo parámetro `nms: bool | None = None`.
- `detect()` construye kwargs y solo agrega `nms` si no es `None`.
- `model_version` devuelve el `stem` del artefacto o `unknown` si no hay path.

### `default_model_version()`

Precedencia:

1. `PPE_MODEL_VERSION` explícito.
2. Stem de `PPE_MODEL_PATH` si está definido.
3. Versión del manifiesto.
4. `unknown`.

Esto permite que `/health` reporte `yolo26n_clean` cuando se cambia el artefacto,
aunque `models.lock` todavía apunte al modelo anterior. La validación de integridad
sigue en HU-026.

### Tests

- Equivalencia de salidas YOLO11/YOLO26.
- `nms=False` se pasa; `None` se omite.
- Versión inferida y `/health`.
- Cajas, catálogo y errores existentes se conservan.

## Risks

- **Cambio de precedencia**: los tests de HU-025 que asumen manifiesto sin path deben
  seguir pasando; se revisan.
- **YOLO26 real**: los tests usan Result simulados; el smoke real queda para
  integración.
- **Specs/ es de Jesús**: la spec genera aviso de propiedad.
