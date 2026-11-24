# Feature Specification: HU-096 — Validador de specs SDD

**Feature Branch**: `feature/097-hu-096-validador-specs`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #152 — «Validador de specs SDD». Asignada a Jesús (`jesusriverosUAO`),
épica `ep-14`, P1, Ola 2, 3 SP, 12 pruebas objetivo. No tiene dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Detectar una spec incompleta antes del merge (Priority: P1)

Como dueño del backlog, quiero un comando que verifique que cada spec tiene sus tres
archivos, sus secciones obligatorias y cada AC con evidencia, para que el flujo SDD no se
quede en un documento a medias.

**Why this priority**: hoy la calidad de una spec depende de que el revisor se acuerde de
todo. Con 32 specs y cuatro agentes, la compuerta automática es la única forma de
sostener el estándar.

**Independent Test**: `uv run python -m ppe_detection.tools.check_specs` recorre `specs/`
y sale con 0; `--strict` muestra los problemas de las specs antiguas. Las pruebas usan
specs de ejemplo en `tmp_path`.

**Acceptance Scenarios** (AC de la issue #152):

1. **AC-01**: **Dada** una carpeta de spec, **Cuando** falta `spec.md`, `plan.md` o
   `tasks.md`, o un AC declarado no tiene evidencia, **Entonces** el validador falla.
2. **AC-02**: **Dado** el repositorio, **Cuando** se ejecuta el comando en local o en CI,
   **Entonces** devuelve el mismo resultado y un código de salida distinto de cero si hay
   problemas.
3. **AC-03**: **Dado** el módulo, **Cuando** se ejecutan las pruebas, **Entonces** crean
   specs de ejemplo en `tmp_path`, sin tocar las specs reales.

### Edge Cases

- **Spec anterior a la compuerta** (< 092): se valida solo la presencia de archivos; el
  resto se reporta como aviso. Se documenta como deuda histórica.
- **AC con evidencia documental** (un informe, un ADR, una tabla de otro documento): es
  evidencia válida aunque no sea una prueba.
- **Referencia a una prueba inexistente**: falla, incluso si el archivo existe.
- **AC con varias filas**: basta con que una fila tenga evidencia válida.
- **Spec sin tabla de aceptación**: falla en las specs nuevas.
- **Spec de ejemplo sin `tasks.md`**: falla con un mensaje que nombra el archivo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El repositorio MUST exponer `python -m ppe_detection.tools.check_specs`.
- **FR-002**: El validador MUST exigir `spec.md`, `plan.md` y `tasks.md` en cada carpeta
  de `specs/`.
- **FR-003**: `spec.md` MUST contener las secciones «User Scenarios & Testing»,
  «Requirements» y «Success Criteria».
- **FR-004**: Cada AC declarado en las specs nuevas MUST aparecer en la tabla de
  aceptación con evidencia resoluble (prueba existente o documento).
- **FR-005**: Una referencia `tests/...::test_...` MUST resolver a un archivo y una
  función existentes; un nombre suelto se busca en los archivos de prueba.
- **FR-006**: Las specs anteriores a 092 MUST validarse solo por presencia de archivos.
- **FR-007**: `--strict` MUST aplicar la regla completa también a las specs antiguas.
- **FR-008**: Un workflow de CI MUST ejecutar el validador en cada PR.
- **FR-009**: No se agregan dependencias.

### Key Entities

- **SpecDir**: carpeta `specs/NNN-...` con sus tres documentos.
- **ACDeclarado**: identificador `AC-NN` de la sección de escenarios.
- **Evidencia**: referencia a prueba o documento que respalda un AC.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Falta un archivo | `tests/test_tools_check_specs.py::test_missing_spec_file_fails`, `::test_missing_plan_file_fails`, `::test_missing_tasks_file_fails` |
| AC-01 AC sin evidencia | `::test_declared_ac_without_row_fails`, `::test_broken_test_reference_fails` |
| AC-01 Evidencia válida | `::test_bare_test_name_resolves`, `::test_frontend_test_reference_resolves`, `::test_document_evidence_is_accepted` |
| AC-02 Local y CI | `::test_main_returns_nonzero_with_problems`, `::test_main_returns_zero_without_problems` |
| AC-03 Specs de ejemplo | `::test_legacy_spec_only_checks_files`, `::test_validate_reports_all_problems` |

## Success Criteria *(mandatory)*

- **SC-001**: `make specs-check` pasa en `develop` y falla si una spec nueva queda
  incompleta.
- **SC-002**: El comando no modifica ningún archivo.
- **SC-003**: `make check` pasa con las pruebas nuevas.
- **SC-004**: `make ownership-check` solo genera los avisos esperados.

## Out of Scope

- Corregir las specs antiguas; se reportan con `--strict`.
- Validar el contenido semántico de los AC (solo su trazabilidad).
- Reescribir `specs/` o el flujo de Spec Kit.
- Generar specs nuevas.

## Assumptions

- Las specs nuevas (≥ 092) siguen el formato con tabla «Acceptance → Test» o
  «Acceptance → Evidence».
- Las specs antiguas usan formatos heterogéneos; exigirles la tabla completa dejaría el
  CI en rojo desde el primer día.
- La evidencia documental es aceptable: una HU documental no tiene pruebas unitarias.
