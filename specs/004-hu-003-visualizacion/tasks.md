---
description: "Task list for HU-003 — Visualización de detecciones"
---

# Tasks: HU-003 — Visualizar las detecciones sobre la imagen

**Input**: Design documents from `specs/004-hu-003-visualizacion/`

**Prerequisites**: `plan.md`, `spec.md`, contrato TA-11 y carga de HU-001

**Tests**: obligatorias y **antes** de la implementación (test-first). Cada AC tiene al
menos una prueba que lo referencia.

## Phase 1: Tests first (deben fallar)

- [x] T001 [P] `test_empty_detections_return_unchanged_image` → AC-003.3.
- [x] T002 [P] `test_draws_box_at_expected_pixels` → AC-003.1.
- [x] T003 [P] `test_scales_when_canvas_differs` → AC-003.2.
- [x] T004 [P] `test_format_label` → AC-003.1.
- [x] T005 [P] `test_does_not_modify_input` → FR-001.
- [x] T006 [P] `test_write_image_roundtrip` → guardado.
- [x] T007 [P] `test_write_image_rejects_unknown_extension` → guardado.
- [x] T008 [P] `test_run_saves_annotated_images` → FR-007.
- [x] T009 `uv run pytest` en rojo.

## Phase 2: Implementación

- [x] T010 `io/images.py`: `write_image` y exportación en `io/__init__.py`.
- [x] T011 `visualization/overlay.py`: `DISPLAY_NAMES`, `COLORS`, `format_label` y
      `draw_detections`.
- [x] T012 `visualization/__init__.py` con la API pública.
- [x] T013 `detection/predict.py`: flag `--annotated` y guardado en `<salida>/annotated/`.
- [x] T014 `uv run pytest` en verde.

## Phase 3: Polish

- [x] T015 Documentar el componente en `docs/architecture/contracts.md`.
- [x] T016 Actualizar `docs/curso/backlog.md` con el enlace a la spec.
- [x] T017 `make check` y `uv build`.
- [x] T018 `make estado-write` y entrada en la bitácora.

## Dependencies & Execution Order

- T001–T008 pueden escribirse en paralelo.
- T010 → T011 → T012 → T013 → T014.
- T015–T018 al final.

## Notes

- Sin GPU, dataset, pesos ni red.
- No se dibujan advertencias de cumplimiento: fuera de alcance.
- La interfaz (HU-007) reutiliza `draw_detections`; aquí no se construye UI.
