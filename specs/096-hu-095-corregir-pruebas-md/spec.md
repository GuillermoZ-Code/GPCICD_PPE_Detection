# Feature Specification: HU-095 — Corregir el inventario y el plan hacia 1.200 pruebas

**Feature Branch**: `feature/096-hu-095-corregir-pruebas-md`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #151 — «Corregir `PRUEBAS.md` y plan hacia 1.200 pruebas». Asignada a
Jesús (`jesusriverosUAO`), épica `ep-14`, P0, Ola 1, 1 SP, 4 pruebas objetivo. Depende
de HU-094 (#150, fusionada en #183).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Un solo número y un plan que cuadre (Priority: P0)

Como equipo, quiero un inventario con una única cifra vigente y un plan que reparta la
brecha hasta 1.200, para no presentar 375, 425, 451 y 515 en documentos distintos.

**Why this priority**: el AC original se escribió el 21/11 con 451 pruebas; desde
entonces se fusionaron ocho HU del M4 y el repositorio tiene 533. Un plan que ignore lo
entregado no sirve para cerrar el 26/11.

**Independent Test**: leer `docs/curso/PLAN-PRUEBAS.md` y ejecutar
`uv run pytest tests/test_plan_pruebas.py`. El punto de partida, la brecha y el reparto
por integrante deben cuadrar, y el comando de conteo debe ser el de HU-094.

**Acceptance Scenarios** (AC de la issue #151):

1. **AC-01**: **Dado** el repositorio, **Cuando** se revisa el plan, **Entonces** hay un
   único punto de partida (**533**) y un objetivo (**1.200**), sin cifras congeladas.
2. **AC-02**: **Dado** el plan, **Cuando** se suma el reparto por integrante,
   **Entonces** coincide con la brecha de **667** pruebas.
3. **AC-03**: **Dado** el plan, **Cuando** se busca el conteo, **Entonces** documenta la
   fecha y el comando (`make pruebas-write`).

### Edge Cases

- **Cifras históricas**: 375, 425 y 451 se conservan en una tabla de historial, no como
  baseline vigente.
- **HU que entrega menos pruebas de las planificadas**: el faltante se compensa en la
  siguiente HU del mismo integrante; el plan lo declara.
- **HU de documentación**: aporta pruebas estructurales; no se descuenta del reparto.
- **`PRUEBAS.md` generado**: no se edita a mano; lo regenera `make pruebas-write`.
- **Cambio de baseline tras una fusión**: se actualiza la tabla y el historial en el
  mismo PR que cambia el conteo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `docs/curso/PLAN-PRUEBAS.md` MUST declarar un único punto de partida
  medido con `make pruebas`.
- **FR-002**: El plan MUST repartir la brecha por integrante y sumar exactamente la
  brecha hasta 1.200.
- **FR-003**: El plan MUST documentar la fecha de medición y el comando de conteo.
- **FR-004**: El plan MUST conservar las cifras anteriores en una tabla de historial.
- **FR-005**: `docs/curso/PRUEBAS.md` MUST seguir siendo generado por HU-094; esta HU no
  lo edita a mano.
- **FR-006**: No se modifican títulos, AC ni SP de las issues; el cambio de cifras se
  documenta como decisión del dueño del backlog.

### Key Entities

- **Baseline**: pruebas recolectadas en una fecha, medidas con `make pruebas`.
- **Brecha**: objetivo menos baseline.
- **Reparto**: pruebas que cada integrante debe aportar según sus HU abiertas.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Baseline y objetivo | `tests/test_plan_pruebas.py::test_plan_has_one_baseline_and_target` |
| AC-02 Reparto por integrante | `test_plan_splits_remaining_tests_by_integrator` |
| AC-03 Fecha y comando | `test_plan_documents_counting_command_and_date` |
| AC-01 Historial | `test_plan_keeps_correction_history` |

## Success Criteria *(mandatory)*

- **SC-001**: El plan y `PRUEBAS.md` muestran la misma cifra vigente.
- **SC-002**: La suma del reparto por integrante es igual a la brecha.
- **SC-003**: `make check` pasa con las pruebas nuevas.
- **SC-004**: `make ownership-check` no reporta bloqueos.

## Out of Scope

- Cambiar el objetivo de 1.200 o el requisito de 400 del M3.
- Editar issues, labels o el tablero (HU-090).
- Reescribir el historial de `PRUEBAS.md`; el archivo es generado.
- Repartir pruebas nuevas por archivo; el reparto es por integrante y por HU.

## Assumptions

- **Decisión del dueño del backlog (23/11/2026):** se adopta el conteo real como
  baseline. El AC original (375 pytest + 76 Vitest = 451 y 749 nuevas) queda superado
  por 533 y 667; la diferencia se explica en el historial del plan.
- El conteo incluye las 4 pruebas de esta HU: 457 pytest + 76 Vitest = 533.
- Las HU cerradas y sus pruebas planificadas se toman de `ASIGNACION.md` y de las issues
  cerradas: 104 pruebas planificadas ya entregadas.
