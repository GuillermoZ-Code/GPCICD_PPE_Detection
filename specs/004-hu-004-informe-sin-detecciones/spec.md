# Feature Specification: HU-004 — Informar cuando no se detectan elementos de protección personal

**Feature Branch**: `feature/004-hu-004-informe-sin-detecciones`

**Created**: 2026-11-10

**Status**: Especificada

**Input**: Issue #4 — “HU-004 — Informar cuando no se detectan elementos de
protección personal”. Asignada a Eliana (EP-01, Must Have, M3-S1).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Distinguir una inferencia vacía de un fallo (Priority: P1)

Como usuario del sistema, quiero recibir una indicación clara cuando el modelo no
encuentre objetos de las categorías configuradas, para distinguir una inferencia sin
detecciones de un fallo de la aplicación.

**Why this priority**: una respuesta vacía es un resultado válido; tratarla como error
o como “cumplimiento/incumplimiento” haría inviable la API (HU-006), la interfaz
(HU-007) y gRPC (HU-010).

**Independent Test**: con `FakeDetector` del contrato, un resultado vacío produce una
colección vacía, un mensaje en español y `is_error = False`; un fallo real
(excepción) produce `is_error = True` y nunca el mensaje de vacío. Sin GPU, sin
pesos y sin red.

**Acceptance Scenarios** (AC de la issue #4):

1. **AC-004.1**: **Dada** una imagen procesada correctamente, **Y** una respuesta del
   modelo sin detecciones que cumplan el criterio de filtrado configurado, **Cuando**
   se consulta el resultado, **Entonces** el sistema devuelve una colección vacía de
   detecciones, **Y** comunica que no se detectaron objetos EPP.
2. **AC-004.2**: **Dada** una inferencia ejecutada correctamente sin objetos,
   **Cuando** el sistema genera su respuesta, **Entonces** no clasifica el resultado
   como error de procesamiento (los fallos reales siguen siendo errores).
3. **AC-004.3**: **Dado** un resultado vacío, **Cuando** se presenta al usuario,
   **Entonces** no se afirma que una persona incumple una norma de seguridad, **Y** no
   se interpreta la ausencia de detección como prueba de ausencia real de EPP.

### Edge Cases

- Respuesta `None` del modelo (violación del contrato) ≠ colección vacía `[]`.
- Fallos reales: imagen corrupta (`ContractError` de HU-001/HU-005), artefacto no
  cargado, `ultralytics` ausente.
- Un solo objeto detectado: redacción singular en español (“Se detectó 1 objeto EPP”).
- Varios objetos de la misma clase: agrupación por clase con recuento `xN`.
- Mensajes no deben usar verbos afirmativos de presencia/ausencia real ni
  “incumple/incumplía/falta”.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST exponer un `InferenceResult` que envuelva la colección
  de `Detection` y un mensaje textual en español, con `is_empty` y `is_error`
  explícitos, para que HU-006, HU-007 y HU-010 compartan la misma semántica.
- **FR-002**: Con colección vacía, `InferenceResult` MUST devolver `detections` vacía
  y el mensaje exacto `NO_DETECTIONS_MESSAGE = "No se detectaron objetos EPP en la
  imagen."` (redacción por detección: “no se detectaron”, no “no hay”).
- **FR-003**: El resultado vacío MUST clasificarse con `is_empty = True` e
  `is_error = False`; MUST NOT levantar excepciones ni marcar fallo.
- **FR-004**: Fallos reales (excepción o respuesta `None`) MUST clasificarse con
  `is_error = True`, `is_empty = False` y un mensaje que identifique el fallo, sin
  confundirse con el caso vacío.
- **FR-005**: Con detecciones, el mensaje MUST listar las clases detectadas con
  recuento usando los nombres canónicos del catálogo (`CLASSES` del `data.yaml`).
- **FR-006**: El módulo MUST ser determinista, offline y reutilizar el contrato
  existente (`Detection`, `FakeDetector`); sin GPU ni dataset.
- **FR-007**: MUST existir una constante `RESPONSIBLE_USE_NOTE` que enuncie que la
  ausencia de detección no prueba ausencia real de EPP ni constituye incumplimiento,
  disponible para API/UI (AC AGPL/uso responsable propuesto para HU-007/HU-015,
  pendiente de validación de Jesús).
- **FR-008**: La CLI de inferencia (punto de consulta existente de HU-002) MUST
  incluir `NO_DETECTIONS_MESSAGE` en su resumen cuando la corrida no genera
  detecciones, sin clasificarse como error (código de salida 0); los fallos reales
  de carga (imagen corrupta, modelo ausente) se lanzan como excepciones.

### Key Entities

- **InferenceResult**: `detections: tuple[Detection, ...]`, `is_empty: bool`,
  `is_error: bool`, `message: str`.
- **Detection / ImageData / FakeDetector**: contrato existente de HU-001/HU-002.
- **NO_DETECTIONS_MESSAGE / RESPONSIBLE_USE_NOTE**: constantes de redacción.

## Acceptance → Test

| AC | Prueba pytest |
|----|----------------|
| AC-004.1 Colección vacía + mensaje | `tests/test_results.py::test_empty_inference_returns_empty_collection_and_message` |
| AC-004.2 Vacío no es error | `tests/test_results.py::test_empty_result_is_not_classified_as_error` |
| AC-004.2 Fallos reales sí son error | `tests/test_results.py::test_real_failure_is_classified_as_error_and_not_empty_success` |
| AC-004.2 `None` ≠ vacío | `tests/test_results.py::test_null_response_is_rejected_as_contract_error` |
| AC-004.3 Redacción responsable | `tests/test_results.py::test_empty_message_does_not_assert_noncompliance_or_absence` |
| FR-005 Resumen con clases | `tests/test_results.py::test_nonempty_result_summarizes_detected_classes` |
| FR-005 Orden canónico | `tests/test_results.py::test_listing_order_follows_canonical_catalog` |
| FR-006 Integración FakeDetector | `tests/test_results.py::test_fake_detector_empty_result_flows_through_contract` |
| FR-007 Nota de uso responsable | `tests/test_results.py::test_responsible_use_note_states_detection_only` |
| FR-008 Resumen CLI vacío | `tests/test_predict.py::test_format_summary_empty_uses_contract_message` |
| AC-004.1/.2 Flujo CLI sin detecciones | `tests/test_predict.py::test_run_prints_empty_message_without_error` |
| AC-004.2 Error real en CLI | `tests/test_predict.py::test_run_raises_real_error_for_corrupt_image` |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `make check` pasa en verde (pruebas sin GPU, sin pesos, sin red).
- **SC-002**: Cada AC de la issue #4 tiene al menos una prueba pytest que lo
  referencia (`AC-004.x` en docstring), escrita antes de la implementación (rojo
  primero).
- **SC-003**: El mensaje vacío es literal e idéntico para futuras superficies: API
  (HU-006), Streamlit (HU-007) y gRPC (HU-010) consumen este contrato; no lo
  redefinen.

## Assumptions

- El filtrado (confianza, IoU/NMS) ya lo aplica HU-002; este módulo recibe
  detecciones post-filtrado.
- El mensaje vacío queda integrado en el punto de consulta disponible (CLI de
  `detection.predict.format_summary`); la presentación HTTP/gráfica llega con
  HU-006/HU-007/HU-010 reutilizando este mismo contrato.
- Los nombres de clase se muestran tal cual el catálogo canónico; capitalizarlos o
  traducirlos es de la interfaz (HU-007), no de este contrato.
- No hay dependencias nuevas: usa `numpy`; sin `ultralytics` en las pruebas.
