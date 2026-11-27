# Tasks: HU-032 — Robustez ante luz, ruido y escala

**Input**: `specs/033-hu-032-robustez/spec.md` y `plan.md`.

**Prerequisites**: issue #88, `develop` actualizado, HU-019 cerrada.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas.
- [ ] T002 Mover #88 a **In progress** en el tablero.
- [x] T003 Verificar que los archivos nuevos no están bloqueados por propiedad.

## Phase 2: Tests

- [x] T004 [AC-01] `test_brightness_is_deterministic_and_clipped`.
- [x] T005 [AC-01] `test_gaussian_noise_is_reproducible_with_the_same_seed`.
- [x] T006 [AC-01] `test_apply_perturbation_covers_the_canonical_names`.
- [x] T007 [AC-03] `test_resize_scale_changes_dimensions_and_preserves_channels`.
- [x] T008 [AC-03] `test_invalid_perturbation_parameters_are_rejected`.
- [x] T009 Ejecutar `uv run pytest tests/test_robustness.py -q`.

## Phase 3: Implementation

- [x] T010 Implementar `adjust_brightness`.
- [x] T011 Implementar `add_gaussian_noise` con semilla.
- [x] T012 Implementar `resize_scale` y `apply_perturbation`.
- [x] T013 Exportar el módulo en `evaluation/__init__.py`.
- [x] T014 Generar las cuatro variantes sobre 100 imágenes de test.
- [x] T015 Validar con YOLO26n y escribir `docs/evaluation/robustez.md`.
- [x] T016 Guardar la evidencia en `dist/robustez/summary.json`.

## Phase 4: Verification and close

- [x] T017 Ejecutar `make specs-check`.
- [x] T018 Ejecutar `make check`.
- [x] T019 Ejecutar `uv build`.
- [ ] T020 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md`.
- [ ] T021 Abrir PR a `develop` con `Closes #88`.
- [ ] T022 Tras el merge, cerrar #88 a mano y moverla a Done.

## Notes

- La evidencia usa una muestra de 100 imágenes, no el test completo.
- Las pruebas no cargan YOLO.
- No se publican imágenes perturbadas.
