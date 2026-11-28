---
description: "Task list for HU-029 — Calibración de umbrales por clase"
---

# Tasks: HU-029 — Calibración de umbrales por clase

**Input**: `specs/030-hu-029-umbrales-por-clase/spec.md` y `plan.md`.

**Prerequisites**: issue #85, rama `feature/030-hu-029-umbrales-por-clase`,
`develop` actualizado.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-029.
- [ ] T002 Mover #85 a **In progress** en el tablero.
- [ ] T003 Ejecutar `make ownership-check` antes del primer cambio.

## Phase 2: Tests

- [x] T004 [P] `test_calibrate_maximizes_f1_for_gloves` → AC-01.
- [x] T005 [P] `test_calibrate_uses_all_validation_records` → AC-01.
- [x] T006 [P] `test_calibrate_handles_class_without_ground_truth` → AC-01.
- [x] T007 [P] `test_calibrate_handles_class_without_predictions` → AC-01.
- [x] T008 [P] `test_calibrate_ties_prefer_higher_threshold` → AC-01.
- [x] T009 [P] `test_evaluate_thresholds_returns_before_after_counts` → AC-02.
- [x] T010 [P] `test_calibration_payload_is_traceable` → AC-02.
- [x] T011 [P] `test_threshold_map_has_all_canonical_classes` → AC-03.
- [x] T012 [P] `test_write_and_load_thresholds_roundtrip` → AC-03.
- [x] T013 [P] `test_write_thresholds_rejects_missing_class` → AC-03.
- [x] T014 [P] `test_repository_thresholds_yaml_has_six_classes` → AC-03.

## Phase 3: Implementation

- [x] T015 Implementar `GroundTruth`, `Prediction`, `ImageRecord` y
  `ThresholdMetrics`.
- [x] T016 Implementar `calibrate_thresholds` con rejilla y desempate.
- [x] T017 Implementar `evaluate_thresholds` y `calibration_payload`.
- [x] T018 Implementar `write_thresholds` y `load_thresholds` sin PyYAML.
- [x] T019 Recolectar predicciones de YOLO26n en validación y test.
- [x] T020 Escribir `configs/thresholds.yaml`.
- [x] T021 Escribir `docs/evaluation/umbrales.md` con tablas antes/después.
- [x] T022 Ejecutar `uv run pytest tests/test_thresholds.py -q` en verde.

## Phase 4: Verification and close

- [ ] T023 Ejecutar `make check` y resolver el espejo del backlog.
- [ ] T024 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md` y del
  backlog con la spec 030.
- [ ] T025 Abrir PR a `develop` con la plantilla UAO y `Closes #85`.
- [ ] T026 Tras el merge, cerrar #85 a mano y moverla a Done.

## Notes

- La calibración pura no importa Ultralytics, torch, OpenCV ni YAML.
- El test se usa solo para la tabla antes/después; nunca para elegir umbrales.
- `configs/thresholds.yaml` es el contrato que consumirá HU-036.
