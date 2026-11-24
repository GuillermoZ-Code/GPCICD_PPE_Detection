# Implementation Plan: HU-029 — Calibración de umbrales por clase

**Branch**: `feature/030-hu-029-umbrales-por-clase` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #85 y `specs/030-hu-029-umbrales-por-clase/spec.md`.

## Summary

Agregar un módulo puro de calibración que elige, por clase, el umbral de confianza
que maximiza F1. La evidencia se calcula una vez sobre validación y se reporta sobre
test. El resultado se exporta a `configs/thresholds.yaml` para que el futuro
postprocesamiento lo consuma sin acoplarse a YOLO ni al dataset.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `ppe_detection.contracts` y
`ppe_detection.evaluation.metrics`; sin Ultralytics en las pruebas

**Storage**: `configs/thresholds.yaml`; evidencia local en
`dist/analisis/calibracion/summary.json` (fuera de Git)

**Testing**: pytest AAA; casos sintéticos y un YAML temporal

**Target Platform**: CPU / CI

**Project Type**: biblioteca de evaluación

**Constraints**: no cargar GPU, dataset completo ni red en las pruebas; no modificar
el contrato; no versionar pesos

**Scale/Scope**: 6 clases; rejilla de 99 umbrales; 2.188 imágenes de validación y
1.095 de test para la evidencia real

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Pruebas en `tests/` y patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin GPU, dataset completo ni red en las pruebas.
- [x] Test-first: primero las pruebas de calibración y YAML.
- [x] No se cambia el contrato `ImageData → list[Detection]`.
- [x] Pesos y dataset fuera de Git.

## Project Structure

```text
src/ppe_detection/evaluation/
├── thresholds.py          # calibración pura, YAML y payload
tests/
└── test_thresholds.py     # 11 pruebas de AC-01/02/03
configs/
└── thresholds.yaml        # umbrales versionados de YOLO26n
docs/evaluation/
└── umbrales.md            # método, tablas y limitaciones
specs/030-hu-029-umbrales-por-clase/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Entradas

`ImageRecord` agrupa `GroundTruth` y `Prediction` de una imagen, ambos en coordenadas
xyxy. El módulo no interpreta imágenes ni etiquetas YOLO: recibe datos ya
normalizados.

### Calibración

Para cada clase se evalúa una rejilla de 0,01 a 0,99. En cada umbral:

1. Se filtran las predicciones de la clase con `confidence >= umbral`.
2. Se emparejan con las etiquetas por IoU 0,5 usando `match_detections`.
3. Se acumulan TP, FP y FN y se calcula P/R/F1.
4. Se elige el mayor F1; los empates se resuelven por precision y luego por umbral
   más alto.

Si no hay etiquetas o predicciones de una clase, se conserva 0,25.

### Evaluación antes/después

`evaluate_thresholds` recibe un mapa clase → umbral y devuelve las mismas métricas.
La tabla de test compara el mapa base (0,25 para todas) con el mapa calibrado.

### Exportación

`write_thresholds` escribe un YAML estable con versión, IoU y las seis clases.
`load_thresholds` lo lee sin PyYAML para que el postprocesamiento no arrastre una
dependencia nueva. `calibration_payload` deja un resumen trazable.

## Phases

1. **Tests**: 11 casos sintéticos de calibración, empates, clases vacías, evaluación
   y roundtrip YAML.
2. **Implementación**: `thresholds.py` y exportación a `configs/thresholds.yaml`.
3. **Evidencia**: recolectar predicciones de YOLO26n en validación/test con la misma
   configuración de evaluación; escribir `docs/evaluation/umbrales.md`.
4. **Cierre**: `make check`, PR con `Closes #85` y revisión.

## Risks

| Riesgo | Mitigación |
|---|---|
| Sobreajuste a validación | El test se reserva solo para la tabla antes/después |
| Clases con pocos objetos | Se reportan conteos y limitaciones; no se usa test para elegir |
| Umbrales extremos | La rejilla se limita a [0,01, 0,99] y se prefiere el umbral alto en empates |
| YAML sin PyYAML | Lector propio para el formato simple y versionado |
| Cambios de postprocesamiento | HU-036 consume el YAML; esta HU no modifica el detector |

## Verification

```bash
uv run pytest tests/test_thresholds.py -q
make check
```

La calibración real se ejecutó con YOLO26n (`best.pt`, SHA256
`FEFB1F1A…0F27F9`), `imgsz=640`, `conf=0.001`, `iou=0.7` y CPU. El resumen local está
en `dist/analisis/calibracion/summary.json`.
