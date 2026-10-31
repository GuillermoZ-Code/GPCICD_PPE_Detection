---
description: "Task list for TA Contract-first"
---

# Tasks: TA Contract-first `Image → list[Detection]`

**Input**: Design documents from `specs/001-ta-contract-first/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: incluidas porque la TA exige pruebas de contrato.

**Organization**: una sola historia (P1) con fase de setup, fundacional y polish.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: puede ejecutarse en paralelo (archivos distintos)
- **[Story]**: US1

## Phase 1: Setup

- [ ] T001 Crear `src/ppe_detection/contracts.py` con el catálogo `CLASSES`.
- [ ] T002 Crear `tests/test_contracts.py` con fixtures sintéticas.

## Phase 2: Foundational

- [ ] T003 Definir `ImageData` con `array`, `width`, `height`, `format`, `source`.
- [ ] T004 Definir `Detection` con `class_id`, `class_name`, `confidence`, `bbox`,
      `image_width`, `image_height`.
- [ ] T005 Validar `confidence` finito en `[0,1]` y `bbox` con `x1 < x2`, `y1 < y2`.
- [ ] T006 Validar `class_name` contra `CLASSES`.

## Phase 3: User Story 1 - Contrato estable (P1)

**Goal**: permitir que API, UI y gRPC trabajen contra un contrato y un fake.

**Independent Test**: `FakeDetector.detect(ImageData(...))` devuelve `list[Detection]`
sin YOLO, dataset ni GPU.

- [ ] T007 Definir el protocolo `Detector.detect(image) -> list[Detection]`.
- [ ] T008 Implementar `FakeDetector` vacío y con cajas fijas.
- [ ] T009 Probar imagen válida con detecciones.
- [ ] T010 Probar imagen sin detecciones (`[]`).
- [ ] T011 Probar confianza negativa, >1 y `NaN`.
- [ ] T012 Probar clase fuera del catálogo y `bbox` inválida.
- [ ] T013 Probar determinismo con la misma entrada.

## Phase N: Polish

- [ ] T014 Documentar el contrato en `docs/architecture/contracts.md`.
- [ ] T015 Enlazar el contrato desde HU-006, HU-007 y HU-010.
- [ ] T016 Ejecutar `make check` y registrar evidencia.

## Dependencies & Execution Order

- Setup → Foundational → US1 → Polish.
- T003 y T004 pueden ir en paralelo.
- T007 depende de T003 y T004.
- T008 depende de T007.
- T009–T013 dependen de T008.
- T014–T016 dependen de T009–T013.

## Implementation Strategy

1. Completar Setup y Foundational.
2. Implementar US1 y validar el contrato con el fake.
3. Documentar y ejecutar `make check`.
4. **Detenerse**: no implementar el detector real ni el preprocesamiento.

## Notes

- Sin GPU, dataset, pesos ni red.
- El detector real (HU-002) debe cumplir este contrato.
- Cualquier cambio de contrato se registra en ADR 0005.
