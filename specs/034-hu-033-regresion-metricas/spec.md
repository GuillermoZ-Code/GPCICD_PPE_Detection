# Feature Specification: HU-033 — Pruebas de regresión de métricas

**Feature Branch**: `feature/034-hu-033-regresion-metricas`

**Created**: 2026-11-21

**Status**: En implementación

**Input**: Issue #89 — «Pruebas de regresión de métricas (golden)». Asignada a
Hernán (`HestradaUAO`), épica `ep-09`, P1, Ola 1, 2 SP, 8 pruebas objetivo. No tiene
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Proteger el cálculo de métricas (Priority: P1)

Como integrante del equipo, quiero que un cambio que degrade el cálculo de métricas
falle, para proteger la evaluación y evitar que un resultado defectuoso llegue al
informe o a la sustentación.

**Why this priority**: las métricas son la evidencia central de HU-008 y del modelo
desplegado. Un cambio silencioso en IoU, emparejamiento o AP puede alterar las
conclusiones sin que `make check` lo detecte.

**Independent Test**: ejecutar una suite de casos sintéticos con cajas, etiquetas y
métricas esperadas; todos los valores deben coincidir dentro de una tolerancia
explícita, sin GPU, dataset ni red.

**Acceptance Scenarios** (AC de la issue #89):

1. **AC-01**: **Dados** predicciones y etiquetas sintéticas, **Cuando** se calculan
   IoU, emparejamientos, precision/recall/F1, AP y mAP, **Entonces** coinciden con los
   valores dorados documentados.
2. **AC-02**: **Dada** una comparación numérica, **Cuando** se usa la suite, **Entonces**
   la tolerancia es explícita y suficientemente estricta para detectar una regresión.
3. **AC-03**: **Dado** el entorno de CI, **Cuando** se ejecuta la suite, **Entonces**
   corre sin GPU, sin dataset completo y sin red.

### Edge Cases

- Listas vacías: IoU, emparejamientos y AP devuelven valores definidos.
- Cajas degeneradas o disjuntas: IoU 0 y sin emparejamiento.
- Predicciones duplicadas: una predicción no se reutiliza para dos objetos.
- Clases distintas con cajas solapadas: no se emparejan entre sí.
- TP, FP o FN en cero: precision/recall/F1 no dividen por cero.
- AP con un solo punto o con recalls repetidos: el resultado es estable.
- `NaN` o infinito: el contrato de métricas los rechaza.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La suite MUST usar casos sintéticos pequeños, deterministas y legibles.
- **FR-002**: Cada caso MUST declarar el valor esperado y la tolerancia numérica.
- **FR-003**: La suite MUST cubrir IoU, emparejamiento, precision/recall/F1, AP y mAP.
- **FR-004**: La suite MUST incluir al menos un escenario compuesto por clase con
  TP, FP y FN.
- **FR-005**: La suite MUST ejecutarse sin `ultralytics`, GPU, dataset ni red.
- **FR-006**: La suite MUST fallar si un valor se desvía más allá de la tolerancia.
- **FR-007**: No se modifica el código de `metrics.py` en esta HU; las pruebas son el
  entregable.

### Key Entities

- **Caso dorado**: cajas, etiquetas, predicciones y resultados esperados.
- **Tolerancia**: diferencia absoluta máxima aceptada por `pytest.approx`.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Casos dorados | `tests/test_metrics_golden.py` |
| AC-02 Tolerancia explícita | Constante `TOL` y aserciones con `pytest.approx(..., abs=TOL)` |
| AC-03 Sin GPU/dataset/red | Imports solo de `ppe_detection.evaluation.metrics` y stdlib |

## Success Criteria *(mandatory)*

- **SC-001**: La suite pasa en `make check` sin extras de inferencia.
- **SC-002**: Un cambio en una fórmula de métricas produce al menos un fallo.
- **SC-003**: Los casos se entienden sin abrir el dataset ni el modelo.
- **SC-004**: La suite añade 8 pruebas al inventario.

## Out of Scope

- Cambiar `metrics.py` o `evaluate.py`.
- Evaluar el modelo real o descargar el dataset.
- Calibrar umbrales o analizar FP/FN (HU-029/HU-030).
- Medir latencia o rendimiento.

## Assumptions

- Las funciones de `metrics.py` son la fuente de verdad del cálculo.
- Los valores dorados se calculan a mano y se documentan en el test.
- La tolerancia `1e-12` es suficiente para operaciones de punto flotante y
  suficientemente estricta para detectar una regresión real.
