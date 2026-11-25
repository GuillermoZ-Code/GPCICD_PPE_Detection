# Feature Specification: HU-048 — Límites de tamaño y tipo de archivo en REST

**Feature Branch**: `feature/049-hu-048-limites-carga`

**Created**: 2026-11-24

**Status**: En implementación

**Input**: Issue #104 — «Límites de tamaño y tipo de archivo en REST». Asignada a
Eliana (`ElianaCardona`), épica `ep-08`, P1, Ola 2, 2 SP, 8 pruebas objetivo. Sin
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Proteger el servicio público (Priority: P1)

Como operador, quiero rechazar archivos demasiado grandes o de tipo no permitido, para
proteger el servicio desplegado sin degradar las peticiones válidas.

**Why this priority**: `/predict` lee el cuerpo completo antes de validar; sin un límite
configurable, un cliente puede agotar memoria o enviar cualquier tipo de archivo.

**Independent Test**: `uv run pytest -v tests/test_api_upload_limits.py` configura
`PPE_MAX_UPLOAD_MB` con un valor pequeño y comprueba 413, 415 y disponibilidad posterior
usando `FakeDetector` y PNG generado en memoria.

**Acceptance Scenarios** (AC de la issue #104):

1. **AC-01**: **Dado** `PPE_MAX_UPLOAD_MB`, **Cuando** el archivo excede ese límite,
   **Entonces** `/predict` devuelve 413 con el límite en el mensaje.
2. **AC-02**: **Dado** un `content-type` no permitido, **Cuando** se envía a `/predict`,
   **Entonces** devuelve 415 indicando PNG/JPEG.
3. **AC-03**: **Dado** un rechazo previo, **Cuando** llega una petición válida,
   **Entonces** la API sigue respondiendo 200 y el detector no queda corrompido.

### Edge Cases

- Sin `PPE_MAX_UPLOAD_MB`, `io.images` mantiene su límite interno de 10 MB y devuelve
  400; el 413 aparece solo cuando el operador configura el límite.
- Se aceptan `image/png` e `image/jpeg`, incluso con parámetros en el MIME.
- Un MIME no permitido se rechaza por 415 antes de decodificar.
- Un contenido corrupto con MIME permitido sigue devolviendo 400 por `io.images`.
- El límite se comprueba antes de intentar la inferencia.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `app.py` MUST leer `PPE_MAX_UPLOAD_MB` cuando esté configurado.
- **FR-002**: Un archivo mayor al límite configurado MUST devolver 413, no 400 ni 500.
- **FR-003**: Solo `image/png` e `image/jpeg` MUST pasar el filtro de MIME.
- **FR-004**: Un MIME no permitido MUST devolver 415 con mensaje claro.
- **FR-005**: Tras un rechazo, las peticiones válidas MUST seguir funcionando.
- **FR-006**: No se MUST modificar `io/images.py`, `detector_config.py` ni agregar
  dependencias.

### Key Entities

- **UploadLimit**: bytes máximos derivados de `PPE_MAX_UPLOAD_MB`.
- **AllowedType**: MIME aceptado en `/predict`.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 tamaño | `tests/test_api_upload_limits.py::test_file_above_configured_limit_returns_413`, `::test_default_limit_allows_small_image` |
| AC-02 tipo | `tests/test_api_upload_limits.py::test_disallowed_mime_returns_415`, `::test_mime_with_parameters_is_accepted`, `::test_415_message_names_allowed_types`, `::test_valid_jpeg_is_still_accepted` |
| AC-03 disponibilidad | `tests/test_api_upload_limits.py::test_service_responds_after_rejection`, `::test_valid_prediction_after_rejection` |

## Success Criteria *(mandatory)*

- **SC-001**: Las 8 pruebas nuevas y la suite completa pasan.
- **SC-002**: ruff, formato y ty pasan sin hallazgos.
- **SC-003**: `ownership --base origin/develop` no bloquea los archivos tocados.
- **SC-004**: La PR queda abierta con revisor de otro integrante.

## Out of Scope

- Límites en el servidor web, Caddy o el proxy (HU-041/HU-083).
- Rate limiting global (HU-054).
- Modificar `validate_image_bytes` ni su límite interno de 10 MB.
- Actualizar `.env.example`: coordinar con la PR de HU-044 (#210) por ser archivo de un
  solo escritor; esta PR no lo toca.

## Assumptions

- `UploadFile.content_type` refleja el MIME enviado por el cliente.
- Las firmas `PNG_MAGIC` y `JPEG_MAGIC` ya están disponibles en `ppe_detection.io.images`.
- Los rechazos son respuestas HTTP normales; no cambian el estado del detector.
