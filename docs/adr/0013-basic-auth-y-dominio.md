# ADR 0013 — Basic auth del sitio y dominio `sslip.io`

- **Fecha:** 2026-11-27
- **Estado:** Aceptada
- **Decisores:** Grupo 4
- **Evidencia:** HU-041 (#97), HU-042 (#98), HU-055 (#111)

## Contexto

El sistema quedó accesible en `https://143.198.10.157.sslip.io` sin autenticación: la
SPA, la API y los archivos estáticos eran públicos. Para la sustentación hace falta que
el sitio pida credenciales, sin comprar un dominio ni contratar un proveedor de
identidad, y sin romper el smoke del despliegue ni el monitoreo de salud.

Además, Caddy necesita un nombre de host para emitir el certificado: una IP suelta no
sirve para Let's Encrypt.

## Decisión

1. **Autenticación en el proxy, no en la aplicación.** Caddy aplica `basic_auth` con un
   único usuario (`demo`) y un hash bcrypt que llega por la variable de entorno
   `PPE_AUTH_HASH`. La API y la SPA no conocen la existencia del login.
2. **`/health*` queda fuera de la protección.** El job de despliegue y el monitoreo
   consultan la salud sin credenciales; el resto del sitio, incluido `/api/*`, exige
   autenticación.
3. **Dominio gratuito `IP.sslip.io`.** El Droplet no tiene dominio propio; `sslip.io`
   resuelve `<ip>.sslip.io` a esa IP, así que Caddy obtiene un certificado válido de
   Let's Encrypt sin registrar nada.
4. **El hash vive en el `.env` del servidor.** El `Caddyfile` se versiona sin secretos.

## Alternativas consideradas

- **Solo `PPE_API_KEY` en la API.** Protege `/predict`, pero deja la SPA y los estáticos
  abiertos, y obliga a cada cliente a enviar una cabecera.
- **OAuth/OIDC con un proveedor.** Correcto para producción, desproporcionado para una
  demo de dos días y añade credenciales y dependencia externa.
- **Comprar un dominio.** Da HTTPS con nombre propio, pero cuesta y requiere DNS.
- **Cloudflare Access.** Gratis hasta cierto uso, pero exige cuenta y configuración
  externa; el túnel de Cloudflare se evaluó como alternativa de despliegue y se descartó.

## Consecuencias

- La contraseña se cambia regenerando el hash con `caddy hash-password` y recreando el
  contenedor `caddy`; no hay que tocar código.
- En el `.env`, el hash lleva signos `$` y Docker Compose los interpreta: hay que
  escribirlos como `$$` o el valor llega truncado.
- `sslip.io` es un servicio de terceros: si desaparece, el certificado deja de renovarse.
  Migrar a un dominio propio es un cambio de una línea (`PPE_DOMAIN`).
- Basic auth viaja en cada petición: solo tiene sentido sobre HTTPS, que es el caso.
- El smoke del despliegue sigue funcionando porque `/health` no pide credenciales.

## Referencias

- `docker/Caddyfile` y `compose.prod.yml`.
- [`docs/operacion/despliegue.md`](../operacion/despliegue.md).
- ADR 0003 — licencia AGPL y servicio en red.
- ADR 0008 — despliegue en Droplet con Caddy.
