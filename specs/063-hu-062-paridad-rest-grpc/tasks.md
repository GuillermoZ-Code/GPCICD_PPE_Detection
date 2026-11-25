---
description: "Task list for HU-062 — Paridad REST/gRPC con el modelo productivo"
---

# Tasks: HU-062 — Paridad REST/gRPC con el modelo productivo

**Input**: `specs/063-hu-062-paridad-rest-grpc/spec.md` y `plan.md`.

**Prerequisites**: issue #118, tarjeta #118 en *In progress* (WIP 1 verificado),
rama `feature/063-hu-062-paridad-rest-grpc` desde `develop` actualizado.

**Tests**: obligatorias y antes de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Revisar issue #118, AC y propiedad de archivos.
- [x] T002 Crear spec, plan y tareas.
- [x] T003 Mover #118 a **In progress** en el tablero (WIP 1).
- [x] T004 Crear la rama desde `develop` actualizado.

## Phase 2: Tests first (deben fallar)

- [x] T005 `test_same_png_returns_identical_detections` → AC-01.
- [x] T006 `test_same_jpeg_is_accepted_by_both_protocols` → AC-01.
- [x] T007 `test_empty_result_is_equivalent` → AC-01.
- [x] T008 `test_detection_order_and_bbox_are_equivalent` → AC-01.
- [x] T009 `test_model_identity_is_equivalent` → AC-01.
- [x] T010 `test_both_protocols_report_same_image_dimensions` → AC-01.
- [x] T011 `test_invalid_image_maps_400_to_invalid_argument` → AC-02.
- [x] T012 `test_missing_model_maps_503_to_unavailable` → AC-02.
- [x] T013 `test_detection_time_unconfigured_maps_503_to_unavailable` → AC-02.
- [x] T014 `test_service_recovers_after_rejection` → AC-02.
- [x] T015 `test_shared_fake_detector_needs_no_model_weights` → AC-03.
- [x] T016 `test_shared_fake_detector_is_called_once_per_protocol` → AC-03.
- [x] T017 `test_shared_fake_detector_confidences_match` → AC-03.

## Phase 3: Implementation

- [x] T018 Mapear `DetectorNotConfiguredError` durante `detect()` a HTTP 503 en `app.py`.
- [x] T019 Verificar que el detalle REST y gRPC es el mismo y que el servicio sigue arriba.

## Phase 4: Validation and delivery

- [x] T020 Ejecutar ruff, ty, pytest y validación de spec/propiedad.
- [x] T021 Commit convencional y push de la rama.
- [x] T022 Abrir PR a `develop` con plantilla UAO, `Closes #118` y revisor par.
- [x] T023 Dejar la PR pendiente de aprobación (sin merge ni autoaprobación).
