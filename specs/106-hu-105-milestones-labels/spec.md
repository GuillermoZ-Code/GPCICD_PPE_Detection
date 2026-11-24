# Feature Specification: HU-105 — Milestones y labels de las nuevas épicas

**Feature Branch**: `feature/106-hu-105-milestones-labels`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #161 — «Milestones y labels de las nuevas épicas». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-14`, P0, Ola 1, 1 SP, 4 pruebas objetivo. No tiene
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Clasificar las 100 HU sin ambigüedad (Priority: P0)

Como dueño del backlog, quiero que `.github/labels.yml` declare todas las épicas y
prioridades del M4, y que los milestones cerrados dejen de aparecer como activos, para
filtrar el tablero y las issues sin duplicados ni etiquetas grises sin descripción.

**Why this priority**: las 100 issues se crearon con `ep-06`…`ep-15` y `could-have`, pero
el archivo versionado solo declara `ep-01`…`ep-05`. El workflow `Labels` sincroniza desde
el archivo, así que hoy la fuente de verdad está incompleta.

**Independent Test**: `uv run pytest tests/test_labels.py` y revisar en GitHub que
`M3-S1` y `M3-S2` están cerrados y que `ep-06`…`ep-15` tienen descripción y color.

**Acceptance Scenarios** (AC de la issue #161):

1. **AC-01**: **Dado** el repositorio y GitHub, **Cuando** se revisa la clasificación,
   **Entonces** `M3-S1` y `M3-S2` están cerrados, y `ep-06`…`ep-15` y `could-have`
   existen con descripción y color.
2. **AC-02**: **Dado** `.github/labels.yml`, **Cuando** se compara con GitHub,
   **Entonces** el archivo es la fuente versionada y contiene todas las épicas y
   prioridades que usan las issues.
3. **AC-03**: **Dado** el archivo, **Cuando** se ejecuta la suite, **Entonces** una
   prueba confirma que el YAML es válido y que cada etiqueta tiene nombre, color y
   descripción.

### Edge Cases

- **Etiqueta duplicada**: dos entradas con el mismo nombre harían que GitHub se quede
  con la última; la prueba debe fallar.
- **Color inválido**: GitHub exige seis dígitos hexadecimales sin `#`; un color con `#`
  o con cinco dígitos se rechaza.
- **Descripción vacía**: la etiqueta existe pero no explica nada; la prueba la rechaza.
- **Etiqueta usada por una issue y ausente del archivo**: el workflow no la borra
  (`skip-delete: true`), pero deja de ser reproducible; la prueba exige el catálogo
  completo `ep-01`…`ep-15`.
- **Milestone con issues abiertas**: no se cierra; `M3-S1` y `M3-S2` tienen cero issues
  abiertas, por eso se pueden cerrar.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `.github/labels.yml` MUST declarar `ep-01`…`ep-15` con descripción y color.
- **FR-002**: El archivo MUST declarar las tres prioridades: `must-have`, `should-have`
  y `could-have`.
- **FR-003**: Cada etiqueta MUST tener un nombre único, un color de seis dígitos
  hexadecimales y una descripción no vacía.
- **FR-004**: Los milestones `M3-S1` y `M3-S2` MUST quedar cerrados en GitHub.
- **FR-005**: El archivo MUST seguir siendo la fuente que consume el workflow `Labels`
  (`skip-delete: true`; no se borran etiquetas ajenas).
- **FR-006**: No se renombran ni se eliminan las etiquetas existentes `ep-01`…`ep-05`.

### Key Entities

- **Etiqueta**: nombre, color y descripción; la consume el workflow `Labels`.
- **Milestone**: agrupación por sprint; `M3-S1` y `M3-S2` se cierran al terminar el M3.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Épicas del M4 | `tests/test_labels.py::test_labels_cover_all_epics` |
| AC-01 Prioridades | `tests/test_labels.py::test_labels_cover_priorities` |
| AC-02 Fuente versionada | `test_labels_is_a_list_of_mappings` |
| AC-03 YAML válido y campos | `test_labels_have_unique_name_color_and_description` |

> El cierre de `M3-S1` y `M3-S2` se verifica en GitHub, no con pytest: `gh api` no debe
> usarse en pruebas unitarias (sin red).

## Success Criteria *(mandatory)*

- **SC-001**: El workflow `Labels` puede sincronizar el catálogo completo desde el
  archivo sin intervención manual.
- **SC-002**: Las 100 issues del M4 conservan sus etiquetas y ninguna queda sin épica.
- **SC-003**: `make check` pasa con las pruebas nuevas.
- **SC-004**: `make ownership-check` reporta la edición de `.github/labels.yml` como
  aviso (dueño: Guillermo), no como bloqueo.

## Out of Scope

- Crear o mover issues del tablero (HU-089 y HU-090).
- Cambiar títulos, AC o SP de las issues.
- Borrar etiquetas que no estén en el archivo.
- Sincronizar el tablero o los campos `Size` y `Priority` de los 113 items.

## Assumptions

- Los milestones `M3-S1` y `M3-S2` tienen cero issues abiertas y se pueden cerrar.
- El workflow `Labels` corre en cada push a `develop` que toque `labels.yml`, así que la
  sincronización ocurre al fusionar esta HU.
- `.github/labels.yml` pertenece a Guillermo en `propiedad.toml`; la PR necesita su
  revisión, pero no está en `[[locked]]`.
