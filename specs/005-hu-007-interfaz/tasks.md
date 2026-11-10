---
description: "Task list for HU-007 — Interfaz web React"
---

# Tasks: HU-007 — Interfaz gráfica del detector

**Input**: Design documents from `specs/005-hu-007-interfaz/`

**Prerequisites**: `plan.md`, `spec.md`, ADR 0006, contrato TA-11 y HU-003

**Tests**: obligatorias y antes de la implementación. Cada AC tiene al menos una prueba.

## Phase 1: Setup

- [ ] T001 Crear `frontend/` con `package.json`, Vite, React y TypeScript estricto.
- [ ] T002 Configurar Vitest, Testing Library, ESLint y `npm run build`.

## Phase 2: Tests first

- [ ] T003 [P] `client.test.ts`: cliente simulado determinista y cliente HTTP.
- [ ] T004 [P] `App.test.tsx`: flujo completo con detecciones → AC-007.1.
- [ ] T005 [P] `App.test.tsx`: sin detecciones no es error → AC-007.3.
- [ ] T006 [P] `App.test.tsx`: archivo inválido y app disponible → AC-007.4.
- [ ] T007 [P] `DetectionTable.test.tsx`: categoría y confianza → AC-007.2.
- [ ] T008 [P] `App.test.tsx`: atribución AGPL y CC-BY → FR-010.
- [ ] T009 `npm run test` en rojo.

## Phase 3: Implementación

- [ ] T010 `types.ts` con `Detection` y `PredictResponse`.
- [ ] T011 `api/client.ts` con `DetectorClient`, `MockDetectorClient`,
      `HttpDetectorClient` y `createClient`.
- [ ] T012 `components/UploadPanel.tsx` con validación de tipo y tamaño.
- [ ] T013 `components/AnnotatedCanvas.tsx` con escalado y paleta por clase.
- [ ] T014 `components/DetectionTable.tsx` y `StatusBanner.tsx`.
- [ ] T015 `App.tsx` con los estados `idle`, `loading`, `ready`, `error`.
- [ ] T016 `styles.css` con diseño responsive y accesible.
- [ ] T017 `npm run test` en verde.

## Phase 4: Integración

- [ ] T018 Job `frontend` en `.github/workflows/ci.yml`.
- [ ] T019 Targets `frontend-*` en el `Makefile`.
- [ ] T020 `frontend/README.md` con instalación, scripts y variables de entorno.
- [ ] T021 Actualizar `CONSTITUTION.md`, `README.md`, `docs/curso/` y la plantilla de PR.
- [ ] T022 `make check`, `npm run build` y `make estado-write`.

## Dependencies & Execution Order

- T001 → T002 → T003–T008 → T009 → T010–T017 → T018–T022.
- T003–T008 pueden escribirse en paralelo.

## Notes

- Sin backend, GPU, dataset ni red en las pruebas.
- El cliente HTTP usa `POST /predict` multipart; se ajusta cuando cierre HU-006.
- No se versionan `node_modules/` ni `dist/`.
