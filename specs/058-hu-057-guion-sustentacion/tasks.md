---
description: "Task list for HU-057 — Guion de la sustentación M4 y checklist"
---

# Tasks: HU-057 — Guion de la sustentación M4 y checklist

**Input**: `specs/058-hu-057-guion-sustentacion/spec.md` y `plan.md`.

**Prerequisites**: issue #113, tarjeta #113 en *In progress* (WIP 1 verificado),
rama `feature/058-hu-057-guion-sustentacion` desde `develop`.

**Tests**: obligatorias y antes de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Revisar issue #113, AC, rúbrica y propiedad de archivos.
- [x] T002 Crear spec, plan y tareas.
- [x] T003 Mover #113 a **In progress** en el tablero (WIP 1).
- [x] T004 Crear la rama desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T005 `test_ficha_exists_and_has_script` → AC-01.
- [x] T006 `test_script_has_six_time_blocks` → AC-01.
- [x] T007 `test_each_block_has_speaker_and_evidence` → AC-01.
- [x] T008 `test_script_covers_required_topics` → AC-01.
- [x] T009 `test_checklist_has_responsible_column` → AC-02.
- [x] T010 `test_checklist_covers_environment_items` → AC-02.
- [x] T011 `test_timed_rehearsal_log_exists` → AC-03.
- [x] T012 `test_rehearsal_rows_have_goal_real_and_status` → AC-03.
- [x] T013 `test_rehearsal_distinguishes_static_and_team_execution` → AC-03.

## Phase 3: Implementation

- [x] T014 Escribir `docs/entrega/FICHA-M4.md` con guion, checklist y registro.
- [x] T015 Registrar honestamente ensayo estático vs. ensayo del equipo pendiente.

## Phase 4: Validation and delivery

- [x] T016 Ejecutar ruff, ty, pytest y validación de spec/propiedad.
- [x] T017 Commit convencional y push de la rama.
- [x] T018 Abrir PR a `develop` con plantilla UAO, `Closes #113` y revisor par.
- [x] T019 Dejar la PR pendiente de aprobación (sin merge ni autoaprobación).
