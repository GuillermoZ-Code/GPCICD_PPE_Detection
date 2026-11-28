---
description: "Task list for HU-064 — Notas de versión v1.0.0 y CHANGELOG"
---

# Tasks: HU-064 — Notas de versión v1.0.0 y CHANGELOG

**Input**: `specs/065-hu-064-release-notes/spec.md` y `plan.md`.

**Prerequisites**: issue #120, tarjeta #120 en *In progress* (WIP 1 verificado),
rama `feature/065-hu-064-release-notes` desde `develop`.

**Tests**: obligatorias y antes de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Revisar issue #120, AC y propiedad de archivos.
- [x] T002 Crear spec, plan y tareas.
- [x] T003 Mover #120 a **In progress** en el tablero (WIP 1).
- [x] T004 Crear la rama desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T005 `test_keep_a_changelog_header_is_present` → AC-01.
- [x] T006 `test_unreleased_precedes_release_section` → AC-01.
- [x] T007 `test_release_notes_link_real_hus_and_prs` → AC-02.
- [x] T008 `test_categories_and_iso_date_are_valid` → AC-03.

## Phase 3: Implementation

- [x] T009 Redactar `CHANGELOG.md` con Keep a Changelog y notas de v1.0.0.
- [x] T010 Enlazar cada cambio M4 con su HU y su PR real.

## Phase 4: Validation and delivery

- [x] T011 Ejecutar ruff, ty, pytest y validación de spec/propiedad.
- [x] T012 Commit convencional y push de la rama.
- [x] T013 Abrir PR a `develop` con plantilla UAO, `Closes #120` y revisor par.
- [x] T014 Dejar la PR pendiente de aprobación (sin merge ni autoaprobación).
