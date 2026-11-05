# Feature Specification: HU-001 — Cargar una imagen para su análisis

**Feature Branch**: `feature/002-hu-001-carga-imagen`

**Created**: 2026-11-04

**Status**: Draft

**Input**: Issue #1 — “Cargar una imagen para su análisis”.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cargar una imagen válida (Priority: P1)

Como usuario del sistema de detección de EPP, quiero proporcionar una imagen digital
para que pueda ser analizada por el modelo.

**Why this priority**: es la entrada de todo el pipeline; sin una imagen decodificada y
validada no pueden existir HU-002, HU-005 ni la API.

**Independent Test**: se puede cargar un JPEG/PNG sintético, obtener un `ImageData`
con dimensiones verificables y comprobar que no se ejecutó inferencia, sin GPU, sin
dataset y sin red.

**Acceptance Scenarios**:

1. **Given** un archivo JPEG o PNG válido, **When** se carga, **Then** se decodifica a
   un arreglo `uint8 HxWx3` en RGB y se entrega al preprocesamiento.
2. **Given** una imagen válida, **When** se construye el `ImageData`, **Then** el ancho
   y el alto originales se conservan como metadatos.
3. **Given** una carga válida, **When** termina, **Then** no se ejecuta inferencia y el
   resultado cumple el contrato de datos.

### Edge Cases

- Archivo vacío (0 bytes).
- Archivo corrupto o truncado.
- Formato no admitido (GIF, BMP, TIFF, PDF).
- Ruta inexistente o directorio en lugar de archivo.
- Imagen de 1×1 píxeles.
- PNG con canal alfa o imagen en escala de grises.
- Nombre de archivo con extensión distinta al contenido real.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST cargar imágenes JPEG y PNG desde una ruta y desde bytes.
- **FR-002**: El resultado MUST ser un `ImageData` con `array` `uint8` de forma
  `(alto, ancho, 3)` en RGB, más `width`, `height`, `format` y `source`.
- **FR-003**: El sistema MUST conservar las dimensiones originales de la imagen.
- **FR-004**: El sistema MUST rechazar archivos vacíos, corruptos o de formato no
  admitido con un error tipado y comprensible, sin ejecutar el detector.
- **FR-005**: La carga MUST NOT ejecutar inferencia ni cargar pesos.
- **FR-006**: La carga MUST ser determinista y no depender de GPU, red ni dataset.

### Key Entities

- **ImageData**: imagen decodificada en RGB, dimensiones originales, formato y origen.
  Contrato compartido con HU-002, HU-005, HU-006 y HU-007.

## Acceptance → Test

| AC | Prueba pytest |
|----|----------------|
| AC-01 Imagen válida decodificada | `tests/test_image_loader.py::test_load_png_returns_rgb_image_data` |
| AC-01 Imagen válida decodificada | `tests/test_image_loader.py::test_load_jpeg_returns_rgb_image_data` |
| AC-02 Dimensiones originales | `tests/test_image_loader.py::test_preserves_original_dimensions` |
| AC-03 Sin inferencia | `tests/test_image_loader.py::test_loading_does_not_invoke_detector` |
| FR-004 Archivo vacío | `tests/test_image_loader.py::test_empty_file_is_rejected` |
| FR-004 Archivo corrupto | `tests/test_image_loader.py::test_corrupt_file_is_rejected` |
| FR-004 Formato no admitido | `tests/test_image_loader.py::test_unsupported_format_is_rejected` |
| FR-001 Bytes | `tests/test_image_loader.py::test_load_bytes_uses_source_label` |
| Contrato | `tests/test_contracts.py::test_image_data_rejects_invalid_arrays` |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `make check` pasa en verde.
- **SC-002**: 100 % de las pruebas de carga corren sin GPU, dataset, pesos ni red.
- **SC-003**: Cada AC de la issue #1 tiene al menos una prueba que lo referencia.

## Assumptions

- El contrato `ImageData` se define en `src/ppe_detection/contracts.py` como parte del
  prerrequisito TA-11 (`specs/001-ta-contract-first`), porque TA-04 aún no existe.
- La decodificación usa OpenCV headless y NumPy; las imágenes de prueba se generan
  sintéticamente en los tests.
- El formato se detecta por los bytes de cabecera, no por la extensión.
- Los nombres canónicos de las seis clases son los del `data.yaml`:
  `Gloves, Vest, goggles, helmet, mask, safety_shoe`.
