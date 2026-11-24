---
description: "Task list for HU-112 — Glosario y mapa de documentación"
---

# Tasks: HU-112 — Glosario y mapa de documentación

**Input**: `specs/113-hu-112-glosario/spec.md` y `plan.md`.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas.
- [x] T002 Mover #168 a **In progress** en el tablero.
- [x] T003 Crear la rama `feature/113-hu-112-glosario`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_readme_exists` → AC-01.
- [x] T005 [P] `test_map_covers_key_areas` → AC-01.
- [x] T006 [P] `test_glossary_has_required_terms` → AC-02.
- [x] T007 [P] `test_relative_links_resolve` → AC-03.

## Phase 3: Implementation

- [x] T008 Escribir `docs/README.md`.
- [x] T009 Enlazar la spec 113 en `docs/curso/backlog.md`.
- [x] T010 Ejecutar las pruebas en verde.

## Phase 4: Evidence and close

- [x] T011 Ejecutar `make check` y `make ownership-check`.
- [ ] T012 Abrir PR y cerrar #168 tras el merge.

## Notes

- Los enlaces son relativos a `docs/`.
- El glosario incluye MaaS, SDD y DinD.
