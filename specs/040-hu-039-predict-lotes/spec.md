# Feature Specification: HU-039 — Inferencia por lotes desde CLI

**Feature Branch**: `feature/040-hu-039-predict-lotes`

**Created**: 2026-11-26

**Status**: En implementación

**Input**: Issue #95 — «Inferencia por lotes desde CLI». Asignada a Hernán
(`HestradaUAO`), épica `ep-09`, P2, ola 3, 1 SP, 4 pruebas objetivo. Sin dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Procesar una carpeta sin interfaz (Priority: P2)

Como evaluador técnico, quiero procesar una carpeta de imágenes y obtener un JSON por
imagen, para evaluar casos sin abrir la SPA.

**Why this priority**: la CLI ya procesa carpetas y escribe un CSV global, pero falta
un resultado por imagen que conserve la identidad del modelo y los parámetros de la
corrida.

**Independent Test**: con un detector simulado y una carpeta temporal se ejecuta la
CLI con `--dir` y se comprueban los JSON por imagen.

**Acceptance Scenarios** (AC de la issue #95):

1. **AC-01**: **Dada** una carpeta, **Cuando** se ejecuta
   `python -m ppe_detection.detection.predict --dir`, **Entonces** se genera un JSON
   por imagen.
2. **AC-02**: **Dado** un JSON, **Cuando** se inspecciona, **Entonces** registra la
   versión del modelo, `imgsz` y los umbrales.
3. **AC-03**: **Dado** un detector simulado, **Cuando** corre la suite, **Entonces**
   no se carga Ultralytics ni se necesita GPU.

### Edge Cases

- `--source` y `--dir` son alias mutuamente excluyentes; falta uno: error de argparse.
- Carpeta sin imágenes: la CLI falla con un mensaje claro.
- Detector vacío: el JSON contiene `detections: []` y el mensaje de HU-004.
- Dos imágenes con el mismo nombre base y extensión distinta: los JSON usan el
  nombre completo (`a.png.json`, `a.jpg.json`) y no colisionan.
- Imagen individual con `--source`: también genera su JSON.
- La salida CSV y el manifiesto existentes se conservan.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `--dir` MUST ser alias de entrada por carpeta y excluirse con `--source`.
- **FR-002**: Por cada imagen se MUST escribir `<salida>/json/<nombre-completo>.json`.
- **FR-003**: El JSON MUST incluir imagen, dimensiones, modelo (`path`, `version`,
  `sha256`), parámetros (`conf`, `iou`, `imgsz`, `device`, `seed`) y detecciones.
- **FR-004**: El JSON MUST incluir el mensaje vacío de HU-004 cuando no hay detecciones.
- **FR-005**: La corrida MUST conservar el CSV y el manifiesto existentes.
- **FR-006**: Las pruebas MUST usar un detector simulado, sin Ultralytics.
- **FR-007**: No se modifica el contrato `ImageData → list[Detection]`.
- **FR-008**: No se agregan dependencias.

### Key Entities

- **Predicción por imagen**: JSON con identidad, parámetros y detecciones.
- **Manifiesto de corrida**: resumen global existente.
- **Detector simulado**: implementación inyectada para pruebas.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 `--dir` y JSON por imagen | `tests/test_predict_batch.py::test_parse_args_accepts_dir_alias`, `tests/test_predict_batch.py::test_run_writes_one_json_per_image` |
| AC-02 Identidad y parámetros | `tests/test_predict_batch.py::test_image_json_records_identity_and_parameters` |
| AC-03 Detector simulado | `tests/test_predict_batch.py::test_run_json_handles_empty_detections`, `tests/test_predict.py` |

## Success Criteria *(mandatory)*

- **SC-001**: La CLI procesa una carpeta y deja un JSON por imagen.
- **SC-002**: Cada JSON conserva modelo, `imgsz` y umbrales.
- **SC-003**: El CSV y el manifiesto anteriores siguen funcionando.
- **SC-004**: La HU añade al menos 4 pruebas al inventario.

## Out of Scope

- Cambiar el detector, el contrato o el formato del CSV.
- Procesar video, RTSP o streaming.
- Añadir autenticación a la CLI.
- Cambiar el modelo productivo.

## Assumptions

- La CLI existente procesa imágenes JPEG/PNG.
- `args.model` es un artefacto local verificable por SHA256.
- La salida JSON es un artefacto de evaluación, no de producción.
- No se publican imágenes.
