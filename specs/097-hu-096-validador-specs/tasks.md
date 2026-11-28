---
description: "Task list for HU-096 — Validador de specs SDD"
---

# Tasks: HU-096 — Validador de specs SDD

**Input**: `specs/097-hu-096-validador-specs/spec.md` y `plan.md`.

**Prerequisites**: issue #152, rama `feature/097-hu-096-validador-specs`.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-096.
- [x] T002 Mover #152 a **In progress** en el tablero (WIP 1).
- [x] T003 Crear la rama `feature/097-hu-096-validador-specs` desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_missing_spec_file_fails` → AC-01.
- [x] T005 [P] `test_missing_plan_file_fails` → AC-01.
- [x] T006 [P] `test_missing_tasks_file_fails` → AC-01.
- [x] T007 [P] `test_declared_ac_without_row_fails` → AC-01.
- [x] T008 [P] `test_broken_test_reference_fails` → AC-01.
- [x] T009 [P] `test_document_evidence_is_accepted` → AC-01.
- [x] T010 [P] `test_main_returns_nonzero_with_problems` → AC-02.
- [x] T011 [P] `test_legacy_spec_only_checks_files` → AC-03.
- [x] T012 Ejecutar `uv run pytest tests/test_tools_check_specs.py` y confirmar rojo.
      *(ImportError: el modulo no existia.)*

## Phase 3: Implementation

- [x] T013 Crear `src/ppe_detection/tools/check_specs.py`.
- [x] T014 Añadir el objetivo `specs-check` al Makefile.
- [x] T015 Crear `.github/workflows/specs.yml` con el job de CI.

## Phase 4: Evidence and close

- [x] T016 Ejecutar `make specs-check`.
- [x] T017 Ejecutar `make check`.
- [ ] T018 Abrir PR a `develop` con la plantilla UAO y `Closes #152`.
- [ ] T019 Tras el merge, cerrar #152 a mano y moverla a Done.

## Notes

- Las specs anteriores a 092 se validan solo por archivos; `--strict` las revisa.
- La evidencia documental es válida: una HU documental no tiene pruebas unitarias.
- El validador no modifica archivos.
