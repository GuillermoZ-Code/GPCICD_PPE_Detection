# Feature Specification: HU-002 — Detectar las seis categorías de EPP

**Feature Branch**: `feature/003-hu-002-deteccion`

**Created**: 2026-11-04

**Status**: Draft

**Input**: Issue #2 — “Detectar las seis categorías de EPP en una imagen”.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Detectar EPP con el modelo entrenado (Priority: P1)

Como usuario del sistema, quiero que el modelo identifique y localice EPP en una
imagen, para conocer qué categorías fueron detectadas y dónde.

**Why this priority**: es el núcleo del producto; sin inferencia no hay API, interfaz
ni evaluación que mostrar.

**Independent Test**: con un modelo falso inyectado, se obtiene una `list[Detection]`
con clase, caja y confianza válidas, sin GPU, sin pesos y sin red. La prueba con los
pesos reales se ejecuta solo si el artefacto local está disponible.

**Acceptance Scenarios**:

1. **Given** un modelo cargado y una `ImageData` válida, **When** se ejecuta
   `detect()`, **Then** se obtiene una lista de `Detection` sin entrenar.
2. **Given** una detección del modelo, **When** se construye, **Then** usa el catálogo
   de las seis clases del `data.yaml` y `class_id` coincide con `class_name`.
3. **Given** una caja del modelo, **When** se convierte, **Then** incluye `bbox` `xyxy`
   y `confidence` finita en `[0, 1]`, recortada a los límites de la imagen.
4. **Given** una imagen sin objetos, **When** se ejecuta el detector, **Then** devuelve
   `[]` y no un error.

### Edge Cases

- Modelo con un catálogo de clases distinto (otro orden, otras clases, 80 clases COCO).
- `class_id` fuera de 0–5.
- Caja invertida, degenerada o fuera de la imagen.
- Confianza `NaN`, `inf` o fuera de `[0, 1]`.
- Modelo sin resultados o con `boxes = None`.
- `ultralytics` no instalado.
- Pesos locales ausentes (la prueba real se omite).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST cargar un artefacto YOLO desde una ruta configurable y
  ejecutar inferencia sin entrenar.
- **FR-002**: El detector MUST exponer `detect(image: ImageData) -> list[Detection]` y
  cumplir el protocolo `Detector` del contrato.
- **FR-003**: El catálogo MUST ser el del `data.yaml`:
  `Gloves, Vest, goggles, helmet, mask, safety_shoe`.
- **FR-004**: Cada `Detection` MUST cumplir `confidence` en `[0, 1]`, `bbox` `xyxy`
  válida y dimensiones de la imagen.
- **FR-005**: El detector MUST recortar cajas al tamaño de la imagen y descartar cajas
  degeneradas.
- **FR-006**: Sin detecciones MUST devolver `[]`, no `None`.
- **FR-007**: La inferencia MUST ser reproducible: ruta del modelo, confianza, IoU,
  tamaño de entrada y dispositivo se registran en la CLI.
- **FR-008**: La CLI MUST exportar las detecciones a CSV con imagen, clase, confianza y
  coordenadas.

### Key Entities

- **YoloDetector**: adaptador del artefacto YOLO al protocolo `Detector`.
- **Detection**: clase, confianza y caja en píxeles (contrato TA-11).
- **ImageData**: entrada RGB validada (HU-001).

## Acceptance → Test

| AC | Prueba pytest |
|----|----------------|
| AC-01 Inferencia sin entrenamiento | `tests/test_yolo_detector.py::test_detector_maps_boxes_to_detections` |
| AC-02 Catálogo de seis clases | `tests/test_yolo_detector.py::test_detector_uses_canonical_catalog` |
| AC-03 Clase, coordenadas y confianza | `tests/test_yolo_detector.py::test_detector_clips_boxes_to_image` |
| AC-04 Evaluación reproducible | `docs/spikes/SPI-02-baseline-evaluacion.md` + `tests/test_predict.py` |
| FR-006 Lista vacía | `tests/test_yolo_detector.py::test_detector_returns_empty_list_without_boxes` |
| FR-008 CSV | `tests/test_predict.py::test_run_writes_detections_csv` |
| Modelo real (opcional) | `tests/test_yolo_detector.py::test_real_weights_smoke` |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `make check` pasa en verde sin `ultralytics` instalado.
- **SC-002**: La prueba con pesos reales se ejecuta localmente si el artefacto existe y
  se omite en CI sin GPU/pesos.
- **SC-003**: Cada AC de la issue #2 tiene al menos una prueba que lo referencia.

## Assumptions

- Los pesos entrenados están fuera de Git en `artifacts/models/` (yolo11s_clean o
  yolov8n_clean); HU-002 no entrena ni descarga.
- `ultralytics` se importa de forma perezosa; en producción se instala con
  `uv sync --extra inference` o `uv run --with ultralytics`.
- La evaluación cuantitativa formal (mAP, precision, recall) es HU-008; aquí se
  enlaza el baseline de SPI-02 como evidencia reproducible.
- Las imágenes de prueba sintéticas y el modelo falso no requieren GPU ni dataset.
