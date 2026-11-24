---
description: "Task list for HU-108 — Retrospectiva y lecciones aprendidas"
---

# Tasks: HU-108 — Retrospectiva y lecciones aprendidas

**Input**: `specs/109-hu-108-retrospectiva/spec.md` y `plan.md`.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas.
- [x] T002 Mover #164 a **In progress** en el tablero.
- [x] T003 Crear la rama `feature/109-hu-108-retrospectiva`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_document_has_retro_sections` → AC-03.
- [x] T005 [P] `test_all_integrators_have_sections` → AC-01.
- [x] T006 [P] `test_sections_have_items` → AC-01.
- [x] T007 [P] `test_actions_have_owner_and_date` → AC-02.

## Phase 3: Implementation

- [x] T008 Escribir `docs/curso/M4/RETRO.md`.
- [x] T009 Enlazar la spec 109 en `docs/curso/backlog.md`.
- [x] T010 Ejecutar las pruebas en verde.

## Phase 4: Evidence and close

- [x] T011 Ejecutar `make check` y `make ownership-check`.
- [ ] T012 Abrir PR y cerrar #164 tras el merge.

## Notes

- Cuatro integrantes, tres listas cada uno y acciones con fecha.
- Se evalúan prácticas, no personas.
