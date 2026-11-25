---
description: "Task list for HU-031 — Matriz de confusión y curvas PR como artefactos"
---

# Tasks: HU-031 — Matriz de confusión y curvas PR como artefactos

**Input**: `specs/032-hu-031-artefactos-evaluacion/spec.md` y `plan.md`.

**Prerequisites**: issue #87, rama `feature/032-hu-031-artefactos-evaluacion`,
`develop` actualizado.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-031.
- [ ] T002 Mover #87 a **In progress** en el tablero.
- [x] T003 Ejecutar `make ownership-check` antes del primer cambio.

## Phase 2: Tests

- [x] T004 [P] `test_artifact_slug_is_stable_and_safe` → AC-02.
- [x] T005 [P] `test_collect_copies_confusion_and_pr_curves` → AC-01.
- [x] T006 [P] `test_collect_returns_empty_without_plots` → AC-01/AC-03.
- [x] T007 [P] `test_collect_rejects_unknown_figure` → AC-02.
- [x] T008 [P] `test_evaluate_adds_stable_artifacts_to_summary` → AC-03.
- [x] T009 Ejecutar `uv run pytest tests/test_evaluation_artifacts.py -q` en verde.

## Phase 3: Implementation

- [x] T010 Implementar `artifact_slug` y `stable_artifact_name`.
- [x] T011 Implementar `collect_evaluation_artifacts`.
- [x] T012 Integrar la recolección en `evaluate()` y exportar en
  `evaluation/__init__.py`.

## Phase 4: Verification and close

- [x] T013 Ejecutar `make specs-check`.
- [x] T014 Ejecutar `make check`.
- [x] T015 Ejecutar `uv build`.
- [ ] T016 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md` con las
  5 pruebas nuevas.
- [ ] T017 Abrir PR a `develop` con la plantilla UAO y `Closes #87`.
- [ ] T018 Tras el merge, cerrar #87 a mano y moverla a Done.

## Notes

- No se modifica `src/ppe_detection/tracking/`; se usan los artefactos del summary.
- Las figuras las sigue generando Ultralytics con `plots=True`.
- El nombre estable es `figura_<version>-<sha12>.png`.
