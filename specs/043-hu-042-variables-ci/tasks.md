# Tasks: HU-042 — Variables CI enmascaradas y protegidas

**Input**: Design documents from `specs/043-hu-042-variables-ci/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #98.

## Phase 2: Pruebas

- [x] T002 [AC-01] Comprobación estática del primer criterio.
- [x] T003 [AC-02] Comprobación estática del segundo criterio.
- [x] T004 [AC-03] Comprobación estática del tercer criterio.

## Phase 3: Verificación

- [x] T005 `make check` en verde.
- [ ] T006 PR con plantilla UAO, `Closes #98`.
