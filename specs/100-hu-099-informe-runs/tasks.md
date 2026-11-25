---
description: "Task list for HU-099 — Informe comparativo de runs"
---

# Tasks: HU-099 — Informe comparativo de runs

**Input**: `specs/100-hu-099-informe-runs/spec.md` y `plan.md`.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas.
- [x] T002 Mover #155 a **In progress** en el tablero.
- [x] T003 Crear la rama `feature/100-hu-099-informe-runs`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_report_has_table` → AC-01.
- [x] T005 [P] `test_report_has_one_row_per_run` → AC-01.
- [x] T006 [P] `test_report_shows_metrics` → AC-01.
- [x] T007 [P] `test_report_links_each_run` → AC-02.
- [x] T008 [P] `test_report_shows_artifact_reference` → AC-02.
- [x] T009 [P] `test_report_has_generation_date` → AC-01.
- [x] T010 [P] `test_write_report_creates_file` → AC-03.

## Phase 3: Implementation

- [x] T011 Añadir `render_comparison_report` y exportarlo.
- [x] T012 Generar `docs/evaluation/mlflow-comparacion.md`.
- [x] T013 Ejecutar las pruebas en verde.

## Phase 4: Evidence and close

- [x] T014 Ejecutar `make check` y `make ownership-check`.
- [ ] T015 Abrir PR y cerrar #155 tras el merge.

## Notes

- El informe del repo usa los resúmenes de HU-019; se regenera contra MLflow.
