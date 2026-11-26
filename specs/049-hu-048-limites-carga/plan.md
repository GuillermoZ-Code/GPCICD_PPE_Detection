# Implementation Plan: HU-048 — Límites de tamaño y tipo de archivo en REST

**Branch**: `feature/049-hu-048-limites-carga` | **Date**: 2026-11-24

**Spec**: [spec.md](spec.md)

**Input**: Issue #104 y `specs/049-hu-048-limites-carga/spec.md`.

## Summary

Añadir compuertas en `POST /predict` antes de decodificar: tamaño máximo configurable
por `PPE_MAX_UPLOAD_MB` (413) y MIME restringido a PNG/JPEG (415). El detector y
`validate_image_bytes` permanecen intactos, por lo que un contenido corrupto con MIME
válido sigue devolviendo 400.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: FastAPI, constantes de `ppe_detection.io.images`; sin nuevas

**Storage**: ninguno; solo lectura de la variable de entorno y de los bytes subidos

**Testing**: pytest, `TestClient`, `FakeDetector`, PNG/JPEG generados con `cv2`

**Target Platform**: CPU, Windows/Linux

**Project Type**: validación de entrada en la API REST

**Constraints**: una HU por PR; test-first; no tocar `.env.example` ni archivos de otros
dueños.

## Design

1. `_configured_upload_bytes()` convierte `PPE_MAX_UPLOAD_MB` a bytes solo si está
   configurado; sin variable se conserva el 400 histórico de `io.images`.
2. `_is_allowed_type(content_type)` normaliza el MIME y acepta solo `image/png` o
   `image/jpeg`.
3. En `predict`: leer bytes, comparar tamaño, comprobar MIME y solo después llamar a
   `validate_image_bytes`.
4. Los errores usan `HTTPException(413/415, detail=...)` con mensajes accionables.
5. No se modifica el estado de la aplicación en las compuertas.

## Test-first plan

- Crear `tests/test_api_upload_limits.py` con 8 pruebas AC-01/02/03.
- Confirmar que fallan antes de tocar `app.py`.
- Implementar y repetir suite completa.

## Validation

- `uv run pytest -v tests/test_api_upload_limits.py`
- `uv run ruff check .` · `uv run ruff format --check .` · `uv run ty check`
- `uv run pytest -v`
- validación aislada de la spec con `check_specs._validate_spec`
- `uv run python -m ppe_detection.tools.ownership --base origin/develop`

## Risks

- Un MIME no permitido ahora es 415; las pruebas M3 que envían bytes corruptos con MIME
  PNG siguen recibiendo 400 desde `io.images`.
- `PPE_MAX_UPLOAD_MB` aún no está en `.env.example` (HU-044, PR #210); se documenta la
  coordinación en la descripción de la PR para evitar un conflicto de archivo compartido.
