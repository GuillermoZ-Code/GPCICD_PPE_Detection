---
description: "Task list for HU-040 — Guía de reproducibilidad del entrenamiento"
---

# Tasks: HU-040 — Guía de reproducibilidad del entrenamiento

**Input**: `specs/041-hu-040-reproducibilidad-entrenamiento/spec.md` y `plan.md`.

**Prerequisites**: issue #96, rama
`feature/041-hu-040-reproducibilidad-entrenamiento`, `develop` actualizado.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-040.
- [ ] T002 Mover #96 a **In progress** en el tablero.
- [x] T003 Ejecutar `make ownership-check` antes del primer cambio.

## Phase 2: Tests

- [x] T004 [P] `test_guide_has_required_sections` → AC-03.
- [x] T005 [P] `test_guide_documents_uv_versions_seed_hardware_and_time` → AC-01.
- [x] T006 [P] `test_guide_links_mlflow_and_model_package` → AC-02.
- [x] T007 [P] `test_guide_does_not_expose_secrets_or_user_paths` → AC-03.
- [x] T008 Ejecutar `uv run pytest tests/test_reproducibilidad.py -q`.

## Phase 3: Implementation

- [x] T009 Escribir la guía con alcance, entorno y versiones.
- [x] T010 Añadir datos, comandos `uv`, semilla y tiempos.
- [x] T011 Enlazar MLflow, comparación de runs y `models.lock`.
- [x] T012 Añadir verificación del artefacto y límites.

## Phase 4: Verification and close

- [x] T013 Ejecutar `make specs-check`.
- [x] T014 Ejecutar `make check`.
- [x] T015 Ejecutar `uv build`.
- [ ] T016 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md` con las
  4 pruebas nuevas.
- [ ] T017 Abrir PR a `develop` con la plantilla UAO y `Closes #96`.
- [ ] T018 Tras el merge, cerrar #96 a mano y moverla a Done.

## Notes

- No se entrena en CI ni se descargan datos.
- La guía usa rutas externas genéricas.
- El SHA256 del artefacto es el de `models.lock`.
