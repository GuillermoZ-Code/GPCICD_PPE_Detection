# Feature Specification: HU-006 — API REST con FastAPI

**Feature Branch**: `feature/008-hu-006-api-rest`

**Created**: 2026-11-10

**Status**: En revisión (PR #42)

**Input**: Issue #6 — «Consultar inferencias mediante una API REST con FastAPI».
Asignada a Hernán (EP-03, Must Have, M3-S1). Depende de HU-002 (cerrada) y HU-005
(PR #39). El contrato HTTP lo consume la SPA React de HU-007.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Enviar una imagen por HTTP y recibir detecciones (Priority: P1)

Como desarrollador que integra el detector, quiero enviar una imagen a una API HTTP y
recibir resultados estructurados, para usar el modelo sin depender de la interfaz
gráfica.

**Why this priority**: es la puerta de entrada de la SPA React, de gRPC y del
despliegue; sin API no hay integración posible.

**Independent Test**: con `TestClient` y `FakeDetector`, un PNG se envía a
`POST /predict` y devuelve `detections`, dimensiones, versión del modelo y tiempo; un
archivo corrupto devuelve 400 y una petición posterior sigue funcionando.

**Acceptance Scenarios** (AC de la issue #6):

1. **AC-01**: **Dada** una imagen compatible, **Cuando** se envía a `POST /predict`,
   **Entonces** la respuesta cumple el esquema publicado con las detecciones.
2. **AC-02**: **Dado** un archivo inválido, **Cuando** se envía, **Entonces** la API
   devuelve un error de cliente y el servidor sigue disponible.
3. **AC-03**: **Dado** el documento OpenAPI, **Cuando** se consulta, **Entonces**
   documenta la operación, la entrada `file` y el esquema de respuesta.
4. **AC-04**: **Dado** el artefacto configurado, **Cuando** se infiere, **Entonces** se
   usa el detector cargado y no se entrena ni se descargan pesos.

### Edge Cases

- Sin `PPE_MODEL_PATH` configurado: respuesta 503 comprensible, no un 500.
- Archivo vacío o corrupto: 400 con el mensaje de `InvalidImageError`.
- Petición sin el campo `file`: 422 de validación de FastAPI.
- `FakeDetector` sin detecciones: 200 con `detections: []`.
- Origen del frontend en desarrollo (`http://localhost:5173`): CORS permitido.
- Archivo mayor de 10 MB: 400 antes de decodificar.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La API MUST exponer `POST /predict` con `multipart/form-data` y el campo
  `file`.
- **FR-002**: La respuesta MUST incluir `detections`, `image_width`, `image_height`,
  `model_version` y `elapsed_ms`, con el mismo contrato que consume el frontend.
- **FR-003**: Cada detección MUST incluir `class_id`, `class_name`, `confidence`,
  `bbox` `xyxy`, `image_width` e `image_height`.
- **FR-004**: Un archivo inválido MUST devolver 4xx y no ejecutar el detector.
- **FR-005**: La API MUST reutilizar `validate_image_bytes` de HU-005 y el protocolo
  `Detector`; no entrena ni descarga pesos.
- **FR-006**: El detector MUST ser inyectable para pruebas (`FakeDetector`) y cargarse
  de forma perezosa desde `PPE_MODEL_PATH` en producción.
- **FR-007**: OpenAPI MUST documentar la operación, el `file` multipart y el esquema
  `PredictResponse`.
- **FR-008**: CORS MUST permitir el origen de desarrollo del frontend, configurable por
  `PPE_CORS_ORIGINS`.

## Success Criteria *(mandatory)*

- **SC-001**: AC-01 a AC-04 tienen pruebas pytest con `TestClient`.
- **SC-002**: `make check` pasa sin GPU, sin dataset y sin red.
- **SC-003**: El esquema de respuesta coincide con `PredictResponse` del frontend.
- **SC-004**: La API se puede levantar con `uv run uvicorn ppe_detection.api.app:app`.

## Out of Scope

- gRPC (HU-010), Docker (HU-011), autenticación y cuotas.
- Persistencia de resultados o historial.
- Entrenamiento o descarga de pesos.
