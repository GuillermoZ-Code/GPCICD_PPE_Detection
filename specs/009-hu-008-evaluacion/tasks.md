---
description: "Task list for HU-008 — Evaluación del detector"
---

# Tasks: HU-008 — Evaluar el desempeño del modelo

**Input**: Design documents from `specs/009-hu-008-evaluacion/`

**Prerequisites**: `plan.md`, `spec.md`, modelo y dataset identificados

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Tests first

- [ ] T001 Crear `tests/test_evaluation.py` con métricas falsas y fixtures.
- [ ] T002 [P] `test_report_records_model_partition_and_config` → AC-008.1.
- [ ] T003 [P] `test_report_contains_global_and_per_class_metrics` → AC-008.2.
- [ ] T004 [P] `test_report_requires_error_analysis_section` → AC-008.3.
- [ ] T005 [P] `test_eval_partition_is_explicit` → AC-008.4.
- [ ] T006 [P] `test_evaluator_does_not_train` → FR-001.
- [ ] T007 [P] `test_default_config_is_deterministic` → FR-007.
- [ ] T008 Ejecutar `uv run pytest tests/test_evaluation.py` y confirmar rojo.

## Phase 2: Evaluador

- [ ] T009 Crear `src/ppe_detection/evaluation/__init__.py` y `evaluate.py`.
- [ ] T010 Cargar el modelo desde `--model`, validar catálogo y SHA256.
- [ ] T011 Ejecutar `YOLO.val` con `imgsz=640`, `conf=0.001`, `iou=0.7`, `seed=42`.
- [ ] T012 Escribir `summary.json`, `summary.md`, matriz y curvas en `artifacts/eval/`.
- [ ] T013 Verificar que no se entrena ni se descargan pesos.
- [ ] T014 Ejecutar pruebas unitarias en verde.

## Phase 3: Evidencia

- [ ] T015 Evaluar `test_original_sin_fuga` (492) y comparar con SPI-02.
- [ ] T016 Evaluar `test` limpio (1.094) y registrar métricas por clase.
- [ ] T017 Documentar FP/FN representativos y limitaciones.
- [ ] T018 Completar `docs/evaluation/HU-008.md` con la evidencia versionada.

## Phase 4: Cierre

- [ ] T019 `make check` y `uv build`.
- [ ] T020 Actualizar `specs/README.md`, backlog y estado.
- [ ] T021 Abrir PR a `develop` y solicitar revisión.

## Notes

- El informe preliminar de esta rama ya contiene las métricas reproducidas con
  Ultralytics 8.4.202; la implementación versionada debe regenerarlo.
- No se versionan pesos, dataset, `runs/` ni `artifacts/`.
- `safety_shoe` tiene solo 6 objetos en eval492; no se deben sacar conclusiones de esa
  clase en esa partición.
