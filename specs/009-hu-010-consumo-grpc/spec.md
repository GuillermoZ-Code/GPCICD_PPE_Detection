# Feature Specification: HU-010 — Consumir inferencias mediante gRPC

**Feature Branch**: `feature/009-hu-010-consumo-grpc`

**Created**: 2026-11-10

**Status**: En revisión (PR #46)

**Input**: Issue #10 — «HU-010 — Consumir inferencias mediante gRPC».
Asignada a ElianaCardona (EP-03, Must Have, M3-S2). Depende de HU-006 (PR #42,
fusionada). El requisito de origen es la lámina del Módulo 3: FastAPI y gRPC como
componentes de la aplicación local.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Solicitud gRPC válida (Priority: P1)

Como desarrollador integrador, quiero invocar la operación de inferencia publicada
mediante gRPC y recibir una respuesta estructurada, para integrar el detector sin la
API HTTP.

**Why this priority**: es la operación única del servicio; sin ella no hay HU-010.

**Independent Test**: con un servidor gRPC en bucle local y `FakeDetector`, un cliente
envía una imagen JPEG/PNG válida y recibe `detections`, dimensiones, versión del
modelo y tiempo; el catálogo de clases es el canónico de seis clases.

**Acceptance Scenarios** (AC-010.1 de la issue #10):

1. **AC-010.1**: **Dado** un servidor gRPC disponible, **Y** una solicitud de
   inferencia válida, **Cuando** un cliente invoca la operación publicada,
   **Entonces** recibe una respuesta estructurada, **Y** esta utiliza el catálogo de
   seis clases acordado (`Gloves, Vest, goggles, helmet, mask, safety_shoe`).

### User Story 2 — Equivalencia de contratos REST ↔ gRPC (Priority: P2)

Como responsable técnico, quiero que REST y gRPC representen la misma imagen y la
misma configuración bajo las mismas convenciones, para que ningún consumidor observe
dos verdadades distintas.

**Why this priority**: la issue exige un solo componente central del modelo; gRPC es
un adaptador, no una segunda implementación.

**Independent Test**: con la misma imagen y el mismo `FakeDetector` inyectado, la
respuesta REST (`POST /predict`) y la respuesta gRPC coinciden campo a campo en
`class_id`, `class_name`, `confidence`, `bbox` `xyxy`, dimensiones y versión del
modelo; ambos consumen el mismo constructor de detector desde variables de entorno.

**Acceptance Scenarios** (AC-010.2 de la issue #10):

1. **AC-010.2**: **Dada** una misma imagen y una misma configuración de modelo,
   **Cuando** se realiza la inferencia mediante FastAPI y gRPC, **Entonces** ambos
   mecanismos representan los resultados bajo las mismas convenciones semánticas y
   espaciales, **Y** no requieren detectores independientes.

### User Story 3 — Solicitud inválida con servicio disponible (Priority: P3)

Como cliente del servicio, quiero un estado de error definido ante una solicitud no
compatible con el contrato, para distinguir mis errores de entrada de fallos del
servidor y reintentar.

**Why this priority**: sin estados definidos el integrador no puede mapear errores;
la disponibilidad posterior prueba que el fallo no corrompió el servicio.

**Independent Test**: bytes vacíos, corruptos y sobre el límite de 10 MB producen
`INVALID_ARGUMENT` con el mensaje de `InvalidImageError`; la ausencia de artefacto
produce `UNAVAILABLE`; tras cada error, una solicitud válida posterior se atiende.

**Acceptance Scenarios** (AC-010.3 de la issue #10):

1. **AC-010.3**: **Dada** una solicitud no compatible con el contrato, **Cuando** se
   invoca el servicio, **Entonces** el servidor devuelve un estado de error definido,
   **Y** permanece disponible para nuevas solicitudes.

### Resultados vacíos (contrato de HU-004)

- `FakeDetector` sin detecciones: respuesta válida sin `RpcError`, con
  `detections: []` y `message` idéntico a `NO_DETECTIONS_MESSAGE`
  («No se detectaron objetos EPP en la imagen.»). No afirma incumplimiento ni
  ausencia real de EPP.

## Edge Cases

- Entrada vacía (`image: ""`): `INVALID_ARGUMENT` con el detalle de HU-005; el
  detector no se invoca.
- Bytes corruptos o formato no JPEG/PNG: `INVALID_ARGUMENT`; el detector no se
  invoca.
- Tamaño > 10 MB (`MAX_IMAGE_BYTES`): `INVALID_ARGUMENT` antes de decodificar.
- Sin `PPE_MODEL_PATH` ni detector inyectado: `UNAVAILABLE` con el detalle del
  constructor compartido; no confunde un error de despliegue con un 500/`INTERNAL`.
- Error inesperado del detector: `INTERNAL` con el nombre de la excepción.
- El campo `message` replica el contrato de resultado de HU-004
  (`build_inference_result`): es la única adición semántica respecto al esquema REST.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El servicio MUST definir el contrato en `ppe.proto` con
  `rpc Detect(PredictRequest) returns (PredictResponse)` bajo el paquete `ppe.v1`.
- **FR-002**: `PredictResponse` MUST incluir `detections`, `image_width`,
  `image_height`, `model_version`, `elapsed_ms` y `message`; cada detección MUST
  incluir `class_id`, `class_name`, `confidence` en `[0, 1]`, `bbox` `xyxy` en
  píxeles de la imagen original, `image_width` e `image_height`.
- **FR-003**: Un archivo inválido (vacío, corrupto o > 10 MB) MUST devolver
  `INVALID_ARGUMENT` con el detalle de `InvalidImageError` y MUST NOT ejecutar el
  detector.
- **FR-004**: El servicer MUST reutilizar `validate_image_bytes` (HU-005), el
  protocolo `Detector` (contrato de ADR 0005) y `build_inference_result` (HU-004);
  MUST NOT entrenar, descargar pesos ni duplicar lógica del detector.
- **FR-005**: La construcción del detector desde variables de entorno
  (`PPE_MODEL_PATH`, `PPE_CONF`, `PPE_IOU`, `PPE_IMGSZ`, `PPE_DEVICE`,
  `PPE_MODEL_VERSION`) MUST vivir en un único módulo compartido por REST y gRPC;
  el detector y la versión del modelo siguen siendo inyectables para pruebas.
- **FR-006**: Los estados de error MUST estar mapeados: validación de entrada →
  `INVALID_ARGUMENT`, artefacto no configurado → `UNAVAILABLE`, fallo interno →
  `INTERNAL`, con `details` comprensible en español.
- **FR-007**: El código generado (`*_pb2.py`, `*_pb2_grpc.py`) MUST regenerarse con
  `uv run python -m ppe_detection.grpc.gen` (`grpcio-tools`); los módulos generados
  se versionan y quedan excluidos de Ruff y `ty`.
- **FR-008**: El paquete MUST exponer servidor (`python -m ppe_detection.grpc`) y
  cliente de prueba (`python -m ppe_detection.grpc.client --image <ruta>`), con
  host/puerto configurables (`PPE_GRPC_HOST`, `PPE_GRPC_PORT`, por omisión
  `0.0.0.0:9000`).

## Success Criteria *(mandatory)*

- **SC-001**: AC-010.1, AC-010.2 y AC-010.3 tienen pruebas pytest cliente-servidor
  (servidor gRPC real en bucle local) escritas antes del código de producción
  (test-first).
- **SC-002**: `make check` y `uv build` pasan sin GPU, sin dataset, sin red externa
  y sin pesos.
- **SC-003**: Inferencia de extremo a extremo demostrada por gRPC con el mismo
  componente central del modelo que la API REST (misma imagen, mismo detector).
- **SC-004**: La generación, el arranque y el consumo del servicio están documentados
  en `README.md`, `docs/architecture/contracts.md` y esta spec.

## Out of Scope

- Streaming de video, RPCs bidireccionales y procesamiento distribuido.
- Autenticación, TLS, cuotas y métricas de servicio.
- Docker (HU-011), versionado de modelo (HU-013) y despliegue (HU-014/015).
- Cambios al contrato HTTP de HU-006 o al `Detector` de ADR 0005.
