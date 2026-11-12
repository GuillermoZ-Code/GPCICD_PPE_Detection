---
description: "Task list for HU-012 — Verificaciones de calidad"
---

# Tasks: HU-012 — Verificaciones automatizadas de calidad

**Input**: Design documents from `specs/010-hu-012-calidad/`

**Prerequisites**: `plan.md`, `spec.md`, contratos de HU-006/007/010 fusionados.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-012.
- [x] T002 Enlazar la spec en `docs/curso/backlog.md` y `specs/README.md`.

## Phase 2: Tests first (deben fallar)

- [x] T003 [P] `test_main_returns_zero_when_all_checks_pass` → AC-01.
- [x] T004 [P] `test_deliberate_regression_makes_main_fail` → AC-02.
- [x] T005 [P] `test_ruff_reports_configured_violation` → AC-03.
- [x] T006 [P] `test_default_checks_do_not_require_gpu_or_dataset` → AC-04.
- [x] T007 [P] `test_render_report_marks_failure` → FR-002/FR-003.
- [x] T008 Ejecutar `uv run pytest tests/test_calidad.py` en rojo.

## Phase 3: Implementation

- [x] T009 Crear `src/ppe_detection/tools/calidad.py` con `Check`, `Result`,
  `run_check`, `run_all`, `render_report` y `main`.
- [x] T010 Añadir el target `make calidad`.
- [x] T011 Documentar el comando en `README.md` o `docs/curso/`.
- [x] T012 Ejecutar el comando real y comprobar el informe.

## Phase 4: Verification

- [x] T013 Ejecutar `uv run pytest tests/test_calidad.py` en verde.
- [x] T014 Ejecutar `make check` y `uv build`.
- [x] T015 Marcar tareas y estado de la spec como implementada.
