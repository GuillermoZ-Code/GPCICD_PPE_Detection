---
description: "Task list for HU-094 — Conteo reproducible de pruebas"
---

# Tasks: HU-094 — Conteo reproducible de pruebas (`make pruebas`)

**Input**: `specs/095-hu-094-conteo-pruebas/spec.md` y `plan.md`.

**Prerequisites**: issue #150, rama `feature/095-hu-094-conteo-pruebas`, `develop`
actualizado.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-094.
- [x] T002 Mover #150 a **In progress** en el tablero (WIP 1).
- [x] T003 Crear la rama `feature/095-hu-094-conteo-pruebas` desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_pytest_counter_accepts_both_formats` → AC-01.
- [x] T005 [P] `test_vitest_counter_reads_json` → AC-01.
- [x] T006 [P] `test_report_maps_owner_from_manifest` → AC-02.
- [x] T007 [P] `test_report_has_suite_and_owner_totals` → AC-02.
- [x] T008 [P] `test_report_writes_markdown_to_target` → AC-03.
- [x] T009 Ejecutar `uv run pytest tests/test_tools_pruebas.py` y confirmar rojo.
      *(ImportError: el modulo no existia.)*

## Phase 3: Implementation

- [x] T010 Crear `src/ppe_detection/tools/pruebas.py` con parsers, filas y render.
- [x] T011 Añadir el objetivo `pruebas` al Makefile sin reordenar lo existente.
- [x] T012 Ejecutar las pruebas nuevas en verde.

## Phase 4: Regeneración

- [x] T013 Ejecutar `make pruebas-write` y revisar el diff de `PRUEBAS.md`.
- [x] T014 Confirmar que el total coincide con `make check` + `make frontend-check`.
      *(453 pytest + 76 Vitest = 529.)*

## Phase 5: Evidence and close

- [x] T015 Ejecutar `make ownership-check`.
- [x] T016 Ejecutar `make check`. *(451 passed + 2 skipped.)*
- [ ] T017 Abrir PR a `develop` con la plantilla UAO y `Closes #150`.
- [ ] T018 Tras el merge, cerrar #150 a mano y moverla a Done.

## Notes

- Las pruebas no lanzan pytest ni Vitest: usan salidas simuladas.
- `make pruebas-write` es el único camino para actualizar `PRUEBAS.md`.
- `PLAN-PRUEBAS.md` a 1.200 corresponde a HU-095 (#151).
