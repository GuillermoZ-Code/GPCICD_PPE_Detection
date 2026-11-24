---
description: "Task list for HU-095 — Corregir el inventario y el plan hacia 1.200 pruebas"
---

# Tasks: HU-095 — Corregir el inventario y el plan hacia 1.200 pruebas

**Input**: `specs/096-hu-095-corregir-pruebas-md/spec.md` y `plan.md`.

**Prerequisites**: issue #151, rama `feature/096-hu-095-corregir-pruebas-md`, HU-094
fusionada (#183).

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-095.
- [x] T002 Mover #151 a **In progress** en el tablero (WIP 1).
- [x] T003 Crear la rama `feature/096-hu-095-corregir-pruebas-md` desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_plan_has_one_baseline_and_target` → AC-01.
- [x] T005 [P] `test_plan_splits_remaining_tests_by_integrator` → AC-02.
- [x] T006 [P] `test_plan_documents_counting_command_and_date` → AC-03.
- [x] T007 [P] `test_plan_keeps_correction_history` → AC-01.
- [x] T008 Ejecutar `uv run pytest tests/test_plan_pruebas.py` y confirmar rojo.
      *(4 fallos: el plan seguía en 400/451.)*

## Phase 3: Implementation

- [x] T009 Reescribir `docs/curso/PLAN-PRUEBAS.md` con baseline, brecha y reparto.
- [x] T010 Regenerar `docs/curso/PRUEBAS.md` con `make pruebas-write`. *(533.)*
- [x] T011 Ejecutar las pruebas nuevas en verde.

## Phase 4: Evidence and close

- [x] T012 Ejecutar `make ownership-check`.
- [x] T013 Ejecutar `make check`. *(455 passed + 2 skipped.)*
- [ ] T014 Abrir PR a `develop` con la plantilla UAO y `Closes #151`.
- [ ] T015 Tras el merge, cerrar #151 a mano y moverla a Done.

## Notes

- El AC original (451 + 749) queda superado por la decisión del dueño del backlog
  (23/11/2026): baseline 533 y brecha 667.
- `PRUEBAS.md` no se edita a mano: lo regenera `make pruebas-write`.
