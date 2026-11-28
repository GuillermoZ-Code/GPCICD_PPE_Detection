---
description: "Task list for HU-035 — Módulo de preprocesamiento con contrato numérico"
---

# Tasks: HU-035 — Módulo de preprocesamiento con contrato numérico

**Input**: `specs/036-hu-035-preprocessing/spec.md` y `plan.md`.

**Prerequisites**: issue #91, rama `feature/036-hu-035-preprocessing`,
`develop` actualizado.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-035.
- [ ] T002 Mover #91 a **In progress** en el tablero.
- [x] T003 Ejecutar `make ownership-check` antes del primer cambio.

## Phase 2: Tests

- [x] T004 [P] `test_letterbox_preserves_aspect_ratio_and_shape` → AC-01.
- [x] T005 [P] `test_letterbox_uses_configured_padding_color` → AC-01.
- [x] T006 [P] `test_letterbox_can_disable_scaleup` → AC-03.
- [x] T007 [P] `test_letterbox_rejects_invalid_image` → AC-01.
- [x] T008 [P] `test_inverse_letterbox_restores_original_coordinates` → AC-02.
- [x] T009 [P] `test_inverse_letterbox_clips_to_original_image` → AC-02.
- [x] T010 [P] `test_normalize_image_returns_float32_in_unit_range` → AC-01.
- [x] T011 [P] `test_non_square_target_centers_padding` → AC-03.
- [x] T012 Ejecutar `uv run pytest tests/test_preprocessing.py -q`.

## Phase 3: Implementation

- [x] T013 Implementar `LetterboxResult` y `letterbox`.
- [x] T014 Implementar `inverse_letterbox_boxes`.
- [x] T015 Implementar `normalize_image`.
- [x] T016 Exportar el módulo en `preprocessing/__init__.py`.

## Phase 4: Verification and close

- [x] T017 Ejecutar `make specs-check`.
- [x] T018 Ejecutar `make check`.
- [x] T019 Ejecutar `uv build`.
- [ ] T020 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md` con las
  8 pruebas nuevas.
- [ ] T021 Abrir PR a `develop` con la plantilla UAO y `Closes #91`.
- [ ] T022 Tras el merge, cerrar #91 a mano y moverla a Done.

## Notes

- No se modifica el detector ni el contrato.
- Las pruebas usan imágenes sintéticas; no se leen datasets.
- El orden de `new_shape` es `(alto, ancho)`.
