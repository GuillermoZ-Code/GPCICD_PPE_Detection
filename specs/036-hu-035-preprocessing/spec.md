# Feature Specification: HU-035 — Módulo de preprocesamiento con contrato numérico

**Feature Branch**: `feature/036-hu-035-preprocessing`

**Created**: 2026-11-26

**Status**: En implementación

**Input**: Issue #91 — «Módulo de preprocesamiento con contrato numérico». Asignada a
Hernán (`HestradaUAO`), épica `ep-09`, P2, ola 2, 2 SP, 8 pruebas objetivo. Sin
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Preparar imágenes sin perder coordenadas (Priority: P2)

Como desarrollador, quiero un módulo `preprocessing/` con letterbox y normalización
documentados, para preparar imágenes para el detector y recuperar las cajas en las
coordenadas originales.

**Why this priority**: el contrato de detección usa píxeles de la imagen original.
Cualquier letterbox debe declarar escala, padding y transformación inversa para no
romper las cajas.

**Independent Test**: con imágenes sintéticas rectangulares se verifica forma,
escala, padding, color, normalización y roundtrip de cajas.

**Acceptance Scenarios** (AC de la issue #91):

1. **AC-01**: **Dada** una imagen RGB uint8, **Cuando** se aplica letterbox y
   normalización, **Entonces** se conserva la relación de aspecto y el contrato
   numérico documentado.
2. **AC-02**: **Dada** una caja en el lienzo, **Cuando** se aplica la transformación
   inversa, **Entonces** vuelve a las coordenadas originales y se recorta.
3. **AC-03**: **Dadas** imágenes pequeñas o no cuadradas, **Cuando** se procesan,
   **Entonces** el padding queda centrado y `scaleup=False` no amplía.

### Edge Cases

- Imagen pequeña con `scaleup=False`: no se amplía; se rellena el lienzo.
- Imagen no cuadrada: padding centrado; escala mínima entre ejes.
- Destino no cuadrado: se respeta el orden `(alto, ancho)`.
- Imagen con dtype incorrecto o forma inválida: error explícito.
- Caja fuera del lienzo: se recorta a la imagen original.
- Normalización: `float32` en `[0,1]`, sin cambiar HWC.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `letterbox()` MUST aceptar RGB uint8 HWC y devolver una imagen del
  tamaño solicitado.
- **FR-002**: MUST conservar la relación de aspecto y centrar el padding.
- **FR-003**: MUST exponer escala, padding y dimensiones originales/destino.
- **FR-004**: `inverse_letterbox_boxes()` MUST invertir y recortar cajas xyxy.
- **FR-005**: `normalize_image()` MUST devolver float32 en `[0,1]`.
- **FR-006**: `scaleup=False` MUST impedir ampliaciones.
- **FR-007**: Las entradas inválidas MUST fallar con `PreprocessingError`.
- **FR-008**: No se agregan dependencias fuera de OpenCV/NumPy ya presentes.

### Key Entities

- **LetterboxResult**: imagen, escala, padding y dimensiones.
- **PreprocessingError**: error de entrada o parámetros.
- **Caja xyxy**: coordenadas que se invierten y recortan.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 Letterbox y normalización | `tests/test_preprocessing.py::test_letterbox_preserves_aspect_ratio_and_shape`, `tests/test_preprocessing.py::test_letterbox_uses_configured_padding_color`, `tests/test_preprocessing.py::test_normalize_image_returns_float32_in_unit_range` |
| AC-02 Transformación inversa | `tests/test_preprocessing.py::test_inverse_letterbox_restores_original_coordinates`, `tests/test_preprocessing.py::test_inverse_letterbox_clips_to_original_image` |
| AC-03 Bordes | `tests/test_preprocessing.py::test_letterbox_can_disable_scaleup`, `tests/test_preprocessing.py::test_letterbox_rejects_invalid_image`, `tests/test_preprocessing.py::test_non_square_target_centers_padding` |

## Success Criteria *(mandatory)*

- **SC-001**: La suite pasa sin GPU, dataset, red ni YOLO.
- **SC-002**: Las cajas del lienzo vuelven a la imagen original.
- **SC-003**: El padding y la escala son deterministas.
- **SC-004**: La HU añade al menos 8 pruebas al inventario.

## Out of Scope

- Modificar `YoloDetector` o el contrato de detección.
- Entrenar o calibrar el modelo.
- Cambiar las imágenes del dataset.
- Añadir dependencias de inferencia.

## Assumptions

- La imagen de entrada es RGB uint8 HWC.
- El orden de `new_shape` es `(alto, ancho)`.
- OpenCV y NumPy son dependencias base del paquete.
- Las cajas están en píxeles xyxy.
