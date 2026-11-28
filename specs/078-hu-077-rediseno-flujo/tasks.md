# Tasks: HU-077 â€” RediseÃ±o del flujo de carga y resultados

**Input**: Design documents from `specs/078-hu-077-rediseno-flujo/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/078-hu-077-rediseno-flujo` desde `develop`.
- [x] T002 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #133.
- [x] T003 Verificar la dependencia HU-076 (#132) en *Done*.

## Phase 2: Pruebas (test-first)

- [x] T004 [AC-01] Arrastre de una imagen con vista previa y nombre del archivo.
- [x] T005 [AC-01] Selector de archivo con vista previa.
- [x] T006 [AC-01] Paso 01 activo antes de seleccionar.
- [x] T007 [AC-01] Paso 02 activo y `progressbar` durante la inferencia.
- [x] T008 [AC-01] Vista previa conservada durante el anÃ¡lisis.
- [x] T009 [AC-02] Resumen con detecciones, clases, confianza media, tiempo y modelo.
- [x] T010 [AC-02] Leyenda por clase con color y conteo.
- [x] T011 [AC-03] Cierre del flujo con el paso 03 activo y la tabla visible.

## Phase 3: Componentes

- [x] T012 `FlowSteps`: tres pasos con `aria-current="step"`.
- [x] T013 `DetectionSummary`: totales y confianza media.
- [x] T014 `DetectionLegend`: agrupaciÃ³n por clase, color y conteo.
- [x] T015 `App`: integrar pasos, resumen, leyenda y `progressbar`.
- [x] T016 `design.css`: estilos responsivos y accesibles.

## Phase 4: Cierre

- [x] T017 `make frontend-check` en verde (ESLint + Vitest + build).
- [x] T018 `make check` y `ownership-check` en verde.
- [ ] T019 PR con plantilla UAO, `Closes #133`, revisiÃ³n de otro integrante.
