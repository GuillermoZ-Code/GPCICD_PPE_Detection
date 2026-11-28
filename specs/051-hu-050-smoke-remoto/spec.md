# Feature Specification: HU-050 — Cliente de verificación remota REST y gRPC

**Feature Branch**: `feature/051-hu-050-smoke-remoto`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #106 — «Cliente de verificación remota REST y gRPC». Asignada a
Eliana (`ElianaCardona`), épica `ep-13`, SP 2, P0, Ola 2, 8 pruebas objetivo.
Depende de HU-045 (#101), ya fusionada en `develop`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Verificar el servicio desplegado desde otro equipo (Priority: P0)

Como evaluador, quiero un script que pruebe la URL pública desde otro equipo, para
demostrar el servicio desplegado sin depender del entorno local.

**Why this priority**: el despliegue M4 debe comprobarse desde fuera con los mismos
contratos que consume la SPA; una prueba local no demuestra que el proxy y la API
responden en producción.

**Independent Test**: `uv run pytest -v tests/test_smoke_remote.py` inyecta
transportes simulados REST y gRPC, sin red, pesos ni GPU.

**Acceptance Scenarios** (AC de la issue #106):

1. **AC-01**: **Dado** un servicio remoto accesible, **Cuando** se ejecuta el cliente,
   **Entonces** comprueba `/health/ready`, una predicción real por REST y por gRPC,
   e imprime la versión del modelo y la latencia.
2. **AC-02**: **Dado** una entrada inválida, **Cuando** se envía por REST y por gRPC,
   **Entonces** REST responde 400 y gRPC `INVALID_ARGUMENT`; el cliente termina con
   código distinto de cero si alguna comprobación falla y el servicio sigue listo.
3. **AC-03**: **Dado** transportes simulados, **Cuando** se ejecutan las pruebas,
   **Entonces** no se abre ninguna conexión real ni se carga ningún modelo.

### Edge Cases

- `/health/ready` con estado `not_ready` (HTTP 503) cuenta como fallo, no como excepción.
- Una respuesta de predicción sin versión de modelo es un fallo de verificación.
- Un cuerpo corrupto con MIME válido se rechaza por contenido antes de inferir.
- Tras un rechazo, la comprobación de disponibilidad siguiente debe seguir pasando.
- Los errores de red y de gRPC se informan en `stderr` y se resumen en la salida.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `src/ppe_detection/tools/smoke_remote.py` MUST exponer una función de
  verificación con transportes inyectables y un CLI con `--api-url`, `--grpc-target`,
  `--image` y `--timeout`.
- **FR-002**: El cliente MUST comprobar `/health/ready`, `POST /predict` con una imagen
  válida y `POST /predict` con bytes inválidos por REST.
- **FR-003**: El cliente MUST comprobar `Detect` con una imagen válida y con bytes
  inválidos por gRPC, usando el contrato `ppe.proto` existente.
- **FR-004**: El cliente MUST imprimir versión del modelo y latencia, y MUST devolver
  código de salida 0 solo si todas las comprobaciones pasan.
- **FR-005**: Las pruebas MUST usar transportes simulados, sin red, dataset, pesos ni GPU.
- **FR-006**: No se MUST modificar `contracts.py`, `ppe.proto`, el servidor gRPC ni
  `api/app.py`; no se MUST agregar dependencias.

### Key Entities

- **RestTransport**: callable `(method, url, data, content_type, timeout)` → estado, cuerpo.
- **GrpcTransport**: callable `(target, image, timeout)` → respuesta tipada o excepción.
- **SmokeReport**: lista de comprobaciones con nombre, resultado y detalle.

## Acceptance → prueba

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 | `tests/test_smoke_remote.py::test_ready_reports_model_version_ac_01`, `::test_valid_rest_prediction_reports_latency_ac_01`, `::test_grpc_prediction_reports_version_and_latency_ac_01` |
| AC-02 | `tests/test_smoke_remote.py::test_invalid_rest_image_returns_400_ac_02`, `::test_invalid_grpc_image_is_rejected_ac_02`, `::test_failed_check_returns_nonzero_ac_02`, `::test_service_stays_ready_after_rejection_ac_02` |
| AC-03 | `tests/test_smoke_remote.py::test_simulated_transports_need_no_network_ac_03` |

## Success Criteria *(mandatory)*

- **SC-001**: Las 8 pruebas nuevas pasan y la suite completa sigue verde.
- **SC-002**: ruff, formato y ty pasan sin hallazgos.
- **SC-003**: `ownership --base origin/develop` no bloquea los archivos tocados.
- **SC-004**: La PR queda abierta con revisor de otro integrante.

## Out of Scope

- Desplegar ni configurar Caddy, HTTPS ni el Droplet (HU-041/HU-070).
- Modificar el contrato gRPC ni añadir un RPC de salud.
- Instalar dependencias nuevas: se usa `urllib` y el cliente gRPC existente.
- Tocar `docs/curso/`, `uv.lock`, `tests/conftest.py` ni specs de otros integrantes.

## Assumptions

- `GET /health/ready` devuelve `status`, `model_version` y `model_loaded` (HU-045).
- `POST /predict` devuelve `model_version`, `elapsed_ms` y `detections` (HU-006/HU-062).
- `Detect` de `ppe.proto` devuelve `model_version` y `elapsed_ms`.
- Un PNG mínimo generado en memoria es suficiente para las pruebas simuladas.
