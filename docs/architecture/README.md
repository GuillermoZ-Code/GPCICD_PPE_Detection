# Arquitectura

- **Fuente versionada:** [`arquitectura.json`](arquitectura.json)
- **Diagrama interactivo:** [`arquitectura.html`](arquitectura.html)

El HTML **no se edita a mano**: se regenera desde el JSON con
[Archify](https://github.com/tt-a1i/archify).

```bash
make arch
# o:
node "$HOME/.agents/skills/archify/bin/archify.mjs" finalize architecture \
  docs/architecture/arquitectura.json docs/architecture/arquitectura.html \
  --quality showcase
```

Si Archify está en otra ruta, usa `ARCHIFY_BIN=/ruta/al/archify.mjs make arch`.

## Lectura

El diagrama muestra el flujo objetivo del M3–M4:

```text
Imagen → validación → preprocesamiento → YOLO → postprocesamiento
       → FastAPI / gRPC → SPA React
```

Incluye el artefacto del modelo, MLflow, Docker CPU, CI/CD hacia Droplet y
health/logs. Las tarjetas resumen el contrato, el modelo, la operación y los límites
del dataset.

## Flujo de despliegue (HU-086)

La cadena que muestra el diagrama es:

```text
GitHub → GitLab CI → Container Registry → Droplet → Caddy → usuario
```

- El Droplet ejecuta `docker compose` con Caddy delante de la SPA (interno `:80`) y la
  API REST (interno `:8000`); gRPC permanece interno en `:9000`.
- Caddy publica `80/443` con TLS automático y basic auth; `/health` queda abierto para
  el smoke y `/health/ready` se consulta con credenciales.
- Los secretos se nombran, nunca se versionan: `SSH_KEY`, `DOCKERHUB_TOKEN` y
  `PPE_AUTH_HASH` (en `/opt/ppe/.env`). El detalle operativo está en
  [`../operacion/despliegue.md`](../operacion/despliegue.md).

Para regenerar el HTML, se edita solo `arquitectura.json` y se ejecuta el comando
mostrado arriba. `finalize`/`deliver` valida la composición antes de escribir el
artefacto.

## Límites

- Es una **arquitectura objetivo**, no una implementación terminada.
- Las clases son las seis del dataset; no hay `person` ni `no-EPP`.
- El detector es nivel 3 (YOLO nano/small); la variante exacta se confirma en SPI-01.
- El HTML es un artefacto generado; los cambios van en el JSON.
