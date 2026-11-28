# Tasks: HU-063 — Prueba de carga ligera e informe de capacidad

**Input**: `specs/064-hu-063-prueba-carga/spec.md` y `plan.md`.

**Prerequisites**: issue #119 en *In progress*, rama desde `origin/develop`, `develop` actualizado.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/064-hu-063-prueba-carga` desde `origin/develop`.
- [x] T002 Mover #119 a *In progress* antes del primer commit.
- [x] T003 Crear spec, plan y tasks.

## Phase 2: Tests (test-first)

- [x] T004 [AC-01] `test_ac01_parse_args_defaults_and_validation`.
- [x] T005 [AC-01] `test_ac01_rejects_invalid_configuration`.
- [x] T006 [AC-01] `test_ac01_sends_get_requests_through_client`.
- [x] T007 [AC-01] `test_ac01_sends_multipart_post_when_image_is_given`.
- [x] T008 [AC-01] `test_ac01_concurrency_configures_executor`.
- [x] T009 [AC-01] `test_ac01_forwards_timeout_and_auth`.
- [x] T010 [AC-02] `test_ac02_percentile_uses_nearest_rank`.
- [x] T011 [AC-02] `test_ac02_counts_successes_and_normalizes_errors`.
- [x] T012 [AC-02] `test_ac02_computes_throughput_from_elapsed_time`.
- [x] T013 [AC-02] `test_ac02_captures_cpu_ram_and_rss_samples`.
- [x] T014 [AC-02] `test_ac02_report_contains_metrics`.
- [x] T015 [AC-02] `test_ac02_report_labels_local_validation_not_real_droplet`.
- [x] T016 [AC-03] `test_ac03_recommends_small_droplet_when_headroom`.
- [x] T017 [AC-03] `test_ac03_recommends_medium_droplet_when_p95_grows`.
- [x] T018 [AC-03] `test_ac03_recommends_large_droplet_or_error_fix`.
- [x] T019 [AC-03] `test_ac03_report_shows_recommendation_and_reproduction`.
- [x] T020 Ejecutar `uv run pytest tests/test_load_test.py -q` en fase roja.

## Phase 3: Implementation

- [x] T021 Crear `src/ppe_detection/tools/load_test.py` con CLI, ejecución y métricas.
- [x] T022 Generar `docs/operacion/capacidad.md` desde una validación local.
- [x] T023 Ejecutar la fase verde de las 16 pruebas.

## Phase 4: Verification and close

- [x] T024 Ejecutar `uv run pytest` completo.
- [x] T025 Ejecutar Ruff, formato, `ty`, specs y propiedad.
- [x] T026 Comitear, hacer push y abrir PR `Closes #119` con revisor Guillermo.
- [x] T027 Vigilar CI y mover #119 a *In review*.
- [x] T028 Solicitar a Jesús la regeneración de `docs/curso/PRUEBAS.md`.
- [x] T029 Publicar el bloqueo de HU-058 en #114 por dependencia de HU-077/#133.

## Notes

- Ninguna medición local se presenta como capacidad real del Droplet.
- Guillermo ejecutará la validación real contra el servidor desplegado.
- `src/ppe_detection/tools/` y `specs/` tienen dueño Jesús: se pide revisión, no se bloquea.
