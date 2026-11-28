# Feature Specification: HU-104 — Registro de riesgos del M4

**Feature Branch**: `feature/105-hu-104-riesgos`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #160 — «Registro de riesgos del M4». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-14`, P1, Ola 2, 1 SP, 4 pruebas objetivo. Sin
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Anticipar el fallo de la demo (Priority: P1)

Como equipo, quiero una matriz de riesgo, impacto y mitigación, para anticipar fallos de
la demo del 26/11 y de la sustentación del 28/11.

**Why this priority**: el cierre depende de infraestructura que no controlamos (cuota de
CI, Droplet, artefacto del modelo) y de la disponibilidad de cuatro personas.

**Independent Test**: abrir `docs/curso/M4/RIESGOS.md` y comprobar que cada riesgo tiene
categoría, dueño, disparador y mitigación; ejecutar
`uv run pytest tests/test_riesgos_m4.py`.

**Acceptance Scenarios** (AC de la issue #160):

1. **AC-01**: **Dado** el registro, **Cuando** se revisa, **Entonces** cubre riesgos de
   infraestructura, cuota de CI, modelo y equipo.
2. **AC-02**: **Dado** cada riesgo, **Cuando** se revisa, **Entonces** tiene dueño y
   disparador.
3. **AC-03**: **Dado** el repositorio, **Cuando** se ejecuta la suite, **Entonces** una
   prueba estructural valida el registro.

### Edge Cases

- **Riesgo sin dueño**: la prueba falla; un riesgo sin responsable no se mitiga.
- **Riesgo sin disparador**: no se sabe cuándo actuar; la prueba falla.
- **Categoría desconocida**: solo se admiten infraestructura, CI, modelo o equipo.
- **Riesgo materializado**: se marca en la columna de estado y se enlaza la evidencia.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El registro MUST estar en `docs/curso/M4/RIESGOS.md`.
- **FR-002**: Cada riesgo MUST declarar categoría, probabilidad, impacto, dueño,
  disparador, mitigación y estado.
- **FR-003**: Las categorías MUST cubrir infraestructura, CI, modelo y equipo.
- **FR-004**: Cada fila MUST tener dueño y disparador no vacíos.
- **FR-005**: Una prueba estructural MUST validar tabla, categorías y campos.

### Key Entities

- **Riesgo**: identificador, categoría, probabilidad, impacto, dueño, disparador,
  mitigación y estado.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Categorías | `tests/test_riesgos_m4.py::test_file_exists`, `::test_all_categories_present` |
| AC-02 Dueño y disparador | `::test_every_risk_has_owner_and_trigger` |
| AC-03 Prueba estructural | `::test_minimum_number_of_risks` |

## Success Criteria *(mandatory)*

- **SC-001**: La sustentación tiene un plan de contingencia por riesgo.
- **SC-002**: `make check` pasa con las pruebas nuevas.
- **SC-003**: `make ownership-check` no reporta bloqueos.

## Out of Scope

- Ejecutar las mitigaciones.
- Cambiar el alcance o los SP de las issues.
- Documentar riesgos del M3, ya cerrado.

## Assumptions

- El registro es una instantánea del 23/11; el estado se actualiza al cierre.
- `docs/curso/` pertenece a Jesús; sin avisos de propiedad.
