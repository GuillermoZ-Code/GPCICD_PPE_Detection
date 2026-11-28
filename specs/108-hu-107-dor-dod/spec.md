# Feature Specification: HU-107 — Definición de Ready y Done del M4

**Feature Branch**: `feature/108-hu-107-dor-dod`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #163 — «Definición de Ready y Done del M4». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-14`, P0, Ola 1, 1 SP, 4 pruebas objetivo. No tiene
dependencias. Se apoya en la plantilla de HU-091 (#147).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Saber cuándo una HU está lista y cuándo está terminada (Priority: P0)

Como integrante del equipo, quiero criterios explícitos de entrada y de salida de una
HU, para no empezar historias a medias ni cerrarlas sin pruebas, revisión ni conteo.

**Why this priority**: con cuatro agentes trabajando en paralelo, la ambigüedad cuesta
más que el código. La DoR evita arrancar sin spec y la DoD evita cerrar sin evidencia.

**Independent Test**: leer la sección nueva de `CONTRIBUTING.md` y ejecutar
`uv run pytest tests/test_dor_dod.py`. Los criterios deben cubrir los cinco puntos de
entrada y los cinco de salida, y coincidir con el checklist de la plantilla de HU.

**Acceptance Scenarios** (AC de la issue #163):

1. **AC-01**: **Dado** `CONTRIBUTING.md`, **Cuando** se revisa la DoR, **Entonces**
   exige spec, criterios de aceptación, SP Fibonacci, dueño y dependencias.
2. **AC-02**: **Dado** `CONTRIBUTING.md`, **Cuando** se revisa la DoD, **Entonces**
   exige pruebas por AC, `make check`, PR revisada, issue cerrada y conteo actualizado.
3. **AC-03**: **Dado** el repositorio, **Cuando** se ejecuta la suite, **Entonces** una
   prueba confirma que `CONTRIBUTING.md` tiene la sección, la enlaza desde la tabla de
   contenidos y expresa cada criterio como una casilla marcable.

### Edge Cases

- **HU sin dependencias**: la DoR exige dejar `—` explícito; no vale dejar el campo
  vacío.
- **Documentación sin pruebas**: una HU de documentación sigue necesitando pruebas
  estructurales; la excepción de test-first solo cubre SPI y specs de documentación.
- **PR de otra persona**: la DoD exige aprobación de otro integrante; el autor nunca se
  autoaprueba.
- **Conteo de pruebas**: `docs/curso/PRUEBAS.md` es `[[locked]]` y lo actualiza su dueño;
  la DoD lo pide, no lo ejecuta cualquiera.
- **Plantilla y guía desincronizadas**: si cambia un ítem del formulario y no la guía,
  la prueba de consistencia falla.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `CONTRIBUTING.md` MUST incluir una sección de criterios de entrada y salida
  (DoR/DoD) enlazada desde su tabla de contenidos.
- **FR-002**: La DoR MUST exigir spec de Spec Kit, AC numerados, SP Fibonacci con dueño
  y dependencias identificadas.
- **FR-003**: La DoD MUST exigir al menos una prueba por AC, `make check` y CI en verde,
  PR aprobada por otra persona, issue cerrada a mano y conteo de pruebas actualizado.
- **FR-004**: Cada criterio MUST expresarse como una casilla (`- [ ]`) para que se pueda
  marcar en la issue o en la PR.
- **FR-005**: La sección MUST ser verificable sin red y sin dependencias nuevas.
- **FR-006**: No se modifican títulos, AC ni SP de las issues.

### Key Entities

- **DoR**: criterios que una HU cumple antes del primer commit.
- **DoD**: criterios que una HU cumple antes de cerrar la issue.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 DoR | `tests/test_dor_dod.py::test_dor_lists_entry_criteria` |
| AC-02 DoD | `tests/test_dor_dod.py::test_dod_lists_exit_criteria` |
| AC-03 Guía actualizada | `test_contributing_has_dor_dod_sections` |
| AC-03 Casillas marcables | `test_dor_and_dod_items_are_checkboxes` |

## Success Criteria *(mandatory)*

- **SC-001**: Un integrante nuevo sabe qué necesita para empezar y para cerrar sin
  preguntar.
- **SC-002**: La guía y la plantilla de issue no se contradicen.
- **SC-003**: `make check` pasa con las pruebas nuevas y sin dependencias adicionales.
- **SC-004**: `make ownership-check` no reporta bloqueos.

## Out of Scope

- Cambiar el flujo de Spec Kit o el tablero (HU-090).
- Crear las 100 issues (HU-089) o los labels (HU-105).
- Reescribir `CONTRIBUTING.md` completo; solo se añade la sección de DoR/DoD y su
  entrada en la tabla de contenidos.

## Assumptions

- La DoR y la DoD del M4 son las mismas para las cuatro personas y para sus agentes.
- El conteo de pruebas lo actualiza el dueño de `docs/curso/PRUEBAS.md`
  (`jesusriverosUAO`).
- La plantilla de issue de HU-091 (#147) todavía está en revisión; esta HU escribe los
  mismos ítems en la guía, pero **no** se acopla a ese archivo ni a su rama. La
  comprobación automática entre guía y formulario queda para una HU posterior.
