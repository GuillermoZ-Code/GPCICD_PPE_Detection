---
description: "Task list for HU-097 — Runs comparables en MLflow"
---

# Tasks: HU-097 — Runs comparables en MLflow

**Input**: `specs/098-hu-097-runs-mlflow/spec.md` y `plan.md`.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas.
- [x] T002 Mover #153 a **In progress** en el tablero.
- [x] T003 Crear la rama `feature/098-hu-097-runs-mlflow`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_builds_one_payload_per_summary` → AC-01.
- [x] T005 [P] `test_shared_params_are_identical` → AC-01.
- [x] T006 [P] `test_per_class_metrics_are_logged` → AC-01.
- [x] T007 [P] `test_artifact_reference_uses_sha256` → AC-02.
- [x] T008 [P] `test_rejects_different_seed` → AC-03.
- [x] T009 [P] `test_rejects_different_imgsz` → AC-03.
- [x] T010 [P] `test_requires_at_least_two_summaries` → AC-03.
- [x] T011 [P] `test_run_names_are_distinct` → AC-03.

## Phase 3: Implementation

- [x] T012 Añadir `build_comparison_payloads` y exportarlo.
- [x] T013 Ejecutar las pruebas en verde.

## Phase 4: Evidence and close

- [x] T014 Ejecutar `make check` y `make ownership-check`.
- [ ] T015 Abrir PR y cerrar #153 tras el merge.

## Notes

- No se ejecuta MLflow real: los resúmenes son simulados.
- Los pesos no se registran; solo su SHA256.
