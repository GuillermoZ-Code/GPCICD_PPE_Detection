# Feature Specification: HU-044 — Configuración por entorno validada al arrancar

**Feature Branch**: `feature/045-hu-044-config-entorno`

**Created**: 2026-11-24

**Status**: En implementación

**Input**: Issue #100 — «Configuración por entorno validada al arrancar». Asignada a
Eliana (`ElianaCardona`), épica `ep-10`, P0, Ola 1, 2 SP, 8 pruebas objetivo. Sin
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Fallar temprano con configuración inválida (Priority: P0)

Como operador, quiero configurar la API por variables de entorno con validación
temprana, para detectar errores antes de servir tráfico y sin exponer secretos en los
logs.

**Why this priority**: hoy `env_float`/`env_int` silencian valores inválidos y caen al
default; un despliegue puede arrancar con umbrales o puertos equivocados sin aviso.

**Independent Test**: `uv run pytest -v tests/test_api_settings.py` comprueba que
`.env.example` cubre todas las variables `PPE_*` usadas en `src/`, que los valores
válidos se parsean y que los inválitos fallan con mensaje claro y código no cero.

**Acceptance Scenarios** (AC de la issue #100):

1. **AC-01**: **Dado** el repositorio, **Cuando** se inspecciona `.env.example`,
   **Entonces** documenta cada variable `PPE_*` referenciada en `src/ppe_detection/`.
2. **AC-02**: **Dado** una variable inválida (`PPE_CONF`, `PPE_API_PORT`,
   `PPE_MODEL_SHA256` o `PPE_CORS_ORIGINS`), **Cuando** arranca la API o se ejecuta el
   validador, **Entonces** el error nombra la variable y el proceso termina con código
   distinto de cero.
3. **AC-03**: **Dado** un secreto como `PPE_API_KEY`, **Cuando** falla la validación,
   **Entonces** ni el mensaje ni la salida estándar contienen su valor.

### Edge Cases

- Variables ausentes usan los defaults actuales del detector (`0.25`, `0.7`, `640`,
  `cpu`) y de la API (`0.0.0.0:8000`, `http://localhost:5173`).
- Un puerto fuera de 1–65535 y un SHA256 que no tenga 64 hexadecimales son errores.
- Orígenes CORS se separan por comas; cada uno debe ser http/https con host.
- `PPE_API_KEY` es opcional y su valor nunca se interpola en mensajes de error.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `.env.example` MUST listar todas las variables `PPE_*` usadas en el
  código, con valor de ejemplo o comentario explicativo.
- **FR-002**: `src/ppe_detection/api/settings.py` MUST exponer `load_settings`,
  `validate_environment` y `SettingsError`.
- **FR-003**: `load_settings` MUST validar antes de construir la app y MUST lanzar
  `SettingsError` con el nombre de cada variable inválida.
- **FR-004**: `python -m ppe_detection.api.settings` MUST imprimir el error en stderr y
  devolver código 1 cuando la configuración sea inválida.
- **FR-005**: Los mensajes de error MUST redactar los valores de variables secretas.
- **FR-006**: `create_app` MUST llamar a `load_settings()` antes de registrar rutas.
- **FR-007**: No se MUST cambiar el comportamiento de `env_float`/`env_int` ni agregar
  dependencias.

### Key Entities

- **Settings**: configuración tipada y validada de API, gRPC y detector.
- **SettingsError**: error de configuración con mensaje accionable.
- **Variable secreta**: nombre cuyo valor jamás se incluye en mensajes.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 inventario | `tests/test_api_settings.py::test_env_example_documents_every_ppe_variable` |
| AC-02 validación | `tests/test_api_settings.py::test_valid_environment_is_accepted`, `::test_invalid_conf_reports_variable_and_reason`, `::test_invalid_port_reports_range`, `::test_invalid_sha256_reports_length`, `::test_invalid_cors_origin_is_rejected`, `::test_create_app_fails_early_on_invalid_environment` |
| AC-03 secretos y salida | `tests/test_api_settings.py::test_cli_fails_without_leaking_secret` |

## Success Criteria *(mandatory)*

- **SC-001**: Las 8 pruebas nuevas pasan y la suite completa sigue en verde.
- **SC-002**: ruff, formato y ty pasan sin hallazgos.
- **SC-003**: `ownership --base origin/develop` no bloquea los archivos tocados.
- **SC-004**: La PR queda abierta con revisor de otro integrante.

## Out of Scope

- Cargar un `.env` automáticamente (no se agrega `python-dotenv`).
- Cambiar la lógica de inferencia ni los defaults del detector.
- MaaS/clave de API funcional (HU-051); aquí solo se documenta y protege la variable.
- Archivos `.github/`, `compose.yml` o `Dockerfile` (HU-083/HU-084).

## Assumptions

- El entorno del proceso es la única fuente de configuración.
- Las variables `PPE_*` no listadas en `settings.py` no existen aún en el código.
- Los mensajes pueden mostrar valores no secretos para facilitar la corrección.
