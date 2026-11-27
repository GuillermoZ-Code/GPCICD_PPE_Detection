# Feature Specification: HU-067 — Job `build_image` con Docker-in-Docker

**Feature Branch**: `feature/067-hu-066-gitlab-ci`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #123 — «HU-067 — Job `build_image` con Docker-in-Docker». Asignada a
Guillermo (`GuillermoZ-Code`), épica `ep-06`, P0, ola 3, 3 SP, 12 pruebas objetivo.
Depende de HU-066.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - La imagen se construye en el pipeline, no en una máquina (Priority: P0)

Como equipo, queremos que GitLab construya las imágenes del backend y de la SPA en cada
versión, para desplegar exactamente el código que pasó las compuertas y no el que
quedó en el portátil de alguien.

**Why this priority**: sin imagen construida por el pipeline no hay despliegue
reproducible; el Droplet solo baja lo que GitLab publicó.

**Independent Test**: en `main`, el job `build_image` construye los targets `runtime` y
`web`, ejecuta el smoke de importación y termina en verde.

**Acceptance Scenarios** (AC de la issue #123):

1. **AC-01**: **Dado** el pipeline de `main`, **Cuando** corre `build_image`,
   **Entonces** construye los targets `runtime` y `web` usando cache de capas.
2. **AC-02**: **Dado** un build exitoso, **Cuando** se etiqueta la imagen,
   **Entonces** lleva `$CI_COMMIT_SHORT_SHA` y `latest`.
3. **AC-03**: **Dado** el Dockerfile, **Cuando** se construye la imagen, **Entonces** el
   modelo no está dentro: se descarga verificado en el deploy.

### Edge Cases

- **Primer build**: no existe `:latest`; el `pull` previo falla y se ignora.
- **Digest distinto**: si el modelo cambia, el deploy lo detecta por SHA256.
- **Build lento**: `timeout: 45 minutes` y cache de capas por `:latest`.
- **Cambio solo en la SPA**: el target `runtime` se reutiliza desde el cache.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El job MUST usar Docker-in-Docker con `docker:29.10.0-cli` y
  `docker:29.10.0-dind`.
- **FR-002**: El job MUST construir los targets `runtime` y `web` del `Dockerfile`.
- **FR-003**: El job MUST usar `--cache-from` con `:latest` y `BUILDKIT_INLINE_CACHE`.
- **FR-004**: Las imágenes MUST llevar `$CI_COMMIT_SHORT_SHA` y `latest`.
- **FR-005**: El job MUST ejecutar el smoke de importación antes de publicar.
- **FR-006**: La imagen MUST NOT contener el artefacto del modelo.

### Key Entities

- **Imagen `api`**: backend con API REST y gRPC, sin pesos.
- **Imagen `web`**: SPA estática servida por nginx.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `build_image` termina en menos de 45 minutos en un runner limpio.
- **SC-002**: 12 pruebas estáticas cubren los dos targets, los tags y la ausencia del
  modelo en la imagen.
- **SC-003**: `docker inspect` del smoke reporta la app creada sin modelo montado.

## Assumptions

- El runner compartido permite DinD (lo permite por defecto en gitlab.com).
- El `Dockerfile` ya tiene los targets `runtime` y `web` (HU-011).
- El modelo se publica en el registry de paquetes (HU-024) y se monta en el servidor.
