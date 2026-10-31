---
description: "Task list for TA Contract-first"
---

# Tasks: TA Contract-first `Image → list[Detection]`

**Input**: Design documents from `specs/001-ta-contract-first/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias y **antes** de la implementación (test-first). Cada AC tiene
al menos una prueba que lo referencia.

**Organization**: una sola historia (P1) con fase de tests, implementación y polish.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: puede ejecutarse en paralelo (archivos distintos)
- **[Story]**: US1

## Phase 1: Setup

- [ ] T001 Crear `tests/test_contracts.py` con fixtures sintéticas y helpers.
- [ ] T002 Crear `src/ppe_detection/contracts.py` solo con `CLASSES` (sin lógica).

## Phase 2: Tests first (deben fallar)

- [ ] T003 [P] [US1] `test_fake_detector_returns_list` → **AC-01**.
- [ ] T004 [P] [US1] `test_detection_validates_class_confidence_and_bbox` → **AC-02**.
- [ ] T005 [P] [US1] `test_empty_detections_returns_empty_list` → **AC-03**.
- [ ] T006 [P] [US1] `test_fake_detector_is_deterministic` → **AC-04**.
- [ ] T007 [P] [US1] `test_invalid_confidence_and_class_are_rejected` → **AC-05**.
- [ ] T008 [P] [US1] `test_contract_is_documented` → **AC-06**.
- [ ] T009 Ejecutar `uv run pytest tests/test_contracts.py` y confirmar que fallan.

## Phase 3: Implementación (US1)

- [ ] T010 Definir `ImageData` con `array`, `width`, `height`, `format`, `source`.
- [ ] T011 Definir `Detection` con `class_id`, `class_name`, `confidence`, `bbox`,
      `image_width`, `image_height`; validar confianza y bbox.
- [ ] T012 Definir el protocolo `Detector.detect(image) -> list[Detection]`.
- [ ] T013 Implementar `FakeDetector` vacío y con cajas fijas.
- [ ] T014 Ejecutar `uv run pytest tests/test_contracts.py` y confirmar verde.

## Phase 4: Polish

- [ ] T015 Documentar el contrato en `docs/architecture/contracts.md`.
- [ ] T016 Enlazar el contrato desde HU-006, HU-007 y HU-010.
- [ ] T017 Ejecutar `make check` y registrar evidencia.

## Dependencies & Execution Order

- Setup → Tests first → Implementación → Polish.
- T003–T008 pueden escribirse en paralelo.
- T009 depende de T003–T008.
- T010–T013 dependen de T009 (tests en rojo).
- T014 depende de T010–T013.
- T015–T017 dependen de T014.

## Implementation Strategy

1. Escribir las pruebas de los AC y verlas fallar.
2. Implementar el contrato mínimo hasta ponerlas en verde.
3. Documentar y ejecutar `make check`.
4. **Detenerse**: no implementar el detector real ni el preprocesamiento.

## Notes

- Sin GPU, dataset, pesos ni red.
- El detector real (HU-002) debe cumplir este contrato.
- Cualquier cambio de contrato se registra en ADR 0005.
- Sin umbral de cobertura; se decide en HU-012.
