---
description: "Task list for HU-098 — Model Registry con alias champion/challenger"
---

# Tasks: HU-098 — Model Registry con alias champion/challenger

**Input**: `specs/099-hu-098-registry/spec.md` y `plan.md`.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas.
- [x] T002 Mover #154 a **In progress** en el tablero.
- [x] T003 Crear la rama `feature/099-hu-098-registry`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_champion_points_to_adr_model` → AC-01.
- [x] T005 [P] `test_champion_sha_matches_adr` → AC-01.
- [x] T006 [P] `test_challenger_points_to_candidate` → AC-02.
- [x] T007 [P] `test_validate_rejects_unknown_alias` → AC-02.
- [x] T008 [P] `test_validate_rejects_invalid_sha` → AC-02.
- [x] T009 [P] `test_plan_promotion_moves_challenger` → AC-03.
- [x] T010 [P] `test_plan_promotion_keeps_rollback` → AC-03.
- [x] T011 Ejecutar `uv run pytest tests/test_tracking_registry.py` y confirmar rojo.

## Phase 3: Implementation

- [x] T012 Crear `src/ppe_detection/tracking/registry.py`.
- [x] T013 Ejecutar las pruebas en verde.

## Phase 4: Evidence and close

- [x] T014 Ejecutar `make check` y `make ownership-check`.
- [ ] T015 Abrir PR y cerrar #154 tras el merge.

## Notes

- La lógica es pura; no se llama a MLflow.
- El SHA del champion es el de `models.lock`.
