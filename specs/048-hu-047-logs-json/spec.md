# Feature Specification: HU-047 — Logs estructurados JSON con request_id

**Feature Branch**: `feature/048-hu-047-logs-json`

**Created**: 2026-11-24

**Status**: En implementación

**Input**: Issue #103 — «Logs estructurados JSON con request_id». Asignada a Eliana
(`ElianaCardona`), épica `ep-13`, P1, Ola 1, 3 SP, 12 pruebas objetivo. Sin dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Diagnosticar peticiones desplegadas (Priority: P1)

Como operador, quiero una línea JSON por petición con `request_id`, para correlacionar
solicitudes, latencias y errores sin exponer credenciales ni imágenes.

**Why this priority**: los logs de texto libre actuales no permiten filtrar por petición
ni correlacionar con el cliente; sin `request_id`, un incidente en producción no se
puede reconstruir.

**Independent Test**: `uv run pytest -v tests/test_api_logs_json.py` usa `caplog` y
`TestClient` para verificar el registro por petición, la redacción de datos sensibles y
la cabecera `X-Request-ID`, sin red ni pesos.

**Acceptance Scenarios** (AC de la issue #103):

1. **AC-01**: **Dado** cualquier request, **Cuando** termina, **Entonces** se emite una
   línea JSON con método, ruta, estado, latencia y `request_id`; incluidos errores 500.
2. **AC-02**: **Dado** un request con `Authorization`, `X-API-Key` o cuerpo con imagen,
   **Cuando** se registra, **Entonces** ningún valor sensible aparece en el log.
3. **AC-03**: **Dado** un `X-Request-ID` entrante, **Cuando** responde la API,
   **Entonces** devuelve ese mismo identificador; si falta o está vacío, genera uno.

### Edge Cases

- `X-Request-ID` vacío se trata como ausente.
- Un error interno se registra como 500 sin incluir el mensaje de la excepción.
- No se registran cabeceras, query string ni cuerpo; solo metadatos de la petición.
- Los mensajes de log son JSON válido con claves estables.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `src/ppe_detection/api/logging.py` MUST exponer `RequestLoggingMiddleware`.
- **FR-002**: `create_app()` MUST instalar el middleware para todas las rutas.
- **FR-003**: Cada registro MUST incluir `event`, `method`, `path`, `status`,
  `duration_ms` y `request_id`.
- **FR-004**: El middleware MUST emitir exactamente un registro JSON por petición.
- **FR-005**: El middleware MUST NO registrar cabeceras, cuerpo, imágenes ni tokens.
- **FR-006**: La respuesta MUST incluir `X-Request-ID` con el valor entrante o uno
  generado con `uuid4`.
- **FR-007**: Los errores internos MUST registrarse con estado 500 y devolver una
  respuesta segura con la cabecera propagada.
- **FR-008**: No se MUST agregar dependencias nuevas.

### Key Entities

- **RequestLog**: registro JSON inmutable con metadatos de la petición.
- **Request ID**: valor entrante o UUIDv4 devuelto en la respuesta.
- **Middleware**: capa Starlette que envuelve cada petición.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 campos y una línea por petición | `tests/test_api_logs_json.py::test_logs_method_path_status_latency_and_request_id`, `::test_each_request_emits_one_json_log_record`, `::test_generated_request_id_is_present_in_log`, `::test_log_line_is_valid_json`, `::test_error_responses_are_logged_with_500` |
| AC-02 redacción | `tests/test_api_logs_json.py::test_authorization_header_is_never_logged`, `::test_api_key_header_is_never_logged`, `::test_request_body_is_never_logged`, `::test_image_bytes_are_never_logged` |
| AC-03 propagación | `tests/test_api_logs_json.py::test_request_id_header_is_propagated`, `::test_generated_request_id_is_returned`, `::test_empty_request_id_header_generates_new_identifier` |

## Success Criteria *(mandatory)*

- **SC-001**: Las 12 pruebas nuevas y la suite completa pasan.
- **SC-002**: ruff, formato y ty pasan sin hallazgos.
- **SC-003**: `ownership --base origin/develop` no bloquea los archivos tocados.
- **SC-004**: La PR queda abierta con revisor de otro integrante.

## Out of Scope

- Persistencia de logs, agregación o paneles (HU-056).
- Cambiar el formato de `/health` ni de `/predict`.
- Añadir librerías de logging estructurado.
- Logs de gRPC (se evaluará en otra HU).

## Assumptions

- `caplog` captura el logger `ppe_detection.api` en pruebas.
- El cuerpo de la petición puede contener imágenes; nunca se serializa en el log.
- El logger emite una sola línea por petición, exitosa o no.
