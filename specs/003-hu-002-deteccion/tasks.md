---
description: "Task list for HU-002 — Detección de EPP"
---

# Tasks: HU-002 — Detectar las seis categorías de EPP

**Input**: Design documents from `specs/003-hu-002-deteccion/`

**Prerequisites**: `plan.md`, `spec.md`, contrato TA-11 y carga de HU-001

**Tests**: obligatorias y **antes** de la implementación (test-first). Cada AC tiene
al menos una prueba que lo referencia.

## Phase 1: Setup

- [x] T001 Agregar `ultralytics` como extra opcional `inference` con `uv add`.
- [x] T002 Crear `tests/test_yolo_detector.py` con modelo falso inyectado.

## Phase 2: Tests first (deben fallar)

- [x] T003 [P] `test_detector_maps_boxes_to_detections` → AC-01.
- [x] T004 [P] `test_detector_uses_canonical_catalog` → AC-02.
- [x] T005 [P] `test_detector_clips_boxes_to_image` → AC-03.
- [x] T006 [P] `test_detector_returns_empty_list_without_boxes` → FR-006.
- [x] T007 [P] `test_detector_converts_rgb_to_bgr` → contrato de entrada.
- [x] T008 [P] `test_detector_skips_degenerate_boxes` → FR-005.
- [x] T009 [P] `test_detector_rejects_wrong_catalog` → FR-003.
- [x] T010 [P] `test_detector_rejects_out_of_range_class` → FR-004.
- [x] T011 [P] `test_detector_passes_thresholds_to_model` → FR-007.
- [x] T012 `uv run pytest tests/test_yolo_detector.py` en rojo.

## Phase 3: Implementación

- [x] T013 `detection/yolo.py`: `YoloDetector`, carga perezosa y mapeo a `Detection`.
- [x] T014 `detection/__init__.py` con la API pública.
- [x] T015 `tests/test_predict.py`: CLI, CSV, resumen y detecciones vacías.
- [x] T016 `detection/predict.py`: CLI que reutiliza `load_image` y `YoloDetector`.
- [x] T017 `uv run pytest` en verde.

## Phase 4: Polish

- [x] T018 Documentar el adaptador en `docs/architecture/contracts.md`.
- [x] T019 Ejecutar la prueba real con `artifacts/models/*/weights/best.pt` y registrar
      la evidencia en el PR (sin versionar pesos).
- [x] T020 `make check` y `uv build`.

## Dependencies & Execution Order

- T001 → T002 → T003–T011 → T012 → T013–T017 → T018–T020.
- T003–T011 pueden escribirse en paralelo.
- T015 depende de T013/T014; T016 depende de T015.

## Notes

- Sin GPU, dataset, pesos ni red en las pruebas unitarias.
- La prueba real usa `pytest.importorskip("ultralytics")` y se omite si faltan pesos.
- La evaluación formal (mAP, precision, recall) es HU-008; se enlaza SPI-02.
- No se dibujan cajas: eso es HU-003.
