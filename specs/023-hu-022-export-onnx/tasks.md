---
description: "Task list for HU-022 — Exportación ONNX y backend opcional"
---

# Tasks: HU-022 — Exportación ONNX y backend opcional

**Input**: `specs/023-hu-022-export-onnx/spec.md` y `plan.md`.

**Prerequisites**: issue #78, rama `feature/023-hu-022-export-onnx`, HU-020 cerrada.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-022.
- [ ] T002 Mover #78 a **In progress** en el tablero.
- [x] T003 Crear la rama desde `develop`.

## Phase 2: Tests first

- [x] T004 [P] `test_resolve_backend_defaults_to_pt` → AC-03.
- [x] T005 [P] `test_resolve_backend_prefers_onnx` → AC-03.
- [x] T006 [P] `test_resolve_backend_rejects_unknown_format` → edge case.
- [x] T007 [P] `test_resolve_backend_requires_existing_onnx` → edge case.
- [x] T008 [P] `test_export_onnx_writes_manifest` → AC-01.
- [x] T009 [P] `test_export_onnx_requires_optional_dependencies` → edge case.
- [x] T010 [P] `test_compare_detections_within_tolerance` → AC-02.
- [x] T011 [P] `test_compare_detections_reports_difference` → AC-02.
- [x] T012 [P] `test_build_detector_uses_onnx` → AC-03.
- [x] T013 Ejecutar las pruebas nuevas y confirmar rojo.

## Phase 3: Implementation

- [x] T014 Crear `src/ppe_detection/detection/onnx.py`.
- [x] T015 Integrar `PPE_MODEL_FORMAT` en `build_detector`.
- [x] T016 Implementar exportación y manifiesto.
- [x] T017 Ejecutar las pruebas en verde (9 passed).

## Phase 4: Verification and close

- [x] T018 Ejecutar `make ownership-check`.
- [x] T019 Ejecutar `make check` (455 passed, 1 skipped).
- [ ] T020 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md`.
- [ ] T021 Abrir PR a `develop` con la plantilla UAO y `Closes #78`.
- [ ] T022 Tras el merge, cerrar #78 a mano y moverla a Done.

## Notes

- No se agregan dependencias obligatorias.
- El export es estático a 640 por omisión.
- La comparación de detecciones es una utilidad de validación.
