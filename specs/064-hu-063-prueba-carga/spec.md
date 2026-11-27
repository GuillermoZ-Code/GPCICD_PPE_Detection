# Feature Specification: HU-063 — Prueba de carga ligera e informe de capacidad

**Feature Branch**: `feature/064-hu-063-prueba-carga`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #119 — «HU-063 — Prueba de carga ligera e informe de capacidad».
Épica `ep-13`, P2, ola 3, 5 SP, 16 pruebas objetivo. Depende de HU-070.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Instrumento reproducible de carga (Priority: P1)

Como responsable técnico, quiero un script que repita una carga ligera con concurrencia
configurable, para comparar escenarios sin depender de mediciones anecdóticas.

**Why this priority**: sin un instrumento versionado no hay evidencia reproducible ni se
puede repetir la medición cuando cambie el Droplet o el número de workers.

**Independent Test**: el script acepta `--url`, `--path`, `--requests`, `--concurrency`,
`--timeout` y `--output`, valida los valores y ejecuta exactamente el número de peticiones
configurado a través de `httpx` (o su alias `httpx2` en entornos sin extras).

**Acceptance Scenarios** (AC de la issue #119):

1. **AC-01**: **Dado** un objetivo HTTP y una concurrencia, **Cuando** se ejecuta el
   script, **Entonces** usa `httpx` para enviar el número configurado de peticiones con
   el timeout y la autenticación indicados.
2. **AC-02**: **Dado** un lote de respuestas, **Cuando** termina la carga, **Entonces**
   el informe contiene p50, p95, throughput, errores y uso de CPU/RAM.
3. **AC-03**: **Dado** el informe anterior, **Cuando** se lee la recomendación,
   **Entonces** propone tamaño de Droplet y número de workers con su motivo.

### Edge Cases

- `requests` o `concurrency` menores o iguales a cero: error de configuración, sin red.
- URL sin esquema `http`/`https`, ruta que no empieza por `/`: error de configuración.
- `--image` inexistente: error antes de abrir conexiones.
- Errores de red, timeouts y respuestas 4xx/5xx: se cuentan como errores, no se ocultan.
- Sin `httpx` ni `httpx2`: el CLI avisa y termina con error explícito.
- Sin `psutil`: el muestreo usa una aproximación estándar y lo declara en el informe.
- Credenciales: se leen de `PPE_LOAD_AUTH` y nunca se escriben en el informe.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El CLI MUST exponer `--url`, `--path`, `--requests`, `--concurrency`,
  `--timeout`, `--image`, `--sample-interval`, `--auth-env`, `--label` y `--output`.
- **FR-002**: La configuración MUST validarse antes de crear clientes o abrir red.
- **FR-003**: `run_load` MUST aceptar un cliente inyectable con `request(method, url, **kwargs)`.
- **FR-004**: El número de peticiones MUST ser exactamente `requests`.
- **FR-005**: La concurrencia MUST pasarse al executor como `max_workers`.
- **FR-006**: `--image` MUST producir `POST` multipart; sin imagen MUST producir `GET`.
- **FR-007**: Cada petición MUST registrar latencia en ms, código y error normalizado.
- **FR-008**: p50 y p95 MUST calcularse con percentil nearest-rank documentado.
- **FR-009**: El informe MUST incluir CPU, RSS y RAM muestreados durante la carga.
- **FR-010**: El informe MUST declarar que la medición es local del instrumento y **no**
  una medición real del Droplet.
- **FR-011**: La recomendación MUST derivar tamaño de Droplet y workers de p95,
  throughput, CPU y tasa de error.
- **FR-012**: El CLI MUST escribir el informe en `--output` y no versionar credenciales.

### Key Entities

- **`LoadConfig`**: parámetros validados del ensayo.
- **`RequestResult`**: latencia, código y error de una petición.
- **`ResourceUsage`**: máximos de CPU, RSS y RAM observados.
- **`LoadSummary`**: agregación de peticiones, percentiles, throughput y recursos.
- **`Recommendation`**: tamaño de Droplet, workers y motivo.
- **`docs/operacion/capacidad.md`**: informe versionado con la medición local.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 Instrumento reproducible | `tests/test_load_test.py::test_ac01_parse_args_defaults_and_validation`, `tests/test_load_test.py::test_ac01_rejects_invalid_configuration`, `tests/test_load_test.py::test_ac01_sends_get_requests_through_client`, `tests/test_load_test.py::test_ac01_sends_multipart_post_when_image_is_given`, `tests/test_load_test.py::test_ac01_concurrency_configures_executor`, `tests/test_load_test.py::test_ac01_forwards_timeout_and_auth` |
| AC-02 Informe de capacidad | `tests/test_load_test.py::test_ac02_percentile_uses_nearest_rank`, `tests/test_load_test.py::test_ac02_counts_successes_and_normalizes_errors`, `tests/test_load_test.py::test_ac02_computes_throughput_from_elapsed_time`, `tests/test_load_test.py::test_ac02_captures_cpu_ram_and_rss_samples`, `tests/test_load_test.py::test_ac02_report_contains_metrics`, `tests/test_load_test.py::test_ac02_report_labels_local_validation_not_real_droplet` |
| AC-03 Recomendación | `tests/test_load_test.py::test_ac03_recommends_small_droplet_when_headroom`, `tests/test_load_test.py::test_ac03_recommends_medium_droplet_when_p95_grows`, `tests/test_load_test.py::test_ac03_recommends_large_droplet_or_error_fix`, `tests/test_load_test.py::test_ac03_report_shows_recommendation_and_reproduction` |

## Success Criteria *(mandatory)*

- **SC-001**: 16 pruebas nuevas referencian AC-01, AC-02 y AC-03.
- **SC-002**: `uv run pytest`, Ruff, formato, `ty`, specs y propiedad quedan en verde.
- **SC-003**: El informe no afirma una medición real del Droplet y deja el pendiente a
  Guillermo.
- **SC-004**: La PR tiene revisor Guillermo y CI en verde antes de revisión.

## Out of Scope

- Medir el Droplet real sin ejecutar el script en ese servidor.
- Cambiar el despliegue, Caddy, los workers o las variables de producción.
- Agregar dependencias nuevas: se usa `httpx`/`httpx2` y `psutil` ya presentes en el lock.
- Sustituir la decisión de tamaño por una prueba de estrés prolongada.

## Assumptions

- HU-070 dejó el despliegue operativo; no implica que esta HU mida ese servidor.
- La validación local usa un servidor ficticio o una API local sin modelo productivo.
- `httpx` está disponible en el entorno de ejecución; en CI se usa `httpx2` o un cliente
  inyectable para que las pruebas no abran red.
- El informe real contra el Droplet se ejecutará con el mismo script y responsable
  Guillermo Zabala.
