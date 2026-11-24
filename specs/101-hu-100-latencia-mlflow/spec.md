# Feature Specification: HU-100 — Latencia del benchmark en MLflow

**Feature Branch**: `feature/101-hu-100-latencia-mlflow`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #156 — «Registrar la latencia del benchmark en MLflow». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-14`, P2, Ola 3, 1 SP, 4 pruebas objetivo. Depende de HU-020
(cerrada).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Comparar desempeño y velocidad en el mismo run (Priority: P2)

Como responsable MLOps, quiero la latencia como métrica del run, para comparar desempeño
y velocidad juntos.

**Why this priority**: el benchmark de HU-020 vive en un informe; sin las métricas en
MLflow, la calidad y la latencia se consultan en dos sitios distintos.

**Independent Test**: construir el payload de latencia con dos resoluciones y comprobar
que registra `p50_ms_<imgsz>`, `p95_ms_<imgsz>`, hardware y el SHA256 del modelo.

**Acceptance Scenarios** (AC de la issue #156):

1. **AC-01**: **Dadas** las muestras por resolución, **Cuando** se construye el payload,
   **Entonces** registra p50 y p95 por resolución.
2. **AC-02**: **Dado** el run, **Cuando** se revisa, **Entonces** el hardware y la versión
   son parámetros y el modelo se referencia por SHA256.
3. **AC-03**: **Dado** el módulo, **Cuando** se ejecutan las pruebas, **Entonces** usan un
   tracker simulado, sin MLflow real.

### Edge Cases

- **Sin mediciones**: falla con un mensaje claro.
- **SHA inválido**: falla.
- **Muestras no positivas**: `latency_stats` las rechaza.
- **Varias resoluciones**: cada una tiene sus métricas; `resolutions` lista el orden.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El módulo MUST exponer `ResolutionLatency` y `build_latency_payload`.
- **FR-002**: `latency_stats` MUST calcular p50 y p95 por rango más cercano.
- **FR-003**: El payload MUST registrar p50, p95, media y fps por resolución.
- **FR-004**: El payload MUST registrar hardware, versión y SHA256 como parámetros.
- **FR-005**: MUST fallar sin mediciones o con un SHA inválido.
- **FR-006**: No se agregan dependencias.

### Key Entities

- **ResolutionLatency**: resolución y muestras de latencia.
- **Payload de latencia**: métricas por resolución y parámetros del entorno.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 p50/p95 por resolución | `tests/test_tracking_latency_run.py::test_payload_has_p50_and_p95_per_resolution`, `::test_multiple_resolutions_are_separate_metrics`, `::test_p50_uses_nearest_rank` |
| AC-02 Hardware y SHA256 | `::test_payload_records_hardware_params`, `::test_payload_references_model_by_sha`, `::test_rejects_invalid_sha` |
| AC-03 Tracker simulado | `::test_rejects_empty_measurements`, `::test_rejects_non_positive_samples` |

## Success Criteria *(mandatory)*

- **SC-001**: Calidad y latencia se comparan en la misma vista de MLflow.
- **SC-002**: `make check` pasa con las pruebas nuevas.
- **SC-003**: No se agregan dependencias.

## Out of Scope

- Ejecutar el benchmark (HU-020).
- Registrar el modelo en el Registry (HU-098).
- Medir la latencia de la API completa.

## Assumptions

- Las muestras vienen del benchmark de HU-020.
- `tracking/` pertenece a Jesús.
