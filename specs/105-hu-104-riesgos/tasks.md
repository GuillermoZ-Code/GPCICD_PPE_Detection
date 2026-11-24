---
description: "Task list for HU-104 — Registro de riesgos del M4"
---

# Tasks: HU-104 — Registro de riesgos del M4

**Input**: `specs/105-hu-104-riesgos/spec.md` y `plan.md`.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas.
- [x] T002 Mover #160 a **In progress** en el tablero.
- [x] T003 Crear la rama `feature/105-hu-104-riesgos`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_file_exists` → AC-01.
- [x] T005 [P] `test_all_categories_present` → AC-01.
- [x] T006 [P] `test_every_risk_has_owner_and_trigger` → AC-02.
- [x] T007 [P] `test_minimum_number_of_risks` → AC-03.

## Phase 3: Implementation

- [x] T008 Escribir `docs/curso/M4/RIESGOS.md` con diez riesgos.
- [x] T009 Enlazar la spec 105 en `docs/curso/backlog.md`.
- [x] T010 Ejecutar las pruebas en verde.

## Phase 4: Evidence and close

- [x] T011 Ejecutar `make check` y `make ownership-check`.
- [ ] T012 Abrir PR y cerrar #160 tras el merge.

## Notes

- Categorías: infraestructura, CI, modelo y equipo.
- El estado se revisa al cierre del 26/11.
