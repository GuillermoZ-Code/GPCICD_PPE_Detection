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
       → FastAPI / gRPC → Streamlit
```

Incluye el artefacto del modelo, MLflow, Docker CPU, CI/CD hacia Droplet y
health/logs. Las tarjetas resumen el contrato, el modelo, la operación y los límites
del dataset.

## Límites

- Es una **arquitectura objetivo**, no una implementación terminada.
- Las clases son las seis del dataset; no hay `person` ni `no-EPP`.
- El detector es nivel 3 (YOLO nano/small); la variante exacta se confirma en SPI-01.
- El HTML es un artefacto generado; los cambios van en el JSON.
