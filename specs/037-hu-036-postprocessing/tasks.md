---
description: "Task list for HU-036 — Postprocesamiento con umbrales por clase"
---

# Tasks: HU-036 — Postprocesamiento con umbrales por clase

**Input**: `specs/037-hu-036-postprocessing/spec.md` y `plan.md`.

**Prerequisites**: issue #92, rama `feature/037-hu-036-postprocessing`,
`develop` actualizado.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-036.
- [ ] T002 Mover #92 a **In progress** en el tablero.
- [x] T003 Ejecutar `make ownership-check` antes del primer cambio.

## Phase 2: Tests

- [x] T004 [P] `test_loads_repository_thresholds` → AC-01.
- [x] T005 [P] `test_missing_default_config_uses_safe_defaults` → AC-01.
- [x] T006 [P] `test_explicit_missing_config_fails` → AC-03.
- [x] T007 [P] `test_invalid_threshold_fails` → AC-03.
- [x] T008 [P] `test_missing_class_fails` → AC-03.
- [x] T009 [P] `test_threshold_config_rejects_foreign_class` → AC-03.
- [x] T010 [P] `test_apply_filters_each_class_with_its_threshold` → AC-02.
- [x] T011 [P] `test_apply_preserves_order_and_does_not_mutate` → AC-02.
- [x] T012 [P] `test_apply_empty_list` → AC-02.
- [x] T013 [P] `test_default_apply_uses_repository_config` → AC-02.
- [x] T014 Ejecutar `uv run pytest tests/test_postprocessing_thresholds.py -q`.

## Phase 3: Implementation

- [x] T015 Implementar `ThresholdConfig` y `ThresholdConfigError`.
- [x] T016 Implementar `load_threshold_config` con respaldo seguro.
- [x] T017 Implementar `apply_thresholds` sin mutar la entrada.
- [x] T018 Exportar el módulo en `postprocessing/__init__.py`.

## Phase 4: Verification and close

- [x] T019 Ejecutar `make specs-check`.
- [x] T020 Ejecutar el `make check` completo cuando `develop` esté verde; hoy falla
  por errores ajenos de API/frontend.
- [ ] T021 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md` con las
  10 pruebas nuevas.
- [ ] T022 Abrir PR a `develop` con la plantilla UAO y `Closes #92`.
- [ ] T023 Tras el merge, cerrar #92 a mano y moverla a Done.

## Notes

- No se modifica la API ni gRPC en esta HU.
- La integración de producción deberá llamar al cargador en el arranque.
- La rama se rebasa sobre `develop` cuando se corrijan los errores de integración.
