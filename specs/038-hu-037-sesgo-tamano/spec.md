# Feature Specification: HU-037 — Evaluación por tamaño de objeto

**Feature Branch**: `feature/038-hu-037-sesgo-tamano`

**Created**: 2026-11-26

**Status**: En implementación

**Input**: Issue #93 — «Evaluación por tamaño de objeto». Asignada a Hernán
(`HestradaUAO`), épica `ep-09`, P2, ola 3, 1 SP, 4 pruebas objetivo. Depende de HU-019,
ya cerrada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Medir el sesgo de tamaño (Priority: P2)

Como evaluador del modelo, quiero AP por objetos pequeños, medianos y grandes, para
entender el sesgo de tamaño y explicar dónde falla el detector.

**Why this priority**: el error global puede ocultar que las clases con objetos
pequeños tienen un rendimiento distinto. La tabla por tamaño permite una lectura más
honesta.

**Independent Test**: con cajas sintéticas se verifica la clasificación por área y el
AP de un bucket; con el modelo real se genera la tabla por clase.

**Acceptance Scenarios** (AC de la issue #93):

1. **AC-01**: **Dada** una caja y una imagen, **Cuando** se clasifica, **Entonces** se
   asigna a pequeño, mediano o grande con umbrales documentados.
2. **AC-02**: **Dado** el conjunto de test, **Cuando** se evalúa, **Entonces** existe
   una tabla de AP por clase y tamaño.
3. **AC-03**: **Dadas** las funciones puras, **Cuando** corren las pruebas, **Entonces**
   no requieren YOLO, GPU ni dataset.

### Edge Cases

- Caja sin área: cae en `small`.
- Imagen o umbral inválido: error explícito.
- Clase sin GT en un bucket: AP 0 y conteo 0.
- Predicción sin GT en su bucket: FP.
- Objeto justo en 1 % o 4 %: se asigna al bucket superior.
- Test desbalanceado: se reportan los conteos GT.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `size_bucket()` MUST usar área relativa y umbrales 1 % / 4 %.
- **FR-002**: `average_precision_by_size()` MUST emparejar GT y predicciones del mismo
  bucket con IoU 0,50.
- **FR-003**: El AP MUST ordenar predicciones por confianza y usar `average_precision`.
- **FR-004**: La tabla MUST cubrir las seis clases y tres buckets.
- **FR-005**: El informe MUST declarar que no publica imágenes.
- **FR-006**: Las pruebas MUST ser puras y no cargar YOLO.
- **FR-007**: No se modifica el contrato ni el modelo.

### Key Entities

- **SizeMetrics**: AP, conteos y P/R de una clase/bucket.
- **Bucket**: small, medium, large.
- **ImageAnnotations**: GT y predicciones ya convertidas.
- **Informe**: `docs/evaluation/tamano.md`.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 Clasificación por área | `tests/test_size_bias.py::test_size_bucket_classifies_relative_area`, `tests/test_size_bias.py::test_size_bucket_rejects_invalid_parameters` |
| AC-02 Tabla AP por clase/tamaño | `tests/test_size_bias.py::test_perfect_detection_has_ap_one`, `tests/test_size_bias.py::test_missed_detection_has_zero_ap`, `tests/test_size_bias.py::test_evaluate_size_bias_covers_all_classes_and_buckets`, `docs/evaluation/tamano.md` |
| AC-03 Funciones puras | Suite completa sin YOLO/GPU/dataset |

## Success Criteria *(mandatory)*

- **SC-001**: La clasificación es determinista y documentada.
- **SC-002**: La tabla incluye conteos GT para interpretar el soporte.
- **SC-003**: El informe no publica imágenes ni recortes.
- **SC-004**: La HU añade al menos 4 pruebas.

## Out of Scope

- Reentrenar o calibrar el modelo.
- Cambiar las etiquetas del dataset.
- Producir recortes o imágenes.
- Calcular mAP COCO oficial; se reporta AP por bucket con el mismo emparejamiento.

## Assumptions

- Las cajas están en píxeles y la imagen tiene dimensiones conocidas.
- El umbral de tamaño es relativo al área de la imagen.
- El test es la partición de 1.095 imágenes.
- Los pesos y el dataset están fuera de Git.
