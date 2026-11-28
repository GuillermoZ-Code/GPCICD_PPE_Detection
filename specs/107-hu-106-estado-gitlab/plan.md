# Plan — HU-106 `make estado` con GitLab

**Branch**: `feature/107-hu-106-estado-gitlab` · **Issue**: #162 · **Spec**: `spec.md`

## Enfoque

Extender `src/ppe_detection/tools/estado.py`, que ya reúne git, PRs e issues, con una
consulta de solo lectura al último pipeline de GitLab. `glab` se invoca por su ruta
absoluta (`shutil.which`) y con `glab api`, que devuelve JSON estable; así no se depende
de la salida de color de `glab ci status`.

La degradación es explícita: sin `glab` o si el comando falla, el informe añade una
advertencia y una nota, y `main` sigue devolviendo cero.

## Componentes

| Pieza | Cambio |
|---|---|
| `Pipeline` | Dataclass congelada: `status`, `sha`, `web_url` |
| `parse_pipeline()` | Parsea lista u objeto JSON; valida los tres campos |
| `_collect_gitlab()` | `shutil.which("glab")` + `glab api …/pipelines?ref=develop&per_page=1` |
| `Report` | Campos `pipeline` y `gitlab_note` con valor por defecto |
| `render()` | Línea `**GitLab:**` con SHA corto, estado y URL, o la nota |

## Decisiones

- **API en vez de `glab ci status`**: la API entrega JSON con `sha`, `status` y `web_url`
  en una sola llamada; el formato de tabla de `ci status` cambia entre versiones.
- **Sin caché**: `make estado` es una foto; una consulta de red por ejecución es aceptable.
- **Tiempo de espera heredado**: `run()` ya limita a 20 s y captura errores.
- **Sin dependencia nueva**: solo `shutil` de la biblioteca estándar.

## Riesgos

- **`glab` autenticado**: si el token no tiene `read_api`, la consulta falla; se muestra
  la nota y no se bloquea el resto del informe.
- **CI sin `glab`**: las pruebas simulan la salida, así que no requieren la herramienta.

## Verificación

```bash
uv run python -m ppe_detection.tools.estado
uv run python -m ppe_detection.tools.check_specs --check
make check
```
