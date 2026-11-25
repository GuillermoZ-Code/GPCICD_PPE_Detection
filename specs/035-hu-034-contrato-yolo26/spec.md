# Feature Specification: HU-034 — Pruebas de contrato del detector con YOLO26

**Feature Branch**: `feature/035-hu-034-contrato-yolo26`

**Created**: 2026-11-24

**Status**: En implementación

**Input**: Issue #90 — «Pruebas de contrato del detector con YOLO26». Asignada a
Hernán (`HestradaUAO`), épica `ep-09`, P0, ola 1, 1 SP, 4 pruebas objetivo. Depende de
HU-021, ya cerrada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Proteger el contrato al cambiar de detector (Priority: P1)

Como desarrollador integrador, quiero pruebas que validen clases, orden, confianza y
cajas del detector, para detectar rupturas al cambiar entre YOLO11s, YOLO26 y ONNX.

**Why this priority**: el modelo productivo cambió a YOLO26n y el backend puede ser
PyTorch u ONNX. Una salida con clases desordenadas, confianza inválida o cajas fuera
de la imagen rompería la API, la SPA y la evaluación sin que el cambio de modelo lo
evidencie.

**Independent Test**: con un modelo falso que imita `Results.boxes` se ejecuta el
adaptador `YoloDetector` y se verifican las seis clases, los rangos de confianza y los
límites de las cajas, sin cargar Ultralytics, GPU ni dataset.

**Acceptance Scenarios** (AC de la issue #90):

1. **AC-01**: **Dado** el catálogo del proyecto, **Cuando** se construye el detector,
   **Entonces** conserva las seis clases en el orden del `data.yaml`.
2. **AC-02**: **Dada** una salida del modelo, **Cuando** se convierte al contrato,
   **Entonces** toda confianza está en `[0, 1]` y toda caja queda dentro de la imagen.
3. **AC-03**: **Dado** un modelo simulado con salida estilo YOLO26, **Cuando** se
   ejecuta la inferencia, **Entonces** las cajas se convierten a `Detection` y se
   respeta el modo NMS-free.

### Edge Cases

- Confianza `NaN`, infinita, negativa o mayor que 1: se descarta.
- Caja parcialmente fuera de la imagen: se recorta a los límites.
- Caja degenerada: se descarta.
- `class_id` fuera de `[0, 5]`: falla de forma explícita.
- Catálogo con clases ajenas al EPP: el detector no se construye.
- Resultado vacío o sin cajas: devuelve una lista vacía.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La suite MUST ser determinista y no cargar Ultralytics, torch, GPU,
  dataset ni red.
- **FR-002**: AC-01 MUST verificar el orden exacto de las seis clases canónicas.
- **FR-003**: AC-02 MUST cubrir confianza en `[0,1]` y cajas dentro de la imagen.
- **FR-004**: AC-03 MUST usar un modelo falso con la forma de salida de YOLO26 y
  comprobar `nms=False`.
- **FR-005**: La suite MUST vivir en `tests/test_detector_contract.py`.
- **FR-006**: No se modifica el contrato `ImageData → list[Detection]` ni el detector
  de producción.

### Key Entities

- **FakeModel**: modelo mínimo que devuelve resultados con `boxes`.
- **FakeBox**: caja con `cls`, `conf` y `xyxy` como tensores.
- **Detection**: salida validada del contrato.
- **YoloDetector**: adaptador bajo prueba.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 Catálogo y orden | `tests/test_detector_contract.py::test_contract_catalog_matches_yaml_order`, `tests/test_detector_contract.py::test_contract_rejects_class_outside_catalog`, `tests/test_detector_contract.py::test_contract_rejects_catalog_outside_epp` |
| AC-02 Confianza y cajas | `tests/test_detector_contract.py::test_contract_confidence_stays_in_closed_range`, `tests/test_detector_contract.py::test_contract_boxes_stay_inside_image` |
| AC-03 YOLO26 simulado | `tests/test_detector_contract.py::test_contract_fake_yolo26_output_maps_all_classes` |

## Success Criteria *(mandatory)*

- **SC-001**: `make check` pasa sin extras de inferencia.
- **SC-002**: Los cambios de catálogo, confianza o cajas producen al menos un fallo.
- **SC-003**: La suite no depende de pesos, dataset, GPU ni red.
- **SC-004**: La HU añade al menos 4 pruebas al inventario.

## Out of Scope

- Entrenar o evaluar el modelo real.
- Medir latencia o calidad.
- Modificar `YoloDetector`, `contracts.py` o `models.lock`.
- Integrar el detector en API, gRPC o SPA.

## Assumptions

- El catálogo canónico es `CLASSES` y coincide con el orden del `data.yaml`.
- El contrato de `Detection` ya valida clase, confianza y caja.
- El comportamiento de `YoloDetector` es el de HU-021/HU-022; esta HU solo lo protege
  con pruebas de contrato.
