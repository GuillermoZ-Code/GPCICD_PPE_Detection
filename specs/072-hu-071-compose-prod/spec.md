# Feature Specification: HU-071 — `compose.prod.yml` con healthchecks y perfiles

**Feature Branch**: `feature/072-hu-071-compose-prod`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #127 — «HU-071 — `compose.prod.yml` con healthchecks y perfiles». Épica
`ep-07`, 2 SP, 8 pruebas objetivo. Depende de
HU-067.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - `compose.prod.yml` con healthchecks y perfiles (Priority: P0)

Como responsable del despliegue, quiero un compose de producción con las imágenes por tag, healthchecks y el modelo montado, para levantar el sistema completo con un solo comando.

**Why this priority**: El compose local construye la imagen; en producción se baja la imagen publicada y se reinicia sola. Sin esa separación el servidor no puede desplegar lo que construyó el pipeline.

**Independent Test**: se levanta el sistema con el compose de producción y el
healthcheck del servicio reporta `healthy` sin intervención manual.

**Acceptance Scenarios** (AC de la issue #127):

1. **AC-01**: **Dado** `compose.prod.yml`, **Cuando** se levanta, **Entonces** arranca `api`, `grpc`, `web` y `caddy` con imágenes por tag.
2. **AC-02**: **Dado** un servicio caído, **Cuando** se reinicia, **Entonces** `restart: unless-stopped` y los healthchecks lo devuelven al servicio.
3. **AC-03**: **Dado** el artefacto del modelo, **Cuando** arranca la API, **Entonces** está montado `:ro` y las variables vienen del `.env`.

### Edge Cases

- **Servicio que no arranca**: el healthcheck falla y el despliegue vuelve al tag
  anterior.
- **Falta el dominio o el host**: el job se salta y no deja el pipeline en rojo por una
  dependencia externa.
- **Reinicio del servidor**: `restart: unless-stopped` devuelve los servicios solos.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Las imágenes MUST recibir el tag por variable (`PPE_API_IMAGE`, `PPE_WEB_IMAGE`).
- **FR-002**: El modelo MUST montarse `:ro` desde `PPE_MODELS_DIR`.
- **FR-003**: Cada servicio MUST declarar `restart: unless-stopped`.
- **FR-004**: `api`, `grpc` y `web` MUST exponerse solo en la red interna; Caddy publica 80/443.
- **FR-005**: El compose MUST fallar con mensaje claro si falta una variable obligatoria.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: el sistema completo arranca con un solo comando en el servidor.
- **SC-002**: 8 pruebas estáticas cubren los AC sin red ni servidor.
- **SC-003**: `make check` en verde y el pipeline de GitLab en verde.

## Assumptions

- El pipeline de GitLab ya construye y publica las imágenes (HU-067 y HU-068).
- El modelo vive en el servidor, montado `:ro`, y se verifica por SHA256.
- El Droplet existe o se aprovisiona con `deploy/droplet/provision.sh` (HU-069).
