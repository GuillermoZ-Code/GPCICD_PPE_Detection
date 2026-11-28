# Implementation Plan: HU-077 — Rediseño del flujo de carga y resultados

**Branch**: `feature/078-hu-077-rediseno-flujo` | **Date**: 2026-11-28 | **Spec**:
[spec.md](./spec.md)

**Input**: `specs/078-hu-077-rediseno-flujo/spec.md`

## Summary

Añadir al flujo de la SPA tres pasos visibles (01 selección, 02 análisis, 03
resultados), un `progressbar` durante la inferencia, un resumen con totales y una
leyenda por clase con color y conteo. Se conservan el arrastre y el selector de
`UploadPanel`, la vista previa y los estados de HU-081. Ocho pruebas de interacción con
Testing Library cubren los AC.

## Technical Context

**Language/Version**: TypeScript 6 + React 19 + Vite 8

**Primary Dependencies**: React, Testing Library, user-event, Vitest; sin dependencias
nuevas

**Storage**: estado local de React; `localStorage` para ajustes (HU-076)

**Testing**: Vitest + Testing Library + jsdom

**Target Platform**: navegador (SPA estática)

**Project Type**: interfaz web

**Performance Goals**: el resumen y la leyenda se calculan en memoria sobre las
detecciones visibles; sin llamadas adicionales

**Constraints**: no cambiar el contrato HTTP ni el cliente; conservar los estados de
HU-081 y el sistema de diseño de HU-076; accesibilidad por roles y `aria-current`

**Scale/Scope**: 3 componentes nuevos (`FlowSteps`, `DetectionSummary`,
`DetectionLegend`), ajustes en `App.tsx` y `design.css`, 8 pruebas

## Constitution Check

- **Spec Kit antes de implementar**: spec/plan/tasks creados antes del código. ✅
- **Test-first**: las 8 pruebas se escriben antes de los componentes y deben fallar. ✅
- **Sin dependencias nuevas**: solo React y Testing Library ya instalados. ✅
- **Accesibilidad**: pasos con `aria-current`, progreso con `role="progressbar"`,
  resumen y leyenda con nombre accesible. ✅
- **Sin secretos ni datos**: todo el cálculo es local. ✅

## Project Structure

```text
frontend/src/
├── App.tsx                         # integra pasos, resumen y leyenda
├── App.flow.test.tsx               # 8 pruebas de interacción (HU-077)
├── components/
│   ├── FlowSteps.tsx               # 01 → 02 → 03
│   ├── DetectionSummary.tsx        # detecciones, clases, confianza, tiempo, modelo
│   ├── DetectionLegend.tsx         # color, clase, conteo y confianza media
│   └── UploadPanel.tsx             # se conserva; arrastre y selector
├── labels.ts                       # nombres y colores existentes
└── design.css                      # estilos de flujo, progreso, resumen y leyenda
```

## Phase Plan

### Phase 0 — Investigación

- Revisar `App.tsx`, `UploadPanel.tsx`, `DetectionTable.tsx`, `labels.ts`, los estilos
  y las pruebas de HU-076/HU-081 para no duplicar estados ni romper roles existentes.

### Phase 1 — Test-first

- Crear `App.flow.test.tsx` con 8 pruebas: arrastre, selector, pasos, progreso, vista
  previa, resumen, leyenda y cierre del flujo.
- Confirmar la fase roja.

### Phase 2 — Componentes

- `FlowSteps`: lista ordenada con tres pasos y `aria-current="step"`.
- `DetectionSummary`: totales y confianza media sobre las detecciones visibles.
- `DetectionLegend`: agrupación por clase con color, conteo y confianza media.
- `App`: integrar los tres componentes y el `progressbar`; conservar los estados.
- `design.css`: estilos responsivos y coherentes con el sistema de HU-076.

### Phase 3 — Verificación

- `npm run test` (Vitest), `npm run lint`, `npm run build`.
- `make frontend-check`.
- Revisar que las pruebas de HU-076/HU-081 sigan en verde.

## Risks

- **Duplicar textos en las pruebas existentes**: `App.test.tsx` usa `getByText('3')` y
  `mock-1.0.0`; el resumen debe mantener un único `3` exacto y un único modelo.
- **Romper roles existentes**: el estado de carga conserva `role="status"`; el
  progressbar se añade dentro, no lo sustituye.
- **Filtros**: el resumen y la leyenda usan las detecciones visibles, no las crudas, para
  no contradecir la tabla.
- **Vista previa**: se mantiene el `URL.revokeObjectURL` al cambiar de imagen.
