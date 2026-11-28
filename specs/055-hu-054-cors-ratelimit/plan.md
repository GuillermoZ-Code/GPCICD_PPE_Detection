# Plan — HU-054

1. Agregar el módulo `caddy-ratelimit` con `docker/Dockerfile.caddy`.
2. Configurar CORS en `docker/Caddyfile`, restringido a `PPE_CORS_ORIGIN`.
3. Configurar `rate_limit` por IP con ventana/eventos configurables mediante
   sustitución en tiempo de adaptación (`{$VAR:default}`).
4. Exponer las variables en `compose.prod.yml` con defaults documentados, sin
   `build:` en producción: la imagen llega por `PPE_CADDY_IMAGE`.
5. Agregar prueba estructural de configuración AC-01/AC-02/AC-03.
6. Validar localmente con Docker: construcción, `caddy validate`, preflight CORS
   y respuesta 429 al exceder el límite.
7. Dejar explícitos los pendientes de publicación de imagen, deploy/CI y
   validación remota; no declarar la HU completa.
