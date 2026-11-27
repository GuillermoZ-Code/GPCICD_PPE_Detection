# Feature Specification: HU-073 — MCP oficial de GitLab y `glab` autenticado

**Feature Branch**: `feature/074-073-gitlab-mcp`

**Created**: 2026-11-27

**Status**: Implementado (spec de cierre)

**Input**: Issue #129 — «HU-073 — MCP oficial de GitLab y `glab` autenticado». Épica `ep-12`,
1 SP.

> Spec escrita al cerrar la HU: el entregable ya está en `develop` y esta ficha deja
> los AC y su evidencia para la compuerta de trazabilidad.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - MCP oficial de GitLab y `glab` autenticado (Priority: P0)

Como equipo, quiero que mcp oficial de gitlab y `glab` autenticado quede verificado y documentado, para que la
entrega del M4 se pueda auditar sin depender de la memoria de quien lo hizo.

**Independent Test**: las pruebas estáticas de `tests/` leen los archivos del entregable
y comprueban los criterios; el comportamiento real se validó en el servidor.

**Acceptance Scenarios** (AC de la issue #129):

1. **AC-01**: El MCP de GitLab está conectado por OAuth, sin token en el repositorio.
2. **AC-02**: `glab auth status` y la consulta de pipelines funcionan.
3. **AC-03**: La configuración no guarda tokens: OAuth o variable de entorno.

## Requirements *(mandatory)*

### Evidence

- .agents/skills/glab/SKILL.md — guía de uso del CLI
- docs/operacion/gitlab-espejo.md — operación de GitLab
- AGENTS.md — tabla de herramientas del equipo

## Success Criteria *(mandatory)*

- **SC-001**: las pruebas de esta HU pasan sin red ni servidor.
- **SC-002**: `make check` en verde.
- **SC-003**: la documentación del M4 enlaza el entregable.

## Assumptions

- El sistema desplegado sigue disponible en `https://143.198.10.157.sslip.io`.
- Las credenciales viven en variables de CI/CD, nunca en el repositorio.
