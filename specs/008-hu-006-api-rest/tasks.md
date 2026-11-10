---
description: "Task list for HU-006 — API REST FastAPI"
---

# Tasks: HU-006 — Consultar inferencias mediante una API REST

**Input**: Design documents from `specs/008-hu-006-api-rest/`

**Prerequisites**: `plan.md`, `spec.md`, contrato TA-11, validación de HU-005 y
`FakeDetector`.

**Tests**: obligatorias y **antes** de la implementación (test-first). Cada AC tiene
al menos una prueba que lo referencia.

## Phase 1: Setup

- [x] T001 Añadir `fastapi`, `uvicorn`, `python-multipart` y `httpx` (dev) con `uv add`.
- [x] T002 Crear la spec, el plan y las tareas de HU-006.
- [x] T003 Enlazar la spec en `docs/curso/backlog.md` y `specs/README.md`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_predict_returns_detections` → AC-01.
- [x] T005 [P] `test_invalid_file_returns_400_and_server_stays_up` → AC-02.
- [x] T006 [P] `test_invalid_file_does_not_invoke_detector` → AC-02/FR-004.
- [x] T007 [P] `test_openapi_documents_predict` → AC-03.
- [x] T008 [P] `test_empty_detections_returns_empty_list` → contrato.
- [x] T009 [P] `test_missing_file_returns_422` → validación FastAPI.
- [x] T010 [P] `test_without_model_returns_503` → edge case.
- [x] T011 Ejecutar `uv run pytest tests/test_api.py` en rojo.

## Phase 3: Implementation

- [x] T012 Crear `api/app.py` con `create_app`, esquemas y `POST /predict`.
- [x] T013 Carga perezosa del detector desde `PPE_MODEL_PATH` y variables de entorno.
- [x] T014 Configurar CORS para el frontend.
- [x] T015 Crear `api/__init__.py` y `api/__main__.py`.
- [x] T016 Documentar el endpoint en `docs/architecture/contracts.md`.

## Phase 4: Verification

- [x] T017 Ejecutar `uv run pytest tests/test_api.py` en verde.
- [x] T018 Ejecutar `make check` y `uv build`.
- [x] T019 Marcar tareas y estado de la spec como implementada.
