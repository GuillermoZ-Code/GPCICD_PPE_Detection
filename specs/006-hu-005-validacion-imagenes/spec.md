# Feature Specification: HU-005 — Validar las imágenes recibidas

**Feature Branch**: `feature/006-hu-005-validacion-imagenes`

**Created**: 2026-11-10

**Status**: Implementada (PR pendiente)

**Input**: Issue #5 — «Validar las imágenes recibidas». Asignada a Hernán
(EP-01, Must Have, M3-S1). Depende de HU-001 (cerrada).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Rechazar una entrada inválida sin ejecutar el detector (Priority: P1)

Como usuario del sistema, quiero recibir un mensaje comprensible cuando la imagen no
pueda procesarse, para corregir la entrada sin provocar un fallo de la aplicación.

**Why this priority**: la API (HU-006) y la interfaz (HU-007) necesitan una validación
común; sin ella, un archivo corrupto o vacío llegaría al detector o tumbaría el
servicio.

**Independent Test**: con `validate_image_bytes` se rechazan bytes vacíos, corruptos,
de formato no admitido y de más de 10 MB sin cargar ni invocar el detector; un PNG o
JPEG válido devuelve `ImageData` listo para el preprocesamiento.

**Acceptance Scenarios** (AC de la issue #5):

1. **AC-01**: **Dado** un archivo corrupto o que no es JPEG/PNG, **Cuando** se valida,
   **Entonces** se rechaza con un mensaje comprensible, **Y** el detector no se
   ejecuta.
2. **AC-02**: **Dado** un archivo vacío, **Cuando** se valida, **Entonces** se rechaza
   con un mensaje comprensible, **Y** el sistema sigue operativo.
3. **AC-03**: **Dada** una imagen JPEG/PNG válida, **Cuando** se valida, **Entonces**
   se acepta y se entrega como `ImageData` al preprocesamiento.

### Edge Cases

- Archivo de exactamente 10 MB: se acepta si decodifica; más de 10 MB se rechaza.
- Extensión `.jpg` con contenido PNG: manda el contenido, no la extensión.
- GIF, BMP, WebP o bytes arbitrarios: se rechazan con «Formato no admitido».
- JPEG truncado con cabecera válida: se rechaza al no poder decodificar.
- Archivo vacío de 0 bytes: se rechaza antes de intentar decodificar.
- Imagen con dimensiones enormes: OpenCV decide si puede decodificarla; el límite de
  tamaño de entrada evita cargas desproporcionadas.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST exponer `validate_image_bytes(data, source="upload")`
  que devuelva `ImageData` o lance `InvalidImageError` con un mensaje en español.
- **FR-002**: La validación MUST rechazar bytes vacíos, formatos distintos de JPEG/PNG
  (detectados por contenido) y archivos mayores de **10 MB**.
- **FR-003**: La validación MUST ocurrir antes de cualquier llamada al detector; el
  módulo de validación no importa ni instancia `YoloDetector`.
- **FR-004**: `load_image` y `load_image_bytes` MUST aplicar las mismas reglas de
  tamaño y formato que la entrada de la API.
- **FR-005**: El límite MUST ser una constante pública (`MAX_IMAGE_BYTES`) alineada
  con el frontend (`MAX_BYTES = 10 MB`).
- **FR-006**: No se añaden dependencias nuevas; se reutilizan `numpy`, `opencv` y el
  contrato `ImageData`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: AC-01, AC-02 y AC-03 tienen al menos una prueba pytest que los
  referencia por nombre o docstring.
- **SC-002**: `make check` pasa sin GPU, sin dataset y sin red.
- **SC-003**: Un archivo rechazado nunca llega a `detect()`; la prueba lo verifica con
  un detector espía.
- **SC-004**: La API (HU-006) puede mapear `InvalidImageError` a un error de cliente
  4xx sin cambios adicionales.

## Out of Scope

- Endpoint HTTP y códigos de estado (HU-006).
- Validación en el navegador (ya existe en HU-007).
- Redimensionado o normalización numérica (TA-02).
- Detección de contenido inseguro o moderación de imágenes.
