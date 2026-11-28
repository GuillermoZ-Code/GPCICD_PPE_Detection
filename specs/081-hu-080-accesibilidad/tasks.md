# Tasks: HU-080 â€” Accesibilidad WCAG 2.2 AA en la SPA

**Input**: Design documents from `specs/081-hu-080-accesibilidad/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/081-hu-080-accesibilidad` desde `develop`.
- [x] T002 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #136.
- [x] T003 Verificar la dependencia HU-076 (#132) en *Done*.

## Phase 2: Pruebas (test-first)

- [x] T004 [AC-01] Enlace Â«Saltar al contenidoÂ» que apunta a `#main`.
- [x] T005 [AC-01] `main` con `id="main"` y foco programÃ¡tico.
- [x] T006 [AC-01] Foco al tÃ­tulo de resultados al terminar.
- [x] T007 [AC-01] `aria-live="polite"` en el resumen.
- [x] T008 [AC-01] `aria-busy` y `progressbar` durante la carga.
- [x] T009 [AC-02] Contraste AA del tema oscuro.
- [x] T010 [AC-02] Contraste AA del tema claro.
- [x] T011 [AC-03] Roles y etiquetas del diÃ¡logo, tabla, progreso, resumen y leyenda.

## Phase 3: ImplementaciÃ³n

- [x] T012 `App.tsx`: enlace de salto, `main#main`, foco al resultado y `aria-busy`.
- [x] T013 `SettingsDrawer.tsx`: foco inicial en Cerrar al abrir.
- [x] T014 `design.css`: estilos del enlace y overrides de contraste del tema claro.

## Phase 4: Cierre

- [x] T015 `make frontend-check` y `make check` en verde.
- [x] T016 `check_specs` y `ownership-check` en verde.
- [ ] T017 PR con plantilla UAO, `Closes #136`, revisiÃ³n de otro integrante.
