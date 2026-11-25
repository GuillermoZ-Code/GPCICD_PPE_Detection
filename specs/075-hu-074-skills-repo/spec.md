# Feature Specification: HU-074 — Instalar skills de GitLab y frontend-design

**Feature Branch**: `feature/075-hu-074-skills-repo`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #130 — «HU-074 — Instalar skills de GitLab y frontend-design». Asignada
a Guillermo (`GuillermoZ-Code`), épica `ep-12`, P0, ola 2, 1 SP, 4 pruebas objetivo. Sin
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Las skills del equipo viven en el repositorio (Priority: P0)

Como integrante del equipo, quiero que las skills de GitLab y de diseño estén
versionadas en el repositorio, para que los cuatro agentes usen las mismas capacidades
sin depender de instalaciones locales distintas.

**Why this priority**: `frontend-design` es requisito de HU-076 (rediseño visual) y
`glab` es requisito de HU-073 y de toda la ola de GitLab. Si cada máquina instala otra
versión, el agente interpreta distinto y el rediseño deja de ser reproducible.

**Independent Test**: en un clon limpio del repositorio, `.agents/skills/glab/SKILL.md` y
`.agents/skills/frontend-design/SKILL.md` existen con frontmatter `name` y `description`;
el agente las lista al iniciar sesión y `AGENTS.md` las documenta.

**Acceptance Scenarios** (AC de la issue #130):

1. **AC-01**: **Dado** un clon del repositorio, **Cuando** se revisa `.agents/skills/`,
   **Entonces** están las skills `glab` (oficial del CLI) y `frontend-design` (de
   `anthropics/skills`), con su licencia cuando aplica.
2. **AC-02**: **Dada** la tabla de skills de `AGENTS.md`, **Cuando** se consulta,
   **Entonces** incluye ambas skills y remite a `.agents/skills/`.
3. **AC-03**: **Dado** un agente compatible, **Cuando** inicia la sesión, **Entonces**
   lista las skills versionadas (cada `SKILL.md` expone `name` y `description`).

### Edge Cases

- El repositorio ya tenía skills de usuario (`archify`, `jan-project-standard`,
  `find-skills`): no se duplican en el repo (una pesa ~17 MB).
- `glab skills install` es experimental: si cambia el formato, el README indica el
  comando de actualización y las pruebas fallan con contexto.
- Una skill sin licencia explícita no se versiona.
- Si `frontend-design` se actualiza, el `LICENSE.txt` se actualiza en el mismo commit.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `.agents/skills/glab/SKILL.md` MUST existir con frontmatter `name: glab`.
- **FR-002**: `.agents/skills/frontend-design/SKILL.md` MUST existir con frontmatter
  `name: frontend-design` y su `LICENSE.txt` (Apache-2.0).
- **FR-003**: Cada `SKILL.md` MUST declarar `name` y `description`, el contrato que
  permite al agente descubrirlas.
- **FR-004**: `AGENTS.md` MUST listar ambas skills en la tabla y remitir a
  `.agents/skills/README.md`.
- **FR-005**: El README de `.agents/skills/` MUST documentar origen, licencia y comando
  de actualización de cada skill, y por qué las skills de usuario no se versionan.
- **FR-006**: Las skills pesadas o personales MUST NOT copiarse al repositorio.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un clon limpio descubre las dos skills sin instalar nada extra.
- **SC-002**: Al menos 4 pruebas estáticas cubren los tres AC.
- **SC-003**: `make check` en verde y CI de GitHub en verde.

## Assumptions

- El formato de skill es el de la Agent Skills specification (`SKILL.md` con frontmatter
  `name` y `description`), compatible con OpenCode, Claude Code, Codex y GitLab Duo.
- `glab` instala en el proyecto (`.agents/skills/`) por omisión; `--global` queda para
  uso personal y no se versiona.
- `frontend-design` se copia desde `~/.agents/skills/` para que la instalación sea
  determinista y sin red; el comando `npx skills add` queda documentado como origen.
