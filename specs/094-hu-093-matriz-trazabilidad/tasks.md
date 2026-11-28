---
description: "Task list for HU-093 — Matriz de trazabilidad"
---

# Tasks: HU-093 — Matriz de trazabilidad HU → issue → spec → PR → pruebas

**Input**: `specs/094-hu-093-matriz-trazabilidad/spec.md` y `plan.md`.

**Prerequisites**: issue #149, rama `feature/094-hu-093-matriz-trazabilidad`, HU-089
cerrada.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-093.
- [x] T002 Mover #149 a **In progress** en el tablero (WIP 1).
- [x] T003 Crear la rama `feature/094-hu-093-matriz-trazabilidad` desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_specs_map_hu_to_directory` → AC-01.
- [x] T005 [P] `test_tests_mentioning_hu_are_detected` → AC-01.
- [x] T006 [P] `test_spec_test_citations_include_pytest_and_vitest` → AC-01.
- [x] T007 [P] `test_prs_link_issues_by_closes` → AC-01.
- [x] T008 [P] `test_matrix_marks_missing_spec` → AC-02.
- [x] T009 [P] `test_matrix_marks_missing_tests` → AC-02.
- [x] T010 [P] `test_check_fails_on_closed_hu_without_spec` → AC-03.
- [x] T011 [P] `test_check_honors_exemptions` → AC-03.
- [x] T012 Ejecutar `uv run pytest tests/test_tools_trazabilidad.py` y confirmar rojo.
      *(ImportError: el modulo no existia.)*

## Phase 3: Implementation

- [x] T013 Crear `src/ppe_detection/tools/trazabilidad.py`.
- [x] T014 Añadir `trazabilidad`, `trazabilidad-write` y `trazabilidad-check` al Makefile.
- [x] T015 Crear `.github/workflows/trazabilidad.yml` con la compuerta.
- [x] T016 Añadir la mención `HU-017`, `HU-020` y `HU-021` a los encabezados de sus
      pruebas para que la matriz las encuentre.

## Phase 4: Evidence and close

- [x] T017 Ejecutar `make trazabilidad-check` (113 HU, ok).
- [x] T018 Generar `docs/curso/TRAZABILIDAD.md` con `make trazabilidad-write`.
- [x] T019 Ejecutar `make ownership-check`.
- [x] T020 Ejecutar `make check`. *(485 passed + 2 skipped.)*
- [ ] T021 Abrir PR a `develop` con la plantilla UAO y `Closes #149`.
- [ ] T022 Tras el merge, cerrar #149 a mano y moverla a Done.

## Notes

- Las exenciones documentales (HU-016, HU-018, HU-019, HU-023, HU-089) están declaradas
  con su motivo en el módulo.
- La matriz es una instantánea; se regenera al cerrar cada ola.
- El mirror de `backlog.md` recibió los enlaces de las specs 023 y 094, creadas después
  de su generación.
