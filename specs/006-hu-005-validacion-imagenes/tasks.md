---
description: "Task list for HU-005 — Validación de imágenes"
---

# Tasks: HU-005 — Validar las imágenes recibidas

**Input**: Design documents from `specs/006-hu-005-validacion-imagenes/`

**Prerequisites**: `plan.md`, `spec.md`, contrato TA-11 y carga de HU-001

**Tests**: obligatorias y **antes** de la implementación (test-first). Cada AC tiene
al menos una prueba que lo referencia.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-005.
- [x] T002 Enlazar la spec en `docs/curso/backlog.md` y `specs/README.md`.

## Phase 2: Tests first (deben fallar)

- [x] T003 [P] `test_corrupt_upload_is_rejected_without_detector` → AC-01.
- [x] T004 [P] `test_empty_upload_is_rejected` → AC-02.
- [x] T005 [P] `test_valid_upload_returns_image_for_preprocessing` → AC-03.
- [x] T006 [P] `test_oversized_upload_is_rejected` → FR-002.
- [x] T007 [P] `test_unsupported_format_is_rejected` → FR-002.
- [x] T008 Ejecutar `uv run pytest tests/test_image_validation.py` en rojo.

## Phase 3: Implementation

- [x] T009 Añadir `MAX_IMAGE_BYTES` y `validate_image_bytes` en `io/images.py`.
- [x] T010 Aplicar el límite en `load_image` antes de leer el archivo.
- [x] T011 Exportar la API pública desde `io/__init__.py`.
- [x] T012 Documentar la validación en `docs/architecture/contracts.md`.

## Phase 4: Verification

- [x] T013 Ejecutar `uv run pytest tests/test_image_validation.py` en verde.
- [x] T014 Ejecutar `make check` y `uv build`.
- [x] T015 Marcar las tareas y el estado de la spec como implementada.
