# Feature Specification: HU-109 — Registro de capacidad y velocidad real

**Feature Branch**: `docs/110-hu-109-capacidad`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #165 — «Registro de capacidad y velocidad real». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-14`, P2, Ola 3, 1 SP, 4 pruebas objetivo. Depende de
HU-103 (informe de sprint), cerrada. Entregable: `docs/curso/M4/CAPACIDAD.md`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Calibrar las estimaciones con datos reales (Priority: P2)

Como dueño del backlog, quiero comparar SP planificados y entregados, para calibrar las
estimaciones Fibonacci del siguiente sprint.

**Why this priority**: el plan del M4 asignó 50 SP por persona en 10 días, cinco veces la
regla 1:1 del curso; sin el registro, el error se repetiría en el M5.

**Independent Test**: abrir `docs/curso/M4/CAPACIDAD.md` y comprobar la tabla por
integrante y la desviación; ejecutar `uv run pytest tests/test_capacidad.py`.

**Acceptance Scenarios** (AC de la issue #165):

1. **AC-01**: **Dado** el sprint, **Cuando** se revisa, **Entonces** hay una tabla por
   integrante y día.
2. **AC-02**: **Dado** el plan 1:1, **Cuando** se compara, **Entonces** la desviación
   está calculada y explicada.
3. **AC-03**: **Dado** el cálculo, **Cuando** se prueba, **Entonces** la capacidad y la
   desviación cuadran.

### Edge Cases

- **Cero personas o cero días**: error explícito, no división por cero.
- **Plan cero**: la desviación no se calcula.
- **Datos en UTC**: el cierre del 28/11 es la noche del 27/11 local.
- **SP abiertos**: el total entregado no llega a 200; se declara.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: MUST existir `capacity()` con SP por persona-día.
- **FR-002**: La desviación MUST calcularse con `deviation()` y explicarse.
- **FR-003**: MUST haber una tabla por integrante con plan, entregado, desviación y
  SP/día.
- **FR-004**: MUST compararse con la regla 1 SP ≈ 1 día.
- **FR-005**: MUST haber pruebas del cálculo.

### Key Entities

- **Capacidad**: SP entregados / (personas × días).
- **Desviación**: (entregado − plan) / plan × 100.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Tabla por integrante | `tests/test_capacidad.py::test_doc_table_sums_to_total`, `::test_doc_capacity_matches_numbers` |
| AC-02 Desviación frente al plan 1:1 | `tests/test_capacidad.py::test_deviation_against_plan`, `::test_doc_states_one_to_one_ratio` |
| AC-03 Cálculo con prueba | `tests/test_capacidad.py::test_capacity_per_person_day`, `::test_capacity_rejects_invalid_inputs` |

## Success Criteria *(mandatory)*

- **SC-001**: La capacidad real (4,6 SP/persona-día) y la planificada (5,0) quedan
  documentadas.
- **SC-002**: La desviación por integrante suma la del equipo (−8 %).
- **SC-003**: `make check` pasa con las pruebas nuevas.

## Out of Scope

- Reestimar las HU del M4.
- Cambiar el reparto de `ASIGNACION.md`.
- Medir horas reales por persona (no hay registro horario).

## Assumptions

- El sprint dura 10 días y participan 4 personas.
- Los SP y los cierres provienen del tablero y del backlog.
