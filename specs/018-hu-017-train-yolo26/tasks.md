---
description: "Task list for HU-017 — Script de entrenamiento YOLO26"
---

# Tasks: HU-017 — Script de entrenamiento YOLO26 parametrizable

**Input**: `specs/018-hu-017-train-yolo26/spec.md` y `plan.md`.

**Prerequisites**: issue #73, rama `feature/018-hu-017-train-yolo26`, HU-016
fusionada.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-017.
- [ ] T002 Mover #73 a **In progress** en el tablero.
- [x] T003 Crear la rama desde `develop`.

## Phase 2: Tests first

- [x] T004 [P] `test_parse_args_loads_yaml_config` → AC-01.
- [x] T005 [P] `test_yaml_accepts_yolo26_models` → AC-01.
- [x] T006 [P] `test_cli_overrides_yaml_config` → FR-003.
- [x] T007 [P] `test_config_rejects_unknown_key` → FR-004.
- [x] T008 [P] `test_config_requires_data_when_missing` → edge case.
- [x] T009 [P] `test_config_records_seed_imgsz_epochs_split` → AC-02.
- [x] T010 [P] `test_dry_run_does_not_require_data_or_gpu` → AC-03.
- [x] T011 [P] `test_versioned_configs_exist` → FR-007.
- [x] T012 Ejecutar `uv run pytest tests/test_training.py -q` y confirmar rojo.

## Phase 3: Implementation

- [x] T013 Añadir `--config`, `--dry-run` y `dry_run` a `TrainConfig`.
- [x] T014 Cargar y validar YAML; mezclar CLI > YAML > defaults.
- [x] T015 Crear `configs/train/yolo26n.yaml` y `yolo26s.yaml`.
- [x] T016 Implementar salida de dry-run sin cargar Ultralytics.
- [x] T017 Ejecutar las pruebas en verde.

## Phase 4: Verification and close

- [x] T018 Ejecutar `make ownership-check`.
- [x] T019 Ejecutar `make check` (438 passed, 1 skipped).
- [ ] T020 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md`.
- [ ] T021 Abrir PR a `develop` con la plantilla UAO y `Closes #73`.
- [ ] T022 Tras el merge, cerrar #73 a mano y moverla a Done.

## Notes

- No se entrena en esta HU.
- No se agregan dependencias.
- `--dry-run` no valida rutas ni carga modelos.
