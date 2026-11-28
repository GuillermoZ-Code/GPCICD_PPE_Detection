# Feature Specification: HU-092 — Sincronizar `backlog.md` con las 113 HU

**Feature Branch**: `feature/093-hu-092-backlog-espejo`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #148 — «Sincronizar `backlog.md` con las 113 HU». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-14`, P0, Ola 2, 2 SP, 8 pruebas objetivo. Depende de
HU-089 (#145, cerrada).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Un espejo que se pueda defender en el documento del curso (Priority: P0)

Como dueño del backlog, quiero que `docs/curso/backlog.md` liste las 113 HU con SP,
dueño, ola, spec y estado, para que el Capítulo 5 y el tablero cuenten lo mismo.

**Why this priority**: el espejo se quedó en 15 HU del M3. El M4 añadió 100 HU y hoy el
documento del curso no puede citar el backlog sin contradecir a GitHub.

**Independent Test**: `uv run pytest tests/test_backlog_mirror.py` y revisar que cada
fila tenga issue, SP y spec, y que los totales cuadren con `ASIGNACION.md`.

**Acceptance Scenarios** (AC de la issue #148):

1. **AC-01**: **Dado** el espejo, **Cuando** se revisa, **Entonces** aparecen las **113
   HU** con SP, dueño, ola y spec.
2. **AC-02**: **Dado** el espejo, **Cuando** se suman los totales, **Entonces** cuadran
   por sprint (7/11, 6/8, 100/200) y por integrante (50 SP y 192 pruebas cada uno en el
   M4).
3. **AC-03**: **Dado** el repositorio, **Cuando** se ejecuta la suite, **Entonces** una
   prueba compara el espejo con la lista de `specs/`.

### Edge Cases

- **HU sin spec todavía**: se muestra el número de spec previsto, sin enlace; no se
  inventa una carpeta.
- **HU de otro sprint**: las 13 del M3 conservan su sprint; las 100 del M4 van a M4-S3.
- **HU-014 y HU-015**: se cuentan en el M4 (allí se ejecutan), así que el M3 queda en
  19 SP y el total en 219.
- **Issue cerrada**: la fila muestra «cerrada»; el espejo no decide el estado, lo copia.
- **Tabla de dependencias**: sus filas no cuentan como HU del espejo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `docs/curso/backlog.md` MUST listar las 113 HU con identificador, issue,
  título, SP, dueño, ola, spec y estado.
- **FR-002**: El espejo MUST separar M3 (HUs 001–013) y M4 (HUs 014–113) y declarar los
  totales por sprint e integrante.
- **FR-003**: Cada enlace `specs/...` del espejo MUST existir, y cada carpeta de `specs/`
  (salvo la TA 001) MUST aparecer referenciada.
- **FR-004**: El espejo MUST declarar su fuente (`ASIGNACION.md` y GitHub Issues) y la
  fecha de generación.
- **FR-005**: No se cambian títulos, AC ni SP de las issues; el espejo los copia.

### Key Entities

- **FilaDelBacklog**: HU, issue, título, SP, dueño, ola, spec y estado.
- **Totales**: HUs y SP por sprint y por integrante.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Las 113 HU | `tests/test_backlog_mirror.py::test_backlog_lists_all_113_hus`, `::test_backlog_m4_rows_have_epic_sp_wave_and_spec` |
| AC-02 Totales | `test_backlog_totals_match_rows` |
| AC-03 Espejo vs. specs | `test_backlog_specs_match_repository` |

## Success Criteria *(mandatory)*

- **SC-001**: El espejo se puede citar en el documento sin contradecir a GitHub.
- **SC-002**: Ninguna HU queda sin SP, dueño, ola o spec prevista.
- **SC-003**: `make check` pasa con las pruebas nuevas.
- **SC-004**: `make ownership-check` no reporta bloqueos (`backlog.md` es del autor).

## Out of Scope

- Cambiar el reparto o las olas (HU-090).
- Crear issues nuevas (HU-089, cerrada).
- Reescribir los AC de cada HU; viven en la issue.
- Generar el espejo automáticamente en cada push.

## Assumptions

- El total de 219 SP = 19 del M3 (13 HU) + 200 del M4 (100 HU, incluidas HU-014 y
  HU-015).
- El espejo es una **instantánea** del 23/11/2026; el estado de cada issue se actualiza
  al regenerarlo, y las pruebas no dependen de GitHub.
- `docs/curso/backlog.md` es `[[locked]]` de `jesusriverosUAO`; el autor lo actualiza.
