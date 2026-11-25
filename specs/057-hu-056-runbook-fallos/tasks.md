---
description: "Task list for HU-056 — Runbook de diagnóstico de fallos"
---

# Tasks: HU-056 — Runbook de diagnóstico de fallos

**Input**: `specs/057-hu-056-runbook-fallos/spec.md` y `plan.md`.

**Prerequisites**: issue #112, tarjeta #112 en *In progress* (WIP 1 verificado),
rama `feature/057-hu-056-runbook-fallos` desde `develop`.

**Tests**: obligatorias y antes de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Revisar issue #112, AC y propiedad de archivos.
- [x] T002 Crear spec, plan y tareas.
- [x] T003 Mover #112 a **In progress** en el tablero (WIP 1).
- [x] T004 Crear la rama desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T005 `test_runbook_has_six_stage_decision_tree` → AC-01.
- [x] T006 `test_each_stage_has_symptom_and_action` → AC-01.
- [x] T007 `test_required_commands_are_documented` → AC-02.
- [x] T008 `test_commands_have_expected_interpretation` → AC-02.
- [x] T009 `test_three_drills_are_documented` → AC-03.
- [x] T010 `test_drill_log_distinguishes_static_and_team_validation` → AC-03.

## Phase 3: Implementation

- [x] T011 Escribir `docs/operacion/fallos.md` con árbol, comandos y tres fallos.
- [x] T012 Registrar honestamente la validación estática y el ensayo pendiente.

## Phase 4: Validation and delivery

- [x] T013 Ejecutar ruff, ty, pytest y validación de spec/propiedad.
- [x] T014 Commit convencional y push de la rama.
- [x] T015 Abrir PR a `develop` con plantilla UAO, `Closes #112` y revisor par.
- [x] T016 Dejar la PR pendiente de aprobación (sin merge ni autoaprobación).
