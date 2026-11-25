# Implementation Plan: HU-047 — Logs estructurados JSON con request_id

**Branch**: `feature/048-hu-047-logs-json` | **Date**: 2026-11-24

**Spec**: [spec.md](spec.md)

**Input**: Issue #103 y `specs/048-hu-047-logs-json/spec.md`.

## Summary

Añadir `RequestLoggingMiddleware` en `src/ppe_detection/api/logging.py` e instalarlo en
`create_app()`. Cada petición produce una línea JSON con método, ruta, estado, latencia
y `request_id`; la cabecera `X-Request-ID` se propaga o se genera con `uuid4`. No se
registran cabeceras sensibles ni cuerpos.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: FastAPI/Starlette, `json`, `logging`, `uuid` (ya presentes)

**Storage**: ninguno; salida por `logging` estándar

**Testing**: pytest + `caplog` + `TestClient`, sin red ni GPU

**Target Platform**: CPU, Windows/Linux

**Project Type**: middleware dentro de la API

**Constraints**: una HU por PR; test-first; sin dependencias nuevas; no tocar `.github/`.

## Design

1. `RequestLoggingMiddleware(BaseHTTPMiddleware)` con `dispatch`.
2. Obtener `request_id` de `X-Request-ID` (si está vacío, generar `uuid4`).
3. Medir latencia con `perf_counter`, ejecutar `call_next`.
4. Capturar excepciones: registrar estado 500 sin mensaje de excepción y devolver
   `JSONResponse` segura con la cabecera `X-Request-ID`.
5. Registrar `json.dumps(payload, sort_keys=True, ensure_ascii=False)` en
   `logging.getLogger("ppe_detection.api")` una sola vez.
6. Añadir la cabecera a la respuesta normal.
7. `create_app()` instala el middleware.

## Test-first plan

- Crear `tests/test_api_logs_json.py` con 12 pruebas AC-01/02/03.
- Verificar que fallan antes de crear el módulo.
- Implementar y repetir suite completa.

## Validation

- `uv run pytest -v tests/test_api_logs_json.py`
- `uv run ruff check .` · `uv run ruff format --check .` · `uv run ty check`
- `uv run pytest -v`
- validación aislada de la spec con `check_specs._validate_spec`
- `uv run python -m ppe_detection.tools.ownership --base origin/develop`

## Risks

- `BaseHTTPMiddleware` envuelve también `/health`; el volumen de logs aumenta, pero es
  una línea JSON por petición y no incluye datos sensibles.
- Capturar excepciones en el middleware evita que se filtren detalles en el log; el
  cliente recibe un 500 genérico.

## Out of Scope

Ver `spec.md`: persistencia, paneles y logs gRPC quedan fuera.
