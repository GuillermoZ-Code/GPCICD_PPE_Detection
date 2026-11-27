---
description: "Task list for HU-039 — Inferencia por lotes desde CLI"
---

# Tasks: HU-039 — Inferencia por lotes desde CLI

**Input**: `specs/040-hu-039-predict-lotes/spec.md` y `plan.md`.

**Prerequisites**: issue #95, rama `feature/040-hu-039-predict-lotes`,
`develop` actualizado.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-039.
- [ ] T002 Mover #95 a **In progress** en el tablero.
- [x] T003 Ejecutar `make ownership-check` antes del primer cambio.

## Phase 2: Tests

- [x] T004 [P] `test_parse_args_accepts_dir_alias` → AC-01.
- [x] T005 [P] `test_image_json_records_identity_and_parameters` → AC-02.
- [x] T006 [P] `test_run_writes_one_json_per_image` → AC-01.
- [x] T007 [P] `test_run_json_handles_empty_detections` → AC-03.
- [x] T008 Ejecutar `uv run pytest tests/test_predict_batch.py tests/test_predict.py -q`.

## Phase 3: Implementation

- [x] T009 Añadir `--dir` como alias mutuamente excluyente de `--source`.
- [x] T010 Implementar `image_json_payload` y `write_image_json`.
- [x] T011 Escribir un JSON por imagen en `<salida>/json/`.
- [x] T012 Conservar CSV, manifiesto y salida anotada.

## Phase 4: Verification and close

- [x] T013 Ejecutar `make specs-check`.
- [x] T014 Ejecutar `make check`.
- [x] T015 Ejecutar `uv build`.
- [ ] T016 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md` con las
  4 pruebas nuevas.
- [ ] T017 Abrir PR a `develop` con la plantilla UAO y `Closes #95`.
- [ ] T018 Tras el merge, cerrar #95 a mano y moverla a Done.

## Notes

- `--source` sigue aceptando archivo o carpeta.
- `--dir` es solo un alias de entrada por carpeta.
- No se carga Ultralytics en las pruebas.
