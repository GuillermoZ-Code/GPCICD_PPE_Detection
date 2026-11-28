# Feature Specification: HU-036 — Postprocesamiento con umbrales por clase

**Feature Branch**: `feature/037-hu-036-postprocessing`

**Created**: 2026-11-24

**Status**: En implementación

**Input**: Issue #92 — «Módulo de postprocesamiento con umbrales por clase». Asignada a
Hernán (`HestradaUAO`), épica `ep-09`, P1, ola 2, 2 SP, 8 pruebas objetivo. Depende de
HU-029, ya cerrada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Aplicar la calibración en producción (Priority: P1)

Como desarrollador, quiero aplicar los umbrales calibrados por clase desde
`configs/thresholds.yaml`, para que las detecciones del servicio usen la misma
configuración que la evaluación.

**Why this priority**: YOLO26n se calibra por clase en HU-029, pero el detector sigue
aplicando un umbral global. Sin este módulo, la calibración queda solo en el informe.

**Independent Test**: con detecciones sintéticas y un mapa de umbrales se verifica que
cada clase usa su valor, que el orden se conserva y que una configuración inválida
falla al cargar.

**Acceptance Scenarios** (AC de la issue #92):

1. **AC-01**: **Dado** `configs/thresholds.yaml`, **Cuando** se carga, **Entonces** el
   módulo obtiene las seis clases y usa 0,25 como respaldo seguro si el archivo no
   existe.
2. **AC-02**: **Dadas** detecciones y una configuración válida, **Cuando** se aplica el
   filtro, **Entonces** se descartan las que no alcanzan el umbral de su clase sin
   alterar el contrato ni la lista original.
3. **AC-03**: **Dada** una configuración inválida o una ruta explícita inexistente,
   **Cuando** se carga, **Entonces** se produce un error claro antes de inferir.

### Edge Cases

- Archivo por defecto ausente: se usan 0,25 para las seis clases.
- Ruta explícita inexistente: error, no respaldo silencioso.
- Umbral fuera de `[0,1]`: error.
- Clase faltante o ajena: error.
- Detección justo en el umbral: se conserva.
- Lista vacía: devuelve lista vacía.
- Entrada con detecciones de varias clases: se respeta el orden original.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `load_threshold_config()` MUST leer el YAML de HU-029 y devolver las seis
  clases.
- **FR-002**: Si el archivo por defecto no existe, MUST devolver 0,25 para todas las
  clases.
- **FR-003**: Una ruta explícita inexistente MUST fallar.
- **FR-004**: Un YAML incompleto, con clase ajena o con valor fuera de `[0,1]` MUST
  fallar con `ThresholdConfigError`.
- **FR-005**: `apply_thresholds()` MUST filtrar por `class_name` sin mutar la entrada.
- **FR-006**: La comparación MUST incluir el límite (`confidence >= umbral`).
- **FR-007**: No se modifica `Detection`, `ImageData` ni el contrato REST/gRPC.
- **FR-008**: No se agregan dependencias.

### Key Entities

- **ThresholdConfig**: mapa inmutable de las seis clases y su umbral.
- **ThresholdConfigError**: error de carga o validación.
- **Detection**: contrato existente que se filtra sin cambios.
- **configs/thresholds.yaml**: fuente calibrada por HU-029.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 Carga y respaldo | `tests/test_postprocessing_thresholds.py::test_loads_repository_thresholds`, `tests/test_postprocessing_thresholds.py::test_missing_default_config_uses_safe_defaults` |
| AC-02 Filtro por clase | `tests/test_postprocessing_thresholds.py::test_apply_filters_each_class_with_its_threshold`, `tests/test_postprocessing_thresholds.py::test_apply_preserves_order_and_does_not_mutate`, `tests/test_postprocessing_thresholds.py::test_apply_empty_list`, `tests/test_postprocessing_thresholds.py::test_default_apply_uses_repository_config` |
| AC-03 Configuración inválida | `tests/test_postprocessing_thresholds.py::test_explicit_missing_config_fails`, `tests/test_postprocessing_thresholds.py::test_invalid_threshold_fails`, `tests/test_postprocessing_thresholds.py::test_missing_class_fails`, `tests/test_postprocessing_thresholds.py::test_threshold_config_rejects_foreign_class` |

## Success Criteria *(mandatory)*

- **SC-001**: La suite pasa sin GPU, dataset, red ni YOLO.
- **SC-002**: La configuración inválida impide el arranque con un mensaje legible.
- **SC-003**: Las seis clases calibradas se aplican de forma independiente.
- **SC-004**: La HU añade al menos 8 pruebas al inventario.
- **SC-005**: No se modifica el contrato de detección.

## Out of Scope

- Integrar el filtro en la API o gRPC; esa integración es de HU-006/HU-010.
- Recalibrar umbrales (HU-029, ya cerrada).
- Cambiar el modelo o el dataset.
- Modificar `configs/thresholds.yaml`.

## Assumptions

- `configs/thresholds.yaml` existe y contiene las seis clases.
- Las detecciones ya cumplen el contrato `Detection`.
- El umbral de respaldo es 0,25.
- El YAML se lee sin PyYAML mediante el lector de HU-029.
