# Tasks: HU-038 — Estadísticas de entrada para deriva

**Input**: `specs/039-hu-038-drift-entrada/spec.md` y `plan.md`.

**Prerequisites**: issue #94, `develop` actualizado.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas.
- [ ] T002 Mover #94 a **In progress** en el tablero.
- [x] T003 Revisar la propiedad de `src/ppe_detection/io/` (aviso de Eliana).

## Phase 2: Tests

- [x] T004 [AC-01] `test_image_statistics_calculates_size_aspect_and_brightness`.
- [x] T005 [AC-02] `test_image_statistics_does_not_keep_the_image`.
- [x] T006 [AC-01/AC-03] `test_summary_aggregates_a_batch_without_images`.
- [x] T007 [AC-03] `test_invalid_inputs_are_rejected`.
- [x] T008 Ejecutar `uv run pytest tests/test_input_stats.py -q`.

## Phase 3: Implementation

- [x] T009 Implementar `ImageStats` e `image_statistics`.
- [x] T010 Implementar `StatsSummary` y `summarize_statistics`.
- [x] T011 Exportar el módulo en `io/__init__.py`.
- [x] T012 Calcular la línea base de 100 imágenes y escribir `deriva.md`.
- [x] T013 Guardar la evidencia en `dist/deriva/summary.json`.

## Phase 4: Verification and close

- [x] T014 Ejecutar `make specs-check`.
- [x] T015 Ejecutar `make check`.
- [x] T016 Ejecutar `uv build`.
- [ ] T017 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md`.
- [ ] T018 Abrir PR a `develop` con `Closes #94`.
- [ ] T019 Tras el merge, cerrar #94 a mano y moverla a Done.

## Notes

- Las pruebas no cargan imágenes del dataset.
- El informe solo publica agregados.
- El archivo `io/stats.py` es nuevo; no se modifica `io/images.py`.
