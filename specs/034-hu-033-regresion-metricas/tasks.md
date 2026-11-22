---
description: "Task list for HU-033 — Pruebas de regresión de métricas"
---

# Tasks: HU-033 — Pruebas de regresión de métricas

**Input**: `specs/034-hu-033-regresion-metricas/spec.md` y `plan.md`.

**Prerequisites**: issue #89, rama `feature/034-hu-033-regresion-metricas`,
`develop` actualizado.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-033.
- [ ] T002 Mover #89 a **In progress** en el tablero.
- [x] T003 Ejecutar `make ownership-check` antes del primer cambio.

## Phase 2: Tests

- [x] T004 [P] `test_golden_iou_known_cases` → AC-01.
- [x] T005 [P] `test_golden_match_detections` → AC-01.
- [x] T006 [P] `test_golden_match_by_class` → AC-01.
- [x] T007 [P] `test_golden_precision_recall_f1` → AC-01.
- [x] T008 [P] `test_golden_average_precision` → AC-01.
- [x] T009 [P] `test_golden_mean_average_precision` → AC-01.
- [x] T010 [P] `test_golden_composite_class_scenario` → AC-01.
- [x] T011 [P] `test_golden_tolerance_is_explicit` → AC-02.
- [x] T012 [P] `test_golden_suite_has_no_optional_imports` → AC-03.
- [x] T013 Ejecutar `uv run pytest tests/test_metrics_golden.py -q` en verde.

## Phase 3: Verification and close

- [x] T014 Ejecutar `make check` (400 passed, 1 skipped).
- [ ] T015 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md` con el conteo.
- [ ] T016 Abrir PR a `develop` con la plantilla UAO y `Closes #89`.
- [ ] T017 Tras el merge, cerrar #89 a mano y moverla a Done.

## Notes

- Esta HU es solo pruebas: no modifica `metrics.py` ni `evaluate.py`.
- Los casos no requieren GPU, dataset, red ni Ultralytics.
- La tolerancia explícita es `1e-12`.
