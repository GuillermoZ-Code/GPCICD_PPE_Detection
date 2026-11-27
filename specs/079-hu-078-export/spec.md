# Feature Specification: HU-078 — Exportar resultados en CSV y JSON

**Feature Branch**: `feature/079-078-export`

**Created**: 2026-11-27

**Status**: Implementado (spec de cierre)

**Input**: Issue #134 — «HU-078 — Exportar resultados en CSV y JSON». Épica `ep-11`,
2 SP.

> Spec escrita al cerrar la HU: el entregable ya está en `develop` y esta ficha deja
> los AC y su evidencia para la compuerta de trazabilidad.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Exportar resultados en CSV y JSON (Priority: P0)

Como equipo, quiero que exportar resultados en csv y json quede verificado y documentado, para que la
entrega del M4 se pueda auditar sin depender de la memoria de quien lo hizo.

**Independent Test**: las pruebas estáticas de `tests/` leen los archivos del entregable
y comprueban los criterios; el comportamiento real se validó en el servidor.

**Acceptance Scenarios** (AC de la issue #134):

1. **AC-01**: La descarga incluye clase, confianza, caja y versión del modelo.
2. **AC-02**: El nombre del archivo lleva fecha y modelo.
3. **AC-03**: Hay pruebas de serialización.

## Requirements *(mandatory)*

### Evidence

- frontend/src/download.ts — CSV y JSON
- frontend/src/download.test.ts — serialización

## Success Criteria *(mandatory)*

- **SC-001**: las pruebas de esta HU pasan sin red ni servidor.
- **SC-002**: `make check` en verde.
- **SC-003**: la documentación del M4 enlaza el entregable.

## Assumptions

- El sistema desplegado sigue disponible en `https://143.198.10.157.sslip.io`.
- Las credenciales viven en variables de CI/CD, nunca en el repositorio.
