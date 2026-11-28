# Feature Specification: HU-110 — MLflow accesible en el Droplet con autenticación

**Feature Branch**: `feature/111-hu-110-mlflow-droplet`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #166 — «MLflow accesible en el Droplet con autenticación». Asignada a
Jesús (`jesusriverosUAO`), épica `ep-14`, P2, Ola 3, 5 SP, 16 pruebas objetivo. Depende
de HU-071 (`compose.prod.yml`), cerrada. Entregable: `compose.prod.yml` (perfil
`mlflow`) + `docs/operacion/mlflow.md`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Mostrar los experimentos en la sustentación (Priority: P2)

Como evaluador, quiero consultar MLflow en una URL protegida, para mostrar los
experimentos del proyecto sin abrir puertos adicionales.

**Why this priority**: el M4 exige evidencia de experimentos; publicar MLflow sin
autenticación expondría datos y ampliaría la superficie de ataque.

**Independent Test**: levantar `docker compose -f compose.prod.yml --profile mlflow up -d
mlflow` y abrir `https://<dominio>/mlflow`; debe pedir las credenciales del sitio y
mostrar los runs. Ejecutar `uv run pytest tests/test_mlflow_droplet.py`.

**Acceptance Scenarios** (AC de la issue #166):

1. **AC-01**: **Dado** el despliegue, **Cuando** se abre `/mlflow`, **Entonces** Caddy
   aplica basic auth y enruta al servicio.
2. **AC-02**: **Dado** el contenedor, **Cuando** se recrea, **Entonces** la base y los
   artefactos sobreviven en el host.
3. **AC-03**: **Dado** el repositorio, **Cuando** se revisa, **Entonces** no hay
   credenciales: solo variables y el hash del `.env`.

### Edge Cases

- **Perfil apagado**: `/mlflow` devuelve 502; el resto del sitio sigue funcionando.
- **Prefijo**: MLflow usa `--static-prefix /mlflow`; Caddy no debe quitar el prefijo.
- **Sin volumen**: si `PPE_MLFLOW_DATA` no existe, Docker crea la carpeta del host.
- **Rotación de contraseña**: se regenera el hash y se recrea Caddy (ADR 0013).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: MUST existir un servicio `mlflow` con `profiles: ["mlflow"]`.
- **FR-002**: MUST usar `--static-prefix /mlflow` y no publicar el puerto 5000.
- **FR-003**: MUST persistir SQLite y artefactos en `PPE_MLFLOW_DATA`.
- **FR-004**: Caddy MUST enrutar `/mlflow/*` con `import protegido`.
- **FR-005**: El repo MUST NOT contener contraseñas ni hashes reales.
- **FR-006**: El runbook MUST documentar variables, arranque, respaldo y seguridad.

### Key Entities

- **Servicio mlflow**: imagen, comando, volumen y healthcheck.
- **Ruta /mlflow**: bloque de Caddy con autenticación.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Caddy con auth | `tests/test_mlflow_droplet.py::test_caddy_routes_mlflow_with_auth`, `::test_caddy_mlflow_proxies_to_service` |
| AC-02 Persistencia | `tests/test_mlflow_droplet.py::test_mlflow_keeps_backend_store_on_host`, `::test_mlflow_serves_artifacts_from_volume` |
| AC-03 Sin credenciales | `tests/test_mlflow_droplet.py::test_caddyfile_has_no_hardcoded_credentials`, `::test_env_example_documents_mlflow_variables` |

## Success Criteria *(mandatory)*

- **SC-001**: `/mlflow` queda protegido con las credenciales del sitio.
- **SC-002**: El backend sobrevive a `docker compose up --force-recreate`.
- **SC-003**: `make check` pasa con las pruebas nuevas.

## Out of Scope

- Instalar o migrar runs en el Droplet (lo hace quien tiene SSH).
- Autenticación propia de MLflow (se usa la de Caddy).
- Exponer MLflow en un subdominio distinto.

## Assumptions

- El Droplet ya tiene `compose.prod.yml` y Caddy con basic auth (ADR 0013).
- La imagen oficial de MLflow incluye Python y el comando `mlflow`.
