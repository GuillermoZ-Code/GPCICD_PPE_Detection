---
description: "Task list for HU-007 — Interfaz web React"
---

# Tasks: HU-007 — Interfaz gráfica del detector

**Input**: Design documents from `specs/005-hu-007-interfaz/`

**Prerequisites**: `plan.md`, `spec.md`, ADR 0006, contrato TA-11 y HU-003

**Tests**: obligatorias y antes de la implementación. Cada AC tiene al menos una prueba.

## Phase 1: Setup

- [x] T001 Crear `frontend/` con `package.json`, Vite, React y TypeScript estricto.
- [x] T002 Configurar Vitest, Testing Library, ESLint y `npm run build`.

## Phase 2: Tests first

- [x] T003 [P] `client.test.ts`: cliente simulado determinista y cliente HTTP.
- [x] T004 [P] `App.test.tsx`: flujo completo con detecciones → AC-007.1.
- [x] T005 [P] `App.test.tsx`: sin detecciones no es error → AC-007.3.
- [x] T006 [P] `App.test.tsx`: archivo inválido y app disponible → AC-007.4.
- [x] T007 [P] `DetectionTable.test.tsx`: categoría y confianza → AC-007.2.
- [x] T008 [P] `App.test.tsx`: atribución AGPL y CC-BY → FR-010.
- [x] T009 `npm run test` en rojo.

## Phase 3: Implementación

- [x] T010 `types.ts` con `Detection` y `PredictResponse`.
- [x] T011 `api/client.ts` con `DetectorClient`, `MockDetectorClient`,
      `HttpDetectorClient` y `createClient`.
- [x] T012 `components/UploadPanel.tsx` con validación de tipo y tamaño.
- [x] T013 `components/AnnotatedCanvas.tsx` con escalado y paleta por clase.
- [x] T014 `components/DetectionTable.tsx` y `StatusBanner.tsx`.
- [x] T015 `App.tsx` con los estados `idle`, `loading`, `ready`, `error`.
- [x] T016 `styles.css` con diseño responsive y accesible.
- [x] T017 `npm run test` en verde.

## Phase 4: Integración

- [x] T018 Job `frontend` en `.github/workflows/ci.yml`.
- [x] T019 Targets `frontend-*` en el `Makefile`.
- [x] T020 `frontend/README.md` con instalación, scripts y variables de entorno.
- [x] T021 Actualizar `CONSTITUTION.md`, `README.md`, `docs/curso/` y la plantilla de PR.
- [x] T022 `make check`, `npm run build` y `make estado-write`.

## Dependencies & Execution Order

- T001 → T002 → T003–T008 → T009 → T010–T017 → T018–T022.
- T003–T008 pueden escribirse en paralelo.

## Notes

- Sin backend, GPU, dataset ni red en las pruebas.
- El cliente HTTP usa `POST /predict` multipart; se ajusta cuando cierre HU-006.
- No se versionan `node_modules/` ni `dist/`.
