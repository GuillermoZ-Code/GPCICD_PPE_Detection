# Feature Specification: HU-108 — Retrospectiva y lecciones aprendidas

**Feature Branch**: `feature/109-hu-108-retrospectiva`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #164 — «Retrospectiva y lecciones aprendidas». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-15`, P2, Ola 3, 1 SP, 4 pruebas objetivo. Sin
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cerrar el M4 con lecciones accionables (Priority: P2)

Como equipo, quiero registrar qué funcionó y qué no, para mejorar en proyectos futuros y
dejar evidencia en el documento del curso.

**Why this priority**: el M4 se cierra con cuatro agentes en paralelo; sin retrospectiva,
los mismos roces (propiedad de archivos, CI rojo, PRs sin revisor) se repetirán en el M5.

**Independent Test**: abrir `docs/curso/M4/RETRO.md` y comprobar que cada integrante tiene
start/stop/continue y que cada acción tiene dueño y fecha; ejecutar
`uv run pytest tests/test_retro_m4.py`.

**Acceptance Scenarios** (AC de la issue #164):

1. **AC-01**: **Dado** el documento, **Cuando** se revisa, **Entonces** cada integrante
   tiene listas de *start*, *stop* y *continue*.
2. **AC-02**: **Dado** el documento, **Cuando** se revisa, **Entonces** hay acciones
   concretas con dueño y fecha.
3. **AC-03**: **Dado** el repositorio, **Cuando** se ejecuta la suite, **Entonces** una
   prueba estructural valida el formato.

### Edge Cases

- **Integrante sin bloque**: la prueba falla; los cuatro participan.
- **Acción sin dueño o fecha**: no es accionable; la prueba falla.
- **Lista vacía**: start/stop/continue deben tener al menos un ítem.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El documento MUST estar en `docs/curso/M4/RETRO.md`.
- **FR-002**: MUST incluir a Guillermo, Eliana, Hernán y Jesús con start/stop/continue.
- **FR-003**: MUST incluir una tabla de acciones con dueño y fecha.
- **FR-004**: Cada lista MUST tener al menos un ítem.
- **FR-005**: Una prueba estructural MUST validar el formato.

### Key Entities

- **Retrospectiva**: integrante y sus listas start/stop/continue.
- **Acción**: descripción, dueño y fecha.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Start/stop/continue | `tests/test_retro_m4.py::test_all_integrators_have_sections`, `::test_sections_have_items` |
| AC-02 Acciones | `::test_actions_have_owner_and_date` |
| AC-03 Prueba estructural | `::test_document_has_retro_sections` |

## Success Criteria *(mandatory)*

- **SC-001**: El equipo puede citar la retrospectiva en el documento del curso.
- **SC-002**: `make check` pasa con las pruebas nuevas.
- **SC-003**: `make ownership-check` sin bloqueos.

## Out of Scope

- Cambiar el proceso del M4 ya ejecutado.
- Evaluar personas; se evalúan prácticas.
- Repetir el informe de sprint (HU-103).

## Assumptions

- La retrospectiva se escribe al cierre del M4, con lo observado hasta el 23/11.
- `docs/curso/` pertenece a Jesús.
