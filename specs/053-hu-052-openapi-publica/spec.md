# Feature Specification: HU-052 — MaaS: documentación pública de la API

**Feature Branch**: `feature/053-hu-052-openapi-publica`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #108 — «MaaS: documentación pública de la API». Asignada a
Eliana (`ElianaCardona`), épica `ep-10`, SP 2, P1, Ola 3, 8 pruebas objetivo.
Depende de HU-045 (healthcheck, cerrada).

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Consumir la API sin leer el código (Priority: P1)

Como desarrollador externo, quiero documentación con ejemplos curl y Python, para
consumir el modelo sin leer el código.

**Why this priority**: una API pública sin ejemplos ni códigos de error obliga al
consumidor a adivinar el contrato y a depurar respuestas por ensayo y error.

**Independent Test**: `uv run pytest -v tests/test_openapi_publica.py` consulta
`/openapi.json` con `TestClient` y lee `docs/maas/README.md`; sin red ni modelo.

**Acceptance Scenarios** (AC de la issue #108):

1. **AC-01**: **Dado** el documento OpenAPI, **Cuando** se inspeccionan `/predict`
   y `/health`, **Entonces** incluyen descripciones, ejemplos y los códigos de
   error 400 y 503.
2. **AC-02**: **Dado** un consumidor externo, **Cuando** abre
   `docs/maas/README.md`, **Entonces** encuentra la URL pública, ejemplos `curl` y
   Python y los límites de entrada.
3. **AC-03**: **Dado** el documento OpenAPI, **Cuando** se buscan los ejemplos,
   **Entonces** están presentes en la respuesta de `/predict` y en el parámetro
   `conf`.

### Edge Cases

- La URL pública aún no está asignada (HU-053 sigue abierta): se documenta como
  variable `PPE_MAAS_URL` / `<URL_PUBLICA>` y no se inventa un dominio.
- Los límites reales son JPEG/PNG y hasta 10 MB (`MAX_IMAGE_BYTES`), con `conf`
  entre 0.01 y 0.99.
- La clave de API (HU-051) y el rate limit (HU-054) no están implementados: la
  guía lo declara como pendiente en lugar de prometerlos.
- No se cambian los nombres ni la obligatoriedad de los campos de
  `PredictResponse`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `/predict` MUST declarar `summary`, `description`, respuestas 400
  y 503 con descripción y ejemplo de respuesta 200 en OpenAPI.
- **FR-002**: `/health` MUST declarar `summary` y `description`.
- **FR-003**: el parámetro `conf` MUST incluir descripción, límites y ejemplo 0.25.
- **FR-004**: `docs/maas/README.md` MUST documentar URL configurable, ejemplos
  `curl` y Python, formatos/límites y códigos de error.
- **FR-005**: las 8 pruebas MUST ser nuevas, AAA y referenciar AC-01/AC-02/AC-03.

### Key Entities

- **OpenAPI**: documento servido en `/openapi.json` y Swagger en `/docs`.
- **Guía pública**: `docs/maas/README.md`, de un solo escritor (Eliana).
- **Límites**: `MAX_IMAGE_BYTES` (10 MB), formatos JPEG/PNG y rango de `conf`.

## Acceptance → prueba

| AC | Evidencia prevista en `tests/test_openapi_publica.py` |
|----|--------------------------------------------------------|
| AC-01 | `…summary_y_descripcion_de_predict_ac_01`, `…codigos_de_error_ac_01`, `…health_descrito_ac_01`, `…limites_de_conf_ac_01` |
| AC-02 | `…guia_incluye_url_y_ejemplos_ac_02`, `…guia_documenta_limites_ac_02` |
| AC-03 | `…ejemplo_de_respuesta_ac_03`, `…info_y_swagger_ac_03` |

## Success Criteria *(mandatory)*

- **SC-001**: las 8 pruebas nuevas pasan y la suite completa sigue verde.
- **SC-002**: `/openapi.json` y `/docs` siguen disponibles; los contratos
  existentes (`PredictResponse.required`, límites de `conf`) no cambian.
- **SC-003**: ruff, pre-commit, ty, check_specs y propiedad pasan sin bloqueos.

## Out of Scope

- Implementar la clave de API (HU-051), el rate limit (HU-054) ni la URL pública
  definitiva (HU-053).
- Cambiar el comportamiento de `/predict`: solo se enriquece su documentación.
- Añadir dependencias o modificar el frontend.

## Assumptions

- FastAPI genera el documento desde las anotaciones; los ejemplos se declaran en
  el decorador de la ruta y en el parámetro `conf`.
- Los ejemplos usan un modelo de muestra, sin pesos reales ni rutas personales.
