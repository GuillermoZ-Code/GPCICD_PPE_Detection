# Feature Specification: HU-015 — Comprobar el funcionamiento del sistema desplegado

**Feature Branch**: `feature/016-015-verificacion`

**Created**: 2026-11-27

**Status**: Implementado (spec de cierre)

**Input**: Issue #15 — «HU-015 — Comprobar el funcionamiento del sistema desplegado». Épica `ep-05`,
1 SP.

> Spec escrita al cerrar la HU: el entregable ya está en `develop` y esta ficha deja
> los AC y su evidencia para la compuerta de trazabilidad.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Comprobar el funcionamiento del sistema desplegado (Priority: P0)

Como equipo, quiero que comprobar el funcionamiento del sistema desplegado quede verificado y documentado, para que la
entrega del M4 se pueda auditar sin depender de la memoria de quien lo hizo.

**Independent Test**: las pruebas estáticas de `tests/` leen los archivos del entregable
y comprueban los criterios; el comportamiento real se validó en el servidor.

**Acceptance Scenarios** (AC de la issue #15):

1. **AC-01**: El healthcheck responde con el estado y el contrato publicado.
2. **AC-02**: Una imagen válida produce una inferencia real con el artefacto configurado.
3. **AC-03**: Los errores se registran sin secretos y la evidencia queda lista.

## Requirements *(mandatory)*

### Evidence

- deploy/deploy.sh — espera de healthchecks e inferencia de humo
- .gitlab-ci.yml — job `deploy` con smoke
- docs/operacion/despliegue.md §6 — diagnóstico

## Success Criteria *(mandatory)*

- **SC-001**: las pruebas de esta HU pasan sin red ni servidor.
- **SC-002**: `make check` en verde.
- **SC-003**: la documentación del M4 enlaza el entregable.

## Assumptions

- El sistema desplegado sigue disponible en `https://143.198.10.157.sslip.io`.
- Las credenciales viven en variables de CI/CD, nunca en el repositorio.
