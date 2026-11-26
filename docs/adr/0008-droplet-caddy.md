# ADR 0008 — Despliegue en Droplet con Docker Compose y Caddy

- **Fecha:** 2026-11-25
- **Estado:** Aceptada
- **Decisores:** Grupo 4
- **Evidencia:** HU-069 (#125), HU-070 (#126), HU-071 (#127), HU-041 (#97)
- **Relacionada:** ADR 0003 (AGPL) y ADR 0007 (GitLab CI y espejo)

## Contexto

El M4 exige un sistema desplegado y verificable: API REST, gRPC y SPA sobre Docker CPU,
con HTTPS, credenciales gestionadas y una prueba funcional posterior al despliegue. El
curso provee un **Droplet** y el presupuesto no contempla servicios administrados.

## Decisión

**Desplegar en el Droplet del curso con Docker Compose y Caddy como proxy inverso con
HTTPS automático.**

- `compose.prod.yml` levanta `api`, `grpc`, `web` y `caddy`, con healthchecks y reinicio
  automático.
- Caddy publica 80/443, obtiene el certificado con Let's Encrypt y enruta:
  `/api/*` a `api`, `/grpc` al servicio gRPC y el resto a la SPA.
- Las imágenes se publican en el registry de GitLab (y Docker Hub como espejo) con tag por
  commit; el `deploy` las baja por tag y hace **rollback** al tag anterior si el smoke
  falla.
- El modelo se monta `:ro` desde el host; nunca viaja dentro de la imagen.
- Los secretos viven en variables protegidas de GitLab CI/CD; el Droplet solo recibe el
  token de despliegue.

## Alternativas consideradas

### Render u otro PaaS

- **A favor:** HTTPS y despliegue gestionados.
- **En contra:** el curso pide el Droplet y credenciales propias; el plan gratuito duerme
  el servicio y no cubre gRPC ni un registry propio.
- **Decisión:** descartado como principal.

### Hugging Face Spaces como despliegue principal

- **A favor:** ya se usa para el modelo y es cómodo para demos.
- **En contra:** no es el entorno del curso, no soporta `compose` multi-servicio ni gRPC,
  y los arranques en frío rompen la medición de latencia.
- **Decisión:** descartado como principal; puede quedar como demo secundaria.

### Kubernetes o un orquestador

- **A favor:** escalado y rolling updates.
- **En contra:** complejidad desproporcionada para tres contenedores y una semana de
  entrega.
- **Decisión:** descartado.

### Servidor propio o máquina local expuesta

- **A favor:** control total.
- **En contra:** sin IP pública estable ni respaldo del curso; la sustentación depende de
  la red del aula.
- **Decisión:** descartado.

## Consecuencias

- Hace falta un dominio o subdominio apuntando al Droplet y abrir 80/443; Caddy gestiona
  la renovación del certificado.
- El pipeline gana un stage `deploy` con rollback por tag y un smoke test posterior.
- La AGPL obliga a enlazar el código fuente en la interfaz publicada y a atribuir el
  dataset CC-BY-4.0 (ADR 0003).
- El Droplet es un único punto de falla: el runbook de operación documenta diagnóstico y
  recuperación (HU-055).
- El costo se mantiene en el Droplet del curso; no hay servicios de pago.

## Referencias

- HU-069 (#125) aprovisionamiento, HU-070 (#126) deploy con rollback, HU-071 (#127)
  `compose.prod.yml`, HU-041 (#97) Caddy.
- ADR 0003 — licencia AGPL-3.0-only.
- `CONSTITUTION.md` §7 y §11.
