# Feature Specification: HU-059 — Catálogo de errores de API e interfaz

**Feature Branch**: `feature/060-hu-059-catalogo-errores`  
**Created**: 2026-11-26  
**Status**: En implementación  
**Input**: Issue #115 — "Catálogo de errores de API e interfaz". Asignada a Eliana (`ElianaCardona`), Épica `ep-15`, SP 1, P2, Ola 3, 4 pruebas objetivo. Depende de HU-048 (#104), fusionada en `develop`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Resolver errores sin soporte (Priority: P2)

Como usuario y desarrollador, quiero un catálogo de mensajes con causa y solución, para resolver errores sin soporte.

**Why this priority**: la API y la SPA ya exponen errores operativos; sin un catálogo único, el diagnóstico depende de conocimiento tribal y complica la sustentación y el soporte.

**Independent Test**: `uv run pytest -v tests/test_api_catalogo_errores.py` verifica que el catálogo documenta los códigos HTTP/gRPC reales y que los mensajes de UI tienen causa/solución.

**Acceptance Scenarios** (AC de la issue #115):

1. **AC-01**: **Dado** los contratos REST y gRPC actuales, **Cuando** se consulta el catálogo, **Entonces** cada código HTTP y estado gRPC usado por la API está documentado con causa, significado y acción recomendada.
2. **AC-02**: **Dado** los mensajes visibles en la UI, **Cuando** ocurre un error o estado de advertencia, **Entonces** el catálogo enlaza el mensaje a su causa y solución.
3. **AC-03**: **Dado** el código fuente de la API, **Cuando** se ejecuta la prueba, **Entonces** todos los códigos HTTP y estados gRPC de la API están presentes en el catálogo.

### Edge Cases

- Un endpoint puede devolver el mismo HTTP por causas distintas (p. ej. 503 por modelo no cargado o no configurado); el catálogo debe distinguir causas.
- FastAPI genera 422 de validación; el catálogo debe cubrirlo aunque no sea un `HTTPException` explícito en `app.py`.
- gRPC usa `OK` implícito en éxito; el catálogo lo documenta para completar el contrato.
- Mensajes de UI que hoy son genéricos (estado HTTP) deben quedar mapeados con causa probable y acción.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `docs/manual/errores.md` MUST documentar códigos HTTP de la API REST y estados gRPC del servicio `PpeDetection`.
- **FR-002**: Cada entrada MUST incluir al menos: código/estado, origen, causa, mensaje observado y solución recomendada.
- **FR-003**: El catálogo MUST incluir los mensajes/estados de error visibles en la SPA y su relación con la causa.
- **FR-004**: `tests/test_api_catalogo_errores.py` MUST verificar que todos los códigos HTTP y estados gRPC usados por la API aparecen en el catálogo.
- **FR-005**: El catálogo MUST mantenerse alineado con el comportamiento actual; no cambia contratos ni mensajes en runtime.

### Key Entities

- **Entrada de catálogo**: fila/documento con código, capa (REST/gRPC/UI), causa y solución.
- **Fuente de verdad API**: códigos levantados por `src/ppe_detection/api/app.py`, `src/ppe_detection/api/security.py`, `src/ppe_detection/io/images.py` y `src/ppe_detection/grpc/servicer.py`.

## Acceptance → prueba

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 | `tests/test_api_catalogo_errores.py::test_catalogo_documenta_codigos_http_api_ac_01`, `::test_catalogo_documenta_estados_grpc_ac_01` |
| AC-02 | `tests/test_api_catalogo_errores.py::test_catalogo_documenta_mensajes_ui_ac_02` |
| AC-03 | `tests/test_api_catalogo_errores.py::test_catalogo_cubre_todos_los_codigos_api_ac_03` |

## Out of Scope

- Cambiar el comportamiento HTTP/gRPC existente.
- Internacionalización o rediseño de la UI.
- Telemetría externa o sistema de tickets.
- Documentar errores de componentes no expuestos por la API/SPA actual.

## Assumptions

- Los códigos HTTP actuales de la API son los observados en `app.py`, `security.py` y validación de imágenes.
- Los estados gRPC actuales son los levantados por `servicer.py` más `OK` implícito.
- La UI actual expone errores genéricos por estado HTTP y estados de advertencia; el catálogo los documenta sin exigir cambio de código frontend.
