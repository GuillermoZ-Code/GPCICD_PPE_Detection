# Tasks: HU-081 — Estados de carga, error y reintento

**Input**: Design documents from `specs/082-hu-081-estados-ui/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/082-hu-081-estados-ui` desde `develop`.
- [x] T002 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #137.

## Phase 2: Pruebas (test-first)

- [x] T003 [AC-01] `App.states.test.tsx`: el aviso de espera aparece tras
      `slowAfterMs`.
- [x] T004 [AC-01] `App.states.test.tsx`: el aviso no aparece si el análisis termina
      antes del umbral.
- [x] T005 [AC-02] `App.states.test.tsx`: «Reintentar» repite el análisis y termina en
      éxito.
- [x] T006 [AC-02] `App.states.test.tsx`: el botón se oculta mientras se reintenta.
- [x] T007 [AC-03] `App.states.test.tsx`: inactivo, seleccionado, carga y error son
      distinguibles.

## Phase 3: Implementación

- [x] T008 `App.tsx`: prop `slowAfterMs` (8 s por omisión) y estado `slow`.
- [x] T009 `App.tsx`: efecto con `setTimeout` reiniciado por intento y limpieza.
- [x] T010 `App.tsx`: aviso «Sigue procesando…» dentro del estado de carga.
- [x] T011 `App.tsx`: botón «Reintentar» en el estado de error con archivo e imagen.

## Phase 4: Cierre

- [x] T012 `make frontend-check` y `make check` en verde.
- [x] T013 PR con plantilla UAO, `Closes #137`, revisor de otro integrante.
