---
description: "Task list for HU-044 — Configuración por entorno validada al arrancar"
---

# Tasks: HU-044 — Configuración por entorno validada al arrancar

**Input**: `specs/045-hu-044-config-entorno/spec.md` y `plan.md`.

**Prerequisites**: issue #100, rama `feature/045-hu-044-config-entorno`, tarjeta #100 en
*In progress* (WIP 1 verificado).

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Revisar issue #100, criterios y propiedad de archivos.
- [x] T002 Crear spec, plan y tareas.
- [x] T003 Mover #100 a **In progress** en el tablero (WIP 1).
- [x] T004 Crear la rama desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T005 `test_env_example_documents_every_ppe_variable` → AC-01.
- [x] T006 `test_valid_environment_is_accepted` → AC-02.
- [x] T007 `test_invalid_conf_reports_variable_and_reason` → AC-02.
- [x] T008 `test_invalid_port_reports_range` → AC-02.
- [x] T009 `test_invalid_sha256_reports_length` → AC-02.
- [x] T010 `test_invalid_cors_origin_is_rejected` → AC-02.
- [x] T011 `test_create_app_fails_early_on_invalid_environment` → AC-02.
- [x] T012 `test_cli_fails_without_leaking_secret` → AC-03.

## Phase 3: Implementation

- [x] T013 Crear `src/ppe_detection/api/settings.py` con `Settings`, `SettingsError`,
  `validate_environment`, `load_settings` y `main`.
- [x] T014 Crear `.env.example` con todas las variables documentadas.
- [x] T015 Llamar a `load_settings()` desde `create_app`.
- [x] T016 Redactar valores secretos en mensajes de error.

## Phase 4: Validation and delivery

- [x] T017 Ejecutar ruff, ty, pytest y validación de spec/propiedad.
- [x] T018 Commit convencional y push de la rama.
- [x] T019 Abrir PR a `develop` con plantilla UAO, `Closes #100` y revisor par.
- [x] T020 Dejar la PR pendiente de aprobación (sin merge ni autoaprobación).
