---
description: "Task list for HU-045 — Healthcheck de liveness y readiness"
---

# Tasks: HU-045 — Healthcheck de liveness y readiness

**Input**: `specs/046-hu-045-health-live-ready/spec.md` y `plan.md`.

**Prerequisites**: issue #101, rama `feature/046-hu-045-health-live-ready`,
tarjeta #101 en *In progress* (WIP 1 verificado).

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Revisar issue #101, criterios y propiedad de archivos.
- [x] T002 Crear spec, plan y tareas.
- [x] T003 Mover #101 a **In progress** en el tablero (WIP 1).
- [x] T004 Crear la rama desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T005 `test_live_responds_without_model` → AC-01.
- [x] T006 `test_live_does_not_build_detector` → AC-01.
- [x] T007 `test_ready_returns_503_without_detector` → AC-01.
- [x] T008 `test_ready_returns_200_with_detector` → AC-01.
- [x] T009 `test_ready_reports_model_version_and_sha256` → AC-02.
- [x] T010 `test_ready_reports_unknown_identity_when_not_configured` → AC-02.
- [x] T011 `test_live_and_ready_are_documented_in_openapi` → AC-03.
- [x] T012 `test_openapi_documents_ready_503_contract` → AC-03.

## Phase 3: Implementation

- [x] T013 Definir `LiveResponse` y `ReadyResponse` en `src/ppe_detection/api/app.py`.
- [x] T014 Registrar `/health/live` sin depender del detector.
- [x] T015 Registrar `/health/ready` con 503/200 e identidad del modelo.
- [x] T016 Documentar 503 en OpenAPI.

## Phase 4: Validation and delivery

- [x] T017 Ejecutar ruff, ty, pytest y validación de spec/propiedad.
- [x] T018 Commit convencional y push de la rama.
- [x] T019 Abrir PR a `develop` con plantilla UAO, `Closes #101` y revisor par.
- [x] T020 Dejar la PR pendiente de aprobación (sin merge ni autoaprobación).
