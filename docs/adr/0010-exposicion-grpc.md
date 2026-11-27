# ADR 0010 - Exposición de gRPC en el despliegue

- **Fecha:** 2026-11-27
- **Estado:** Aceptada
- **Decisores:** Grupo 4
- **Evidencia:** HU-049 (#105), HU-041 (#97), HU-071 (#127), HU-050 (#103)
- **Sustituye:** la mención provisional a una ruta `/grpc` en ADR 0008

## Contexto

El despliegue del Droplet levanta dos servicios de inferencia: REST en el contenedor
`api` y gRPC en el contenedor `grpc`. Caddy publica 80/443 con HTTPS automático y basic
auth; el sitio público, el smoke y el monitoreo usan REST y `/health*`.

La HU-049 pide decidir si gRPC se expone públicamente mediante Caddy con h2c y TLS o si
permanece en la red interna de Docker. No hay un consumidor externo identificado: el
cliente de verificación remota (HU-050) se ejecuta dentro del Droplet. El ADR 0008
describió `/grpc` como una ruta posible, sin llegar a implementarla en el `Caddyfile`.

## Decisión

**gRPC permanece interno; no se publica en el Droplet.**

1. `compose.prod.yml` mantiene `9000` solo en `expose` del servicio `grpc`: está
   disponible para los contenedores de la misma red, no para el host ni para internet.
2. `docker/Caddyfile` no define `/grpc`, no usa `h2c` y no conoce el puerto 9000.
3. `deploy/droplet/provision.sh` conserva UFW con `default deny incoming` y solo 22,
   80 y 443; no se abre 9000.
4. Esta decisión sustituye la referencia provisional a `/grpc` del ADR 0008. El ADR
   0008 no se reescribe: sigue siendo el registro histórico del despliegue.

## Alternativas consideradas

### Publicar gRPC con Caddy (h2c + TLS)

- **A favor:** permite un cliente gRPC externo sin VPN ni túnel; Caddy ya gestiona el
  certificado del dominio.
- **En contra:** exige `reverse_proxy` con `h2c`, un subdominio o ruta dedicada, reglas
  UFW adicionales y pruebas de handshake HTTP/2; amplía la superficie de ataque sin un
  consumidor que lo necesite.
- **Decisión:** descartada por ahora. Si aparece un cliente externo, se reabrirá en un
  ADR nuevo con autenticación fuerte.

### Publicar gRPC con mTLS

- **A favor:** autentica tanto al cliente como al servidor; Reduce el riesgo de una
  exposición pública.
- **En contra:** añade emisión, rotación y distribución de certificados de cliente en
  una entrega de un solo día.
- **Decisión:** descartada como configuración inicial; se recomienda si la alternativa
  anterior llega a implementarse.

## Consecuencias

- El contrato gRPC (`Image` → `Detection`) se verifica desde la red interna del
  Droplet; el sitio público ofrece solo REST y la SPA.
- No hay cambios en código de aplicación ni en los archivos de despliegue: la HU
  documenta y fija con pruebas el estado ya desplegado.
- Un cambio futuro que añada `9000:9000` a `compose.prod.yml`, una ruta `/grpc` al
  `Caddyfile` o `ufw allow 9000` romperá `tests/test_adr_exposicion_grpc.py`.
- Los secretos (`SSH_KEY`, `DOCKERHUB_TOKEN`, `PPE_AUTH_HASH`) no se copian a este ADR.

## Referencias

- Issue #105 (HU-049) y spec `specs/050-hu-049-exposicion-grpc/spec.md`.
- `compose.prod.yml`, `docker/Caddyfile` y `deploy/droplet/provision.sh`.
- [`docs/operacion/despliegue.md`](../operacion/despliegue.md).
- ADR 0008 - despliegue en Droplet con Caddy; ADR 0013 - basic auth y dominio.
