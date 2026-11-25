# Feature Specification: HU-045 — Healthcheck de liveness y readiness

**Feature Branch**: `feature/046-hu-045-health-live-ready`

**Created**: 2026-11-24

**Status**: En implementación

**Input**: Issue #101 — «Healthcheck de liveness y readiness». Asignada a Eliana
(`ElianaCardona`), épica `ep-13`, P0, Ola 1, 2 SP, 8 pruebas objetivo. Sin dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Separar liveness y readiness para el despliegue (Priority: P0)

Como operador del despliegue, quiero endpoints `/health/live` y `/health/ready`
separados, para que el orquestador reinicie solo una aplicación caída y espere a
enrutar tráfico hasta que el modelo esté cargado.

**Why this priority**: `/health` solo informa de `degraded`; un despliegue no puede
distinguir «proceso vivo pero sin modelo» de «proceso caído» sin acoplarse a la
implementación interna del detector.

**Independent Test**: `uv run pytest -v tests/test_api_health_live_ready.py` crea la API
con un `FakeDetector` o sin detector y comprueba los dos endpoints y su contrato
OpenAPI, sin pesos ni red.

**Acceptance Scenarios** (AC de la issue #101):

1. **AC-01**: **Dado** un `TestClient` sin detector, **Cuando** se llama a
   `/health/live`, **Entonces** responde 200 sin construir el detector; **cuando** se
   llama a `/health/ready`, **Entonces** responde 503 hasta que exista un detector.
2. **AC-02**: **Dado** un detector cargado con identidad known, **Cuando** se llama a
   `/health/ready`, **Entonces** el cuerpo incluye `model_version` y `model_sha256`.
3. **AC-03**: **Dado** el esquema OpenAPI, **Cuando** se consulta `/openapi.json`,
   **Entonces** documenta `/health/live`, `/health/ready` y la respuesta 503 de
   readiness.

### Edge Cases

- Sin configuración de modelo, la identidad publicada es `unknown` con `sha256=null`;
  ready sigue en 503 porque el detector no está cargado.
- `/health/live` no dispara la construcción perezosa del detector, incluso si hay
  `PPE_MODEL_PATH` en el entorno.
- `/health/ready` solo consulta el estado del detector; no intenta cargarlo.
- `/health` permanece intacto por compatibilidad con la SPA y las pruebas M3.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `GET /health/live` MUST responder 200 sin leer el estado del detector.
- **FR-002**: `GET /health/ready` MUST responder 503 mientras `state.detector` sea
  `None` y 200 cuando esté cargado.
- **FR-003**: La respuesta de readiness MUST incluir `status`, `model_version` y
  `model_sha256`, tanto en 200 como en 503.
- **FR-004**: Los dos endpoints MUST documentarse en OpenAPI con modelos de respuesta
  y códigos 200/503 explícitos.
- **FR-005**: No se MUST agregar dependencias nuevas ni modificar `/health`, `/predict`
  ni la configuración del detector.
- **FR-006**: Las pruebas MUST usar `FakeDetector` y `tmp_path`/`monkeypatch`, sin
  descargas ni GPU.

### Key Entities

- **LiveResponse**: contrato mínimo e independiente del modelo (`status`).
- **ReadyResponse**: contrato de readiness con identidad verificable del modelo.
- **ModelIdentity**: versión, SHA256, artefacto y referencia ya existentes en
  `ppe_detection.detector_config`.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 liveness sin modelo | `tests/test_api_health_live_ready.py::test_live_responds_without_model`, `::test_live_does_not_build_detector` |
| AC-01 readiness 503/200 | `tests/test_api_health_live_ready.py::test_ready_returns_503_without_detector`, `::test_ready_returns_200_with_detector` |
| AC-02 identidad del modelo | `tests/test_api_health_live_ready.py::test_ready_reports_model_version_and_sha256`, `::test_ready_reports_unknown_identity_when_not_configured` |
| AC-03 contrato OpenAPI | `tests/test_api_health_live_ready.py::test_live_and_ready_are_documented_in_openapi`, `::test_openapi_documents_ready_503_contract` |

## Success Criteria *(mandatory)*

- **SC-001**: Las 8 pruebas nuevas pasan con `uv run pytest`.
- **SC-002**: `uv run ruff check .`, `uv run ruff format --check .` y `uv run ty check`
  pasan sin hallazgos.
- **SC-003**: `uv run python -m ppe_detection.tools.ownership --base origin/develop`
  no reporta bloqueos de archivos ajenos.
- **SC-004**: La PR queda abierta con un revisor de otro integrante y sin aprobaciones.

## Out of Scope

- Cambiar el significado de `/health` ni de `/predict`.
- Cargar el modelo automáticamente desde los endpoints de salud.
- Healthchecks de Docker, Compose o CI (HU-046 y HU-083).
- Configuración por entorno (HU-044).

## Assumptions

- El estado del detector en `application.state` es la única fuente de verdad para
  readiness.
- La identidad del modelo ya se resuelve en `create_app` mediante
  `default_model_identity()`.
- La SPA actual sigue usando `/health`; los nuevos endpoints son aditivos.
