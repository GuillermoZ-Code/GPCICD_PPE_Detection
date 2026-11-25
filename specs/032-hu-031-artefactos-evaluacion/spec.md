# Feature Specification: HU-031 — Matriz de confusión y curvas PR como artefactos

**Feature Branch**: `feature/032-hu-031-artefactos-evaluacion`

**Created**: 2026-11-24

**Status**: En implementación

**Input**: Issue #87 — «Matriz de confusión y curvas PR como artefactos». Asignada a
Hernán (`HestradaUAO`), épica `ep-14`, P1, ola 3, 1 SP, 4 pruebas objetivo. Depende de
HU-019, ya cerrada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Revisar las figuras de evaluación desde el run (Priority: P1)

Como integrante del equipo ML, quiero que la matriz de confusión y las curvas PR se
guarden con nombres estables por modelo, para revisarlas desde MLflow y comparar dos
versiones sin confundir archivos.

**Why this priority**: las figuras de Ultralytics viven en directorios temporales y
con nombres genéricos (`confusion_matrix.png`, `BoxPR_curve.png`). Al registrar varios
runs, se sobrescriben o no se pueden asociar con el modelo que las produjo.

**Independent Test**: con un directorio temporal que contiene figuras de ejemplo, se
ejecuta la función de recolección y se verifica que copia solo las figuras conocidas,
con nombres que incluyen la versión y el SHA256 del modelo.

**Acceptance Scenarios** (AC de la issue #87):

1. **AC-01**: **Dado** un run de evaluación con figuras, **Cuando** se ejecuta el
   código, **Entonces** la matriz de confusión y las curvas PR se copian a artefactos
   versionados.
2. **AC-02**: **Dado** un modelo con versión y SHA256, **Cuando** se generan los
   nombres, **Entonces** son estables, seguros para el sistema de archivos y contienen
   la versión del modelo.
3. **AC-03**: **Dada** una función de recolección, **Cuando** se ejecutan las pruebas,
   **Entonces** se comprueba que genera exactamente los archivos esperados y que
   `evaluate` los registra en el resumen.

### Edge Cases

- Run sin figuras: no se crean archivos vacíos ni se inventan nombres.
- Figura desconocida: no se copia con nombre estable; el nombre estable directo falla.
- Versión con espacios o mayúsculas: se normaliza a slug minúsculas con guiones.
- SHA inválido o vacío: la generación del identificador falla explícitamente.
- Nombre de archivo repetido entre `BoxPR_curve.png` y `PR_curve.png`: se usa el mismo
  nombre estable para el mismo contenido semántico.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La generación de nombres MUST incluir versión normalizada y los primeros
  12 caracteres del SHA256.
- **FR-002**: La recolección MUST copiar `confusion_matrix.png`,
  `confusion_matrix_normalized.png`, `BoxPR_curve.png`, `BoxF1_curve.png`,
  `BoxP_curve.png` y `BoxR_curve.png` cuando existan.
- **FR-003**: La recolección MUST ignorar archivos que no sean figuras de evaluación.
- **FR-004**: La recolección MUST devolver una tupla vacía si el directorio de origen
  no existe o no tiene figuras, sin fallar.
- **FR-005**: `evaluate` MUST añadir las rutas de los artefactos generados al campo
  `artifacts` del `summary.json`.
- **FR-006**: Los nombres MUST ser deterministas para el mismo modelo y SHA256.
- **FR-007**: No se modifica el contrato `ImageData → list[Detection]` ni el modelo.
- **FR-008**: No se agregan dependencias.

### Key Entities

- **Modelo evaluado**: identificado por `model_version` y `sha256`.
- **Figura de evaluación**: archivo PNG generado por Ultralytics.
- **Artefacto estable**: copia con nombre `figura_<version>-<sha12>.png`.
- **Summary**: JSON de evaluación que conserva la lista de artefactos.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 Figuras copiadas | `tests/test_evaluation_artifacts.py::test_collect_copies_confusion_and_pr_curves`, `tests/test_evaluation_artifacts.py::test_collect_returns_empty_without_plots` |
| AC-02 Nombres estables | `tests/test_evaluation_artifacts.py::test_artifact_slug_is_stable_and_safe`, `tests/test_evaluation_artifacts.py::test_collect_rejects_unknown_figure` |
| AC-03 Evaluación integrada | `tests/test_evaluation_artifacts.py::test_evaluate_adds_stable_artifacts_to_summary` |

## Success Criteria *(mandatory)*

- **SC-001**: `make check` pasa sin GPU, dataset ni red.
- **SC-002**: Dos modelos con SHA distinto no generan el mismo nombre de artefacto.
- **SC-003**: Un run sin plots no produce archivos falsos.
- **SC-004**: La HU añade al menos 4 pruebas al inventario.
- **SC-005**: Los artefactos quedan disponibles en el `summary.json` para adjuntarlos
  al run de MLflow con el flujo existente.

## Out of Scope

- Cambiar el entrenamiento o el modelo.
- Modificar `src/ppe_detection/tracking/`; la integración usa los artefactos del
  summary y el mecanismo `--artifact` existente.
- Generar las figuras desde cero; Ultralytics las produce con `plots=True`.
- Analizar falsos positivos (HU-030) o calibrar umbrales (HU-029).

## Assumptions

- Ultralytics guarda las figuras en `metrics.save_dir` o en el directorio de salida.
- Las figuras son PNG y sus nombres son los del contrato de Ultralytics.
- El SHA256 del modelo ya está calculado por `evaluate`.
- Los pesos y datasets siguen fuera de Git.
