---
description: "Task list for HU-030 — Análisis de falsos positivos y negativos"
---

# Tasks: HU-030 — Análisis de falsos positivos y negativos

**Input**: `specs/031-hu-030-analisis-fp-fn/spec.md` y `plan.md`.

**Prerequisites**: issue #86, rama `feature/031-hu-030-analisis-fp-fn`,
`develop` actualizado.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-030.
- [ ] T002 Mover #86 a **In progress** en el tablero.
- [x] T003 Ejecutar `make ownership-check` antes del primer cambio.

## Phase 2: Tests

- [x] T004 [P] `test_matched_box_counts_as_true_positive` → AC-01.
- [x] T005 [P] `test_class_confusion_appears_in_fp_and_fn` → AC-02.
- [x] T006 [P] `test_localization_error_has_partial_overlap` → AC-02.
- [x] T007 [P] `test_small_object_fn_uses_area_ratio` → AC-02.
- [x] T008 [P] `test_background_fp_without_relevant_overlap` → AC-02.
- [x] T009 [P] `test_low_confidence_prediction_is_ignored` → AC-01.
- [x] T010 [P] `test_analysis_is_deterministic` → AC-01.
- [x] T011 [P] `test_report_has_categories_and_no_embedded_images` → AC-03.
- [x] T012 Ejecutar `uv run pytest tests/test_evaluation_errors.py -q` en verde.

## Phase 3: Implementation

- [x] T013 Implementar los tipos de entrada y `ErrorCase`/`ErrorSummary`.
- [x] T014 Implementar emparejamiento y categorías FP/FN.
- [x] T015 Implementar `render_error_report` sin imágenes.
- [x] T016 Exportar el analizador en `evaluation/__init__.py`.
- [x] T017 Recolectar predicciones de YOLO26n en test y escribir
  `docs/evaluation/errores.md`.
- [x] T018 Guardar la evidencia agregada en `dist/analisis/errores/summary.json`.

## Phase 4: Verification and close

- [x] T019 Ejecutar `make specs-check`.
- [x] T020 Ejecutar `make check`.
- [x] T021 Ejecutar `uv build`.
- [ ] T022 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md` con las
  8 pruebas nuevas.
- [ ] T023 Abrir PR a `develop` con la plantilla UAO y `Closes #86`.
- [ ] T024 Tras el merge, cerrar #86 a mano y moverla a Done.

## Notes

- Las categorías son geométricas; `occlusion_or_missed` requiere revisión visual.
- No se publican imágenes ni recortes.
- La evidencia pesada queda fuera de Git.
