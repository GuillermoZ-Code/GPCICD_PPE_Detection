---
description: "Task list for HU-091 — Plantilla de issue HU con AC y DoR/DoD"
---

# Tasks: HU-091 — Plantilla de issue HU con AC y DoR/DoD

**Input**: `specs/092-hu-091-plantilla-hu/spec.md` y `plan.md`.

**Prerequisites**: issue #147, rama `feature/092-hu-091-plantilla-hu`, `develop`
actualizado (`64683dd`).

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-091.
- [x] T002 Mover #147 a **In progress** en el tablero (WIP 1).
- [x] T003 Crear la rama `feature/092-hu-091-plantilla-hu` desde `develop`.
- [x] T004 Ejecutar `make ownership-check` antes del primer cambio.

## Phase 2: Tests first (deben fallar)

- [x] T005 [P] `test_hu_template_is_valid_yaml` → AC-03.
- [x] T006 [P] `test_hu_template_form_contract` → AC-03.
- [x] T007 [P] `test_hu_template_has_unique_field_ids` → AC-03.
- [x] T008 [P] `test_hu_template_requests_required_fields` → AC-01.
- [x] T009 [P] `test_hu_template_uses_fibonacci_story_points` → AC-01.
- [x] T010 [P] `test_hu_template_has_dor_and_dod_checklists` → AC-02.
- [x] T011 Ejecutar `uv run pytest tests/test_issue_template.py` y confirmar rojo.
      *(6 fallos por `FileNotFoundError` antes de crear la plantilla.)*

## Phase 3: Implementation

- [x] T012 Crear `.github/ISSUE_TEMPLATE/hu.yml` con los seis campos y los dos
      checklists.
- [x] T013 Ejecutar las pruebas nuevas en verde.

## Phase 4: Evidence and close

- [x] T014 Ejecutar `make ownership-check`.
- [x] T015 Ejecutar `make check`. *(429 passed + 2 skipped.)*
- [ ] T016 Abrir PR a `develop` con la plantilla UAO y `Closes #147`.
- [ ] T017 Tras el merge, cerrar #147 a mano y moverla a Done.

## Notes

- No se añaden dependencias: PyYAML ya está como transitiva de `pre-commit`.
- No se tocan las 100 issues existentes, `labels.yml` ni el tablero.
- `docs/curso/PRUEBAS.md` es de otro paso: el conteo se actualiza en el cierre, no en
  esta HU.
