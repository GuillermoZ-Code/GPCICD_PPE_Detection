# Implementation Plan: HU-017 — Script de entrenamiento YOLO26

**Branch**: `feature/018-hu-017-train-yolo26` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #73 y `specs/018-hu-017-train-yolo26/spec.md`.

## Summary

Añadir carga de configuración YAML y `--dry-run` a `training/train.py`. La CLI
existente se conserva; los valores YAML se usan como base y la CLI los sobrescribe.
Los YAML de YOLO26n/s quedan versionados en `configs/train/`.

## Technical Context

**Python**: 3.13

**Dependencias**: `PyYAML` ya usada por el script; sin dependencias nuevas para el
paquete base.

**Testing**: pytest con `tmp_path`; no usa GPU, dataset ni Ultralytics.

**Archivos**:

```text
configs/train/yolo26n.yaml
configs/train/yolo26s.yaml
src/ppe_detection/training/train.py
tests/test_training.py
```

## Design

### YAML

Claves permitidas: `data`, `eval_data`, `model`, `epochs`, `imgsz`, `batch`,
`device`, `project`, `name`, `seed`, `patience`, `workers`, `save_period`, `resume`,
`export_onnx`, `backup_dir`, `mlflow_uri`, `mlflow_experiment`, `cache`, `amp`,
`eval_split`, `skip_eval`, `dry_run`.

### Precedencia

1. Argumento CLI explícito.
2. Valor del YAML.
3. Valor por omisión del script.

### Dry-run

`main()` imprime `asdict(config)` y retorna 0 antes de `_validate_config()`. No carga
Ultralytics ni exige rutas existentes.

### Compatibilidad

Sin `--config`, `parse_args()` mantiene los valores por omisión actuales y exige
`--data`. Los tests existentes deben seguir pasando.

## Risks

- **Booleanos opcionales**: `argparse` con `default=None` para distinguir “no
  especificado” de `False`.
- **Rutas YAML**: se convierten a `Path` después de la mezcla.
- **Specs/ es de Jesús**: la spec genera aviso de propiedad.
- **Configs de Colab**: las rutas `/content/...` son intencionales; el dry-run no las
  valida.
