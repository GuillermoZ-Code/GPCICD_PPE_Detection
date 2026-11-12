---
description: "Task list for HU-013 — Versión del modelo"
---

# Tasks: HU-013 — Consultar la versión del modelo utilizado

**Input**: Design documents from `specs/014-hu-013-version-modelo/`

**Prerequisites**: `plan.md`, `spec.md`, artefacto y variables de entorno.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [ ] T001 Crear la spec, el plan y las tareas de HU-013.
- [ ] T002 Enlazar la spec en `docs/curso/backlog.md`, `specs/README.md` y `docs/README.md`.

## Phase 2: Tests first (deben fallar)

- [ ] T003 [P] `test_model_identity_reference_uses_sha256` → AC-013.1.
- [ ] T004 [P] `test_model_identity_reference_falls_back_to_artifact` → AC-013.3.
- [ ] T005 [P] `test_model_identity_reference_falls_back_to_version` → AC-013.1.
- [ ] T006 [P] `test_sha256_file_returns_uppercase_digest` → FR-002.
- [ ] T007 [P] `test_default_model_identity_reads_explicit_sha` → FR-002.
- [ ] T008 [P] `test_default_model_identity_computes_sha_from_path` → FR-002.
- [ ] T009 [P] `test_default_model_identity_rejects_invalid_sha_env` → FR-003.
- [ ] T010 [P] `test_default_model_identity_without_path_has_no_sha` → edge case.
- [ ] T011 [P] `test_default_model_identity_reads_version_and_artifact` → AC-013.3.
- [ ] T012 [P] `test_api_response_includes_model_identity` → AC-013.1.
- [ ] T013 [P] `test_api_two_versions_are_distinguishable` → AC-013.2.
- [ ] T014 [P] `test_api_falls_back_to_version_reference` → AC-013.1.
- [ ] T015 [P] `test_api_openapi_documents_model_identity` → contrato REST.
- [ ] T016 [P] `test_grpc_response_includes_model_identity` → AC-013.1.
- [ ] T017 [P] `test_grpc_two_versions_are_distinguishable` → AC-013.2.
- [ ] T018 [P] `test_grpc_falls_back_to_version_reference` → AC-013.1.
- [ ] T019 [P] `test_grpc_proto_defines_model_identity_fields` → contrato gRPC.
- [ ] T020 [P] `test_model_identity_reference_uses_sha256_format` → FR-007.
- [ ] T021 [P] `test_model_identity_exposes_artifact_path` → AC-013.3.
- [ ] T022 [P] `test_default_model_version_uses_explicit_env` → configuración.
- [ ] T023 Ejecutar `uv run pytest tests/test_model_version.py` y confirmar rojo.

## Phase 3: Implementation

- [ ] T024 Añadir `ModelIdentity`, `sha256_file` y `default_model_identity` en `detector_config.py`.
- [ ] T025 Ampliar `PredictResponse` y `create_app` en la API REST.
- [ ] T026 Ampliar `PpeDetectionServicer` y `create_server` en gRPC.
- [ ] T027 Añadir campos al proto y regenerar stubs con `make protos`.
- [ ] T028 Actualizar tipos del frontend (`frontend/src/types.ts`).
- [ ] T029 Reutilizar `sha256_file` desde `evaluation/evaluate.py` (sin duplicar).
- [ ] T030 Ejecutar `uv run pytest tests/test_model_version.py` en verde.

## Phase 4: Documentation and evidence

- [ ] T031 Actualizar `docs/architecture/contracts.md` (REST, gRPC y `PPE_MODEL_SHA256`).
- [ ] T032 Actualizar el ejemplo de respuesta en `docs/operacion/demo-local.md`.
- [ ] T033 Actualizar `docs/curso/PRUEBAS.md` y `docs/curso/PLAN-PRUEBAS.md` con el conteo.
- [ ] T034 Actualizar backlog, M3, README y `specs/README.md`.

## Phase 5: Close

- [ ] T035 Ejecutar `make check` y `uv build`.
- [x] T036 Abrir PR a `develop` con `Closes #13` y solicitar revisión (PR #54).
- [ ] T037 Cerrar #13 a mano tras el merge y actualizar el estado.

## Notes

- No se copian pesos ni se versionan artefactos; solo se registra ruta y SHA256.
- `PPE_MODEL_VERSION` se conserva; `PPE_MODEL_SHA256` es opcional y se calcula del
  archivo cuando no se define.
- La referencia `sha256:<hash>` es el enlace con el tag `model_reference` de HU-009.
