---
description: "Task list for HU-027 — Model Card v2 con YOLO26, sesgos y limitaciones"
---

# Tasks: HU-027 — Model Card v2 con YOLO26, sesgos y limitaciones

**Input**: `specs/028-hu-027-model-card-v2/spec.md` y `plan.md`.

**Prerequisites**: issue #83, rama `feature/028-hu-027-model-card-v2`,
`develop` actualizado.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-027.
- [ ] T002 Mover #83 a **In progress** en el tablero.
- [x] T003 Ejecutar `make ownership-check` antes del primer cambio.

## Phase 2: Tests

- [x] T004 [P] `test_model_card_selects_yolo26n_and_adr` → AC-01.
- [x] T005 [P] `test_model_card_includes_yolo11s_comparison` → AC-01.
- [x] T006 [P] `test_model_card_documents_safety_shoe_bias` → AC-02.
- [x] T007 [P] `test_model_card_documents_gloves_bias` → AC-02.
- [x] T008 [P] `test_model_card_declares_non_compliance_use` → AC-02.
- [x] T009 [P] `test_model_card_links_manifest_and_evaluation` → AC-03.
- [x] T010 [P] `test_model_card_links_mlflow` → AC-03.
- [x] T011 [P] `test_model_card_declares_license_and_six_classes` → AC-01/02.
- [x] T012 Ejecutar `uv run pytest tests/test_model_card_v2.py -q`.

## Phase 3: Implementation

- [x] T013 Añadir enlaces a `models.lock`, MLflow y errores.
- [x] T014 Revisar estado de modelo seleccionado/desplegado.
- [x] T015 Mantener comparación, sesgos y uso responsable.

## Phase 4: Verification and close

- [x] T016 Ejecutar `make specs-check`.
- [x] T017 Ejecutar `make check`.
- [x] T018 Ejecutar `uv build`.
- [ ] T019 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md` con las
  8 pruebas nuevas.
- [ ] T020 Abrir PR a `develop` con la plantilla UAO y `Closes #83`.
- [ ] T021 Tras el merge, cerrar #83 a mano y moverla a Done.

## Notes

- No se modifica el modelo ni `models.lock`.
- La ficha declara que el servicio sigue en YOLO11s.
- Los enlaces apuntan a documentos versionados.
# Tasks: HU-027 — Model Card v2

**Input**: Design documents from `specs/028-hu-027-model-card-v2/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #83.

## Phase 2: Pruebas

- [x] T002 [AC-01] La tarjeta compara YOLO11s y YOLO26 y cita el ADR 0009.
- [x] T003 [AC-02] La tarjeta documenta los sesgos de `safety_shoe` y `Gloves`.
- [x] T004 [AC-02] La tarjeta declara el uso no apto (no certifica cumplimiento).
- [x] T005 [AC-03] La tarjeta enlaza `models.lock`, MLflow y el informe de evaluación.

## Phase 3: Implementación

- [x] T006 `docs/model-card.md` con la versión `yolo26n-clean` y su SHA256.
- [x] T007 Sección de limitaciones y sesgos por clase.
- [x] T008 Sección de reproducibilidad con los enlaces de evidencia.

## Phase 4: Verificación

- [x] T009 `make trazabilidad-check` pasa para HU-027.
- [ ] T010 `make check` en verde.
- [ ] T011 PR con plantilla UAO y revisor de otro integrante.
