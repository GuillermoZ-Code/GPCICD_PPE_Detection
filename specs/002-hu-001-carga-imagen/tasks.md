---
description: "Task list for HU-001 — Carga de imágenes"
---

# Tasks: HU-001 — Cargar una imagen para su análisis

**Input**: Design documents from `specs/002-hu-001-carga-imagen/`

**Prerequisites**: `plan.md`, `spec.md`, contrato TA-11 (`specs/001-ta-contract-first`)

**Tests**: obligatorias y **antes** de la implementación (test-first). Cada AC tiene
al menos una prueba que lo referencia.

## Phase 1: Setup

- [ ] T001 Agregar `numpy` y `opencv-python-headless` con `uv add`.
- [ ] T002 Crear `tests/test_contracts.py` con fixtures sintéticas del contrato.

## Phase 2: Tests first (deben fallar)

- [ ] T003 [P] `test_load_png_returns_rgb_image_data` → AC-01.
- [ ] T004 [P] `test_load_jpeg_returns_rgb_image_data` → AC-01.
- [ ] T005 [P] `test_preserves_original_dimensions` → AC-02.
- [ ] T006 [P] `test_loading_does_not_invoke_detector` → AC-03.
- [ ] T007 [P] `test_empty_file_is_rejected` → FR-004.
- [ ] T008 [P] `test_corrupt_file_is_rejected` → FR-004.
- [ ] T009 [P] `test_unsupported_format_is_rejected` → FR-004.
- [ ] T010 [P] `test_load_bytes_uses_source_label` → FR-001.
- [ ] T011 `uv run pytest tests/test_contracts.py tests/test_image_loader.py` en rojo.

## Phase 3: Implementación

- [ ] T012 `contracts.py`: `CLASSES`, `ImageData` con validación.
- [ ] T013 `io/images.py`: `InvalidImageError`, `load_image`, `load_image_bytes`.
- [ ] T014 `io/__init__.py` con la API pública.
- [ ] T015 `uv run pytest` en verde.

## Phase 4: Polish

- [ ] T016 Documentar el contrato en `docs/architecture/contracts.md`.
- [ ] T017 Corregir los nombres canónicos de clase en `CONSTITUTION.md` y
      `specs/001-ta-contract-first/spec.md` (data.yaml manda).
- [ ] T018 `make check` y registrar evidencia en el PR.

## Dependencies & Execution Order

- T001 → T002 → T003–T010 → T011 → T012–T015 → T016–T018.
- T003–T010 pueden escribirse en paralelo.
- T016–T018 dependen de T015.

## Notes

- Sin GPU, dataset, pesos ni red.
- Las imágenes de prueba se generan con OpenCV dentro del test (`tmp_path`).
- HU-002 consume `ImageData`; no se define de nuevo.
