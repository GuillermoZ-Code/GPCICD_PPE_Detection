# Implementation Plan: HU-031 — Matriz de confusión y curvas PR como artefactos

**Branch**: `feature/032-hu-031-artefactos-evaluacion` | **Date**: 2026-11-24

**Spec**: [spec.md](spec.md)

**Input**: Issue #87 y `specs/032-hu-031-artefactos-evaluacion/spec.md`.

## Summary

Agregar una capa de recolección de figuras de evaluación. Ultralytics ya genera la
matriz de confusión y las curvas PR cuando `plots=True`; el problema es que sus
nombres son genéricos. La nueva capa copia esas figuras a nombres estables por modelo
y las registra en el `summary.json` para que el flujo de MLflow pueda adjuntarlas.

No se generan figuras nuevas ni se modifica el modelo.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: stdlib (`pathlib`, `shutil`, `re`) y pytest

**Storage**: archivos PNG temporales; el `summary.json` guarda sus rutas

**Testing**: pytest AAA con directorios temporales, sin Ultralytics

**Target Platform**: CPU / CI

**Project Type**: biblioteca de evaluación

**Constraints**: no cargar YOLO, GPU, dataset ni red; no agregar dependencias

**Scale/Scope**: 7 nombres de figura, 5 pruebas, un modelo y su SHA256

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Pruebas en `tests/` y patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin GPU, dataset completo ni red.
- [x] Test-first: primero las pruebas de nombres y copia.
- [x] No se cambia `ImageData → list[Detection]`.
- [x] Pesos y datasets fuera de Git.

## Project Structure

```text
src/ppe_detection/evaluation/
├── artifacts.py              # nombres estables y recolección
└── evaluate.py               # integra los artefactos en el summary
tests/
└── test_evaluation_artifacts.py
specs/032-hu-031-artefactos-evaluacion/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Nombres estables

`artifact_slug(model_version, sha256)` normaliza la versión a minúsculas y guiones y
añade los primeros 12 caracteres del SHA256. Ejemplo:

```text
YOLO26n clean + FEFB1F1A… → yolo26n-clean-fefb1f1a120f
```

`stable_artifact_name()` mapea:

| Fuente Ultralytics | Nombre estable |
|---|---|
| `confusion_matrix.png` | `confusion_matrix_<slug>.png` |
| `confusion_matrix_normalized.png` | `confusion_matrix_normalized_<slug>.png` |
| `BoxPR_curve.png` / `PR_curve.png` | `pr_curve_<slug>.png` |
| `BoxF1_curve.png` | `f1_curve_<slug>.png` |
| `BoxP_curve.png` | `precision_curve_<slug>.png` |
| `BoxR_curve.png` | `recall_curve_<slug>.png` |

### Recolección

`collect_evaluation_artifacts(source_dir, destination_dir, model_version, sha256)`
recorre solo los nombres conocidos, copia los que existen y devuelve las rutas. Un
directorio sin figuras devuelve `()`.

### Integración

`evaluate()` usa `metrics.save_dir` cuando existe; si no, el directorio de salida.
Después de `model.val(plots=True)` copia las figuras y escribe:

```json
"artifacts": [".../confusion_matrix_best-<sha12>.png", "..."]
```

El registro en MLflow conserva el mecanismo `--artifact` existente; no se modifica
`tracking/`.

## Phases

1. **Tests:** nombres, copia, caso vacío, figura desconocida e integración.
2. **Implementación:** `artifacts.py` y llamada desde `evaluate.py`.
3. **Verificación:** `make specs-check`, `make check`, `uv build`.
4. **Cierre:** PR con `Closes #87`.

## Risks

| Riesgo | Mitigación |
|---|---|
| Ultralytics cambia un nombre de figura | El mapeo es explícito y una figura desconocida no se copia |
| Se sobrescriben artefactos | El nombre incluye versión y SHA256 |
| `metrics.save_dir` no existe en pruebas | Se usa el directorio de salida y se devuelve vacío |
| Se copian archivos ajenos | Solo se recorren nombres del contrato FIGURES |
| Se duplica `BoxPR_curve` y `PR_curve` | Ambos apuntan al mismo nombre semántico estable |

## Verification

```bash
uv run pytest tests/test_evaluation_artifacts.py -q
make specs-check
make check
uv build
```
