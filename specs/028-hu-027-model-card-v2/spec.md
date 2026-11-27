# Feature Specification: HU-027 — Model Card v2 con YOLO26, sesgos y limitaciones

**Feature Branch**: `feature/028-hu-027-model-card-v2`

**Created**: 2026-11-26

**Status**: En implementación

**Input**: Issue #83 — «Model Card v2 con YOLO26, sesgos y limitaciones». Asignada a
Hernán (`HestradaUAO`), épica `ep-15`, P1, ola 2, 2 SP, 8 pruebas objetivo. Depende de
HU-023, ya cerrada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Entender el modelo y sus límites (Priority: P1)

Como usuario técnico, quiero una Model Card actualizada con el modelo seleccionado, su
comparación, sus sesgos y la licencia, para saber qué puedo esperar y qué no.

**Why this priority**: el modelo cambió de YOLO11s a YOLO26n. Una ficha antigua
induciría a error sobre el artefacto, las métricas y el uso responsable.

**Independent Test**: leer `docs/model-card.md` y verificar la selección, la
comparación, los sesgos, los enlaces y la licencia.

**Acceptance Scenarios** (AC de la issue #83):

1. **AC-01**: **Dada** la ficha, **Cuando** se revisa, **Entonces** incluye la
   comparación YOLO11s/YOLO26n y la decisión del ADR 0009.
2. **AC-02**: **Dado** el análisis de sesgos, **Cuando** se revisa, **Entonces**
   documenta `safety_shoe`, `Gloves` y el uso no apto.
3. **AC-03**: **Dada** la ficha, **Cuando** se revisa, **Entonces** enlaza
   `models.lock`, MLflow y el informe de evaluación.

### Edge Cases

- El modelo seleccionado no es el desplegado todavía: se declara el estado del rollout.
- Las métricas del eval 492 no son concluyentes: se enlaza el test de 1.095.
- La ficha no debe afirmar cumplimiento normativo.
- La licencia del código y del modelo es AGPL; el dataset es CC-BY.
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

- **FR-001**: La ficha MUST declarar YOLO26n como modelo seleccionado y el ADR 0009.
- **FR-002**: MUST incluir la comparación de mAP con YOLO11s.
- **FR-003**: MUST documentar `safety_shoe` y `Gloves` como clases débiles.
- **FR-004**: MUST declarar el uso no previsto y la ausencia de certificación.
- **FR-005**: MUST enlazar `models.lock`, `YOLO26.md`, errores, MLflow y comparación.
- **FR-006**: MUST declarar AGPL-3.0-only y las seis clases.
- **FR-007**: No se modifica el modelo ni sus métricas.
- **FR-008**: No se agregan dependencias.

### Key Entities

- **Model Card**: `docs/model-card.md`.
- **Modelo seleccionado**: YOLO26n, SHA256 y artefacto.
- **Sesgos**: `safety_shoe`, `Gloves`, dominio y representatividad.
- **Enlaces**: manifiesto, evaluación, MLflow y licencia.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 YOLO26n y comparación | `tests/test_model_card_v2.py::test_model_card_selects_yolo26n_and_adr`, `tests/test_model_card_v2.py::test_model_card_includes_yolo11s_comparison` |
| AC-02 Sesgos y uso no apto | `tests/test_model_card_v2.py::test_model_card_documents_safety_shoe_bias`, `tests/test_model_card_v2.py::test_model_card_documents_gloves_bias`, `tests/test_model_card_v2.py::test_model_card_declares_non_compliance_use` |
| AC-03 Enlaces | `tests/test_model_card_v2.py::test_model_card_links_manifest_and_evaluation`, `tests/test_model_card_v2.py::test_model_card_links_mlflow`, `tests/test_model_card_v2.py::test_model_card_declares_license_and_six_classes` |

## Success Criteria *(mandatory)*

- **SC-001**: La ficha identifica el modelo seleccionado y el desplegado.
- **SC-002**: Las métricas y los sesgos se explican sin abrir el informe.
- **SC-003**: Los enlaces a manifiesto, MLflow y evaluación resuelven.
- **SC-004**: La HU añade al menos 8 pruebas al inventario.

## Out of Scope

- Reentrenar o recalibrar el modelo.
- Cambiar `models.lock` o el artefacto.
- Publicar imágenes o datos personales.
- Modificar la licencia AGPL.

## Assumptions

- El ADR 0009 y HU-019 son la fuente de la comparación.
- El artefacto seleccionado es YOLO26n con SHA256 `FEFB1F1A…`.
- El servicio sigue en YOLO11s hasta el rollout.
- Las métricas se calcularon con `docs/evaluation/YOLO26.md`.
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
