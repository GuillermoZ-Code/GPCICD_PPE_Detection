# Feature Specification: HU-060 — Cumplimiento AGPL y CC-BY en el despliegue

**Feature Branch**: `feature/061-hu-060-agpl-despliegue`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #116 — «Cumplimiento AGPL y CC-BY en el despliegue». Asignada a
Eliana (`ElianaCardona`), épica `ep-08`, SP 1, P1, Ola 3, 4 pruebas objetivo.
Depende de HU-045 (healthcheck, ya cerrada).

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Origen verificable del servicio público (Priority: P1)

Como auditor de licencias, quiero que la versión desplegada enlace su código
fuente, para cumplir AGPL al servir en red.

**Why this priority**: AGPL-3.0-only exige ofrecer el código correspondiente a
todo usuario que interactúa con el servicio por red; el commit desplegado permite
correlacionar la versión sirviendo con ese código.

**Independent Test**: `uv run pytest -v tests/test_agpl_despliegue.py` monta la
API con `TestClient`, sin Docker ni red.

**Acceptance Scenarios** (AC de la issue #116):

1. **AC-01**: **Dado** un despliegue, **Cuando** se consulta `GET /health`,
   **Entonces** la respuesta publica `source_url` (repositorio AGPL) y `commit`
   desplegado.
2. **AC-02**: **Dado** un usuario de la SPA, **Cuando** abre la interfaz,
   **Entonces** encuentra la atribución del dataset CC-BY-4.0 con enlace.
3. **AC-03**: **Dado** el contrato OpenAPI, **Cuando** se inspecciona el schema,
   **Entonces** `/health` documenta ambos campos y la respuesta los incluye.

### Edge Cases

- Sin `PPE_DEPLOY_COMMIT`, `commit` es `null` (no se inventa un hash).
- Sin `PPE_SOURCE_URL`, `source_url` usa el repositorio público del proyecto.
- Los valores se normalizan (espacios recortados); una variable vacía no publica
  una cadena vacía.
- `/health/ready` y `/health/live` no cambian: HU-079 y HU-045 siguen vigentes.
- La atribución de la UI ya existe en el pie de `App.tsx`; se conserva.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `HealthResponse` MUST incluir `source_url: str` y `commit: str | None`.
- **FR-002**: `source_url` MUST tomar `PPE_SOURCE_URL` o el repositorio público
  por omisión; `commit` MUST tomar `PPE_DEPLOY_COMMIT` o `None`.
- **FR-003**: el esquema OpenAPI MUST documentar los dos campos nuevos.
- **FR-004**: `docs/operacion/licencias-despliegue.md` MUST explicar las variables
  y la atribución CC-BY de la UI.
- **FR-005**: las 4 pruebas MUST referenciar AC-01/AC-02/AC-03 y ser nuevas.

### Key Entities

- **HealthResponse**: contrato ampliado de `GET /health`.
- **Despliegue**: par `source_url` + `commit` que identifica el código servido.
- **Atribución**: enlace al dataset CC-BY-4.0 en la SPA.

## Acceptance → prueba

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 | `tests/test_agpl_despliegue.py::test_health_publica_url_del_codigo_ac_01`, `::test_health_publica_commit_desplegado_ac_01` |
| AC-02 | `tests/test_agpl_despliegue.py::test_ui_muestra_atribucion_cc_by_ac_02` |
| AC-03 | `tests/test_agpl_despliegue.py::test_openapi_y_respuesta_incluyen_campos_ac_03` |

## Success Criteria *(mandatory)*

- **SC-001**: las 4 pruebas nuevas pasan y la suite Python sigue verde.
- **SC-002**: los contratos existentes de `/health`, `/live` y `/ready` siguen
  pasando sus pruebas; no se eliminan campos.
- **SC-003**: `ruff`, formato, ty, check_specs y propiedad pasan sin bloqueos.

## Out of Scope

- Cambiar `/health/ready` (HU-079) ni `/health/live` (HU-045).
- Cambiar títulos, AC o SP de la issue #116.
- Modificar licencias, dataset ni dependencias.

## Assumptions

- El despliegue inyecta `PPE_DEPLOY_COMMIT` con el SHA de la imagen publicada;
  en local el campo puede ser `null`.
- El pie de la SPA ya enlaza el dataset CC-BY-4.0; esta HU lo verifica y documenta.
