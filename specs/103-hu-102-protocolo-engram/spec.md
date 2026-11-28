# Feature Specification: HU-102 — Protocolo de uso de Engram y ADR

**Feature Branch**: `feature/103-hu-102-protocolo-engram`

**Created**: 2026-11-24

**Status**: En implementación

**Input**: Issue #158 — «Protocolo de Engram y ADR». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-12`, P1, Ola 3, 2 SP, 8 pruebas objetivo. Depende de
HU-101 (fusionada).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Evitar que la memoria reemplace al repositorio (Priority: P1)

Como equipo, quiero reglas sobre qué se guarda en Engram, para evitar que reemplace
`CONSTITUTION.md` o filtre datos personales.

**Why this priority**: Engram ya está registrado (HU-101); sin protocolo, cada agente
guarda lo que quiere y la memoria puede contradecir al repositorio.

**Independent Test**: abrir el ADR 0011 y comprobar que define qué se guarda, qué no, la
sincronización y la exportación; ejecutar `uv run pytest tests/test_engram_protocol.py`.

**Acceptance Scenarios** (AC de la issue #158):

1. **AC-01**: **Dado** el protocolo, **Cuando** se revisa, **Entonces** define qué se
   guarda, qué no y cómo se exporta o sincroniza.
2. **AC-02**: **Dado** el repositorio, **Cuando** se revisa `docs/adr/`, **Entonces**
   existe el ADR 0011 sobre memoria de agentes y está indexado.
3. **AC-03**: **Dado** `AGENTS.md`, **Cuando** se revisa la tabla de herramientas,
   **Entonces** la fila de Engram remite al ADR 0011.

### Edge Cases

- **Memoria que contradice la constitución**: manda el repositorio.
- **Datos sensibles**: no se guardan credenciales ni datos personales.
- **Equipo sin Engram**: el MCP se desactiva; el protocolo no cambia el resto del flujo.
- **Migración de equipo**: la base se exporta fuera de Git.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El ADR MUST estar en `docs/adr/0011-memoria-agentes.md`.
- **FR-002**: MUST listar qué se guarda y qué no.
- **FR-003**: MUST declarar la memoria como local y subordinada al repositorio.
- **FR-004**: MUST documentar la exportación y la no sincronización por Git.
- **FR-005**: El índice de ADR MUST incluir el 0011.
- **FR-006**: `AGENTS.md` MUST remitir al ADR 0011.
- **FR-007**: Una prueba estructural MUST validar el protocolo.

### Key Entities

- **Protocolo**: reglas de qué guardar y cómo compartirlo.
- **ADR 0011**: decisión registrada e indexada.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Qué se guarda | `tests/test_engram_protocol.py::test_adr_says_what_is_stored`, `::test_adr_forbids_secrets_and_personal_data`, `::test_adr_documents_sync_and_export` |
| AC-02 ADR e índice | `::test_adr_exists_with_decision`, `::test_adr_is_subordinate_to_repository`, `::test_adr_index_lists_0011` |
| AC-03 AGENTS.md | `::test_agents_links_the_adr` |

## Success Criteria *(mandatory)*

- **SC-001**: Un agente nuevo sabe qué guardar y qué no sin preguntar.
- **SC-002**: `make check` pasa con las pruebas nuevas.
- **SC-003**: El ADR queda indexado y enlazado desde `AGENTS.md`.

## Out of Scope

- Sincronizar memorias entre equipos.
- Cambiar `CONSTITUTION.md` (solo se referencia).
- Instalar Engram en los equipos.

## Assumptions

- `docs/adr/` y `AGENTS.md` pertenecen a Guillermo: la PR genera aviso, no bloqueo.
- El número 0011 sigue la serie indicada por la issue.
