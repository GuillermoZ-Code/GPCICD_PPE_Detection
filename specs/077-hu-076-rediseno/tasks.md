# Tasks: HU-076 — Rediseño visual

**Input**: Design documents from `specs/077-hu-076-rediseno/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: se conservan las 93 pruebas de la SPA; la validación es lint + test + build.

## Phase 1: Setup

- [x] T001 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #132.

## Phase 2: Sistema de diseño

- [x] T002 Paleta de 6 tokens por tema (papel, tinta, regla, señal).
- [x] T003 Tipografía Barlow Condensed + Barlow con pila de respaldo.
- [x] T004 Radios 0–2 px, sin sombras ni degradados.

## Phase 3: Armazón

- [x] T005 Barra superior con hairlines y marca de señal.
- [x] T006 Banda de señal con el titular en mayúsculas condensadas.
- [x] T007 Paneles con cabecera reglada y cuerpo sobre papel.
- [x] T008 Cifras tabulares y tabla como reporte.
- [x] T009 Estados vacío, carga y error en el mismo lenguaje.

## Phase 4: Accesibilidad y motion

- [x] T010 Foco visible y `prefers-reduced-motion`.
- [x] T011 Responsive: dos columnas → una.

## Phase 5: Verificación

- [x] T012 `npm run lint` en verde.
- [x] T013 `npm run test` (93) en verde.
- [x] T014 `npm run build` en verde.
- [ ] T015 PR con plantilla UAO, `Closes #132`.
