---
description: "Task list for HU-021 — Adaptar el detector a YOLO26"
---

# Tasks: HU-021 — Adaptar el detector a YOLO26

**Input**: `specs/022-hu-021-detector-nms-free/spec.md` y `plan.md`.

**Prerequisites**: issue #77, rama `feature/022-hu-021-detector-nms-free`, HU-016
fusionada.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-021.
- [ ] T002 Mover #77 a **In progress** en el tablero.
- [x] T003 Crear la rama desde `develop`.

## Phase 2: Tests first

- [x] T004 [P] `test_yolo26_nms_free_passes_nms_false` → AC-03.
- [x] T005 [P] `test_default_detector_omits_nms` → AC-03.
- [x] T006 [P] `test_yolo11_and_yolo26_outputs_are_equivalent` → AC-01.
- [x] T007 [P] `test_detector_exposes_model_version` → AC-02.
- [x] T008 [P] `test_default_model_version_infers_from_artifact` → AC-02.
- [x] T009 [P] `test_health_uses_artifact_version` → AC-02.
- [x] T010 Ejecutar las pruebas nuevas y confirmar rojo.

## Phase 3: Implementation

- [x] T011 Añadir `nms` a `YoloDetector` y pasarlo condicionalmente.
- [x] T012 Añadir `model_version` a `YoloDetector`.
- [x] T013 Ajustar `default_model_version` para preferir el artefacto.
- [x] T014 Verificar que el contrato y los tests existentes siguen en verde.

## Phase 4: Verification and close

- [x] T015 Ejecutar `make ownership-check`.
- [x] T016 Ejecutar `make check` (416 passed, 1 skipped).
- [ ] T017 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md`.
- [ ] T018 Abrir PR a `develop` con la plantilla UAO y `Closes #77`.
- [ ] T019 Tras el merge, cerrar #77 a mano y moverla a Done.

## Notes

- No se cambia el contrato `list[Detection]`.
- No se modifica `models.lock`.
- El smoke real con `best.pt` de YOLO26n pasó con `nms=False`.
