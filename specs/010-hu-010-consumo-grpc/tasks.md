---
description: "Task list for HU-010 — Consumir inferencias mediante gRPC"
---

# Tasks: HU-010 — Consumir inferencias mediante gRPC

**Input**: Design documents from `specs/010-hu-010-consumo-grpc/`

**Prerequisites**: `plan.md`, `spec.md`, contrato de ADR 0005, validación de HU-005,
API REST de HU-006 (PR #42) y el contrato de resultado vacío de HU-004.

**Tests**: obligatorias y **antes** de la implementación (test-first). Cada AC tiene
al menos una prueba que lo referencia.

## Phase 1: Setup

- [x] T001 Añadir `grpcio` y `protobuf` (runtime) y `grpcio-tools` (dev) con `uv add`.
- [x] T002 Crear la spec, el plan y las tareas de HU-010.
- [x] T003 Enlazar la spec en `specs/README.md` y `docs/curso/backlog.md`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_detect_returns_structured_response_with_canonical_catalog` → AC-010.1.
- [x] T005 [P] `test_grpc_rest_equivalence_same_image_and_detector` → AC-010.2.
- [x] T006 [P] `test_grpc_rest_equivalence_empty_result` → AC-010.2 + HU-004.
- [x] T007 [P] `test_empty_image_returns_invalid_argument_and_server_stays_up` → AC-010.3.
- [x] T008 [P] `test_corrupt_image_returns_invalid_argument_without_detector` → AC-010.3.
- [x] T009 [P] `test_oversized_image_returns_invalid_argument` → AC-010.3.
- [x] T010 [P] `test_without_model_returns_unavailable` → FR-006.
- [x] T011 [P] `test_empty_result_message_matches_hu_004_contract` → HU-004.
- [x] T012 [P] `test_prueba_client_detects_against_running_server` → FR-008.
- [x] T013 Ejecutar `uv run pytest tests/test_grpc.py` en rojo.

## Phase 3: Implementation

- [x] T014 Extraer `detector_config.py` compartido y refactor mínimo de `api/app.py`.
- [x] T015 Escribir `grpc/protos/ppe.proto` (servicio `ppe.v1`, mensajes espejo REST).
- [x] T016 Crear `grpc/gen.py`, `make protos` y generar `_pb2`/`_pb2_grpc`.
- [x] T017 Implementar `grpc/servicer.py` (validación → detector → `InferenceResult`).
- [x] T018 Implementar `grpc/server.py`, `grpc/__main__.py` y `grpc/client.py`.
- [x] T019 Excluir generados de Ruff y `ty`; ejecutar `uv run pytest tests/test_grpc.py` en verde.

## Phase 4: Verification

- [x] T020 Ejecutar `make check` y `uv build`.
- [x] T021 Documentar generación, arranque y consumo en `README.md` y
      `docs/architecture/contracts.md`.
- [x] T022 Registrar las pruebas en `docs/curso/PRUEBAS.md` y abrir la PR con
      plantilla UAO, `Closes #10`, assignee y reviewer.
