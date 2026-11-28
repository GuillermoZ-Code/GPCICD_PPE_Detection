# Plan — HU-110 MLflow en el Droplet

**Branch**: `feature/111-hu-110-mlflow-droplet` · **Issue**: #166 · **Spec**: `spec.md`

## Enfoque

Añadir un servicio opcional `mlflow` al compose de producción y una ruta en Caddy. El
servicio no publica puertos: solo Caddy lo alcanza por la red interna, con la misma
autenticación básica del sitio (ADR 0013).

## Componentes

| Pieza | Cambio |
|---|---|
| `compose.prod.yml` | Servicio `mlflow` con perfil, volumen, comando y healthcheck |
| `docker/Caddyfile` | `handle /mlflow/*` con `import protegido` y proxy a `mlflow:5000` |
| `.env.example` | `PPE_MLFLOW_IMAGE` y `PPE_MLFLOW_DATA` |
| `docs/operacion/mlflow.md` | Sección 9: variables, arranque, respaldo y seguridad |
| `tests/test_mlflow_droplet.py` | 17 pruebas estáticas del compose, Caddy y runbook |

## Decisiones

- **Perfil `mlflow`**: el servicio no arranca por omisión; se habilita con
  `--profile mlflow`.
- **`--static-prefix /mlflow`**: MLflow genera URLs con el prefijo; Caddy usa `handle`
  (no `handle_path`) para no quitarlo.
- **SQLite en el host**: suficiente para una demo; el volumen permite respaldar con
  `tar` sin tocar el contenedor.
- **Sin credenciales nuevas**: se reutiliza `PPE_AUTH_HASH` del sitio.

## Riesgos

- **Imagen no disponible**: el tag `v3.18.0` debe existir en ghcr; se puede sobrescribir
  con `PPE_MLFLOW_IMAGE`.
- **502 si el perfil está apagado**: documentado; no afecta al resto.
- **Crecimiento del SQLite**: se respalda y se purga fuera de la demo.

## Verificación

```bash
uv run pytest -q tests/test_mlflow_droplet.py
docker compose -f compose.prod.yml --profile mlflow config
make check
```
