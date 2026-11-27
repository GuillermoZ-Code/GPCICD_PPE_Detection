# Feature Specification: HU-027 — Model Card v2 con YOLO26, sesgos y limitaciones

**Feature Branch**: `docs/m4-plan-real`

**Created**: 2026-11-27

**Status**: Implementado (spec de cierre)

**Input**: Issue #83 — «HU-027 — Model Card v2 con YOLO26, sesgos y limitaciones».
Épica `ep-15`, 2 SP. Dueño: Hernán (`HestradaUAO`).

> Spec escrita al cerrar la HU: la Model Card se entregó en `docs/model-card.md` y la
> issue se cerró sin el directorio de spec, lo que dejó en rojo la compuerta de
> trazabilidad (`make trazabilidad-check`). Este documento registra los AC y su
> evidencia para que la HU quede trazable.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Saber qué hace el modelo y dónde falla (Priority: P0)

Como evaluador y como usuario del sistema, quiero una Model Card que declare el modelo
seleccionado, su comparación con la alternativa, sus sesgos por clase y el uso para el
que **no** sirve, para no atribuirle garantías que no tiene.

**Why this priority**: la rúbrica del M4 pide documentar el modelo y sus límites; además
la licencia AGPL y el dataset CC-BY obligan a declarar procedencia y restricciones.

**Independent Test**: `docs/model-card.md` incluye la comparación YOLO11s/YOLO26, los
sesgos de `safety_shoe` y `Gloves`, y los enlaces a `models.lock`, MLflow y el informe
de evaluación.

**Acceptance Scenarios** (AC de la issue #83):

1. **AC-01**: **Dado** el documento, **Cuando** se lee, **Entonces** compara YOLO11s y
   YOLO26 y cita la decisión del ADR 0009.
2. **AC-02**: **Dado** el documento, **Cuando** se lee la sección de limitaciones,
   **Entonces** documenta los sesgos de `safety_shoe` y `Gloves` y el uso no apto.
3. **AC-03**: **Dado** el documento, **Cuando** se buscan las referencias, **Entonces**
   enlaza `models.lock`, MLflow y el informe de evaluación.

### Edge Cases

- **Modelo seleccionado pero no desplegado**: la tarjeta distingue YOLO26n (seleccionado)
  de YOLO11s (desplegado hasta el rollout).
- **Clase con pocos objetos**: advierte que las métricas minoritarias no son
  representativas.
- **Uso pretendido fuera de alcance**: declara que no certifica cumplimiento normativo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La tarjeta MUST declarar el modelo seleccionado y su versión.
- **FR-002**: La tarjeta MUST comparar YOLO11s y YOLO26 con métricas del test completo.
- **FR-003**: La tarjeta MUST documentar los sesgos por clase y el uso no apto.
- **FR-004**: La tarjeta MUST enlazar `models.lock`, MLflow y el informe de evaluación.
- **FR-005**: La sección de comparación MUST citar el ADR 0009.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `docs/model-card.md` contiene las tres comparaciones y los tres enlaces.
- **SC-002**: `tests/test_model_card_v2.py` verifica AC-01 a AC-03 sin red.
- **SC-003**: `make trazabilidad-check` pasa para HU-027.

## Assumptions

- El modelo seleccionado es YOLO26n y el desplegado sigue siendo YOLO11s (ADR 0009).
- Las métricas provienen de `docs/evaluation/YOLO26.md`, no se escriben a mano.
