# Implementation Plan: HU-080 — Accesibilidad WCAG 2.2 AA en la SPA

**Branch**: `feature/081-hu-080-accesibilidad` | **Date**: 2026-11-28 | **Spec**:
[spec.md](./spec.md)

## Summary

Añadir un enlace de salto, un landmark principal enfocable, foco programático al título
de resultados, `aria-live` y `aria-busy`, foco inicial en el diálogo de configuración y
tokens de estado con contraste AA en el tema claro. Ocho pruebas cubren los AC.

## Technical Context

**Language/Version**: TypeScript 6 + React 19 + Vite 8

**Testing**: Vitest + Testing Library + jsdom; lectura de `design.css` con `node:fs`

**Constraints**: sin dependencias nuevas; no cambiar el contrato ni el flujo de HU-077;
conservar las pruebas de HU-076/HU-077/HU-081

**Scale/Scope**: `App.tsx`, `SettingsDrawer.tsx`, `design.css`, 1 archivo de pruebas

## Constitution Check

- **Test-first**: 8 pruebas escritas antes de los ajustes. ✅
- **Sin dependencias nuevas**: solo React, Testing Library y builtins de Node. ✅
- **Sin secretos**: solo tokens de color. ✅
- **Accesibilidad**: roles, nombres, foco y contraste verificados. ✅

## Phases

1. **Test-first**: `App.a11y.test.tsx` con 8 pruebas; fase roja.
2. **Implementación**: enlace de salto, `main#main`, foco al resultado, `aria-busy`,
   foco del diálogo, overrides de contraste del tema claro, estilos del enlace.
3. **Verificación**: `make frontend-check`, `make check`, specs y propiedad.

## Risks

- **Foco al resultado**: no debe dispararse en cada render, solo al pasar a `ready`.
- **Tema claro**: los estados success/warning/error necesitan tokens más oscuros para
  alcanzar 3:1 sobre blanco.
- **Diálogo**: el foco inicial no debe romper el cierre con Escape ni el retorno al
  botón de configuración.
