# Implementation Plan: HU-045 — Healthcheck de liveness y readiness

**Branch**: `feature/046-hu-045-health-live-ready` | **Date**: 2026-11-24

**Spec**: [spec.md](spec.md)

**Input**: Issue #101 y `specs/046-hu-045-health-live-ready/spec.md`.

## Summary

Añadir dos endpoints aditivos a `src/ppe_detection/api/app.py`: `/health/live` responderá
200 sin tocar el detector y `/health/ready` responderá 503 mientras no haya detector,
incluyendo siempre versión y SHA256 del modelo. Se documentan ambos contratos en
OpenAPI, con modelo de respuesta para el caso 503. `/health` queda intacto.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: FastAPI, Pydantic (ya presentes); sin dependencias nuevas

**Storage**: sin almacenamiento nuevo; se lee `application.state`

**Testing**: pytest + `fastapi.testclient.TestClient`, `FakeDetector`, `monkeypatch`

**Target Platform**: CPU, Windows/Linux

**Project Type**: API REST dentro del paquete `ppe_detection`

**Constraints**: una HU por PR; test-first; no tocar archivos de un solo escritor ni
`.github/`; no cargar el modelo desde los healthchecks.

## Design

1. Definir `LiveResponse` y `ReadyResponse` como `BaseModel` junto a `HealthResponse`.
2. Registrar `GET /health/live` con `response_model=LiveResponse`, sin acceso a
   `application.state.detector`.
3. Registrar `GET /health/ready` con `response_model=ReadyResponse` y
   `responses={503: {"model": ReadyResponse, ...}}`. La función calcula `loaded` desde
   `application.state.detector`, obtiene la identidad de `application.state` y devuelve
   `JSONResponse(status_code=503, content=...)` cuando no está cargado.
4. Mantener `/health` y `/predict` sin cambios de comportamiento.

## Test-first plan

- Crear `tests/test_api_health_live_ready.py` con 8 pruebas que referencien AC-01/02/03.
- Ejecutar solo ese archivo y confirmar que falla antes de tocar `app.py`.
- Implementar los endpoints y repetir la suite completa.

## Validation

- `uv run pytest -v tests/test_api_health_live_ready.py`
- `uv run ruff check .` · `uv run ruff format --check .` · `uv run ty check`
- `uv run pytest`
- validación aislada de la spec con `ppe_detection.tools.check_specs._validate_spec`
- `uv run python -m ppe_detection.tools.ownership --base origin/develop`

## Risks

- Un `\u0060client.get("/health/live")\u0060` dentro de `with TestClient(application)` dispara el
  lifespan: las pruebas limpian `PPE_MODEL_PATH` para garantizar que no se construya el
  detector.
- La respuesta 503 debe usar el mismo esquema que la 200 para que OpenAPI documente el
  contrato completo; `response_model` por sí solo no basta.

## Out of Scope

Ver `spec.md`: HU-046, HU-044 y cambios en `/health` quedan fuera de esta PR.
