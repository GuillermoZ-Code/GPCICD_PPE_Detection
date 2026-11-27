# Feature Specification: HU-070 — Job `deploy` por SSH con rollback

**Feature Branch**: `feature/071-hu-070-deploy`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #126 — «HU-070 — Job `deploy` por SSH con rollback». Épica
`ep-06`, 5 SP, 16 pruebas objetivo. Depende de
HU-068, HU-069.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Job `deploy` por SSH con rollback (Priority: P0)

Como responsable del despliegue, quiero que el pipeline publique en el servidor y vuelva al tag anterior si el smoke falla, para no dejar el sistema caído por una versión mala.

**Why this priority**: Publicar sin verificar es la forma más rápida de tumbar la demo. El rollback convierte un despliegue fallido en un incidente de un minuto.

**Independent Test**: se levanta el sistema con el compose de producción y el
healthcheck del servicio reporta `healthy` sin intervención manual.

**Acceptance Scenarios** (AC de la issue #126):

1. **AC-01**: **Dado** una imagen publicada, **Cuando** corre `deploy`, **Entonces** entra por SSH con la llave enmascarada y ejecuta `docker compose pull && up -d`.
2. **AC-02**: **Dado** el arranque, **Cuando** un servicio no llega a `healthy`, **Entonces** vuelve al tag anterior.
3. **AC-03**: **Dado** dos pipelines simultáneos, **Cuando** llega el segundo, **Entonces** `resource_group` lo serializa.

### Edge Cases

- **Servicio que no arranca**: el healthcheck falla y el despliegue vuelve al tag
  anterior.
- **Falta el dominio o el host**: el job se salta y no deja el pipeline en rojo por una
  dependencia externa.
- **Reinicio del servidor**: `restart: unless-stopped` devuelve los servicios solos.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La llave SSH MUST venir de una variable tipo File y no del repositorio.
- **FR-002**: El job MUST copiar `compose.prod.yml`, `Caddyfile` y `deploy.sh` al servidor.
- **FR-003**: `deploy.sh` MUST guardar el tag anterior y restaurarlo si el smoke falla.
- **FR-004**: El smoke MUST comprobar `/health/ready` y una inferencia real por REST.
- **FR-005**: El job MUST saltarse cuando no hay `DEPLOY_HOST` (sin servidor no se miente).
- **FR-006**: El job MUST usar `resource_group: production`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: el sistema completo arranca con un solo comando en el servidor.
- **SC-002**: 16 pruebas estáticas cubren los AC sin red ni servidor.
- **SC-003**: `make check` en verde y el pipeline de GitLab en verde.

## Assumptions

- El pipeline de GitLab ya construye y publica las imágenes (HU-067 y HU-068).
- El modelo vive en el servidor, montado `:ro`, y se verifica por SHA256.
- El Droplet existe o se aprovisiona con `deploy/droplet/provision.sh` (HU-069).
