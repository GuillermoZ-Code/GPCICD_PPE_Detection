# Feature Specification: HU-103 — Informe de sprint y burndown del M4

**Feature Branch**: `docs/104-hu-103-informe-sprint`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #159 — «Informe de sprint y burndown del M4». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-14`, P1, Ola 3, 2 SP, 8 pruebas objetivo. Depende de
HU-090 (tablero), ya configurada. Entregable: `docs/curso/M4/SPRINT.md`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Mostrar el avance real del sprint (Priority: P1)

Como dueño del backlog, quiero el burndown de SP por día, para mostrar el avance real
del sprint en la sustentación.

**Why this priority**: el tablero muestra el estado, pero no la evolución; sin burndown
no se puede explicar la velocidad ni la desviación frente al plan.

**Independent Test**: abrir `docs/curso/M4/SPRINT.md` y comprobar la tabla diaria y la
velocidad por integrante; ejecutar `uv run pytest tests/test_sprint.py`.

**Acceptance Scenarios** (AC de la issue #159):

1. **AC-01**: **Dado** el tablero, **Cuando** se genera el informe, **Entonces** hay un
   burndown de SP por día.
2. **AC-02**: **Dado** el informe, **Cuando** se revisa, **Entonces** hay velocidad por
   integrante en SP.
3. **AC-03**: **Dado** el cálculo, **Cuando** se prueba con datos simulados,
   **Entonces** los SP restantes cuadran.

### Edge Cases

- **Día sin cierres**: no genera fila; el burndown no inventa puntos.
- **Cierres que superan el total**: error explícito, no un restante negativo.
- **Integrante sin SP**: no aparece en la velocidad.
- **HU sin dueño**: se ignora en la velocidad por persona.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: MUST existir `burndown()` que reste los SP cerrados al total.
- **FR-002**: MUST existir `velocity_by_person()` con los SP por integrante.
- **FR-003**: El informe MUST listar las HU abiertas al corte y su SP.
- **FR-004**: La tabla MUST ser monótona y terminar en el SP abierto.
- **FR-005**: MUST haber pruebas con datos simulados.

### Key Entities

- **Cierre**: día, SP y dueño de una HU cerrada.
- **Punto del burndown**: día, SP cerrados y SP restantes.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Burndown | `tests/test_sprint.py::test_burndown_with_simulated_data`, `::test_doc_burndown_is_monotonic` |
| AC-02 Velocidad por integrante | `tests/test_sprint.py::test_velocity_by_person_sums_sp` |
| AC-03 Cálculo con datos simulados | `tests/test_sprint.py::test_burndown_rejects_closures_over_total`, `::test_deviation_signs` |

## Success Criteria *(mandatory)*

- **SC-001**: El informe explica el 90 % de avance (180/200 SP) con datos reales.
- **SC-002**: Las 9 HU abiertas y sus 20 SP están listadas.
- **SC-003**: `make check` pasa con las pruebas nuevas.

## Out of Scope

- Graficar el burndown en la SPA (HU-103 es documento).
- Calibrar las estimaciones (HU-109).
- Sustituir el tablero como fuente operativa.

## Assumptions

- El tablero y el backlog son la fuente de los SP y de los días de cierre.
- Las fechas del informe son UTC; se advierte la diferencia con UTC-5.
