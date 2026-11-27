---
description: "Task list for HU-037 — Evaluación por tamaño de objeto"
---

# Tasks: HU-037 — Evaluación por tamaño de objeto

**Input**: `specs/038-hu-037-sesgo-tamano/spec.md` y `plan.md`.

**Prerequisites**: issue #93, rama `feature/038-hu-037-sesgo-tamano`,
`develop` actualizado.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-037.
- [ ] T002 Mover #93 a **In progress** en el tablero.
- [x] T003 Ejecutar `make ownership-check` antes del primer cambio.

## Phase 2: Tests

- [x] T004 [P] `test_size_bucket_classifies_relative_area` → AC-01.
- [x] T005 [P] `test_size_bucket_rejects_invalid_parameters` → AC-01.
- [x] T006 [P] `test_perfect_detection_has_ap_one` → AC-02.
- [x] T007 [P] `test_missed_detection_has_zero_ap` → AC-02.
- [x] T008 [P] `test_evaluate_size_bias_covers_all_classes_and_buckets` → AC-02.
- [x] T009 Ejecutar `uv run pytest tests/test_size_bias.py -q`.

## Phase 3: Implementation

- [x] T010 Implementar `size_bucket` con umbrales 1 % / 4 %.
- [x] T011 Implementar AP por clase/bucket con IoU 0,50.
- [x] T012 Exportar el módulo en `evaluation/__init__.py`.
- [x] T013 Recolectar predicciones de YOLO26n en test y escribir `tamano.md`.
- [x] T014 Guardar la evidencia en `dist/analisis/tamano/summary.json`.

## Phase 4: Verification and close

- [x] T015 Ejecutar `make specs-check`.
- [x] T016 Ejecutar `make check`.
- [x] T017 Ejecutar `uv build`.
- [ ] T018 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md` con las
  5 pruebas nuevas.
- [ ] T019 Abrir PR a `develop` con la plantilla UAO y `Closes #93`.
- [ ] T020 Tras el merge, cerrar #93 a mano y moverla a Done.

## Notes

- Las pruebas no cargan YOLO ni dataset.
- La tabla real usa la partición de test de 1.095 imágenes.
- No se publican imágenes ni recortes.
