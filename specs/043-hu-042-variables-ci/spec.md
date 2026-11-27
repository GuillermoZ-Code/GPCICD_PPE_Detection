# Feature Specification: HU-042 — Variables CI enmascaradas y protegidas

**Feature Branch**: `feature/043-042-variables-ci`

**Created**: 2026-11-27

**Status**: Implementado (spec de cierre)

**Input**: Issue #98 — «HU-042 — Variables CI enmascaradas y protegidas». Épica `ep-08`,
2 SP.

> Spec escrita al cerrar la HU: el entregable ya está en `develop` y esta ficha deja
> los AC y su evidencia para la compuerta de trazabilidad.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Variables CI enmascaradas y protegidas (Priority: P0)

Como equipo, quiero que variables ci enmascaradas y protegidas quede verificado y documentado, para que la
entrega del M4 se pueda auditar sin depender de la memoria de quien lo hizo.

**Independent Test**: las pruebas estáticas de `tests/` leen los archivos del entregable
y comprueban los criterios; el comportamiento real se validó en el servidor.

**Acceptance Scenarios** (AC de la issue #98):

1. **AC-01**: Hay inventario de secretos con alcance, rotación y dueño.
2. **AC-02**: Las variables van enmascaradas y nunca se imprimen en los logs.
3. **AC-03**: Permisos mínimos: el token de despliegue solo lee el registry.

## Requirements *(mandatory)*

### Evidence

- docs/operacion/despliegue.md §3 — variables de CI/CD
- .gitlab-ci.yml — `--password-stdin` y `JOB-TOKEN`
- docs/adr/0013-basic-auth-y-dominio.md — el hash vive en el `.env`

## Success Criteria *(mandatory)*

- **SC-001**: las pruebas de esta HU pasan sin red ni servidor.
- **SC-002**: `make check` en verde.
- **SC-003**: la documentación del M4 enlaza el entregable.

## Assumptions

- El sistema desplegado sigue disponible en `https://143.198.10.157.sslip.io`.
- Las credenciales viven en variables de CI/CD, nunca en el repositorio.
