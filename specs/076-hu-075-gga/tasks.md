# Tasks: HU-075 — GGA en pre-commit

**Input**: `specs/076-hu-075-gga/spec.md` y `plan.md`.

**Prerequisites**: issue #131, `develop` actualizado, GGA disponible en el equipo.

## Phase 1: Setup

- [x] T001 Revisar la instalación local de GGA (`gga v2.10.1`).
- [x] T002 Crear la spec, el plan y las tareas.
- [ ] T003 Mover #131 a **In progress** en el tablero.

## Phase 2: Tests

- [x] T004 [AC-01] `test_gga_config_uses_opencode_and_the_constitution`.
- [x] T005 [AC-01] `test_gga_config_reviews_code_and_excludes_artifacts`.
- [x] T006 [AC-01] `test_gga_config_has_no_literal_tokens`.
- [x] T007 [AC-02] `test_precommit_declares_the_optional_hook`.
- [x] T008 [AC-02] `test_hook_is_not_blocking_when_gga_is_absent`.
- [x] T009 [AC-02] `test_hook_propagates_gga_exit_code_when_available`.
- [x] T010 [AC-02] `test_main_prints_a_skip_message_without_gga`.
- [x] T011 [AC-02] `test_runbook_documents_the_optional_behavior`.
- [x] T012 Ejecutar `uv run pytest tests/test_gga.py -q`.

## Phase 3: Implementation

- [x] T013 Crear `.gga` sin credenciales.
- [x] T014 Implementar `gga_hook.py` con salida 0 si GGA falta.
- [x] T015 Agregar el hook local `gga-optional` a pre-commit.
- [x] T016 Escribir `docs/operacion/gga.md`.
- [x] T017 Ejecutar una revisión real con GGA sobre el diff de la PR.
- [ ] T018 Adjuntar la evidencia de GGA a la PR.

## Phase 4: Verification and close

- [x] T019 Ejecutar `make specs-check`.
- [ ] T020 Ejecutar `make check`.
- [ ] T021 Ejecutar `uv build`.
- [ ] T022 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md`.
- [ ] T023 Abrir PR a `develop` con `Closes #131`.
- [ ] T024 Tras el merge, cerrar #131 a mano y moverla a Done.

## Notes

- GGA no se versiona; el wrapper sí.
- El hook no bloquea a quien no tenga GGA.
- La evidencia real se adjunta a la PR, no al repositorio.
