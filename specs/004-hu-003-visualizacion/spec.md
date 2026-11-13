# Feature Specification: HU-003 — Visualizar las detecciones sobre la imagen

**Feature Branch**: `feature/004-hu-003-visualizacion`

**Created**: 2026-11-09

**Status**: Fusionada (PR #33)

**Input**: Issue #3 — "Visualizar las detecciones sobre la imagen".

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ver las detecciones sobre la imagen (Priority: P1)

Como usuario del sistema, quiero visualizar en la imagen la ubicación y categoría de los
elementos detectados, para interpretar fácilmente los resultados del análisis.

**Why this priority**: una lista de coordenadas no le sirve al usuario final; la imagen
anotada es la forma natural de leer el resultado y la base de la interfaz (HU-007).

**Independent Test**: con una imagen sintética y detecciones conocidas se obtiene una
imagen anotada cuyas cajas caen en los píxeles esperados, sin GPU, sin dataset y sin red.

**Acceptance Scenarios**:

1. **Given** una imagen y una colección de detecciones válidas, **When** se genera la
   visualización, **Then** cada detección se representa con una caja delimitadora y se
   identifica con su categoría y confianza.
2. **Given** las coordenadas de una detección y las dimensiones originales de la imagen,
   **When** se dibuja su caja, **Then** se usa la transformación espacial definida y la
   caja aparece sobre la región correspondiente.
3. **Given** una respuesta válida sin detecciones, **When** se genera la visualización,
   **Then** no se dibujan cajas inexistentes y la imagen se presenta sin anotaciones.

### Edge Cases

- Lista de detecciones vacía.
- Lienzo de distinto tamaño que la imagen de la detección (previsualización reducida).
- Caja de menos de un píxel que al redondear podría colapsar.
- Etiqueta que no cabe encima de la caja: se dibuja dentro.
- Imagen de 1×1 píxeles.
- Clase fuera del catálogo: se muestra el nombre canónico como respaldo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `draw_detections(image, detections)` MUST devolver una `ImageData` nueva y
  MUST NOT mutar la imagen de entrada.
- **FR-002**: Cada detección MUST dibujarse con una caja y una etiqueta que contenga la
  categoría legible y la confianza.
- **FR-003**: La transformación espacial MUST ser la identidad cuando el lienzo coincide
  con `image_width`/`image_height` de la detección, y proporcional cuando difiere.
- **FR-004**: Sin detecciones MUST devolver la imagen sin ninguna anotación.
- **FR-005**: El grosor de línea y el tamaño de fuente MUST escalar con el lado mayor de
  la imagen, para que la anotación se lea igual a 640 px y a 3264 px.
- **FR-006**: MUST funcionar sin GPU, sin dataset, sin pesos y sin red.
- **FR-007**: La CLI de inferencia MUST poder guardar las imágenes anotadas con
  `--annotated`, en `<salida>/annotated/`.
- **FR-008**: Las etiquetas visibles MUST usar nombres legibles en español; el contrato
  conserva los nombres canónicos del `data.yaml`.

### Key Entities

- **ImageData**: imagen RGB validada (HU-001).
- **Detection**: clase, confianza y `bbox` `xyxy` en píxeles de la imagen original
  (contrato TA-11).
- **DISPLAY_NAMES**: mapa de nombre canónico a etiqueta legible.

## Acceptance → Test

| AC | Prueba pytest |
|----|----------------|
| AC-003.1 Caja, categoría y confianza | `tests/test_overlay.py::test_draws_box_at_expected_pixels` y `::test_format_label` |
| AC-003.2 Transformación espacial | `tests/test_overlay.py::test_scales_when_canvas_differs` |
| AC-003.3 Sin detecciones | `tests/test_overlay.py::test_empty_detections_return_unchanged_image` |
| FR-001 No muta la entrada | `tests/test_overlay.py::test_does_not_modify_input` |
| FR-007 CLI `--annotated` | `tests/test_predict.py::test_run_saves_annotated_images` |
| Guardado de imagen | `tests/test_image_loader.py::test_write_image_roundtrip` |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `make check` pasa en verde.
- **SC-002**: 100 % de las pruebas corren sin GPU, dataset, pesos ni red.
- **SC-003**: Cada AC de la issue #3 tiene al menos una prueba que lo referencia.

## Assumptions

- Los `bbox` del contrato ya vienen en píxeles de la imagen original: `YoloDetector`
  recorta y conserva `image_width`/`image_height`, así que no hay que reescalar desde el
  tamaño de entrada del modelo.
- El dibujo usa OpenCV sobre una copia en BGR y devuelve el resultado en RGB.
- La traducción de etiquetas vive en el módulo de visualización; el contrato no cambia.
- No se dibujan advertencias de cumplimiento ni alertas: eso está fuera del alcance.
