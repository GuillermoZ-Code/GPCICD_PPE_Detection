# Feature Specification: TA Contract-first `Image → list[Detection]`

**Feature Branch**: `feature/001-ta-11-contract-first`

**Created**: 2026-10-31

**Status**: Draft — pendiente de validación de planificación (Jesús)

**Input**: TA propuesta para definir el contrato de inferencia y un detector simulado,
de modo que API, interfaz y gRPC avancen en paralelo con el modelo real.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Contrato de inferencia estable (Priority: P1)

Como desarrollador del sistema, quiero un contrato estable entre la entrada de imagen
y la salida de detecciones, para construir API, interfaz y gRPC sin esperar al modelo
real.

**Why this priority**: desbloquea HU-006, HU-007 y HU-010, y reduce la ruta crítica
HU-002 → HU-006 → HU-010 → HU-011.

**Independent Test**: se puede instanciar `FakeDetector`, enviar un `ImageData` y
obtener `list[Detection]` sin instalar YOLO, sin dataset y sin GPU.

**Acceptance Scenarios**:

1. **Given** un `ImageData` válido, **When** se llama a `FakeDetector.detect()`,
   **Then** se obtiene una lista de `Detection` o una lista vacía, sin excepción.
2. **Given** una imagen sin detecciones, **When** se ejecuta el detector simulado,
   **Then** se devuelve `[]`, no `None` ni error.
3. **Given** dos ejecuciones con la misma entrada, **When** se comparan,
   **Then** el resultado es determinista.
4. **Given** una `Detection` con confianza fuera de `[0,1]` o clase fuera del catálogo,
   **When** se valida, **Then** se rechaza con un error tipado.

### Edge Cases

- Imagen con dimensiones cero o negativas.
- `confidence` `NaN`, `inf` o fuera de `[0,1]`.
- `bbox` invertida (`x1 >= x2` o `y1 >= y2`).
- `class_name` fuera de las seis clases.
- Lista vacía de detecciones.
- Entrada `None` o tipo incorrecto.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `ImageData` MUST exponer `array` uint8 HxWx3 RGB, `width`, `height`,
  `format` y `source`.
- **FR-002**: `Detection` MUST exponer `class_id`, `class_name`, `confidence`,
  `bbox` `xyxy`, `image_width` e `image_height`.
- **FR-003**: `class_name` MUST pertenecer a Helmet, Vest, Gloves, Goggles, Mask o
  Safety Shoe.
- **FR-004**: `confidence` MUST ser un número finito en `[0,1]`.
- **FR-005**: `Detector.detect(image)` MUST devolver `list[Detection]` sin entrenar ni
  descargar pesos.
- **FR-006**: `FakeDetector` MUST ser determinista y no depender de GPU, dataset o red.

### Key Entities

- **ImageData**: imagen decodificada y metadatos de dimensiones.
- **Detection**: clase, confianza y caja delimitadora.
- **Detector**: protocolo de inferencia.
- **FakeDetector**: implementación determinista para pruebas y desarrollo paralelo.

## Acceptance → Test

| AC | Prueba pytest |
|----|----------------|
| AC-01 | `tests/test_contracts.py::test_fake_detector_returns_list` |
| AC-02 | `tests/test_contracts.py::test_detection_validates_class_confidence_and_bbox` |
| AC-03 | `tests/test_contracts.py::test_empty_detections_returns_empty_list` |
| AC-04 | `tests/test_contracts.py::test_fake_detector_is_deterministic` |
| AC-05 | `tests/test_contracts.py::test_invalid_confidence_and_class_are_rejected` |
| AC-06 | `tests/test_contracts.py::test_contract_is_documented` |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: API, UI y gRPC pueden escribir pruebas contra el contrato sin instalar
  YOLO ni torch.
- **SC-002**: `make check` pasa en verde con las pruebas de contrato.
- **SC-003**: 100 % de las pruebas de contrato corren sin GPU, dataset ni red.

## Assumptions

- `ImageData` se define en TA-04 y se consume aquí; no se duplica.
- Las coordenadas se definen en TA-02; este contrato solo fija su forma.
- Pydantic estará disponible por FastAPI; si no, se usan dataclasses.
- La TA no implementa el modelo real ni el preprocesamiento.
