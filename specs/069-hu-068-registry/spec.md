# Feature Specification: HU-068 — Publicar imágenes en GitLab Registry y Docker Hub

**Feature Branch**: `feature/067-hu-066-gitlab-ci`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #124 — «HU-068 — Publicar imágenes en GitLab Registry y Docker Hub».
Asignada a Guillermo (`GuillermoZ-Code`), épica `ep-06`, P0, ola 3, 2 SP, 8 pruebas
objetivo. Depende de HU-067.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - El servidor baja la imagen ya publicada (Priority: P0)

Como responsable del despliegue, quiero que las imágenes queden en un registry con un
tag inmutable, para que el Droplet descargue exactamente lo que construyó el pipeline.

**Why this priority**: sin registry no hay forma de llevar la imagen al servidor sin
copiar archivos a mano, y el despliegue deja de ser reproducible.

**Independent Test**: tras el build en `main`, el registry del proyecto lista las
imágenes `api` y `web` con el tag del SHA corto; el digest queda como artefacto.

**Acceptance Scenarios** (AC de la issue #124):

1. **AC-01**: **Dado** el pipeline, **Cuando** publica, **Entonces** empuja a
   `registry.gitlab.com/...` autenticándose con `CI_JOB_TOKEN`.
2. **AC-02**: **Dado** `DOCKERHUB_USER` y `DOCKERHUB_TOKEN` configurados, **Cuando**
   publica, **Entonces** empuja además a Docker Hub con variables enmascaradas.
3. **AC-03**: **Dado** un push exitoso, **Cuando** termina el job, **Entonces** el
   digest queda registrado como artefacto.

### Edge Cases

- **Sin credenciales de Docker Hub**: se omite el espejo y el job sigue en verde.
- **Token del job caducado**: el `docker login` falla antes del push, con mensaje claro.
- **Registry caído**: el job falla; no se despliega nada.
- **Reejecución del mismo SHA**: el push sobrescribe el mismo tag; el digest se
  recalcula.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El push al registry de GitLab MUST usar `CI_JOB_TOKEN` y
  `CI_REGISTRY_USER`.
- **FR-002**: El push a Docker Hub MUST ser opcional y usar `DOCKERHUB_USER` y
  `DOCKERHUB_TOKEN` enmascaradas.
- **FR-003**: El job MUST escribir `api-digest.txt` y `web-digest.txt` como artefactos.
- **FR-004**: Ningún token MUST aparecer en el repositorio ni en los logs.
- **FR-005**: Las imágenes MUST publicarse con el tag del SHA corto y con `latest`.

### Key Entities

- **Digest**: identificador inmutable de la imagen publicada.
- **Registry**: `registry.gitlab.com/educacional-group/gpcicd_ppe_detection`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El registry del proyecto lista las cuatro referencias (api/web × sha/latest).
- **SC-002**: 8 pruebas estáticas cubren la autenticación y la ausencia de secretos.
- **SC-003**: El job no falla cuando Docker Hub no está configurado.

## Assumptions

- El Container Registry del proyecto está habilitado (lo está por defecto en gitlab.com).
- El equipo decidió publicar en Docker Hub solo si hay cuenta; el Droplet puede usar el
  registry de GitLab con un deploy token.
