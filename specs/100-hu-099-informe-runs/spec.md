# Feature Specification: HU-099 — Informe comparativo de runs de MLflow

**Feature Branch**: `feature/100-hu-099-informe-runs`

**Created**: 2026-11-24

**Status**: En implementación

**Input**: Issue #155 — «Informe comparativo de runs de MLflow». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-14`, P1, Ola 3, 1 SP, 4 pruebas objetivo. Depende de HU-097
(fusionada).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Revisar la comparación sin abrir MLflow (Priority: P1)

Como evaluador, quiero un informe con tabla y enlaces a los runs, para revisar la
comparación desde el repositorio.

**Why this priority**: la comparación de modelos existe en MLflow y en un informe de
evaluación; falta un documento con enlaces directos a cada run.

**Independent Test**: generar el informe con dos `RunView` simulados y comprobar la tabla,
los enlaces `#/runs/<id>` y la referencia `sha256:` del artefacto.

**Acceptance Scenarios** (AC de la issue #155):

1. **AC-01**: **Dados** los runs, **Cuando** se genera el informe, **Entonces** hay una
   tabla con las métricas de cada run.
2. **AC-02**: **Dado** el informe, **Cuando** se revisa, **Entonces** cada run enlaza a su
   vista en MLflow y muestra su artefacto y SHA256.
3. **AC-03**: **Dado** el módulo, **Cuando** se ejecutan las pruebas, **Entonces** usan
   datos simulados, sin MLflow real.

### Edge Cases

- **Métrica ausente**: se muestra «—».
- **Sin runs**: la tabla queda vacía; el comando lo advierte.
- **Tracking URI con barra final**: se normaliza para el enlace.
- **Artefacto sin SHA**: se muestra solo la ruta.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El módulo MUST exponer `render_comparison_report`.
- **FR-002**: El informe MUST incluir una fila por run con mAP50, mAP50-95, precision y
  recall.
- **FR-003**: Cada fila MUST enlazar a `<tracking_uri>/#/runs/<run_id>`.
- **FR-004**: Cada fila MUST mostrar la ruta del artefacto y su `sha256:<hash>`.
- **FR-005**: El informe MUST declarar la fecha de generación.
- **FR-006**: No se agregan dependencias.

### Key Entities

- **RunView**: run consultado en MLflow.
- **Informe**: tabla Markdown con enlaces y referencias.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Tabla | `tests/test_tracking_report.py::test_report_has_table`, `::test_report_has_one_row_per_run`, `::test_report_shows_metrics`, `::test_report_has_generation_date` |
| AC-02 Enlaces y artefacto | `::test_report_links_each_run`, `::test_report_shows_artifact_reference` |
| AC-03 Datos simulados | `::test_write_report_creates_file` |

## Success Criteria *(mandatory)*

- **SC-001**: La comparación se revisa desde el repositorio con enlaces a MLflow.
- **SC-002**: `make check` pasa con las pruebas nuevas.
- **SC-003**: No se agregan dependencias.

## Out of Scope

- Ejecutar MLflow real.
- Cambiar la evaluación de HU-019.
- Publicar el informe en la web.

## Assumptions

- Los runs existen en MLflow o se construyen desde los resúmenes de evaluación.
- `docs/evaluation/` pertenece a Hernán: la PR genera aviso, no bloqueo.
