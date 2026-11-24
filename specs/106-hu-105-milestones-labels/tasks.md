---
description: "Task list for HU-105 — Milestones y labels de las nuevas épicas"
---

# Tasks: HU-105 — Milestones y labels de las nuevas épicas

**Input**: `specs/106-hu-105-milestones-labels/spec.md` y `plan.md`.

**Prerequisites**: issue #161, rama `feature/106-hu-105-milestones-labels`, `develop`
actualizado (`c33d978`).

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-105.
- [x] T002 Mover #161 a **In progress** en el tablero (WIP 1).
- [x] T003 Crear la rama `feature/106-hu-105-milestones-labels` desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_labels_is_a_list_of_mappings` → AC-02.
- [x] T005 [P] `test_labels_have_unique_name_color_and_description` → AC-03.
- [x] T006 [P] `test_labels_cover_all_epics` → AC-01.
- [x] T007 [P] `test_labels_cover_priorities` → AC-01.
- [x] T008 Ejecutar `uv run pytest tests/test_labels.py` y confirmar rojo.
      *(2 fallos por `ep-06`…`ep-15` y `could-have` ausentes.)*

## Phase 3: Implementation

- [x] T009 Añadir `ep-06`…`ep-15` a `.github/labels.yml` con color y descripción.
- [x] T010 Añadir `could-have`.
- [x] T011 Ejecutar las pruebas nuevas en verde.

## Phase 4: GitHub

- [x] T012 Confirmar que `M3-S1` y `M3-S2` tienen cero issues abiertas.
- [x] T013 Cerrar los dos milestones con `gh api`.

## Phase 5: Evidence and close

- [x] T014 Ejecutar `make ownership-check` (aviso esperado en `labels.yml`).
- [x] T015 Ejecutar `make check`. *(431 passed + 2 skipped.)*
- [ ] T016 Abrir PR a `develop` con la plantilla UAO y `Closes #161`.
- [ ] T017 Tras el merge, verificar que el workflow `Labels` sincronizó, cerrar #161 y
      moverla a Done.

## Notes

- `labels.yml` no está en `[[locked]]`: se edita con aviso y revisión, no con bloqueo.
- El workflow `Labels` no borra etiquetas ajenas (`skip-delete: true`).
