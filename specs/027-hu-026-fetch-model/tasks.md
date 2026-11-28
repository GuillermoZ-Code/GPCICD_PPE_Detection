---
description: "Task list for HU-026 — Descarga y verificación del modelo"
---

# Tasks: HU-026 — Descarga y verificación del modelo por SHA256

**Input**: `specs/027-hu-026-fetch-model/spec.md` y `plan.md`.

**Prerequisites**: issue #82, rama `feature/027-hu-026-fetch-model`, HU-025 fusionada.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-026.
- [ ] T002 Mover #82 a **In progress** en el tablero.
- [x] T003 Crear la rama desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_fetch_from_manifest_file_url` → AC-01.
- [x] T005 [P] `test_cli_fetch_success` → AC-01.
- [x] T006 [P] `test_fetch_rejects_sha_mismatch` → AC-02.
- [x] T007 [P] `test_cli_fetch_sha_mismatch` → AC-02.
- [x] T008 [P] `test_fetch_http_uses_injected_urlopen` → AC-03.
- [x] T009 [P] `test_fetch_cleans_temp_file` → AC-03/FR-006.
- [x] T010 [P] `test_fetch_rejects_unsupported_scheme` → FR-003.
- [x] T011 [P] `test_fetch_does_not_replace_existing_on_failure` → FR-004/006.
- [x] T012 Ejecutar `uv run pytest tests/test_artifact_fetch.py -q` y confirmar rojo.

## Phase 3: Implementation

- [x] T013 Crear `src/ppe_detection/detection/artifact.py` con `ArtifactError`,
      `fetch_artifact` y `main`.
- [x] T014 Implementar `file://`, `http://` y `https://`.
- [x] T015 Implementar temporal, verificación SHA256 y reemplazo atómico.
- [x] T016 Implementar la CLI `fetch`.
- [x] T017 Ejecutar las 8 pruebas en verde.

## Phase 4: Verification and close

- [x] T018 Ejecutar `make ownership-check`.
- [x] T019 Ejecutar `make check` (418 passed, 1 skipped).
- [ ] T020 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md`.
- [ ] T021 Abrir PR a `develop` con la plantilla UAO y `Closes #82`.
- [ ] T022 Tras el merge, cerrar #82 a mano y moverla a Done.

## Notes

- No se agregan dependencias.
- Los tests no usan red externa: `file://` o `urlopen` inyectado.
- El destino por defecto es `artifacts/models/best.pt`.
