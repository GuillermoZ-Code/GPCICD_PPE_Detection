# Feature Specification: HU-032 — Robustez ante luz, ruido y escala

**Feature Branch**: `feature/033-hu-032-robustez`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #88 — «HU-032 — Prueba de robustez ante luz, ruido y escala».
Épica `ep-09`, P2, ola 3, 1 SP, 4 pruebas objetivo. Depende de HU-019, ya cerrada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Medir la caída ante perturbaciones (Priority: P2)

Como evaluador del modelo, quiero medir la caída de desempeño ante brillo, ruido y
escala, para documentar en qué condiciones falla el detector.

**Why this priority**: una métrica global sobre imágenes limpias no dice si el
detector resiste poca luz o sensores ruidosos. La tabla permite explicar el riesgo
operativo con evidencia.

**Independent Test**: con imágenes sintéticas se verifica que las perturbaciones son
deterministas; con la muestra fija de test se obtiene la tabla de mAP.

**Acceptance Scenarios** (AC de la issue #88):

1. **AC-01**: **Dada** una imagen RGB, **Cuando** se aplica brillo, ruido o escala,
   **Entonces** la transformación es determinista y usa una semilla fija cuando
   corresponde.
2. **AC-02**: **Dada** la muestra de test, **Cuando** se evalúan las variantes,
   **Entonces** existe una tabla de mAP por perturbación.
3. **AC-03**: **Dadas** las funciones de perturbación, **Cuando** corren las pruebas,
   **Entonces** no requieren YOLO, GPU ni dataset.

### Edge Cases

- Factor de brillo 0: imagen negra; factor alto: recorte a 255.
- Ruido con sigma 0: imagen sin cambios; misma semilla: mismo resultado.
- Escala que redondea a 0 píxeles: se fuerza a 1 × 1.
- Imagen vacía, sin tres canales o que no sea `uint8`: error explícito.
- Semilla negativa o no entera: error explícito.
- Objetos que quedan fuera de la imagen al reducir: se conservan las cajas
  normalizadas y la evaluación de YOLO las recorta.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `adjust_brightness()` MUST multiplicar por un factor finito ≥ 0 y
  recortar a `[0, 255]`.
- **FR-002**: `add_gaussian_noise()` MUST usar `numpy.random.default_rng(seed)` y ser
  reproducible con la misma semilla.
- **FR-003**: `resize_scale()` MUST devolver una imagen RGB `uint8` con dimensiones
  proporcionales y al menos 1 × 1.
- **FR-004**: `apply_perturbation()` MUST aceptar `clean`, `brightness`, `noise` y
  `scale`, y rechazar cualquier otro nombre.
- **FR-005**: Las funciones MUST validar forma, tipo y parámetros antes de operar.
- **FR-006**: El informe MUST declarar modelo, SHA256, muestra, semilla e intensidades.
- **FR-007**: No se MUST publicar imágenes ni datos personales.
- **FR-008**: Las pruebas MUST ser puras y no cargar YOLO.

### Key Entities

- **ImageArray**: imagen RGB `uint8` con forma `(H, W, 3)`.
- **Perturbación**: `clean`, `brightness`, `noise`, `scale`.
- **Tabla de robustez**: mAP@0.5 y mAP@0.5:0.95 por variante.
- **Informe**: `docs/evaluation/robustez.md`.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 Perturbaciones deterministas | `tests/test_robustness.py::test_brightness_is_deterministic_and_clipped`, `tests/test_robustness.py::test_gaussian_noise_is_reproducible_with_the_same_seed`, `tests/test_robustness.py::test_apply_perturbation_covers_the_canonical_names` |
| AC-02 Tabla de mAP | `docs/evaluation/robustez.md` |
| AC-03 Funciones puras con pruebas | `tests/test_robustness.py::test_resize_scale_changes_dimensions_and_preserves_channels`, `tests/test_robustness.py::test_invalid_perturbation_parameters_are_rejected` |

## Success Criteria *(mandatory)*

- **SC-001**: Las cuatro variantes se aplican de forma determinista.
- **SC-002**: La tabla reporta mAP@0.5 y mAP@0.5:0.95 para las cuatro variantes.
- **SC-003**: Las pruebas corren sin GPU, dataset ni red.
- **SC-004**: El informe declara la muestra de 100 imágenes y sus limitaciones.
- **SC-005**: `make check` y `uv build` quedan en verde.

## Out of Scope

- Reentrenar el modelo o hacer aumento de datos.
- Simular cámaras reales, lluvia, polvo o movimiento.
- Cambiar el contrato del detector.
- Publicar las imágenes perturbadas.

## Assumptions

- La entrada es una imagen RGB `uint8` con tres canales.
- La semilla por defecto es 42 y se puede cambiar.
- La muestra fija son las primeras 100 imágenes de test ordenadas por nombre.
- Las cajas de YOLO están normalizadas; al cambiar la resolución no se reescalan.
- Los pesos y el dataset están fuera de Git.
