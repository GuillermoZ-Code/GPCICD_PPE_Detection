# Feature Specification: HU-021 — Adaptar el detector a YOLO26

**Feature Branch**: `feature/022-hu-021-detector-nms-free`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #77 — «Adaptar el detector a YOLO26 (modo NMS y end-to-end)».
Asignada a Hernán (`HestradaUAO`), épica `ep-09`, P0, Ola 3, 3 SP, 12 pruebas
objetivo. Depende de HU-016, ya fusionada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cambiar de modelo sin cambiar el contrato (Priority: P0)

Como desarrollador integrador, quiero que `YoloDetector` soporte YOLO11 y YOLO26 sin
cambiar el contrato `list[Detection]`, para cambiar de modelo solo con configuración.

**Why this priority**: YOLO26n ya demostró mejor calidad y latencia ONNX. Falta que el
adaptador use su salida NMS-free/end-to-end sin romper REST, gRPC ni la SPA.

**Independent Test**: inyectar un modelo falso con la misma salida que YOLO11 y otro
con salida YOLO26; ambos deben producir `Detection` equivalentes. El detector debe
poder pedir `nms=False` para el modo end-to-end y exponer la versión inferida del
artefacto.

**Acceptance Scenarios** (AC de la issue #77):

1. **AC-01**: **Dados** YOLO11 y YOLO26, **Cuando** se ejecutan, **Entonces**
   `YoloDetector` produce las mismas clases, orden y `bbox xyxy`.
2. **AC-02**: **Dado** un artefacto, **Cuando** se construye la identidad, **Entonces**
   la versión se infiere del artefacto y se expone en `/health`.
3. **AC-03**: **Dados** los dos formatos de salida, **Cuando** se ejecutan las
   pruebas, **Entonces** un detector simulado cubre ambos.

### Edge Cases

- `nms=None`: se conserva el comportamiento actual y no se envía el argumento.
- `nms=False`: modo NMS-free/end-to-end de YOLO26.
- `nms=True`: NMS embebido, si el backend lo soporta.
- Modelo con catálogo distinto: se rechaza antes de inferir.
- Cajas fuera de imagen: se recortan; cajas degeneradas se descartan.
- Versión explícita `PPE_MODEL_VERSION`: prevalece sobre el nombre del artefacto.
- Artefacto `best.pt`: la versión es `best`; si el manifiesto no se usa, no se
  inventa una versión.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `YoloDetector` MUST aceptar `nms: bool | None` y pasarlo a
  `predict()` solo cuando no sea `None`.
- **FR-002**: `detect()` MUST mantener el contrato `list[Detection]` y el catálogo de
  seis clases.
- **FR-003**: MUST soportar la salida `Results.boxes` de YOLO11 y YOLO26.
- **FR-004**: MUST exponer `model_version` inferido del nombre del artefacto.
- **FR-005**: `default_model_version()` MUST preferir el artefacto sobre el manifiesto
  cuando `PPE_MODEL_PATH` está definido y no hay versión explícita.
- **FR-006**: `/health` MUST reportar la versión inferida del artefacto.
- **FR-007**: Las pruebas MUST cubrir `nms=None/False`, equivalencia YOLO11/YOLO26 y
  versión inferida.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Equivalencia | `test_yolo11_and_yolo26_outputs_are_equivalent` |
| AC-02 Versión en /health | `test_default_model_version_infers_from_artifact`, `test_health_uses_artifact_version` |
| AC-03 Formatos simulados | `test_yolo26_nms_free_passes_nms_false`, `test_default_detector_omits_nms` |
| FR-004 Propiedad | `test_detector_exposes_model_version` |

## Success Criteria *(mandatory)*

- **SC-001**: El detector acepta un modelo YOLO26 con el mismo contrato.
- **SC-002**: `/health` identifica la versión del artefacto, no una versión fija.
- **SC-003**: `nms=False` se pasa solo cuando se solicita.
- **SC-004**: `make check` pasa sin GPU, dataset ni red.

## Out of Scope

- Cambiar `models.lock` al modelo YOLO26.
- Entrenar o evaluar modelos.
- Exportar ONNX o cambiar el backend (HU-022).
- Modificar la API o la SPA.
- Decidir el modelo productivo (HU-023).

## Assumptions

- YOLO26 usa la misma estructura `Results.boxes` que YOLO11.
- El modo end-to-end se activa con `nms=False` en Ultralytics.
- Los tests usan modelos falsos, no pesos reales.
