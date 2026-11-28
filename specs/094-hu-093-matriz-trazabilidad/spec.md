# Feature Specification: HU-093 — Matriz de trazabilidad HU → issue → spec → PR → pruebas

**Feature Branch**: `feature/094-hu-093-matriz-trazabilidad`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #149 — «Matriz de trazabilidad HU → issue → spec → PR → pruebas».
Asignada a Jesús (`jesusriverosUAO`), épica `ep-14`, P0, Ola 2, 5 SP, 16 pruebas
objetivo. Depende de HU-089 (#145, cerrada).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Demostrar la trazabilidad en la sustentación (Priority: P0)

Como evaluador, quiero una matriz generada por código que una cada HU con su issue, su
spec, su PR y sus pruebas, para demostrar trazabilidad completa sin revisar el
repositorio a mano.

**Why this priority**: la rúbrica del M4 exige evidencia de trazabilidad. Hoy se puede
seguir a mano para 15 HU, no para 113, y no hay ninguna compuerta que detecte una HU
cerrada sin spec o sin pruebas.

**Independent Test**: `uv run python -m ppe_detection.tools.trazabilidad` imprime la
matriz; `--write` genera `docs/curso/TRAZABILIDAD.md`; `--check` falla si una HU cerrada
no tiene spec o prueba.

**Acceptance Scenarios** (AC de la issue #149):

1. **AC-01**: **Dado** el repositorio y GitHub, **Cuando** se ejecuta el comando,
   **Entonces** la matriz sale de `gh`, de `specs/` y de las pruebas que referencian la
   HU o que su spec cita.
2. **AC-02**: **Dado** el resultado, **Cuando** se revisa, **Entonces** las HU sin spec,
   sin PR o sin pruebas quedan marcadas.
3. **AC-03**: **Dado** el CI, **Cuando** una HU cerrada no tiene spec o prueba,
   **Entonces** el job falla.

### Edge Cases

- **HU documental o de GPU** (spike, ADR, informe, entrenamiento, creación de issues):
  no tiene pruebas unitarias por naturaleza; se declara en una lista de exenciones con
  su motivo y el check no la marca.
- **HU abierta**: puede no tener PR ni pruebas todavía; el check no falla, la matriz lo
  marca.
- **PR sin `Closes #N`**: se enlaza por el título (`HU-NNN`) o por la rama
  (`feature/NNN-hu-...`).
- **Spec sin carpeta**: la matriz muestra «—» y el check falla si la HU está cerrada.
- **Vitest**: las pruebas del frontend se citan como `src/...test.tsx` en la spec; la
  matriz las cuenta igual que pytest.
- **Sin red**: `--check` y `--write` usan `gh`; las pruebas unitarias del módulo usan
  datos simulados y no lo invocan.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El repositorio MUST exponer
  `python -m ppe_detection.tools.trazabilidad` con `--write` y `--check`.
- **FR-002**: La matriz MUST incluir por HU: issue y estado, spec, PR fusionadas y
  archivos de prueba.
- **FR-003**: Una HU cuenta como probada si un archivo de `tests/` o del frontend
  menciona su identificador, o si su `spec.md` cita el archivo en la tabla de
  aceptación.
- **FR-004**: Una PR cuenta para la HU si su cuerpo contiene `Closes #N`, su título
  menciona `HU-NNN` o su rama contiene `hu-nnn`.
- **FR-005**: `--check` MUST fallar si una HU cerrada no tiene spec o pruebas, salvo las
  exenciones declaradas con su motivo.
- **FR-006**: `docs/curso/TRAZABILIDAD.md` MUST generarse con `--write` y no editarse a
  mano.
- **FR-007**: Un workflow de CI MUST ejecutar `--check` en cada PR.
- **FR-008**: No se agregan dependencias; se usa la biblioteca estándar y `gh`.

### Key Entities

- **FilaDeTrazabilidad**: HU, issue, spec, PR, pruebas y estado de completitud.
- **Exención**: HU cerrada sin pruebas por naturaleza, con motivo declarado.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Origen de datos | `tests/test_tools_trazabilidad.py::test_specs_map_hu_to_directory`, `::test_tests_mentioning_hu_are_detected`, `::test_prs_link_issues_by_closes` |
| AC-02 Marcas | `::test_matrix_marks_missing_spec`, `::test_matrix_marks_missing_tests`, `::test_matrix_marks_complete_hu` |
| AC-03 Compuerta | `::test_check_fails_on_closed_hu_without_spec`, `::test_check_fails_on_closed_hu_without_tests`, `::test_check_ignores_open_hu`, `::test_check_honors_exemptions` |

## Success Criteria *(mandatory)*

- **SC-001**: `make trazabilidad-check` pasa en `develop` y falla si se simula una HU
  cerrada sin spec.
- **SC-002**: La matriz cubre las 113 HU y marca las que están incompletas.
- **SC-003**: `make check` pasa con las pruebas nuevas.
- **SC-004**: `make ownership-check` solo genera avisos esperados (`.github/` y
  `Makefile`).

## Out of Scope

- Completar specs o pruebas de HUs ajenas.
- Reescribir el tablero (HU-090).
- Validar el contenido de las specs (HU-096).
- Editar issues o PRs.

## Assumptions

- `gh` está autenticado en local y en CI (`GITHUB_TOKEN`).
- Las exenciones son cinco HUs documentales o de GPU: HU-016, HU-018, HU-019, HU-023 y
  HU-089; se declaran en el módulo con su motivo.
- `docs/curso/TRAZABILIDAD.md` es un archivo generado; se regenera al cerrar cada ola.
