# Tasks: HU-041 — Proxy inverso Caddy con HTTPS automático

**Input**: Design documents from `specs/042-hu-041-caddy/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #97.

## Phase 2: Pruebas (test-first)

- [x] T002 [AC-01] Prueba estática del criterio 1.
- [x] T003 [AC-02] Prueba estática del criterio 2.
- [x] T004 [AC-03] Prueba estática del criterio 3.

## Phase 3: Implementación

- [x] T005 Archivos del entregable.
- [x] T006 Integración con el pipeline y el compose.

## Phase 4: Verificación

- [x] T007 `glab ci lint` valida el pipeline.
- [ ] T008 `make check` en verde.
- [ ] T009 PR con plantilla UAO, `Closes #97`, revisor de otro integrante.
