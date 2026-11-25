# Feature Specification: HU-030 — Análisis de falsos positivos y negativos

**Feature Branch**: `feature/031-hu-030-analisis-fp-fn`

**Created**: 2026-11-24

**Status**: En implementación

**Input**: Issue #86 — «Análisis de falsos positivos y negativos». Asignada a Hernán
(`HestradaUAO`), épica `ep-09`, P1, ola 3, 2 SP, 8 pruebas objetivo. Depende de
HU-019, ya cerrada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Explicar los errores del detector (Priority: P1)

Como evaluador del modelo, quiero ejemplos y causas de falsos positivos y negativos,
para explicar las limitaciones del detector en la sustentación sin publicar imágenes
de personas.

**Why this priority**: las métricas globales no explican por qué falla el modelo.
`helmet`, `Gloves` y `safety_shoe` concentran errores que la matriz de confusión no
desglosa por causa geométrica.

**Independent Test**: con cajas sintéticas se ejecuta el analizador, se comprueban
TP/FP/FN y sus categorías, y se genera un Markdown sin imágenes incrustadas.

**Acceptance Scenarios** (AC de la issue #86):

1. **AC-01**: **Dadas** etiquetas y predicciones, **Cuando** se ejecuta el análisis,
   **Entonces** la selección de TP, FP y FN es reproducible con IoU y confianza
   explícitos.
2. **AC-02**: **Dado** un error, **Cuando** se clasifica, **Entonces** recibe una
   categoría geométrica: confusión de clase, localización, objeto pequeño, duplicado,
   fondo u oclusión/no detectado.
3. **AC-03**: **Dado** el resumen, **Cuando** se genera el informe, **Entonces** usa
   solo conteos, nombres de archivo y geometría, sin publicar imágenes ni recortes.

### Edge Cases

- Predicción bajo el umbral de confianza: no cuenta como FP.
- Caja de otra clase con IoU alto: `class_confusion` en FP y FN.
- Caja desplazada con IoU entre 0,1 y 0,5: `localization`.
- Objeto con área menor al 1 % de la imagen: `small_object`.
- FP sin solapamiento: `background`.
- FN sin predicción cercana: `occlusion_or_missed`.
- Duplicado de una caja ya emparejada: `duplicate`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El análisis MUST usar `match_detections` por clase con IoU 0,50.
- **FR-002**: El umbral de confianza por defecto MUST ser 0,25 y ser configurable.
- **FR-003**: Cada FP y FN MUST registrar clase, imagen, categoría, confianza/IoU y
  área relativa.
- **FR-004**: El resumen MUST incluir TP, FP, FN, precision, recall y F1.
- **FR-005**: El informe MUST declarar que no se publican imágenes ni recortes.
- **FR-006**: El análisis MUST ser determinista y no cargar YOLO, dataset ni red.
- **FR-007**: No se modifica el contrato `ImageData → list[Detection]`.
- **FR-008**: No se agregan dependencias.

### Key Entities

- **GroundTruthBox**: clase y caja anotada.
- **PredictionBox**: clase, confianza y caja predicha.
- **ImageAnnotations**: imagen, tamaño, etiquetas y predicciones.
- **ErrorCase**: FP o FN con categoría y métricas geométricas.
- **ErrorSummary**: agregado de errores y métricas globales.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 TP/FP/FN reproducible | `tests/test_evaluation_errors.py::test_matched_box_counts_as_true_positive`, `tests/test_evaluation_errors.py::test_low_confidence_prediction_is_ignored`, `tests/test_evaluation_errors.py::test_analysis_is_deterministic` |
| AC-02 Categorías | `tests/test_evaluation_errors.py::test_class_confusion_appears_in_fp_and_fn`, `tests/test_evaluation_errors.py::test_localization_error_has_partial_overlap`, `tests/test_evaluation_errors.py::test_small_object_fn_uses_area_ratio`, `tests/test_evaluation_errors.py::test_background_fp_without_relevant_overlap` |
| AC-03 Informe sin imágenes | `tests/test_evaluation_errors.py::test_report_has_categories_and_no_embedded_images`, `docs/evaluation/errores.md` |

## Success Criteria *(mandatory)*

- **SC-001**: `make check` pasa sin GPU, dataset ni red.
- **SC-002**: Los conteos de una ejecución se reproducen dos veces.
- **SC-003**: El informe permite explicar al menos tres causas de error con evidencia.
- **SC-004**: La HU añade al menos 8 pruebas al inventario.
- **SC-005**: No se publican imágenes con personas.

## Out of Scope

- Reentrenar el modelo.
- Calibrar umbrales (HU-029).
- Generar la matriz de confusión o curvas PR (HU-031).
- Revisión visual manual de todas las imágenes.
- Cambiar el dataset o sus etiquetas.

## Assumptions

- Las cajas están en píxeles y la imagen tiene dimensiones conocidas.
- Las categorías son geométricas; la oclusión real requiere revisión visual.
- El test de 1.095 imágenes tiene 1.920 objetos.
- Los pesos y el dataset están fuera de Git.
