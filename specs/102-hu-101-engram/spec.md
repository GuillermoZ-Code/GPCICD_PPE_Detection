# Feature Specification: HU-101 — Engram: memoria persistente para los agentes

**Feature Branch**: `feature/102-hu-101-engram`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #157 — «Engram: memoria persistente para los agentes del equipo».
Asignada a Jesús (`jesusriverosUAO`), épica `ep-12`, P0, Ola 2, 2 SP, 8 pruebas
objetivo. No tiene dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Que el agente recuerde entre sesiones (Priority: P0)

Como integrante del equipo, quiero que OpenCode registre Engram como servidor MCP y que
su base de datos viva fuera de Git, para que cada agente recupere decisiones y hallazgos
de sesiones anteriores sin contaminar el repositorio.

**Why this priority**: el M3 se cerró con observaciones sobre contexto perdido entre
sesiones. Engram ya está instalado en el equipo, pero no está registrado en el proyecto ni
documentado; sin eso, cada agente empieza a ciegas.

**Independent Test**: abrir `opencode.json` y comprobar que declara el MCP `engram`;
seguir `docs/operacion/engram.md` para guardar una memoria, recuperarla con
`mem_search` y verificar que `~/.engram/engram.db` está fuera del repositorio.

**Acceptance Scenarios** (AC de la issue #157):

1. **AC-01**: **Dado** el repositorio, **Cuando** se abre OpenCode, **Entonces**
   `opencode.json` registra Engram como MCP y el runbook explica cómo instalarlo en cada
   equipo.
2. **AC-02**: **Dado** el runbook, **Cuando** se sigue, **Entonces** hay evidencia de una
   memoria guardada y recuperada (`mem_save` → `mem_search`).
3. **AC-03**: **Dado** el repositorio, **Cuando** se revisa `.gitignore`, **Entonces** la
   base de datos local (`*.db`, `*.sqlite`) queda fuera de Git.

### Edge Cases

- **Equipo sin Engram instalado**: el MCP se puede deshabilitar con `"enabled": false`
  sin romper el resto de la configuración; el runbook lo explica.
- **Ruta del binario**: la configuración del proyecto usa `engram` (PATH), no una ruta
  absoluta de una máquina.
- **Base de datos**: vive en `~/.engram/engram.db`; no se versiona ni se copia al repo.
- **Secretos**: las memorias no deben contener credenciales ni datos personales.
- **Otro agente (Codex/Claude)**: el runbook indica el comando de registro equivalente.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `opencode.json` MUST declarar el MCP `engram` con un comando portable.
- **FR-002**: El MCP MUST poder deshabilitarse sin afectar al resto de la configuración.
- **FR-003**: `docs/operacion/engram.md` MUST documentar instalación, registro,
  verificación, uso y desinstalación.
- **FR-004**: El runbook MUST mostrar `mem_save` y `mem_search` con un ejemplo real.
- **FR-005**: El runbook MUST indicar que la base de datos vive fuera de Git.
- **FR-006**: `.gitignore` MUST cubrir `*.db` y `*.sqlite`.
- **FR-007**: Las pruebas MUST validar la configuración y el runbook sin ejecutar Engram.
- **FR-008**: No se agregan dependencias al paquete ni al frontend.

### Key Entities

- **Servidor MCP**: entrada `mcp.engram` de `opencode.json` (tipo local, comando y estado).
- **Memoria**: observación guardada con título, tipo y contenido.
- **Base de datos**: `~/.engram/engram.db`, fuera del repositorio.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 MCP registrado | `tests/test_engram_config.py::test_opencode_json_is_valid_json`, `::test_opencode_declares_engram_mcp`, `::test_opencode_engram_is_enabled` |
| AC-01 Runbook | `::test_runbook_documents_installation`, `::test_runbook_documents_how_to_disable` |
| AC-02 Guardar y recuperar | `::test_runbook_documents_save_and_search` |
| AC-03 Base fuera de Git | `::test_runbook_documents_local_database`, `::test_gitignore_covers_engram_database` |

## Success Criteria *(mandatory)*

- **SC-001**: Un integrante nuevo puede dejar Engram operativo siguiendo el runbook.
- **SC-002**: Ningún archivo de la base de datos aparece en `git status`.
- **SC-003**: `make check` pasa con las pruebas nuevas.
- **SC-004**: `make ownership-check` solo genera los avisos esperados (`opencode.json` y
  `docs/operacion/`).

## Out of Scope

- Sincronizar memorias entre máquinas o con un servidor central.
- Sustituir `CONSTITUTION.md`, los ADR o `ESTADO.md`.
- Instalar Engram en los equipos de los compañeros.
- Definir el protocolo de uso (HU-102, #158).

## Assumptions

- Engram está instalado y expone el subcomando `engram mcp`.
- OpenCode lee `opencode.json` del repositorio y la configuración global; el proyecto
  declara el MCP y la global puede desactivarlo.
- `docs/operacion/` pertenece a Eliana y `opencode.json` a Guillermo: la PR genera aviso
  de propiedad y su revisión, no bloqueo.
