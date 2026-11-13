---
description: "Task list for HU-008 — Evaluación del detector"
---

# Tasks: HU-008 — Evaluar el desempeño del modelo

**Input**: Design documents from `specs/009-hu-008-evaluacion/`

**Prerequisites**: `plan.md`, `spec.md`, modelo y dataset identificados

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Tests first

- [x] T001 Crear `tests/test_evaluation.py` con métricas falsas y fixtures.
- [x] T002 [P] `test_evaluate_writes_summary_and_does_not_train` → AC-008.1/FR-001.
- [x] T003 [P] `test_build_summary_contains_global_and_per_class_metrics` → AC-008.2.
- [x] T004 [P] `test_render_markdown_includes_global_and_classes` → informe.
- [x] T005 [P] `test_count_images_uses_declared_split` → AC-008.4.
- [x] T006 [P] `test_evaluate_writes_summary_and_does_not_train` → FR-001.
- [x] T007 [P] `test_default_config_is_deterministic` → FR-007.
- [x] T008 Ejecutar `uv run pytest tests/test_evaluation.py` y confirmar rojo.

## Phase 2: Evaluador

- [x] T009 Crear `src/ppe_detection/evaluation/__init__.py` y `evaluate.py`.
- [x] T010 Cargar el modelo desde `--model`, validar catálogo y SHA256.
- [x] T011 Ejecutar `YOLO.val` con `imgsz=640`, `conf=0.001`, `iou=0.7`, `seed=42`.
- [x] T012 Escribir `summary.json`, `summary.md`, matriz y curvas en `artifacts/eval/`.
- [x] T013 Verificar que no se entrena ni se descargan pesos.
- [x] T014 Ejecutar pruebas unitarias en verde.

## Phase 3: Evidencia

- [x] T015 Evaluar `test_original_sin_fuga` (492) y comparar con SPI-02.
- [x] T016 Evaluar `test` limpio (1.094) y registrar métricas por clase desde el módulo.
- [x] T017 Documentar FP/FN representativos y limitaciones.
- [x] T018 Completar `docs/evaluation/HU-008.md` con la regeneración versionada del test 1.094.

## Phase 4: Cierre

- [x] T019 `make check` y `uv build`.
- [x] T020 Actualizar `specs/README.md`, backlog y estado.
- [x] T021 Abrir PR a `develop` y solicitar revisión (PR #51).

## Notes

- El evaluador versionado regeneró el informe con Ultralytics 8.4.202; las métricas
  coinciden con la evidencia preliminar.
- No se versionan pesos, dataset, `runs/` ni `artifacts/`.
- `safety_shoe` tiene solo 6 objetos en eval492; no se deben sacar conclusiones de esa
  clase en esa partición.
