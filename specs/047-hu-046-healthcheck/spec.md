# Feature Specification: HU-046 — HEALTHCHECK en la imagen y en compose

**Feature Branch**: `feature/047-hu-046-healthcheck`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #102 — «HU-046 — HEALTHCHECK en la imagen y en compose». Épica
`ep-13`, 1 SP, 4 pruebas objetivo. Depende de
HU-045.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - HEALTHCHECK en la imagen y en compose (Priority: P0)

Como operador, quiero que el contenedor informe por sí mismo si está sano, para que el despliegue espere a que la API responda en vez de asumirlo.

**Why this priority**: Sin HEALTHCHECK no hay forma de distinguir «arrancó» de «puede atender». El deploy con rollback depende de esa señal.

**Independent Test**: se levanta el sistema con el compose de producción y el
healthcheck del servicio reporta `healthy` sin intervención manual.

**Acceptance Scenarios** (AC de la issue #102):

1. **AC-01**: **Dado** el contenedor en marcha, **Cuando** Docker consulta el healthcheck, **Entonces** ejecuta `/health/ready` en el servicio REST.
2. **AC-02**: **Dado** el smoke del deploy, **Cuando** se inspecciona el contenedor, **Entonces** `docker inspect` reporta `healthy`.
3. **AC-03**: **Dado** el `Dockerfile`, **Cuando** se revisa estáticamente, **Entonces** declara `HEALTHCHECK` con intervalo, timeout y reintentos.

### Edge Cases

- **Servicio que no arranca**: el healthcheck falla y el despliegue vuelve al tag
  anterior.
- **Falta el dominio o el host**: el job se salta y no deja el pipeline en rojo por una
  dependencia externa.
- **Reinicio del servidor**: `restart: unless-stopped` devuelve los servicios solos.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El healthcheck MUST usar `python` del entorno virtual, sin instalar curl.
- **FR-002**: El servicio gRPC MUST comprobar el puerto 9000 y no el HTTP.
- **FR-003**: El intervalo MUST ser 30 s con `start-period` de 90 s (torque de torch).
- **FR-004**: El healthcheck MUST salir con código distinto de cero cuando falla.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: el sistema completo arranca con un solo comando en el servidor.
- **SC-002**: 4 pruebas estáticas cubren los AC sin red ni servidor.
- **SC-003**: `make check` en verde y el pipeline de GitLab en verde.

## Assumptions

- El pipeline de GitLab ya construye y publica las imágenes (HU-067 y HU-068).
- El modelo vive en el servidor, montado `:ro`, y se verifica por SHA256.
- El Droplet existe o se aprovisiona con `deploy/droplet/provision.sh` (HU-069).
