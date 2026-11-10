# Implementation Plan: HU-007 — Interfaz web

**Branch**: `feature/005-hu-007-interfaz` | **Date**: 2026-11-09 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/005-hu-007-interfaz/spec.md`, issue #7 y
ADR 0006 (React + Vite + TypeScript).

## Summary

SPA en `frontend/` con React 19, Vite y TypeScript estricto. Consume un
`DetectorClient` con dos implementaciones: HTTP (cuando exista HU-006) y simulada
(determinista, para desarrollo y pruebas). Dibuja las cajas en `<canvas>` y lista las
detecciones en una tabla accesible.

## Technical Context

**Language/Version**: TypeScript 6.0 + React 19.3

**Build**: Vite 8.3

**Testing**: Vitest 5 + Testing Library + jsdom

**Linting**: ESLint 10 (flat config) + typescript-eslint

**Storage**: ninguna; la imagen vive en memoria

**Target Platform**: navegador moderno; build estático

**Constraints**: sin backend para las pruebas; sin GPU; sin datos versionados

**Scale/Scope**: 1 SPA, 5 componentes, 2 clientes, ~15 pruebas

## Constitution Check

- [x] `uv` sigue siendo el gestor de Python; el frontend usa `npm` (ADR 0006).
- [x] src-layout de Python intacto; el frontend vive en `frontend/`.
- [x] Ruff/`ty`/pytest para Python; ESLint/Vitest para TypeScript.
- [x] Sin datos ni pesos en Git; `node_modules/` y `dist/` ignorados.
- [x] Contract-first: los tipos replican `Detection` y `ImageData`.
- [x] Sin LLM en inferencia.
- [x] Test-first con cliente simulado.

## Project Structure

```text
frontend/
├── index.html
├── package.json
├── package-lock.json
├── tsconfig.json
├── vite.config.ts
├── eslint.config.js
├── README.md
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── styles.css
    ├── types.ts
    ├── api/
    │   ├── client.ts          # DetectorClient, HTTP y simulado
    │   └── client.test.ts
    ├── components/
    │   ├── UploadPanel.tsx
    │   ├── AnnotatedCanvas.tsx
    │   ├── DetectionTable.tsx
    │   └── StatusBanner.tsx
    └── setupTests.ts
```

**Structure Decision**: el frontend es un proyecto independiente con su propio
`package.json`; el paquete Python no lo importa ni lo empaqueta. La API se consume por
HTTP, no por RPC.

## Phase 0 — Investigación

- Vite 7 + React 19 + TS 5.9 funcionan con Node 24.
- `canvas.getContext('2d')` no existe en jsdom: el componente debe degradar sin dibujar
  para que las pruebas no dependan del motor gráfico.
- `URL.createObjectURL` no existe en jsdom: se mockea en las pruebas.

## Phase 1 — Diseño

- `DetectorClient` con `detect(file: File): Promise<PredictResponse>`.
- `createClient()` decide HTTP vs simulado según `VITE_API_URL`.
- El cliente simulado devuelve dos detecciones con dimensiones 640×480; el lienzo escala
  por `displayWidth / image_width`.
- Estados de la UI: `idle`, `loading`, `ready`, `error`.
- Validación de archivo por tipo MIME y tamaño (10 MB).
- Atribución AGPL y CC-BY en el pie.

## Phase 2 — Integración continua

- Job `frontend` en `.github/workflows/ci.yml`: `npm ci`, `npm run lint`, `npm run test`,
  `npm run build`.
- `make frontend-check` para ejecutarlo en local.

## Complexity Tracking

La introducción de Node/npm es la única desviación del stack original y está justificada
en el ADR 0006. No se añaden dependencias de UI pesadas: CSS propio, sin Tailwind.
