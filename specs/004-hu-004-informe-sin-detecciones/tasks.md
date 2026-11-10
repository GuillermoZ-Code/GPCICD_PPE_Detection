---
description: "Task list for HU-004 — Informe sin detecciones"
---

# Tasks: HU-004 — Informar cuando no se detectan elementos de protección personal

**Input**: Design documents from `specs/004-hu-004-informe-sin-detecciones/`

**Prerequisites**: `plan.md`, `spec.md`, contrato TA-11 (`contracts.py`), especificación
de HU-002 (el detector ya devuelve `[]` sin cajas) e issue #4.

**Tests**: obligatorias y **antes** de la implementación (test-first). Cada AC tiene
al menos una prueba que lo referencia (`AC-004.x` en docstring).

## Phase 1: Setup

- [x] T001 Crear rama `feature/004-hu-004-informe-sin-detecciones` desde `develop`
      con la extensión git de Spec Kit.

## Phase 2: Tests first (deben fallar)

- [x] T002 [P] `tests/test_results.py::test_empty_inference_returns_empty_collection_and_message` → AC-004.1.
- [x] T003 [P] `tests/test_results.py::test_empty_result_is_not_classified_as_error` → AC-004.2.
- [x] T004 [P] `tests/test_results.py::test_real_failure_is_classified_as_error_and_not_empty_success` → AC-004.2.
- [x] T005 [P] `tests/test_results.py::test_null_response_is_rejected_as_contract_error` → AC-004.2 (frontera `None` ≠ `[]`).
- [x] T006 [P] `tests/test_results.py::test_empty_message_does_not_assert_noncompliance_or_absence` → AC-004.3.
- [x] T007 [P] `tests/test_results.py::test_nonempty_result_summarizes_detected_classes` → FR-005.
- [x] T008 [P] `tests/test_results.py::test_listing_order_follows_canonical_catalog` → FR-005.
- [x] T009 [P] `tests/test_results.py::test_fake_detector_empty_result_flows_through_contract` → FR-006.
- [x] T010 [P] `tests/test_results.py::test_responsible_use_note_states_detection_only` → FR-007.
- [x] T011 `uv run pytest tests/test_results.py` en rojo.

## Phase 3: Implementación

- [x] T012 `src/ppe_detection/results.py`: `InferenceResult`,
      `build_inference_result`, `build_error_result`, `NO_DETECTIONS_MESSAGE`,
      `RESPONSIBLE_USE_NOTE`.
- [x] T013 `uv run pytest` en verde (suite completa, no solo el archivo nuevo).

## Phase 4: Integración en puntos de consulta

- [x] T018 `detection/predict.py::format_summary` incluye
      `NO_DETECTIONS_MESSAGE` con corridas sin detecciones (código de salida 0).
- [x] T019 Pruebas de integración CLI: `test_format_summary_empty_uses_contract_message`,
      `test_run_prints_empty_message_without_error` (CSV vacío, sin error) y
      `test_run_raises_real_error_for_corrupt_image` (fallo real como excepción).
- [x] T020 `uv run pytest` en verde tras la integración.

## Phase 5: Polish

- [x] T021 Documentar el contrato de resultado en `docs/architecture/contracts.md`
      y la integración en la CLI.
- [x] T022 Actualizar `specs/README.md` (fila de la spec 004) y el enlace en
      `docs/curso/backlog.md` (HU-004).
- [x] T023 Verificación completa: Ruff check, Ruff format --check, `ty check`,
      pytest (equivalente a `make check`).
- [x] T024 Actualizar estado: `make estado-write` + bitácora en
      `docs/curso/ESTADO.md`; commit, push y PR a `develop` (revisor: Guillermo).

## Dependencies & Execution Order

- T001 → T002–T010 (paralelizables) → T011 → T012 → T013 → T018–T020 →
  T021–T024.
- Ninguna tarea de código depende de red eventual: todo corre en CPU local.
- T015 depende de que exista la carpeta de la spec (T001) y de la bitácora de T017
  para no contradecir el estado.

## Notes

- Sin GPU, dataset, pesos ni red en las pruebas.
- `None` no se normaliza a colección vacía: es error de contrato (FR-004).
- La presentación en API/Streamlit/gRPC es de HU-006/007/010; la CLI ya consume el
  contrato.
- Los commits, el push y la PR se ejecutan tras la verificación, con revisión de
  otro integrante antes de fusionar (DoD).
