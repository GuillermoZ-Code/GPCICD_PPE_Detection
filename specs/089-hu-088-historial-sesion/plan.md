# Implementation Plan: HU-088 — Historial de análisis de la sesión

**Branch**: `feature/089-hu-088-historial-sesion` | **Date**: 2026-11-28 | **Spec**:
[spec.md](./spec.md)

## Summary

Añadir un historial de la sesión en `localStorage`: módulo puro de almacenamiento,
componente `History.tsx` con miniatura, nombre, conteo y modelo, detalle de clases y
botón para limpiar. La SPA registra cada análisis al terminar. Doce pruebas cubren los
AC.

## Technical Context

**Language/Version**: TypeScript 6 + React 19

**Storage**: `localStorage` (`ppe.history.v1`), máximo 8 entradas

**Testing**: Vitest + Testing Library + jsdom

**Constraints**: sin llamadas de red; sin dependencias nuevas; no romper las pruebas de
HU-077/HU-080/HU-081; las miniaturas `blob:` viven solo en la sesión

**Scale/Scope**: `history.ts`, `History.tsx`, integración en `App.tsx`, estilos, 12
pruebas

## Constitution Check

- **Test-first**: 12 pruebas antes de la implementación. ✅
- **Sin secretos**: solo nombre de archivo, conteos y modelo. ✅
- **Sin red**: el historial no llama a `fetch`. ✅
- **Trazabilidad**: cada AC tiene pruebas que lo referencian. ✅

## Phases

1. **Test-first**: `App.history.test.tsx` con 12 pruebas; fase roja.
2. **Almacenamiento**: `history.ts` con validación, límite y limpieza.
3. **UI**: `History.tsx` y estilos; integración en `App.tsx` al terminar el análisis.
4. **Verificación**: `make frontend-check`, `make check`, specs y propiedad.

## Risks

- **Duplicar textos de pruebas existentes**: el modelo se muestra como «Modelo X» y el
  conteo como «N detecciones», para no chocar con `getByText('3')` o `mock-1.0.0`.
- **Cuota de `localStorage`**: `saveHistory` no debe lanzar; si falla, la inferencia
  sigue.
- **Miniaturas**: las `blob:` no se persisten; al recargar se muestra el marcador.
- **Datos corruptos**: `loadHistory` valida el JSON y devuelve lista vacía.
