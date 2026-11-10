# Implementation Plan: HU-006 — API REST con FastAPI

**Branch**: `feature/008-hu-006-api-rest` | **Date**: 2026-11-10 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/008-hu-006-api-rest/spec.md` e issue #6.

## Summary

Exponer `POST /predict` con FastAPI para que la SPA React, gRPC y el despliegue
consuman el detector sin cargar Python. La API valida la imagen con HU-005, usa el
protocolo `Detector` (inyectable en pruebas) y devuelve el esquema `PredictResponse`
que ya espera el frontend.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `fastapi`, `uvicorn`, `python-multipart`; `httpx` en dev.

**Storage**: n/a (sin persistencia).

**Testing**: pytest + `fastapi.testclient.TestClient` + `FakeDetector`; sin GPU ni red.

**Target Platform**: CPU

**Project Type**: web service

**Performance Goals**: la inferencia depende del detector; la API añade solo validación
y serialización. `elapsed_ms` mide la llamada al detector.

**Constraints**: contrato `Detection` de TA-11; validación de HU-005; sin entrenamiento;
CORS para `http://localhost:5173`; errores de cliente 4xx.

**Scale/Scope**: 1 paquete `api/` (~120 líneas), 1 archivo de pruebas (~7 pruebas).

## Constitution Check

- [x] `uv` como único gestor; dependencias añadidas con `uv add`.
- [x] src-layout y pruebas en `tests/` con patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin datos ni pesos en Git.
- [x] Contract-first: reutiliza `Detector`, `Detection` y `ImageData`.
- [x] Sin LLM en inferencia.
- [x] Test-first: pruebas antes de la implementación.
- [x] La API reporta detecciones, no cumplimiento.

## Project Structure

```text
src/ppe_detection/api/
├── __init__.py       # create_app y app
├── __main__.py       # python -m ppe_detection.api
└── app.py            # FastAPI, esquemas y endpoint /predict
tests/
└── test_api.py
```

## Design

- `create_app(detector=None, model_version=None)` permite inyectar `FakeDetector` y
  fijar la versión en pruebas.
- El detector real se construye de forma perezosa desde `PPE_MODEL_PATH`, con
  `PPE_CONF`, `PPE_IOU`, `PPE_IMGSZ` y `PPE_DEVICE`.
- `POST /predict` lee el `UploadFile`, llama a `validate_image_bytes` (HU-005),
  ejecuta `detector.detect(image)` y serializa `PredictResponse`.
- `InvalidImageError` → 400; falta de modelo → 503; falta de `file` → 422.
- CORS configurable por `PPE_CORS_ORIGINS` (por defecto `http://localhost:5173`).
- `model_version` se toma de `PPE_MODEL_VERSION` o del nombre del artefacto.

## Risks

- **Carga de ultralytics en tests:** se evita inyectando `FakeDetector`; la carga real
  es perezosa.
- **Tamaño de archivo:** se valida con HU-005 antes de decodificar.
- **Contrato frontend:** cualquier cambio de campos debe actualizar `frontend/src/types.ts`
  y este spec.
- **CORS:** en producción el frontend se sirve desde el mismo origen o se configura
  `PPE_CORS_ORIGINS`.

## Verification

- `uv run pytest tests/test_api.py`
- `make check`
- `uv build`
- `uv run uvicorn ppe_detection.api.app:app` (humo manual)
