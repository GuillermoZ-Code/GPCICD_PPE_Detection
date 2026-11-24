# Implementation Plan: HU-022 — Exportación ONNX y backend opcional

**Branch**: `feature/023-hu-022-export-onnx` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #78 y `specs/023-hu-022-export-onnx/spec.md`.

## Summary

Añadir `detection/onnx.py` con selección de backend y exportación ONNX reproducible.
`build_detector()` resolverá `.pt`/`.onnx` por `PPE_MODEL_FORMAT`. La suite usa
archivos temporales y un exportador simulado; no agrega dependencias obligatorias.

## Technical Context

**Python**: 3.13

**Dependencias opcionales**: `ultralytics`, `onnx`, `onnxslim`, `onnxruntime`.

**Testing**: pytest con `tmp_path` y monkeypatch; sin GPU ni red.

## Design

### `resolve_backend_path(model_path, fmt=None)`

- `fmt=None` → `PPE_MODEL_FORMAT` o `pt`.
- `pt` → ruta original.
- `onnx` → hermana `.onnx`; si la ruta ya termina en `.onnx`, se respeta.
- Formato desconocido o archivo ausente → `OnnxError`.

### `export_onnx(weights, *, imgsz=640, opset=17, output=None)`

- Carga Ultralytics de forma perezosa.
- Exporta `format=onnx`, `opset`, `imgsz`, `simplify=True`, `dynamic=False`.
- Escribe `<onnx>.json` con:
  `weights`, `onnx`, `sha256` de ambos, `imgsz`, `opset`, `ultralytics`, `torch`.
- Devuelve `OnnxExportResult`.

### `compare_detections(reference, candidate, ...)`

- Compara listas de `Detection` por clase/confianza/bbox con tolerancias explícitas.
- Reporta diferencias; no se usa en producción.

### Integración

`build_detector()`:
1. Lee `PPE_MODEL_PATH`.
2. Si `PPE_MODEL_FORMAT` está definido, resuelve la ruta con
   `resolve_backend_path`.
3. Construye `YoloDetector` con la ruta resuelta.

## Risks

- **Dependencias opcionales**: no se agregan al paquete base; el error debe ser claro.
- **ONNX fijo a 640**: el export estático usa 640; otras resoluciones pueden requerir
  otro export.
- **Specs/ es de Jesús**: la spec genera aviso de propiedad.
