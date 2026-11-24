# Feature Specification: HU-091 — Plantilla de issue HU con AC y DoR/DoD

**Feature Branch**: `feature/092-hu-091-plantilla-hu`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #147 — «Plantilla de issue HU con AC y DoR/DoD». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-14`, P0, Ola 1, 1 SP, 4 pruebas objetivo. No tiene
dependencias. Es la base de HU-089 (#145), que no se repite porque las 100 issues ya
existen.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Crear una HU con formato uniforme (Priority: P0)

Como dueño del backlog, quiero un formulario de issue que pida historia, criterios de
aceptación, SP Fibonacci, dependencias, spec y pruebas objetivo, para que toda HU nueva
nazca con la misma estructura y se pueda revisar sin reescribirla.

**Why this priority**: las 100 issues del M4 se generaron por script; la HU-091 deja el
formulario para las que vengan y es la dependencia de HU-089. Sin él, cada autor inventa
el formato y el tablero deja de ser comparable.

**Independent Test**: abrir *New issue → HU* en GitHub y comprobar que el formulario
pide los seis campos y los dos checklists, y ejecutar
`uv run pytest tests/test_issue_template.py`. El YAML debe cargar sin errores y el
formulario debe declarar los campos obligatorios.

**Acceptance Scenarios** (AC de la issue #147):

1. **AC-01**: **Dado** el repositorio, **Cuando** se abre la plantilla de HU, **Entonces**
   pide historia, criterios de aceptación, SP de la serie Fibonacci, dependencias, ruta
   de la spec y número de pruebas objetivo.
2. **AC-02**: **Dado** el formulario, **Cuando** se revisa, **Entonces** incluye un
   checklist de *Definition of Ready* y otro de *Definition of Done* con sus ítems
   obligatorios.
3. **AC-03**: **Dado** el archivo de la plantilla, **Cuando** se ejecuta la suite,
   **Entonces** una prueba confirma que el YAML es válido y cumple el contrato de los
   issue forms de GitHub.

### Edge Cases

- **SP fuera de Fibonacci**: el desplegable solo ofrece `1, 2, 3, 5, 8, 13`; no hay
  campo libre donde escribir `4` o `10`.
- **Sin dependencias**: el campo de dependencias es obligatorio, pero admite `—` como
  respuesta explícita; así se distingue «no tiene» de «no se revisó».
- **YAML con tabulaciones o claves repetidas**: la prueba debe fallar; los issue forms
  no admiten tabulaciones y una clave repetida sobrescribe la anterior en silencio.
- **Id de campo repetido**: la prueba debe fallar; GitHub usa `id` como nombre del campo
  y un duplicado rompe el formulario.
- **Elemento no soportado**: la prueba valida los tipos que GitHub admite
  (`markdown`, `textarea`, `input`, `dropdown`, `checkboxes`); cualquier otro se rechaza.
- **Plantilla sin `validations.required`**: el formulario se podría enviar vacío; la
  prueba exige obligatoriedad en los campos de AC y en los checklists.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El repositorio MUST incluir `.github/ISSUE_TEMPLATE/hu.yml` como issue
  form con `name`, `description` y `body`.
- **FR-002**: El formulario MUST pedir la historia en formato «Como …, quiero …, para …».
- **FR-003**: El formulario MUST pedir los criterios de aceptación numerados `AC-01`,
  `AC-02`, …
- **FR-004**: Los SP MUST elegirse de un desplegable con la serie Fibonacci
  `1, 2, 3, 5, 8, 13`.
- **FR-005**: El formulario MUST pedir dependencias, ruta de la spec y número de pruebas
  objetivo como campos obligatorios.
- **FR-006**: El formulario MUST incluir un checklist de DoR y otro de DoD con ítems
  obligatorios.
- **FR-007**: La DoD MUST recoger las reglas del equipo: cada AC con prueba, `make check`
  y CI en verde, PR aprobada por otra persona y cierre manual de la issue.
- **FR-008**: No se agregan dependencias: la prueba usa PyYAML, que ya llega como
  dependencia transitiva de `pre-commit` (grupo `dev`) y de `mlflow` (extra
  `tracking`).
- **FR-009**: La plantilla MUST respetar la propiedad de rutas:
  `.github/ISSUE_TEMPLATE/` pertenece a `jesusriverosUAO` en `propiedad.toml`.

### Key Entities

- **HuIssueForm**: documento YAML con `name`, `description`, `title`, `labels` y `body`.
- **Campo del formulario**: elemento de `body` con `type`, `id` y `attributes`; los
  `checkboxes` añaden `options[].label` y `options[].required`.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Campos obligatorios | `tests/test_issue_template.py::test_hu_template_requests_required_fields` |
| AC-01 SP Fibonacci | `test_hu_template_uses_fibonacci_story_points` |
| AC-02 DoR y DoD | `test_hu_template_has_dor_and_dod_checklists` |
| AC-03 YAML válido | `test_hu_template_is_valid_yaml` |
| AC-03 Contrato del form | `test_hu_template_form_contract` |
| AC-03 Ids únicos | `test_hu_template_has_unique_field_ids` |

## Success Criteria *(mandatory)*

- **SC-001**: GitHub muestra el formulario como una issue form válida, sin avisos de
  esquema.
- **SC-002**: Una HU creada desde la plantilla trae los seis campos y los dos checklists
  sin edición manual.
- **SC-003**: `make check` pasa con las pruebas nuevas y sin dependencias adicionales.
- **SC-004**: `make ownership-check` no reporta bloqueos para esta rama.

## Out of Scope

- Crear las 100 issues (HU-089, #145): ya existen y solo se validan.
- Labels, milestones y tablero (HU-105 y HU-090).
- Editar `docs/curso/backlog.md` o `docs/curso/PRUEBAS.md` (archivos `[[locked]]`).
- Sustituir las plantillas `bug_report.yml`, `feature_request.yml` o `spike.yml`.

## Assumptions

- El repositorio usa issue forms de GitHub (`.yml`), no Markdown en
  `.github/ISSUE_TEMPLATE/`.
- La serie Fibonacci del curso es `1, 2, 3, 5, 8, 13`; `1 SP ≈ 1 día`.
- La ruta `.github/ISSUE_TEMPLATE/` es la única del manifiesto de propiedad que cubre
  este entregable; `config.yml` no se modifica.
- PyYAML está disponible en el entorno de desarrollo y en la CI por `pre-commit`; si el
  equipo decide declararla de forma explícita, se hará en un PR del dueño de
  `pyproject.toml` y `uv.lock`.
