---
description: "Task list for HU-113 — Informe de cumplimiento de la rúbrica M4"
---

# Tasks: HU-113 — Informe de cumplimiento de la rúbrica M4

**Input**: `specs/114-hu-113-rubrica/spec.md` y `plan.md`.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas.
- [x] T002 Mover #169 a **In progress** en el tablero.
- [x] T003 Crear la rama `feature/114-hu-113-rubrica`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_validate_items_accepts_complete` → AC-03.
- [x] T005 [P] `test_validate_items_rejects_missing_owner` → AC-03.
- [x] T006 [P] `test_build_rows_marks_existing_evidence` → AC-01.
- [x] T007 [P] `test_build_rows_marks_missing_evidence` → AC-02.
- [x] T008 [P] `test_render_lists_all_items` → AC-01.
- [x] T009 [P] `test_render_marks_ok_and_pending` → AC-02.
- [x] T010 [P] `test_write_report_creates_file` → AC-03.
- [x] T011 [P] `test_main_check_passes_with_real_rubric` → AC-03.

## Phase 3: Implementation

- [x] T012 Crear `src/ppe_detection/tools/rubrica.py` con los 14 ítems.
- [x] T013 Añadir `rubrica`, `rubrica-write` y `rubrica-check` al Makefile.
- [x] T014 Generar `docs/entrega/RUBRICA-M4.md` con `make rubrica-write`.
- [x] T015 Enlazar la spec 114 en `docs/curso/backlog.md`.

## Phase 4: Evidence and close

- [x] T016 Ejecutar `make rubrica-check` y `make check`.
- [ ] T017 Abrir PR y cerrar #169 tras el merge.

## Notes

- Los documentos de PRs abiertas quedan ✘ hasta su merge.
- El corte es el 27/11/2026.
