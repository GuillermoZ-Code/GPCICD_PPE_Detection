---
description: "Task list for HU-034 — Pruebas de contrato del detector con YOLO26"
---

# Tasks: HU-034 — Pruebas de contrato del detector con YOLO26

**Input**: `specs/035-hu-034-contrato-yolo26/spec.md` y `plan.md`.

**Prerequisites**: issue #90, rama `feature/035-hu-034-contrato-yolo26`,
`develop` actualizado.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-034.
- [ ] T002 Mover #90 a **In progress** en el tablero.
- [x] T003 Ejecutar `make ownership-check` antes del primer cambio.

## Phase 2: Tests

- [x] T004 [P] `test_contract_catalog_matches_yaml_order` → AC-01.
- [x] T005 [P] `test_contract_confidence_stays_in_closed_range` → AC-02.
- [x] T006 [P] `test_contract_boxes_stay_inside_image` → AC-02.
- [x] T007 [P] `test_contract_fake_yolo26_output_maps_all_classes` → AC-03.
- [x] T008 [P] `test_contract_rejects_class_outside_catalog` → AC-01.
- [x] T009 [P] `test_contract_rejects_catalog_outside_epp` → AC-01.
- [x] T010 Ejecutar `uv run pytest tests/test_detector_contract.py -q` en verde.

## Phase 3: Verification and close

- [x] T011 Ejecutar `make specs-check` (debe incluir la spec 035).
- [x] T012 Ejecutar `make check`.
- [ ] T013 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md` con las
  8 pruebas nuevas.
- [ ] T014 Abrir PR a `develop` con la plantilla UAO y `Closes #90`.
- [ ] T015 Tras el merge, cerrar #90 a mano y moverla a Done.

## Notes

- La suite no carga Ultralytics, GPU, dataset ni red.
- No se modifica `src/ppe_detection/detection/yolo.py`.
- El modelo falso imita `Results.boxes` y `nms=False` de YOLO26.
