# Implementation Plan: HU-081 — Estados de carga, error y reintento

**Branch**: `feature/082-hu-081-estados-ui` | **Date**: 2026-11-25 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `specs/082-hu-081-estados-ui/spec.md`

## Summary

Añadir a `App.tsx` un aviso de espera configurable (`slowAfterMs`, 8 s por omisión) y un
botón «Reintentar» en el estado de error que reutiliza el archivo y la URL ya cargados.
Los estados existentes no cambian; se vuelven observables y accionables.

## Technical Context

**Language/Version**: TypeScript 6, React 19

**Primary Dependencies**: React (estado y efectos), Vitest 5 + Testing Library

**Storage**: N/A

**Testing**: Vitest + Testing Library (jsdom)

**Target Platform**: navegador (SPA)

**Project Type**: aplicación web

**Performance Goals**: el temporizador no bloquea el hilo; un `setTimeout` por análisis

**Constraints**: sin dependencias nuevas; sin cambiar el contrato `DetectorClient`

**Scale/Scope**: `frontend/src/App.tsx` + un archivo de pruebas

## Constitution Check

- **Test-first**: cada AC tiene prueba que lo referencia. ✅
- **Sin dependencias nuevas**: solo React y Vitest. ✅
- **Calidad**: `make frontend-check` y `make check` en verde. ✅
- **Contract-first**: `DetectorClient` intacto. ✅
- **Propiedad**: `frontend/` es de Guillermo. ✅
- **Una HU por PR**. ✅

## Project Structure

```text
frontend/src/App.tsx                 # slowAfterMs, aviso de espera y botón Reintentar
frontend/src/App.states.test.tsx     # 5 pruebas de los tres estados
specs/082-hu-081-estados-ui/
```

## Design decisions

1. **El umbral es una prop, no una constante.** `slowAfterMs` (8 s por omisión) permite
   probar el aviso en milisegundos y ajustarlo en la demo sin tocar el código.
2. **El temporizador se reinicia por intento.** Un contador `attempt` en las dependencias
   del efecto evita que un reintento herede el aviso del intento anterior.
3. **El reintento solo existe si hay archivo y URL.** Un error de validación no tiene
   imagen que reenviar; ofrecer «Reintentar» ahí sería un botón muerto.
4. **Se reutiliza `StatusBanner`.** El error mantiene su `role="alert"`; el botón va
   debajo, sin introducir un componente nuevo para una acción de una línea.
5. **No se aborta la petición.** El umbral es informativo; cancelar requeriría `AbortSignal`
   y un cambio de contrato que no pide la HU.

## Risks

| Riesgo | Mitigación |
|---|---|
| Temporizador que actualiza tras desmontar | `clearTimeout` en el cleanup del efecto |
| Aviso que se queda tras un reintento | `attempt` en las dependencias y reset explícito |
| Reintento con archivo revocado | Se reutiliza la URL vigente; el flujo de selección no cambia |
| Botón que no hace nada en error de validación | Se renderiza solo con archivo e imagen |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `App.states.test.tsx` (aviso tras el umbral y ausencia antes del umbral) |
| AC-02 | `App.states.test.tsx` (reintento exitoso y ocultación durante el reintento) |
| AC-03 | `App.states.test.tsx` (inactivo → seleccionado → carga) |
