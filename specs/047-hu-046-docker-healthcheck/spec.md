# Feature Specification: HU-046 — HEALTHCHECK en la imagen y en compose

**Feature Branch**: `feature/047-hu-046-docker-healthcheck`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #102 — «HU-046 — `HEALTHCHECK` en la imagen y compose». Asignada a
Guillermo (`GuillermoZ-Code`), épica `ep-13`, P0, ola 3, 1 SP, 4 pruebas objetivo. Depende
de HU-045 (fusionada: `/health/live` y `/health/ready`).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Saber si el contenedor está sano sin mirar logs (Priority: P0)

Como operador, quiero que Docker marque el contenedor como `healthy` o `unhealthy`, para
verificar el despliegue sin intervención manual y para que `compose` no arranque tráfico
sobre un servicio que aún carga el modelo.

**Why this priority**: el 30 % de la rúbrica es el despliegue; un contenedor sin
healthcheck pasa por bueno aunque la API no responda.

**Independent Test**: `docker inspect --format '{{.State.Health.Status}}'` devuelve
`healthy` con la API levantada y `unhealthy` si se corta el servicio.

**Acceptance Scenarios** (AC de la issue #102):

1. **AC-01**: **Dado** el contenedor REST, **Cuando** corre el healthcheck, **Entonces**
   consulta `/health/ready`.
2. **AC-02**: **Dado** el smoke, **Cuando** se inspecciona el contenedor, **Entonces**
   reporta `healthy`.
3. **AC-03**: **Dada** la imagen, **Cuando** se ejecutan las pruebas, **Entonces** hay una
   prueba estática del Dockerfile.

### Edge Cases

- Contenedor solo gRPC: no hay endpoint HTTP; el healthcheck comprueba el puerto 9000.
- Arranque lento por torch: `start-period` de 40 s evita falsos `unhealthy`.
- Modelo ausente: el entrypoint avisa y el healthcheck falla; es el comportamiento
  esperado.
- `docker compose up` espera a `healthy` antes de exponer tráfico si se usa
  `depends_on: condition: service_healthy`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La imagen `runtime` MUST declarar `HEALTHCHECK` con intervalo, timeout,
  `start-period` y reintentos.
- **FR-002**: Con `PPE_SERVICES=rest` (o `both`), el healthcheck MUST consultar
  `/health/ready`.
- **FR-003**: Con `PPE_SERVICES=grpc`, el healthcheck MUST comprobar el puerto 9000.
- **FR-004**: `compose.yml` MUST declarar el healthcheck para los servicios de backend.
- **FR-005**: El runbook MUST documentar `docker inspect` y el estado `healthy`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `docker inspect` responde `healthy` con el servicio sano.
- **SC-002**: Al menos 4 pruebas estáticas cubren los tres AC.
- **SC-003**: `make check` en verde y CI de GitHub en verde.

## Assumptions

- `/health/ready` existe desde HU-045 y devuelve 200 cuando el detector está listo.
- El contenedor gRPC no expone HTTP; el chequeo por puerto es suficiente.
- Docker 20.10+ soporta `HEALTHCHECK` en el Dockerfile y en compose.
