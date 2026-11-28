# Feature Specification: HU-090 — Tablero con campos Fibonacci, olas y vistas

**Feature Branch**: `docs/091-hu-090-tablero`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #146 — «Tablero con campos Fibonacci, olas y vistas». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-14`, P0, Ola 2, 2 SP, 8 pruebas objetivo. Depende de
HU-089 (crear las 100 issues), ya cerrada. Entregable: **GitHub Project #1**.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ver la carga y el avance sin contar a mano (Priority: P0)

Como equipo, quiero vistas por persona, ola y épica, para ver la carga 1:1 y el avance
del M4 sin abrir el backlog.

**Why this priority**: el tablero es la evidencia operativa del sprint; sin campos ni
vistas, la suma de 50 SP por integrante y el avance de las olas no son verificables.

**Independent Test**: abrir el Project #1 y comprobar que cada item tiene `Estimate`,
`Size`, `Priority`, `Ola` y `Épica`, y que existen las vistas de integrante, ola y
épica; ejecutar `uv run pytest tests/test_board_m4.py`.

**Acceptance Scenarios** (AC de la issue #146):

1. **AC-01**: **Dado** el tablero, **Cuando** se revisa un item, **Entonces** `Estimate`
   usa solo 1, 2, 3, 5 y 8, y `Size` (XS–XL) es coherente.
2. **AC-02**: **Dado** el tablero, **Cuando** se navega, **Entonces** hay vistas por
   integrante, por ola, por épica y un burndown.
3. **AC-03**: **Dado** el tablero, **Cuando** se agrupa por integrante, **Entonces** la
   suma de SP es 50 para cada uno.

### Edge Cases

- **HU del M3 en el mismo tablero**: no tienen `Ola` ni `Épica`; se excluyen de la suma
  del M4.
- **Item sin `Estimate`**: la prueba del backlog falla porque el SP no cuadra.
- **Burndown**: GitHub Projects no tiene ese layout; se documenta el paso manual en
  *Insights*.
- **Item duplicado**: dos filas con el mismo número de issue rompen la suma.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El tablero MUST tener `Estimate`, `Size`, `Priority`, `Ola` y `Épica`.
- **FR-002**: `Estimate` MUST ser 1, 2, 3, 5 u 8; `Size` MUST ser XS–XL coherente.
- **FR-003**: MUST existir una vista por integrante, una por ola y una por épica.
- **FR-004**: El burndown MUST quedar documentado con su paso manual en *Insights*.
- **FR-005**: La suma de SP del M4 MUST ser 50 por integrante.
- **FR-006**: Una prueba MUST validar los datos del backlog que alimentan el tablero.

### Key Entities

- **Item del tablero**: issue con `Estimate`, `Size`, `Priority`, `Ola` y `Épica`.
- **Vista**: tabla o board agrupado por integrante, ola o épica.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Fibonacci y Size | `tests/test_board_m4.py::test_estimates_are_fibonacci`, `::test_size_mapping_is_coherent` |
| AC-02 Vistas y burndown | `tests/test_board_m4.py::test_board_doc_lists_required_views`, `::test_board_doc_explains_burndown` |
| AC-03 50 SP por integrante | `tests/test_board_m4.py::test_each_integrator_sums_fifty_sp` |

## Success Criteria *(mandatory)*

- **SC-001**: Los 100 items del M4 tienen los cinco campos completos.
- **SC-002**: Las vistas existen y el burndown tiene instrucciones reproducibles.
- **SC-003**: `make check` pasa con las pruebas nuevas.

## Out of Scope

- Crear un gráfico de burndown por API (no existe esa mutación).
- Cambiar SP, prioridad u ola de las HU (los define el backlog de Jesús).
- Sincronizar el tablero con GitLab.

## Assumptions

- El Project #1 es público y vive en la cuenta `GuillermoZ-Code`.
- El backlog es la fuente de verdad de SP, prioridad, ola y épica.
