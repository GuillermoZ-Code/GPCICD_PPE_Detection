# Feature Specification: HU-073 — MCP oficial de GitLab y `glab` autenticado

**Feature Branch**: `feature/074-hu-073-gitlab-mcp-glab`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #129 — «HU-073 — MCP oficial de GitLab y `glab` autenticado». Asignada a
Guillermo (`GuillermoZ-Code`), épica `ep-12`, P0, ola 2, 1 SP, 4 pruebas objetivo. Depende
de HU-065 (en revisión, PR #218).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Operar GitLab desde el agente y la terminal (Priority: P0)

Como integrante del equipo, quiero operar GitLab desde OpenCode y desde la terminal con
`glab`, para revisar pipelines, MRs y variables sin salir del flujo de trabajo y sin
tokens en el repositorio.

**Why this priority**: el pipeline del M4 (40 % de la rúbrica) se opera desde GitLab;
tener el MCP y el CLI autenticados es requisito de la entrega de herramientas del agente.

**Independent Test**: `glab auth status` muestra la sesión, `opencode mcp list` lista el
servidor y el runbook permite repetir la verificación desde cero.

**Acceptance Scenarios** (AC de la issue #129):

1. **AC-01**: **Dado** el repositorio, **Cuando** se abre una sesión de agente,
   **Entonces** el MCP de GitLab está declarado contra `https://gitlab.com/api/v4/mcp` y
   responde.
2. **AC-02**: **Dado** el CLI, **Cuando** se ejecuta `glab auth status` y una consulta,
   **Entonces** funcionan contra el proyecto del curso.
3. **AC-03**: **Dada** la configuración versionada, **Cuando** se revisa, **Entonces** no
   contiene tokens ni credenciales.

### Edge Cases

- El servidor se llama `gitlab` en la configuración aunque la issue lo mencione como
  `gitlab-mcp`: es el mismo y el prefijo es `gitlab.*`.
- La configuración global y la del repositorio pueden coexistir; la del repositorio la
  hace explícita para el equipo.
- Sin sesión en el keyring, `glab auth status` falla: el runbook indica `glab auth login`.
- El token del espejo (HU-065) no se usa aquí; vive solo en GitHub Secrets.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `opencode.json` MUST declarar el MCP `gitlab` como remoto contra
  `https://gitlab.com/api/v4/mcp` y habilitado.
- **FR-002**: La configuración existente (Engram) MUST conservarse.
- **FR-003**: El runbook MUST documentar `glab auth status`, `glab api user` y
  `opencode mcp list`.
- **FR-004**: El runbook MUST explicar que la conexión es OAuth y que no hay tokens en el
  repositorio.
- **FR-005**: La configuración MUST NOT contener `glpat-`, `PRIVATE-TOKEN` con valor ni
  `GITLAB_TOKEN`.
- **FR-006**: El runbook MUST aclarar la diferencia de nombre entre `gitlab` y
  `gitlab-mcp`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Cualquier integrante puede verificar el MCP y el CLI en dos comandos.
- **SC-002**: Al menos 4 pruebas estáticas cubren los tres AC.
- **SC-003**: `make check` en verde y CI de GitHub en verde.

## Assumptions

- `glab` 1.131.0 o superior está instalado y autenticado en el equipo.
- El MCP remoto de GitLab usa OAuth y no requiere token en la configuración.
- Las operaciones de escritura en GitLab las hace el Code Reviewer y se trazan en GitHub.
