# Feature Specification: HU-029 — Calibración de umbrales por clase

**Feature Branch**: `feature/030-hu-029-umbrales-por-clase`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #85 — «Calibración de umbrales de confianza por clase». Asignada a
Hernán (`HestradaUAO`), épica `ep-09`, P1, ola 3, 2 SP, 8 pruebas objetivo. Depende
de HU-019, ya cerrada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Elegir un umbral por clase con evidencia (Priority: P1)

Como evaluador del modelo, quiero un umbral de confianza por clase calculado sobre
validación, para mejorar el recall de las clases débiles sin aumentar de forma
descontrolada los falsos positivos.

**Why this priority**: un único umbral global de 0,25 no aprovecha que cada clase
tiene una distribución de confianza distinta. `safety_shoe`, `mask` y `Gloves` son
las clases con más margen de mejora.

**Independent Test**: con etiquetas y predicciones sintéticas se verifica que el
umbral elegido maximiza F1 por clase, que el YAML se escribe y se vuelve a leer, y
que la tabla antes/después conserva TP, FP, FN y P/R/F1.

**Acceptance Scenarios** (AC de la issue #85):

1. **AC-01**: **Dado** un conjunto de validación con etiquetas y predicciones,
   **Cuando** se ejecuta la calibración, **Entonces** se obtiene por clase el umbral
   que maximiza F1, calculado con código versionado.
2. **AC-02**: **Dado** el conjunto de test reservado, **Cuando** se comparan los
   umbrales base y calibrados, **Entonces** existe una tabla antes/después por clase
   con TP, FP, FN, precision, recall y F1.
3. **AC-03**: **Dado** el resultado de calibración, **Cuando** se exporta, **Entonces**
   se escribe `configs/thresholds.yaml` con las seis clases y un formato que el
   postprocesamiento puede consumir.

### Edge Cases

- Clase sin etiquetas en validación: conserva el umbral por defecto 0,25.
- Clase sin predicciones: conserva el umbral por defecto 0,25.
- Empate de F1 entre dos umbrales: se prefiere el umbral más alto.
- Predicciones duplicadas: el emparejamiento greedy no reutiliza una predicción.
- Clases distintas con cajas solapadas: no se emparejan entre sí.
- YAML incompleto o con una clase desconocida: falla con un error explícito.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La calibración MUST ser una función pura que reciba etiquetas y
  predicciones y no dependa de Ultralytics, GPU, dataset ni red.
- **FR-002**: La función MUST recorrer una rejilla de umbrales y elegir por clase el
  que maximiza F1; los empates se resuelven por precision y luego por umbral alto.
- **FR-003**: La calibración MUST conservar el umbral por defecto cuando una clase no
  tenga etiquetas o predicciones.
- **FR-004**: La evaluación antes/después MUST reportar TP, FP, FN, precision, recall
  y F1 por clase y un agregado micro.
- **FR-005**: El YAML MUST incluir versión, IoU de calibración y las seis clases
  canónicas; el lector MUST funcionar sin PyYAML.
- **FR-006**: La tabla antes/después MUST calcularse sobre test, no sobre validación.
- **FR-007**: No se modifica el contrato `ImageData → list[Detection]` ni el modelo.

### Key Entities

- **GroundTruth**: clase canónica y caja xyxy anotada.
- **Prediction**: clase canónica, confianza y caja xyxy candidata.
- **ImageRecord**: etiquetas y predicciones de una imagen.
- **ThresholdMetrics**: TP, FP, FN, precision, recall y F1 de una clase en un umbral.
- **configs/thresholds.yaml**: mapa clase → umbral consumible por postprocesamiento.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 Calibración por F1 | `tests/test_thresholds.py::test_calibrate_maximizes_f1_for_gloves`, `tests/test_thresholds.py::test_calibrate_uses_all_validation_records`, `tests/test_thresholds.py::test_calibrate_handles_class_without_ground_truth`, `tests/test_thresholds.py::test_calibrate_handles_class_without_predictions`, `tests/test_thresholds.py::test_calibrate_ties_prefer_higher_threshold` |
| AC-02 Tabla antes/después | `tests/test_thresholds.py::test_evaluate_thresholds_returns_before_after_counts`, `tests/test_thresholds.py::test_calibration_payload_is_traceable`, `docs/evaluation/umbrales.md` |
| AC-03 YAML consumible | `tests/test_thresholds.py::test_write_and_load_thresholds_roundtrip`, `tests/test_thresholds.py::test_repository_thresholds_yaml_has_six_classes` |

## Success Criteria *(mandatory)*

- **SC-001**: `make check` pasa sin extras de inferencia para las pruebas de
  calibración.
- **SC-002**: El umbral de cada clase se reproduce con `thresholds.py` y la evidencia
  local de validación/test.
- **SC-003**: El YAML contiene exactamente las seis clases canónicas.
- **SC-004**: La HU añade al menos 8 pruebas al inventario.

## Out of Scope

- Integrar el YAML en el detector o en la API; esa integración pertenece a HU-036.
- Analizar falsos positivos y negativos (HU-030) o matrices de confusión (HU-031).
- Reentrenar o cambiar el modelo productivo.
- Modificar `models.lock` o el artefacto desplegado.

## Assumptions

- La partición de validación es la del dataset limpio: 2.188 imágenes.
- La partición de test es la del dataset limpio: 1.095 imágenes.
- El IoU de calibración es 0,5 y el de evaluación del modelo es 0,7.
- Los pesos y el dataset están fuera de Git.
