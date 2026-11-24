# Feature Specification: HU-097 — Registrar en MLflow los runs de YOLO26 y YOLO11s

**Feature Branch**: `feature/098-hu-097-runs-mlflow`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #153 — «Registrar en MLflow los runs de YOLO26 y YOLO11s». Asignada a
Jesús (`jesusriverosUAO`), épica `ep-14`, P0, Ola 3, 2 SP, 8 pruebas objetivo. Depende de
HU-019 (cerrada).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Comparar modelos con trazabilidad (Priority: P0)

Como integrante del equipo ML, quiero tres runs comparables en MLflow, para comparar
modelos con los mismos parámetros y la referencia de su artefacto.

**Why this priority**: la comparación de HU-019 vive en un informe; sin runs comparables
no se puede reproducir ni auditar desde MLflow.

**Independent Test**: construir los payloads de tres resúmenes de evaluación y comprobar
que comparten `imgsz`, `conf`, `iou`, `seed` y partición, que cada uno referencia su
modelo por `sha256:<hash>` y que las métricas por clase están.

**Acceptance Scenarios** (AC de la issue #153):

1. **AC-01**: **Dados** tres resúmenes de evaluación, **Cuando** se construyen los
   payloads, **Entonces** comparten los parámetros clave y traen métricas por clase.
2. **AC-02**: **Dado** cada run, **Cuando** se revisa, **Entonces** referencia su
   artefacto por SHA256 y no copia pesos.
3. **AC-03**: **Dado** el módulo, **Cuando** se ejecutan las pruebas, **Entonces** usan
   resúmenes simulados, sin MLflow real.

### Edge Cases

- **Un solo resumen**: no hay comparación; falla con un mensaje claro.
- **Semilla o `imgsz` distintos**: los runs no son comparables; falla.
- **Métricas por clase ausentes**: el payload de HU-009 ya lo rechaza.
- **Pesos como artefacto**: se rechazan; solo se registra el SHA256.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El módulo MUST exponer `build_comparison_payloads`.
- **FR-002**: Cada payload MUST compartir `imgsz`, `conf`, `iou`, `seed` y partición.
- **FR-003**: Cada payload MUST incluir las métricas por clase del resumen.
- **FR-004**: Cada payload MUST referenciar el modelo por `sha256:<hash>`.
- **FR-005**: MUST fallar con menos de dos resúmenes o parámetros distintos.
- **FR-006**: No se agregan dependencias.

### Key Entities

- **Resumen de evaluación**: salida de HU-008 con modelo, dataset, configuración,
  métricas y métricas por clase.
- **Payload comparable**: par nombre de run y `RunPayload`.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Runs comparables | `tests/test_tracking_comparison.py::test_builds_one_payload_per_summary`, `::test_shared_params_are_identical`, `::test_per_class_metrics_are_logged` |
| AC-02 Referencia por SHA256 | `::test_artifact_reference_uses_sha256` |
| AC-03 Resúmenes simulados | `::test_rejects_different_seed`, `::test_rejects_different_imgsz`, `::test_requires_at_least_two_summaries`, `::test_run_names_are_distinct` |

## Success Criteria *(mandatory)*

- **SC-001**: Tres modelos se comparan desde MLflow sin abrir el informe.
- **SC-002**: Ningún peso entra a Git ni a los artefactos del run.
- **SC-003**: `make check` pasa con las pruebas nuevas.

## Out of Scope

- Ejecutar MLflow real en las pruebas.
- Registrar el modelo en el Registry (HU-098).
- Cambiar la evaluación (HU-019).

## Assumptions

- Los resúmenes siguen el formato de `build_run_payload` (HU-009).
- `tracking/` pertenece a Jesús.
