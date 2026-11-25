# Feature Specification: HU-062 — Paridad REST/gRPC con el modelo productivo

**Feature Branch**: `feature/063-hu-062-paridad-rest-grpc`

**Created**: 2026-11-24

**Status**: En implementación

**Input**: Issue #118 — «Paridad REST/gRPC con el modelo productivo». Asignada a
Eliana (`ElianaCardona`), épica `ep-10`, SP 3, P1, Ola 3, 12 pruebas objetivo. Sin
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Elegir protocolo sin cambiar semántica (Priority: P1)

Como desarrollador integrador, quiero que REST y gRPC devuelvan la misma semántica, para
elegir protocolo sin diferencias en detecciones ni en errores.

**Why this priority**: dos adaptadores sobre el mismo detector deben comportarse igual;
una divergencia en el mapeo de errores obliga a los clientes a implementar lógica
distinta para el mismo fallo.

**Independent Test**: `uv run pytest -v tests/test_paridad_protocolos.py` levanta un
servidor gRPC efímero y un `TestClient` REST con el mismo `FakeDetector`, sin pesos.

**Acceptance Scenarios** (AC de la issue #118):

1. **AC-01**: **Dado** un mismo PNG/JPEG y detector, **Cuando** se envía por REST y
   gRPC, **Entonces** ambos devuelven las mismas detecciones, orden, dimensiones,
   confianzas, bbox xyxy e identidad del modelo.
2. **AC-02**: **Dado** un error de entrada o de modelo, **Cuando** se envía por ambos
   protocolos, **Entonces** REST responde 400/503 y gRPC INVALID_ARGUMENT/UNAVAILABLE
   con el mismo detalle, y el servicio sigue disponible.
3. **AC-03**: **Dado** un detector simulado común, **Cuando** se ejecutan las pruebas,
   **Entonces** ninguna necesita pesos, GPU ni red externa.

### Edge Cases

- El detector inyectado que falla en `detect()` con `DetectorNotConfiguredError` debe
  traducirse a 503 en REST, igual que gRPC ya lo traduce a UNAVAILABLE.
- Un detector genérico que falla sigue siendo INTERNAL en gRPC; REST no cambia ese
  comportamiento en esta HU.
- El formato inválido se rechaza por contenido, no por extensión del archivo.
- Un resultado vacío es válido en ambos protocolos, con el mismo resumen semántico en
  gRPC y lista vacía en REST.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `src/ppe_detection/api/app.py` MUST traducir `DetectorNotConfiguredError`
  durante `detect()` a HTTP 503, con el mismo detalle que gRPC expone como UNAVAILABLE.
- **FR-002**: `tests/test_paridad_protocolos.py` MUST cubrir AC-01, AC-02 y AC-03 con
  al menos 12 pruebas que usen un detector simulado compartido.
- **FR-003**: Las pruebas MUST usar el mismo PNG/JPEG, la misma `ModelIdentity` y el
  mismo servidor gRPC efímero que las demás pruebas del contrato.
- **FR-004**: No se MUST modificar `contracts.py`, `io/images.py`, `results.py`,
  `detector_config.py` ni `ppe.proto`.
- **FR-005**: No se MUST agregar dependencias ni cambiar umbrales del detector.

### Key Entities

- **ParityCase**: bytes de imagen + detector + identidad → respuesta REST y gRPC.
- **ErrorParity**: error de dominio → `(HTTP status, gRPC status, detalle)`.

## Acceptance → prueba

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 | `tests/test_paridad_protocolos.py::test_same_png_returns_identical_detections`, `::test_same_jpeg_is_accepted_by_both_protocols`, `::test_empty_result_is_equivalent`, `::test_detection_order_and_bbox_are_equivalent`, `::test_model_identity_is_equivalent`, `::test_both_protocols_report_same_image_dimensions` |
| AC-02 | `tests/test_paridad_protocolos.py::test_invalid_image_maps_400_to_invalid_argument`, `::test_missing_model_maps_503_to_unavailable`, `::test_detection_time_unconfigured_maps_503_to_unavailable`, `::test_service_recovers_after_rejection` |
| AC-03 | `tests/test_paridad_protocolos.py::test_shared_fake_detector_needs_no_model_weights`, `::test_shared_fake_detector_is_called_once_per_protocol`, `::test_shared_fake_detector_confidences_match` |

## Success Criteria *(mandatory)*

- **SC-001**: Las 13 pruebas nuevas (objetivo: 12) pasan y la suite completa sigue verde.
- **SC-002**: ruff, formato y ty pasan sin hallazgos.
- **SC-003**: `ownership --base origin/develop` no bloquea los archivos tocados.
- **SC-004**: La PR queda abierta con revisor de otro integrante.

## Out of Scope

- Añadir `conf` al contrato gRPC: el RPC actual no expone ese parámetro.
- Cambiar el mapeo de errores genéricos a INTERNAL/500: no forma parte de la issue.
- Modificar `.env.example`, CI ni imágenes Docker.
- Tocar `docs/curso/` (un solo escritor) ni specs de otros integrantes.

## Assumptions

- `DetectorNotConfiguredError` hereda de `RuntimeError` y ya se traduce a 503 cuando
  ocurre durante la construcción del detector; la paridad exige cubrir también el
  momento de inferencia.
- `FakeDetector` devuelve las mismas `Detection` en cada llamada, sin estado oculto.
- gRPC usa el mismo `validate_image_bytes` que REST (AC-010.2).
