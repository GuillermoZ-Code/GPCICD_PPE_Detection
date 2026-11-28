---
description: "Task list for HU-092 — Sincronizar backlog.md con las 113 HU"
---

# Tasks: HU-092 — Sincronizar `backlog.md` con las 113 HU

**Input**: `specs/093-hu-092-backlog-espejo/spec.md` y `plan.md`.

**Prerequisites**: issue #148, rama `feature/093-hu-092-backlog-espejo`, HU-089 cerrada.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-092.
- [x] T002 Mover #148 a **In progress** en el tablero (WIP 1).
- [x] T003 Crear la rama `feature/093-hu-092-backlog-espejo` desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_backlog_lists_all_113_hus` → AC-01.
- [x] T005 [P] `test_backlog_m4_rows_have_epic_sp_wave_and_spec` → AC-01.
- [x] T006 [P] `test_backlog_totals_match_rows` → AC-02.
- [x] T007 [P] `test_backlog_specs_match_repository` → AC-03.
- [x] T008 Ejecutar `uv run pytest tests/test_backlog_mirror.py` y confirmar rojo.
      *(4 fallos: el espejo seguía en 15 HU.)*

## Phase 3: Implementation

- [x] T009 Regenerar `docs/curso/backlog.md` con las 113 HU.
- [x] T010 Ejecutar las pruebas nuevas en verde.

## Phase 4: Evidence and close

- [x] T011 Ejecutar `make ownership-check`.
- [x] T012 Ejecutar `make check`.
- [ ] T013 Abrir PR a `develop` con la plantilla UAO y `Closes #148`.
- [ ] T014 Tras el merge, cerrar #148 a mano y moverla a Done.

## Notes

- El espejo es una instantánea: no se regenera en cada push.
- Los AC literales de cada HU siguen en su issue; el espejo resume y enlaza.
- HU-014 y HU-015 se cuentan en el M4, por eso el total es 219 SP.
