# Feature Specification: HU-051 — MaaS: clave de API opcional para `/predict`

**Feature Branch**: `feature/052-hu-051-api-key`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #107 — «MaaS: clave de API opcional para `/predict`». Asignada a
Eliana (`ElianaCardona`), épica `ep-10`, SP 3, P1, Ola 3, 12 pruebas objetivo.
Depende de HU-044 (configuración por entorno, cerrada).

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Proteger el consumo sin romper el uso local (Priority: P1)

Como proveedor del servicio, quiero proteger `/predict` con una clave opcional,
para controlar el consumo del modelo publicado.

**Why this priority**: publicar el modelo sin control permite consumo no deseado,
pero obligar a autenticarse rompería el flujo local y los chequeos de salud.

**Independent Test**: `uv run pytest -v tests/test_api_key.py` usa `TestClient` y
un detector doble; no requiere red, modelo ni secretos reales.

**Acceptance Scenarios** (AC de la issue #107):

1. **AC-01**: **Dado** `PPE_API_KEYS` definido, **Cuando** se envía `/predict` sin
   cabecera `X-API-Key` válida, **Entonces** responde `401`.
2. **AC-02**: **Dado** la variable ausente o vacía, **Cuando** se envía `/predict`,
   **Entonces** el comportamiento actual se mantiene (sin autenticación).
3. **AC-03**: **Dado** un atacante que prueba claves, **Cuando** se validan,
   **Entonces** la comparación es de tiempo constante y ninguna clave se registra.

### Edge Cases

- `PPE_API_KEYS` admite varias claves separadas por comas, con espacios y entradas
  vacías; estas últimas se ignoran.
- `PPE_API_KEY` (singular, reservado en HU-044) se mantiene como compatibilidad
  cuando `PPE_API_KEYS` no está definido.
- La cabecera ausente no debe provocar `TypeError` ni `500`.
- Solo `/predict` se protege: `/health`, `/health/live`, `/health/ready`,
  `/docs` y `/openapi.json` siguen públicos para monitoreo y descubrimiento.
- El cuerpo del error 401 no incluye la clave configurada ni la recibida.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `src/ppe_detection/api/security.py` MUST resolver las claves desde
  el entorno y MUST ofrecer una validación que compare todas las claves con
  `hmac.compare_digest` sobre digests SHA-256, sin cortocircuito.
- **FR-002**: `create_app()` MUST aplicar la guarda solo a `/predict`.
- **FR-003**: con claves configuradas, una cabecera ausente o inválida MUST
  devolver `401` con `WWW-Authenticate: ApiKey`.
- **FR-004**: sin claves configuradas, `/predict` MUST comportarse como hoy.
- **FR-005**: la autenticación MUST NO registrar claves ni cabeceras en logs.
- **FR-006**: `.env.example` MUST documentar `PPE_API_KEYS` y `PPE_API_KEY`.

### Key Entities

- **Clave de API**: cadena no vacía configurada por el despliegue.
- **Guardián**: dependencia FastAPI que traduce la validación a `401`.
- **Registro de peticiones**: middleware JSON existente (HU-047), sin cambios.

## Acceptance → prueba

| AC | Evidencia prevista en `tests/test_api_key.py` |
|----|------------------------------------------------|
| AC-01 | `test_sin_cabecera_devuelve_401_ac_01`, `test_clave_incorrecta_devuelve_401_ac_01`, `test_clave_correcta_devuelve_200_ac_01`, `test_multiples_claves_separadas_por_coma_ac_01`, `test_configured_keys_acepta_legacy_y_ignora_vacios_ac_01`, `test_openapi_documenta_401_ac_01` |
| AC-02 | `test_sin_variable_no_exige_clave_ac_02`, `test_variable_vacia_no_exige_clave_ac_02`, `test_solo_predict_esta_protegido_ac_02` |
| AC-03 | `test_comparacion_no_corta_circuito_ac_03`, `test_clave_correcta_por_digest_ac_03`, `test_secretos_nunca_se_registran_ac_03` |

## Success Criteria *(mandatory)*

- **SC-001**: las 12 pruebas nuevas pasan y la suite completa sigue verde.
- **SC-002**: sin claves, las pruebas existentes de `/predict` siguen pasando.
- **SC-003**: ruff, pre-commit, ty, check_specs y propiedad pasan sin bloqueos.

## Out of Scope

- Cambiar `Settings` ni `load_settings`: las claves se resuelven en la capa de
  seguridad, no son parámetros de inferencia.
- Meter claves en OpenAPI como esquema `apiKey`: se documenta el código 401 con
  la cabecera esperada, sin exponer valores.
- Rate limit (HU-054), rotación automática ni persistencia de claves.

## Assumptions

- El despliegue inyecta `PPE_API_KEYS` como entorno; nunca se versiona su valor.
- El middleware de logging (HU-047) serializa solo método, ruta, estado y duración.
- `hmac.compare_digest` sobre digests de 32 bytes da comparación de tiempo constante.
