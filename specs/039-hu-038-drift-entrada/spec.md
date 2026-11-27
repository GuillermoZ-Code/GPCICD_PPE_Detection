# Feature Specification: HU-038 — Estadísticas de entrada para deriva

**Feature Branch**: `feature/039-hu-038-drift-entrada`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #94 — «HU-038 — Estadísticas de entrada para detectar deriva».
Épica `ep-13`, P2, ola 3, 1 SP, 4 pruebas objetivo. Depende de —.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Medir la línea base de las imágenes (Priority: P2)

Como responsable técnico, quiero registrar brillo medio, tamaño y relación de aspecto
de las imágenes recibidas, para detectar deriva de datos en producción.

**Why this priority**: un cambio de cámara, resolución o iluminación puede degradar
las detecciones sin que el modelo cambie. Estos números permiten comparar lotes.

**Independent Test**: con imágenes sintéticas se verifican los cálculos; con una
muestra de test se obtiene una línea base documentada.

**Acceptance Scenarios** (AC de la issue #94):

1. **AC-01**: **Dada** una imagen RGB, **Cuando** se calculan sus estadísticas,
   **Entonces** se obtienen tamaño, relación de aspecto y brillo medio.
2. **AC-02**: **Dado** el resultado, **Cuando** se inspecciona, **Entonces** no
   contiene la imagen ni datos personales.
3. **AC-03**: **Dadas** las funciones puras, **Cuando** corren las pruebas,
   **Entonces** no requieren modelo, GPU ni dataset.

### Edge Cases

- Imagen de 1 × 1: aspecto 1,0 y estadísticas válidas.
- Imagen negra: brillo 0.
- Imagen blanca: brillo 255.
- Lote vacío: error explícito.
- Entrada que no es `ImageData`: error explícito.
- Muestra con imágenes de distinta resolución: el resumen promedia dimensiones.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `image_statistics()` MUST calcular ancho, alto, aspecto y luminancia
  media/estándar.
- **FR-002**: La luminancia MUST usar ITU-R BT.601 (0,299 R + 0,587 G + 0,114 B).
- **FR-003**: `ImageStats` MUST contener solo números; nunca el arreglo de píxeles.
- **FR-004**: `summarize_statistics()` MUST agregar un lote no vacío.
- **FR-005**: Un lote vacío o una entrada inválida MUST fallar con error explícito.
- **FR-006**: Las pruebas MUST ser puras y no cargar YOLO.
- **FR-007**: El informe MUST declarar que no se guardan imágenes ni datos personales.

### Key Entities

- **ImageStats**: width, height, aspect_ratio, brightness_mean, brightness_std.
- **StatsSummary**: count y medias/rango de un lote.
- **Informe**: `docs/evaluation/deriva.md`.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 Cálculo por imagen | `tests/test_input_stats.py::test_image_statistics_calculates_size_aspect_and_brightness`, `tests/test_input_stats.py::test_summary_aggregates_a_batch_without_images` |
| AC-02 Sin imagen almacenada | `tests/test_input_stats.py::test_image_statistics_does_not_keep_the_image`, `docs/evaluation/deriva.md` |
| AC-03 Funciones puras | `tests/test_input_stats.py::test_invalid_inputs_are_rejected` |

## Success Criteria *(mandatory)*

- **SC-001**: Las estadísticas son deterministas y documentadas.
- **SC-002**: El resumen permite comparar una muestra contra una línea base.
- **SC-003**: No se versionan imágenes ni datos personales.
- **SC-004**: `make check`, `make specs-check` y `uv build` quedan en verde.

## Out of Scope

- Detectar deriva automáticamente con un test estadístico.
- Guardar imágenes, recortes o histogramas por píxel.
- Cambiar el contrato de `ImageData`.
- Enviar estadísticas a un servicio externo.

## Assumptions

- La imagen ya pasó por `load_image()` y es RGB `uint8`.
- El brillo es una media global de luminancia.
- La muestra fija son las primeras 100 imágenes de test ordenadas por nombre.
- Los datos personales no se procesan ni se registran.
