# Feature Specification: HU-019 — Comparación YOLO26 vs YOLO11s

**Feature Branch**: `feature/020-hu-019-comparar-yolo26-yolo11`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #75 — «Evaluación comparativa YOLO26 vs. YOLO11s». Asignada a Hernán
(`HestradaUAO`), épica `ep-09`, P0, Ola 3, 3 SP. Depende de HU-018.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Decidir con datos (Priority: P0)

Como evaluador del modelo, quiero comparar YOLO26 y YOLO11s en el mismo conjunto de
evaluación, para sustentar con datos si YOLO26 mejora el detector y si conviene
adoptarlo.

**Why this priority**: el benchmark de latencia y el entrenamiento ya existen, pero
falta una comparación formal que separe la mejora real de los artefactos de las
diferencias de partición.

**Independent Test**: leer los resúmenes de evaluación de ambos modelos, verificar que
usaron el mismo `conf`, `iou`, `imgsz` y semilla, y reproducir las tablas global y por
clase.

**Acceptance Scenarios** (AC de la issue #75):

1. **AC-01**: **Dados** los resúmenes, **Cuando** se comparan, **Entonces** hay tabla
   global y por clase con P, R, mAP50 y mAP50-95 sobre el eval de 492.
2. **AC-02**: **Dados** ambos modelos, **Cuando** se comparan, **Entonces** usan el
   mismo `conf`, `iou`, `imgsz` y semilla.
3. **AC-03**: **Dado** el informe, **Cuando** se revisa, **Entonces** está en
   `docs/evaluation/YOLO26.md` y es reproducible desde los resúmenes generados por
   código.

### Edge Cases

- El eval de 492 tiene solo 6 objetos de `safety_shoe`; no se usa como única prueba.
- El test de 1.095 es la referencia de calidad; se incluye como evidencia
  complementaria.
- `best.pt` con nombre `best` no aporta versión semántica; se usa el SHA256.
- Diferencias de versión de Ultralytics entre entrenamiento y evaluación se declaran.
- Si los YAML de evaluación tienen rutas distintas, se comparan las particiones por
  conteo y nombres de clase.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: MUST comparar YOLO11s y YOLO26n con el mismo `conf`, `iou`, `imgsz` y
  semilla.
- **FR-002**: MUST incluir tabla global y por clase del eval de 492.
- **FR-003**: MUST incluir el test completo de 1.095 como evidencia complementaria.
- **FR-004**: MUST registrar los SHA256 de ambos modelos.
- **FR-005**: MUST explicar la debilidad de `safety_shoe` en el eval de 492.
- **FR-006**: MUST emitir una recomendación preliminar y las condiciones para adoptar
  YOLO26.
- **FR-007**: MUST NOT versionar pesos ni imágenes.
- **FR-008**: MUST dejar la decisión final al ADR 0009 (HU-023).

## Acceptance → Evidence

| AC | Evidencia |
|----|-----------|
| AC-01 Tabla 492 | `docs/evaluation/YOLO26.md` §4 |
| AC-02 Misma configuración | §3 del informe |
| AC-03 Reproducibilidad | §7 y comandos de evaluación |

## Success Criteria *(mandatory)*

- **SC-001**: La comparación distingue eval 492 y test 1.095.
- **SC-002**: La recomendación no oculta la debilidad de `safety_shoe`.
- **SC-003**: Los SHA256 identifican ambos artefactos.
- **SC-004**: No se versionan pesos ni imágenes.

## Out of Scope

- Entrenar YOLO26s.
- Cambiar `models.lock` o el modelo productivo.
- Calibrar umbrales (HU-029).
- Exportar ONNX (HU-022).
- Redactar el ADR final (HU-023).

## Assumptions

- Los resúmenes de YOLO11s (HU-008) y YOLO26n (HU-018) existen y son comparables.
- La configuración de evaluación es `imgsz=640`, `conf=0.001`, `iou=0.7`, `seed=42`.
- El eval de 492 es histórico; el test de 1.095 es la referencia de calidad.
