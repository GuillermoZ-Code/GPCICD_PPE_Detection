---
description: "Task list for HU-107 — Definición de Ready y Done del M4"
---

# Tasks: HU-107 — Definición de Ready y Done del M4

**Input**: `specs/108-hu-107-dor-dod/spec.md` y `plan.md`.

**Prerequisites**: issue #163, rama `feature/108-hu-107-dor-dod`, `develop`
actualizado (`64683dd`).

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-107.
- [x] T002 Mover #163 a **In progress** en el tablero (WIP 1).
- [x] T003 Crear la rama `feature/108-hu-107-dor-dod` desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_dor_lists_entry_criteria` → AC-01.
- [x] T005 [P] `test_dod_lists_exit_criteria` → AC-02.
- [x] T006 [P] `test_contributing_has_dor_dod_sections` → AC-03.
- [x] T007 [P] `test_dor_and_dod_items_are_checkboxes` → AC-03.
- [x] T008 Ejecutar `uv run pytest tests/test_dor_dod.py` y confirmar rojo.
      *(4 fallos por sección ausente antes de editar la guía.)*

## Phase 3: Implementation

- [x] T009 Añadir la sección «Criterios de entrada y salida (DoR / DoD)» a
      `CONTRIBUTING.md`.
- [x] T010 Añadir la entrada a la tabla de contenidos.
- [x] T011 Ejecutar las pruebas nuevas en verde.

## Phase 4: Evidence and close

- [x] T012 Ejecutar `make ownership-check`.
- [x] T013 Ejecutar `make check`. *(427 passed + 2 skipped.)*
- [ ] T014 Abrir PR a `develop` con la plantilla UAO y `Closes #163`.
- [ ] T015 Tras el merge, cerrar #163 a mano y moverla a Done.

## Notes

- No se reescribe el resto de `CONTRIBUTING.md`; los datos obsoletos se reportan aparte.
- `docs/curso/PRUEBAS.md` lo actualiza su dueño en el cierre, no esta HU.
