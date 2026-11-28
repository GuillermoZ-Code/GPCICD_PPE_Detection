---
description: "Task list for HU-047 — Logs estructurados JSON con request_id"
---

# Tasks: HU-047 — Logs estructurados JSON con request_id

**Input**: `specs/048-hu-047-logs-json/spec.md` y `plan.md`.

**Prerequisites**: issue #103, rama `feature/048-hu-047-logs-json`, tarjeta #103 en
*In progress* (WIP 1 verificado).

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Revisar issue #103, criterios y propiedad de archivos.
- [x] T002 Crear spec, plan y tareas.
- [x] T003 Mover #103 a **In progress** en el tablero (WIP 1).
- [x] T004 Crear la rama desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T005 `test_logs_method_path_status_latency_and_request_id` → AC-01.
- [x] T006 `test_each_request_emits_one_json_log_record` → AC-01.
- [x] T007 `test_generated_request_id_is_present_in_log` → AC-01.
- [x] T008 `test_log_line_is_valid_json` → AC-01.
- [x] T009 `test_error_responses_are_logged_with_500` → AC-01.
- [x] T010 `test_authorization_header_is_never_logged` → AC-02.
- [x] T011 `test_api_key_header_is_never_logged` → AC-02.
- [x] T012 `test_request_body_is_never_logged` → AC-02.
- [x] T013 `test_image_bytes_are_never_logged` → AC-02.
- [x] T014 `test_request_id_header_is_propagated` → AC-03.
- [x] T015 `test_generated_request_id_is_returned` → AC-03.
- [x] T016 `test_empty_request_id_header_generates_new_identifier` → AC-03.

## Phase 3: Implementation

- [x] T017 Crear `RequestLoggingMiddleware` en `src/ppe_detection/api/logging.py`.
- [x] T018 Registrar una línea JSON por petición con todos los campos.
- [x] T019 Garantizar que no se registran cabeceras, cuerpo ni imágenes.
- [x] T020 Propagar/generar `X-Request-ID` en respuestas normales y de error.
- [x] T021 Instalar el middleware en `create_app`.

## Phase 4: Validation and delivery

- [x] T022 Ejecutar ruff, ty, pytest y validación de spec/propiedad.
- [x] T023 Commit convencional y push de la rama.
- [x] T024 Abrir PR a `develop` con plantilla UAO, `Closes #103` y revisor par.
- [x] T025 Dejar la PR pendiente de aprobación (sin merge ni autoaprobación).
