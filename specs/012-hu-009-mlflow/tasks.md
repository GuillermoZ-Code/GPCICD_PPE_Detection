---
description: "Task list for HU-009 — Experimentos en MLflow"
---

# Tasks: HU-009 — Consultar y comparar experimentos en MLflow

**Input**: Design documents from `specs/012-hu-009-mlflow/`

**Prerequisites**: `plan.md`, `spec.md`, `summary.json` de HU-008 y MLflow local.

**Tests**: obligatorias y **antes** de la implementación (test-first). Cada AC tiene al
menos una prueba que lo referencia.

## Phase 1: Setup

- [x] T001 Añadir MLflow como extra `tracking` con `uv add --optional tracking`.
- [x] T002 Crear la spec, el plan y las tareas de HU-009.
- [x] T003 Enlazar la spec en `docs/curso/backlog.md`, `specs/README.md` y `docs/README.md`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_build_run_payload_records_model_partition_and_config` → AC-009.1.
- [x] T005 [P] `test_build_run_payload_contains_global_and_per_class_metrics` → AC-009.1.
- [x] T006 [P] `test_build_run_payload_records_dataset_sha_when_provided` → FR-002.
- [x] T007 [P] `test_log_evaluation_run_returns_run_id_and_passes_artifacts` → AC-009.1.
- [x] T008 [P] `test_build_run_payload_rejects_weights` → AC-009.3.
- [x] T009 [P] `test_compare_runs_distinguishes_two_runs` → AC-009.2.
- [x] T010 [P] `test_compare_runs_requires_two_unique_ids` → AC-009.2.
- [x] T011 [P] `test_render_comparison_includes_model_reference` → AC-009.3.
- [x] T012 Ejecutar `uv run pytest tests/test_tracking.py` y confirmar rojo.

## Phase 3: Implementation

- [x] T013 Crear `tracking/mlflow_tracker.py` con `RunPayload`, `RunView` y `TrackingError`.
- [x] T014 Implementar `build_run_payload` y `default_run_name`.
- [x] T015 Implementar `log_evaluation_run`, `compare_runs` y `render_comparison`.
- [x] T016 Implementar `MlflowTracker` con import perezoso de MLflow.
- [x] T017 Implementar la CLI `log` y `compare` y `tracking/__main__.py`.
- [x] T018 Ejecutar `uv run pytest tests/test_tracking.py` en verde (11 pruebas).

## Phase 4: Evidence

- [x] T019 Registrar las evaluaciones reales de 492 y 1.094 en un backend local.
- [x] T020 Comparar los dos `run_id` y guardar la evidencia en `docs/operacion/mlflow.md`.
- [x] T021 Verificar que no se registran pesos ni datasets y que `mlruns/` está ignorado.

## Phase 5: Close

- [x] T022 Documentar el procedimiento de reproducción y la UI de MLflow.
- [x] T023 Ejecutar `make check` (155 passed, 1 skipped) y `uv build`.
- [x] T024 Actualizar `CONSTITUTION.md`, `README.md`, backlog, `specs/README.md` y estado.
- [x] T025 Abrir PR a `develop` y solicitar revisión (PR #50).

## Notes

- No se versionan pesos, dataset, `mlruns/`, `mlartifacts/` ni `mlflow.db`.
- Las pruebas no importan MLflow; usan `FakeTracker`.
- Los `run_id` de la evidencia son locales y no se pueden reproducir fuera de la máquina;
  el nombre del run y las rutas de los `summary.json` sí.
- El extra `tracking` se sincroniza con `uv sync --extra tracking`; para conservar la
  inferencia en el mismo `.venv`, usar `uv sync --all-extras`.
