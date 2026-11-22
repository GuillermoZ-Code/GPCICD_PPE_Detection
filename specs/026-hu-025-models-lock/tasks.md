---
description: "Task list for HU-025 — Manifiesto canónico del modelo"
---

# Tasks: HU-025 — Manifiesto canónico del modelo (`models.lock`)

**Input**: `specs/026-hu-025-models-lock/spec.md` y `plan.md`.

**Prerequisites**: issue #81, rama `feature/026-hu-025-models-lock`, `develop`
actualizado.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-025.
- [ ] T002 Mover #81 a **In progress** en el tablero.
- [x] T003 Ejecutar `make ownership-check` antes del primer cambio.
      *(El comando no detecta archivos untracked; se repetirá al stagear.)*

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_models_lock_has_required_fields` → AC-01.
- [x] T005 [P] `test_load_model_manifest_reads_toml` → FR-002.
- [x] T006 [P] `test_models_lock_rejects_missing_field` → AC-02.
- [x] T007 [P] `test_models_lock_rejects_invalid_sha` → AC-02.
- [x] T008 [P] `test_load_model_manifest_rejects_invalid_toml` → edge case.
- [x] T009 [P] `test_explicit_manifest_path_is_required_to_exist` → FR-004.
- [x] T010 [P] `test_default_model_identity_uses_manifest` → AC-01/FR-003.
- [x] T011 [P] `test_explicit_environment_wins_over_manifest` → FR-003.
- [x] T012 [P] `test_health_uses_manifest_identity` → AC-03.
- [x] T013 [P] `test_mlflow_payload_uses_manifest_reference` → AC-03.
- [x] T014 Aislar `DEFAULT_MANIFEST_PATH` en las pruebas existentes que asumen que
      no hay manifiesto.
- [x] T015 Ejecutar `uv run pytest tests/test_model_manifest.py tests/test_model_version.py`
      y confirmar rojo antes de implementar.

## Phase 3: Implementation

- [x] T016 Añadir `ModelManifest`, `ModelManifestError`, `DEFAULT_MANIFEST_PATH` y
      `load_model_manifest` en `detector_config.py`.
- [x] T017 Integrar el manifiesto en `default_model_identity()` y
      `default_model_version()` con la precedencia documentada.
- [x] T018 Crear `models.lock` con el SHA256 del `best.pt` de yolo11s.
- [x] T019 Ejecutar las pruebas nuevas y las de HU-013 en verde.

## Phase 4: Evidence and close

- [x] T020 Ejecutar `make ownership-check`.
- [x] T021 Ejecutar `make check`.
- [ ] T022 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md` (archivo
      bloqueado) con el conteo antes/después.
- [ ] T023 Abrir PR a `develop` con la plantilla UAO y `Closes #81`.
- [ ] T024 Tras el merge, cerrar #81 a mano y moverla a Done.

## Notes

- No se descargan pesos ni se modifica el detector.
- `models.lock` es la fuente canónica; `PPE_MODEL_PATH`, `PPE_MODEL_VERSION` y
  `PPE_MODEL_SHA256` siguen funcionando como overrides.
- La integración con Docker y el paquete de GitLab pertenece a HU-024/HU-026.
