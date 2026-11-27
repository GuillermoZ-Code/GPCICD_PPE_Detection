# Feature Specification: HU-014 — Publicar versiones mediante un pipeline CI/CD con compuertas

**Feature Branch**: `feature/015-014-compuertas`

**Created**: 2026-11-27

**Status**: Implementado (spec de cierre)

**Input**: Issue #14 — «HU-014 — Publicar versiones mediante un pipeline CI/CD con compuertas». Épica `ep-05`,
2 SP.

> Spec escrita al cerrar la HU: el entregable ya está en `develop` y esta ficha deja
> los AC y su evidencia para la compuerta de trazabilidad.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Publicar versiones mediante un pipeline CI/CD con compuertas (Priority: P0)

Como equipo, quiero que publicar versiones mediante un pipeline ci/cd con compuertas quede verificado y documentado, para que la
entrega del M4 se pueda auditar sin depender de la memoria de quien lo hizo.

**Independent Test**: las pruebas estáticas de `tests/` leen los archivos del entregable
y comprueban los criterios; el comportamiento real se validó en el servidor.

**Acceptance Scenarios** (AC de la issue #14):

1. **AC-01**: Build, deploy y smoke exitosos con cambios autorizados.
2. **AC-02**: Una compuerta fallida bloquea la publicación.
3. **AC-03**: Credenciales seguras y versión desplegada asociada al modelo.

## Requirements *(mandatory)*

### Evidence

- .gitlab-ci.yml — stages y `needs` encadenados
- .github/workflows/ci.yml — compuertas de la PR
- docs/operacion/despliegue.md — procedimiento

## Success Criteria *(mandatory)*

- **SC-001**: las pruebas de esta HU pasan sin red ni servidor.
- **SC-002**: `make check` en verde.
- **SC-003**: la documentación del M4 enlaza el entregable.

## Assumptions

- El sistema desplegado sigue disponible en `https://143.198.10.157.sslip.io`.
- Las credenciales viven en variables de CI/CD, nunca en el repositorio.
