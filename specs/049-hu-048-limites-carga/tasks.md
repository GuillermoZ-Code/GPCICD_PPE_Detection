---
description: "Task list for HU-048 — Límites de tamaño y tipo de archivo en REST"
---

# Tasks: HU-048 — Límites de tamaño y tipo de archivo en REST

**Input**: `specs/049-hu-048-limites-carga/spec.md` y `plan.md`.

**Prerequisites**: issue #104, rama `feature/049-hu-048-limites-carga`, tarjeta #104 en
*In progress* (WIP 1 verificado).

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Revisar issue #104, criterios y propiedad de archivos.
- [x] T002 Crear spec, plan y tareas.
- [x] T003 Mover #104 a **In progress** en el tablero (WIP 1).
- [x] T004 Crear la rama desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T005 `test_file_above_configured_limit_returns_413` → AC-01.
- [x] T006 `test_default_limit_allows_small_image` → AC-01.
- [x] T007 `test_disallowed_mime_returns_415` → AC-02.
- [x] T008 `test_mime_with_parameters_is_accepted` → AC-02.
- [x] T009 `test_415_message_names_allowed_types` → AC-02.
- [x] T010 `test_valid_jpeg_is_still_accepted` → AC-02.
- [x] T011 `test_service_responds_after_rejection` → AC-03.
- [x] T012 `test_valid_prediction_after_rejection` → AC-03.

## Phase 3: Implementation

- [x] T013 Implementar `_configured_upload_bytes()` y `_is_allowed_type()` en `app.py`.
- [x] T014 Aplicar compuerta 413 antes de decodificar.
- [x] T015 Aplicar compuerta 415 por MIME.
- [x] T016 Verificar que el detector no se muta en los rechazos.

## Phase 4: Validation and delivery

- [x] T017 Ejecutar ruff, ty, pytest y validación de spec/propiedad.
- [x] T018 Commit convencional y push de la rama.
- [x] T019 Abrir PR a `develop` con plantilla UAO, `Closes #104` y revisor par.
- [x] T020 Dejar la PR pendiente de aprobación (sin merge ni autoaprobación).
