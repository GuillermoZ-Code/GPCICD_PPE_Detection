# Feature Specification: HU-113 — Informe de cumplimiento de la rúbrica M4

**Feature Branch**: `feature/114-hu-113-rubrica`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #169 — «Informe de cumplimiento de la rúbrica M4». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-15`, P0, Ola 3, 3 SP, 12 pruebas objetivo. Sin
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Llegar a la sustentación sin vacíos (Priority: P0)

Como equipo, quiero un checklist de la rúbrica con evidencia enlazada, para llegar a la
sustentación del 28/11 sin preguntas sin respuesta.

**Why this priority**: la rúbrica del M4 pesa 15 % y el cierre es el 26/11. Un informe
generado por script evita que la evidencia se quede en la cabeza de alguien.

**Independent Test**: ejecutar `make rubrica-write` y revisar
`docs/entrega/RUBRICA-M4.md`; cada ítem debe tener área, criterio, evidencia, responsable
y estado ✔/✘.

**Acceptance Scenarios** (AC de la issue #169):

1. **AC-01**: **Dado** el informe, **Cuando** se revisa, **Entonces** cada ítem de la
   rúbrica tiene evidencia y responsable.
2. **AC-02**: **Dado** el informe, **Cuando** se revisa, **Entonces** el estado ✔/✘ está
   actualizado con fecha de corte 27/11.
3. **AC-03**: **Dado** el repositorio, **Cuando** se ejecuta el script, **Entonces**
   genera o valida el informe.

### Edge Cases

- **Evidencia ausente**: se marca ✘ y queda a cargo del responsable.
- **Ítem sin responsable**: `--check` falla.
- **Documento en otra PR**: se marca ✘ hasta que se fusione.
- **Fecha**: el corte es el 27/11; el informe se regenera ese día.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El repositorio MUST exponer `python -m ppe_detection.tools.rubrica`.
- **FR-002**: La rúbrica MUST declarar id, área, criterio, evidencia y responsable.
- **FR-003**: El informe MUST marcar ✔ si la evidencia existe y ✘ si no.
- **FR-004**: El informe MUST declarar la fecha de corte 27/11/2026.
- **FR-005**: `--check` MUST fallar si un ítem no tiene responsable o criterio.
- **FR-006**: El informe MUST generarse con `--write`, sin edición manual.
- **FR-007**: No se agregan dependencias.

### Key Entities

- **RubricItem**: id, área, criterio, evidencia y responsable.
- **ReportRow**: ítem y si su evidencia existe.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Ítems y evidencia | `tests/test_tools_rubrica.py::test_render_lists_all_items`, `::test_build_rows_marks_existing_evidence` |
| AC-02 Estado ✔/✘ y corte | `::test_render_marks_ok_and_pending`, `::test_build_rows_marks_missing_evidence` |
| AC-03 Script | `::test_validate_items_accepts_complete`, `::test_validate_items_rejects_missing_owner`, `::test_write_report_creates_file`, `::test_main_check_passes_with_real_rubric` |

## Success Criteria *(mandatory)*

- **SC-001**: La sustentación se prepara desde un informe con evidencia enlazada.
- **SC-002**: `make rubrica-check` pasa en `develop`.
- **SC-003**: `make check` pasa con las pruebas nuevas.

## Out of Scope

- Completar la evidencia de otras HUs.
- Calificar el trabajo del equipo.
- Cambiar la rúbrica del curso.

## Assumptions

- La lista de ítems vive en el módulo y se actualiza cuando cambie la rúbrica.
- `docs/entrega/` pertenece a Eliana: la PR genera aviso, no bloqueo.
