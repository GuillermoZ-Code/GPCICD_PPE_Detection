---
description: "Task list for HU-061 — README con badges y enlaces públicos del M4"
---

# Tasks: HU-061 — README con badges y enlaces públicos del M4

**Input**: `specs/062-hu-061-readme-badges/spec.md` y `plan.md`.

**Prerequisites**: issue #117, tarjeta #117 en *In progress* (WIP 1 verificado),
rama `feature/062-hu-061-readme-badges` desde `develop`.

**Tests**: obligatorias y antes de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Verificar que HU-065 está funcionalmente cumplida (PR #218 fusionada).
- [x] T002 Crear spec, plan y tareas.
- [x] T003 Mover #117 a **In progress** en el tablero (WIP 1).
- [x] T004 Crear la rama desde `develop` actualizado.

## Phase 2: Tests first (deben fallar)

- [x] T005 `test_badges_de_ci_pipeline_licencia_y_docker_hub_ac_01` → AC-01.
- [x] T006 `test_badge_docker_hub_no_inventa_namespace_ac_01` → AC-01.
- [x] T007 `test_enlaces_https_registry_y_constitucion_ac_02` → AC-02.
- [x] T008 `test_enlaces_internos_resuelven_y_toc_existe_ac_03` → AC-03.

## Phase 3: Implementation

- [ ] T009 Añadir los cuatro badges al bloque del README.
- [ ] T010 Crear «Enlaces públicos del M4» con HTTPS, Registry, CONSTITUTION y
      `<URL_PUBLICA>`, y añadir la entrada al índice.
- [ ] T011 Documentar los pendientes de HU-053 y HU-068 sin inventar dominios.

## Phase 4: Validation and delivery

- [ ] T012 Ejecutar las 4 pruebas focalizadas en verde y comprobar que fallaron antes.
- [ ] T013 Verificar `ruff format --check README.md`, `check_specs` y propiedad.
- [ ] T014 Commit de pruebas (test-first) y commit de documentación.
- [ ] T015 Push y PR a `develop` con plantilla UAO y `Closes #117`.
- [ ] T016 Mover #117 a **In review** y verificar checks remotos; sin merge ni
      autoaprobación.
