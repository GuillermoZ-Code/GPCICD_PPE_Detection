---
description: "Task list for HU-100 — Latencia del benchmark en MLflow"
---

# Tasks: HU-100 — Latencia del benchmark en MLflow

**Input**: `specs/101-hu-100-latencia-mlflow/spec.md` y `plan.md`.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas.
- [x] T002 Mover #156 a **In progress** en el tablero.
- [x] T003 Crear la rama `feature/101-hu-100-latencia-mlflow`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_payload_has_p50_and_p95_per_resolution` → AC-01.
- [x] T005 [P] `test_multiple_resolutions_are_separate_metrics` → AC-01.
- [x] T006 [P] `test_p50_uses_nearest_rank` → AC-01.
- [x] T007 [P] `test_payload_records_hardware_params` → AC-02.
- [x] T008 [P] `test_payload_references_model_by_sha` → AC-02.
- [x] T009 [P] `test_rejects_invalid_sha` → AC-02.
- [x] T010 [P] `test_rejects_empty_measurements` → AC-03.
- [x] T011 [P] `test_rejects_non_positive_samples` → AC-03.

## Phase 3: Implementation

- [x] T012 Añadir `ResolutionLatency`, `build_latency_payload` y `p50_ms`.
- [x] T013 Exportar y ejecutar las pruebas en verde.

## Phase 4: Evidence and close

- [x] T014 Ejecutar `make check` y `make ownership-check`.
- [ ] T015 Abrir PR y cerrar #156 tras el merge.

## Notes

- No se ejecuta MLflow real.
- El hardware y la versión son parámetros del run.
