# Feature Specification: HU-041 — Proxy inverso Caddy con HTTPS automático

**Feature Branch**: `feature/042-hu-041-caddy`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #97 — «HU-041 — Proxy inverso Caddy con HTTPS automático». Épica
`ep-07`, 3 SP, 12 pruebas objetivo. Depende de
HU-071.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Proxy inverso Caddy con HTTPS automático (Priority: P0)

Como usuario, quiero abrir la SPA por HTTPS con un dominio real, para que la demo del M4 no dependa de `localhost` ni de un puerto con número.

**Why this priority**: La rúbrica pide el sistema desplegado; sin TLS y sin dominio no hay URL pública que mostrar, y AGPL exige que el servicio publicado enlace su fuente.

**Independent Test**: se levanta el sistema con el compose de producción y el
healthcheck del servicio reporta `healthy` sin intervención manual.

**Acceptance Scenarios** (AC de la issue #97):

1. **AC-01**: **Dado** Caddy en marcha, **Cuando** se pide `/`, **Entonces** sirve la SPA, y `/api/*` llega a FastAPI con certificado válido.
2. **AC-02**: **Dado** una petición HTTP, **Cuando** entra por el puerto 80, **Entonces** redirige a HTTPS con cabeceras de seguridad.
3. **AC-03**: **Dado** el `Caddyfile`, **Cuando** se valida, **Entonces** está versionado y pasa `caddy validate`.

### Edge Cases

- **Servicio que no arranca**: el healthcheck falla y el despliegue vuelve al tag
  anterior.
- **Falta el dominio o el host**: el job se salta y no deja el pipeline en rojo por una
  dependencia externa.
- **Reinicio del servidor**: `restart: unless-stopped` devuelve los servicios solos.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Caddy MUST obtener el certificado automáticamente con Let's Encrypt.
- **FR-002**: `/api/*` MUST reenviar a `api:8000` sin el prefijo.
- **FR-003**: El resto MUST reenviar a `web:80`.
- **FR-004**: Las respuestas MUST incluir HSTS, `X-Content-Type-Options` y `Referrer-Policy`.
- **FR-005**: El dominio MUST venir de `PPE_DOMAIN`, no escrito en el archivo.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: el sistema completo arranca con un solo comando en el servidor.
- **SC-002**: 12 pruebas estáticas cubren los AC sin red ni servidor.
- **SC-003**: `make check` en verde y el pipeline de GitLab en verde.

## Assumptions

- El pipeline de GitLab ya construye y publica las imágenes (HU-067 y HU-068).
- El modelo vive en el servidor, montado `:ro`, y se verifica por SHA256.
- El Droplet existe o se aprovisiona con `deploy/droplet/provision.sh` (HU-069).
