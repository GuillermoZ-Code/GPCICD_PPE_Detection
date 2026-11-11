# Feature Specification: HU-008 — Evaluar el desempeño del modelo de detección

**Feature Branch**: `feature/009-hu-008-evaluador`

**Created**: 2026-11-10

**Status**: Implementada — pendiente de PR

**Input**: Issue #8 — “Evaluar el desempeño del modelo de detección”.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Evaluación reproducible (Priority: P1)

Como evaluador del modelo, quiero medir su desempeño sobre una partición identificada,
para conocer su capacidad real y documentar sus limitaciones.

**Why this priority**: sin una evaluación reproducible no se puede afirmar que el
detector funciona ni comparar versiones del modelo con el baseline.

**Independent Test**: con un modelo local identificado y una partición etiquetada, el
evaluador genera un informe con métricas globales y por clase, configuración, versión
del modelo y partición, sin entrenar ni descargar pesos.

**Acceptance Scenarios**:

1. **Given** un modelo identificado y una partición etiquetada, **When** se ejecuta la
   evaluación, **Then** se genera un informe con métricas y quedan registrados la
   versión/SHA256 del modelo, la partición y la configuración.
2. **Given** una evaluación completada, **When** se consulta el informe, **Then** se
   presentan P, R, mAP50 y mAP50-95 globales y por las seis clases, con el número de
   instancias por clase.
3. **Given** una evaluación terminada, **When** se revisan los errores, **Then** se
   documentan casos representativos de falsos positivos y falsos negativos y las
   limitaciones observadas.
4. **Given** el conjunto reservado para evaluación final, **When** se evalúa el modelo,
   **Then** se usa la partición `test_original_sin_fuga` y se documenta cualquier
   contaminación o limitación de separación.

### Edge Cases

- Ruta del modelo inexistente o artefacto corrupto.
- Catálogo de clases del modelo distinto al `data.yaml`.
- Partición vacía o sin etiquetas.
- Clase sin instancias en la partición.
- Imagen sin detecciones; no debe tratarse como error.
- `conf`, `iou`, `imgsz` o `seed` distintos de la configuración registrada.
- Ejecución en CPU sin GPU.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El evaluador MUST cargar un artefacto YOLO desde una ruta configurable y
  MUST NOT entrenar ni descargar pesos.
- **FR-002**: El informe MUST registrar la ruta, versión y SHA256 del modelo, la
  partición usada, el SHA256 del dataset y la configuración de evaluación.
- **FR-003**: El sistema MUST calcular P, R, mAP50 y mAP50-95 globales y por clase, con
  el número de imágenes e instancias.
- **FR-004**: El sistema MUST generar un informe en JSON y Markdown, más matriz de
  confusión y curvas PR/F1 cuando el artefacto lo permita.
- **FR-005**: El informe MUST incluir un análisis de falsos positivos y falsos
  negativos con ejemplos representativos y limitaciones.
- **FR-006**: La evaluación final MUST usar `test_original_sin_fuga` para la comparación
  apples-to-apples y el test limpio para el desempeño del modelo ajustado; cualquier
  fuga o contaminación MUST documentarse.
- **FR-007**: La configuración MUST ser determinista: `imgsz=640`, `conf=0.001`,
  `iou=0.7`, `seed=42`, `deterministic=True`, `device=cpu`.
- **FR-008**: Las pruebas unitarias MUST ejecutarse sin GPU, sin dataset completo y sin
  red; la evaluación real puede omitirse si faltan los artefactos.

### Key Entities

- **ModelArtifact**: ruta, versión y SHA256 del modelo evaluado.
- **EvaluationConfig**: partición, `imgsz`, `conf`, `iou`, `seed` y dispositivo.
- **EvaluationReport**: métricas globales, métricas por clase, matriz de confusión y
  referencias de evidencia.
- **ErrorCase**: ejemplo representativo de falso positivo o falso negativo con su
  clase, confianza y contexto.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-008.1 Evaluación reproducible | `tests/test_evaluation.py::test_evaluate_writes_summary_and_does_not_train` |
| AC-008.2 Resultados por clase | `tests/test_evaluation.py::test_build_summary_contains_global_and_per_class_metrics` |
| AC-008.3 Análisis de errores | `docs/evaluation/HU-008.md` §6 |
| AC-008.4 Protección de particiones | `tests/test_evaluation.py::test_count_images_uses_declared_split` |
| FR-001 Sin entrenamiento | `tests/test_evaluation.py::test_evaluate_writes_summary_and_does_not_train` |
| FR-007 Configuración determinista | `tests/test_evaluation.py::test_default_config_is_deterministic` |
| FR-008 Pruebas sin GPU/dataset | Toda la suite de `tests/test_evaluation.py` usa métricas falsas |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El informe se regenera con un comando documentado y produce los mismos
  valores con la misma configuración y artefactos.
- **SC-002**: La evaluación de `test_original_sin_fuga` reproduce las métricas de
  referencia de Hernán dentro de una tolerancia numérica razonable.
- **SC-003**: `make check` pasa en verde sin GPU, sin dataset completo y sin red.
- **SC-004**: Cada AC de la issue #8 tiene al menos una prueba que lo referencia.

## Assumptions

- El modelo candidato es `yolo11s_clean/weights/best.pt`, SHA256
  `E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959`.
- El dataset limpio `ds_base` tiene 10.941 imágenes: train 7.659, valid 2.188,
  test 1.094 y eval sin fuga 492.
- El eval de 492 es la referencia apples-to-apples contra el baseline preentrenado;
  el test de 1.094 se usa para el desempeño del modelo ajustado.
- El entrenamiento usó Ultralytics 8.4.198; la reproducción local usó 8.4.202, que es
  la versión fijada por `uv.lock`. La diferencia de parche se declara en el informe.
- El informe existe en `docs/evaluation/HU-008.md`; el evaluador versionado está en
  `src/ppe_detection/evaluation/` y regeneró el eval de 492 y el test de 1.094.
