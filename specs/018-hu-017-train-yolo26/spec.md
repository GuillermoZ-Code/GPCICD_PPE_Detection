# Feature Specification: HU-017 — Script de entrenamiento YOLO26 parametrizable

**Feature Branch**: `feature/018-hu-017-train-yolo26`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #73 — «Script de entrenamiento YOLO26 parametrizable». Asignada a
Hernán (`HestradaUAO`), épica `ep-09`, P0, Ola 3, 3 SP, 12 pruebas objetivo. Depende
de HU-016, ya fusionada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reproducir el entrenamiento sin notebooks (Priority: P0)

Como integrante del equipo ML, quiero un script versionado que entrene YOLO26 con la
misma configuración que YOLO11s, para reproducir el experimento en Colab/Kaggle sin
depender de un notebook.

**Why this priority**: el entrenamiento de YOLO26n ya se ejecutó, pero la configuración
estaba repartida entre CLI y argumentos de Colab. Un YAML versionado es necesario para
repetir el run y para HU-018/HU-019.

**Independent Test**: cargar `configs/train/yolo26n.yaml`, sobrescribir un valor por
CLI, ejecutar `--dry-run` y comprobar que la configuración resuelta registra modelo,
semilla, `imgsz`, épocas y partición sin cargar GPU ni Ultralytics.

**Acceptance Scenarios** (AC de la issue #73):

1. **AC-01**: **Dado** `training/train.py`, **Cuando** se pasa `--config` y
   `--model yolo26n.pt|yolo26s.pt`, **Entonces** lee hiperparámetros de un YAML
   versionado.
2. **AC-02**: **Dado** un run, **Cuando** se imprime la configuración, **Entonces**
   semilla, `imgsz`, épocas y partición quedan registradas.
3. **AC-03**: **Dado** `--dry-run`, **Cuando** se ejecuta, **Entonces** valida y
   muestra la configuración sin GPU, dataset ni Ultralytics.

### Edge Cases

- `--config` inexistente: error explícito.
- YAML con clave desconocida: error explícito.
- Config sin `data`: debe fallar si tampoco se pasa `--data`.
- CLI sobre YAML: el valor de CLI gana.
- Booleanos (`amp`, `cache`, `export_onnx`): `--no-amp` y `--amp` se respetan.
- `--dry-run` no exige que las rutas de datos existan.
- Sin `--config`: se conserva la CLI actual.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `parse_args()` MUST aceptar `--config PATH` y cargar YAML.
- **FR-002**: MUST permitir `--model yolo26n.pt` y `--model yolo26s.pt`.
- **FR-003**: CLI MUST sobrescribir los valores del YAML.
- **FR-004**: YAML MUST validar claves conocidas y tipos básicos.
- **FR-005**: `TrainConfig` MUST incluir `dry_run` y registrar la configuración
  resuelta.
- **FR-006**: `--dry-run` MUST salir con 0 sin validar archivos ni cargar modelos.
- **FR-007**: MUST versionar `configs/train/yolo26n.yaml` y `yolo26s.yaml`.
- **FR-008**: No se agregan dependencias; `PyYAML` ya es parte del entorno de
  entrenamiento.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 YAML + modelo | `test_parse_args_loads_yaml_config`, `test_yaml_accepts_yolo26_models` |
| AC-02 Configuración registrada | `test_config_records_seed_imgsz_epochs_split` |
| AC-03 Dry-run | `test_dry_run_does_not_require_data_or_gpu` |
| FR-003 CLI gana | `test_cli_overrides_yaml_config` |
| FR-004 Validación | `test_config_rejects_unknown_key` |
| FR-007 Configs | `test_versioned_configs_exist` |

## Success Criteria *(mandatory)*

- **SC-001**: El mismo YAML reproduce la configuración de YOLO26n.
- **SC-002**: `--dry-run` funciona en CI sin GPU ni dataset.
- **SC-003**: La CLI anterior sigue funcionando.
- **SC-004**: `make check` pasa sin dependencias nuevas.

## Out of Scope

- Entrenar en esta HU.
- Cambiar el modelo productivo.
- Publicar el modelo.
- Modificar la evaluación o la API.

## Assumptions

- `PyYAML` está disponible en el entorno de entrenamiento (ya se usa en `train.py`).
- Los YAML de entrenamiento usan rutas de Colab; `--dry-run` no las valida.
- El script existente conserva su comportamiento si no se usa `--config`.
