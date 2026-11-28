# Cumplimiento AGPL y CC-BY en el despliegue (HU-060)

El servicio se ofrece por red, por lo que AGPL-3.0-only exige que quien interactúa
con él pueda identificar y obtener el código correspondiente. `GET /health`
publica esa información sin exponer secretos ni rutas del host.

## Metadatos publicados

| Campo de `/health` | Origen | Valor por omisión |
|--------------------|--------|-------------------|
| `source_url` | `PPE_SOURCE_URL` | `https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection` |
| `commit` | `PPE_DEPLOY_COMMIT` | `null` |

Los valores se recortan al crear la aplicación: una variable vacía o con solo
espacios no publica una cadena vacía. `source_url` cae al repositorio público y
`commit` se publica como `null` cuando el despliegue no lo inyecta.

Ejemplo de respuesta (se omiten los campos de modelo ya documentados):

```json
{
  "status": "ok",
  "source_url": "https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection",
  "commit": "cd658c0"
}
```

En el despliegue, fija el SHA de la imagen publicada para correlacionar el código
servido con el commit:

```bash
export PPE_SOURCE_URL=https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection
export PPE_DEPLOY_COMMIT=cd658c0
```

`/health/live` y `/health/ready` conservan su contrato: los metadatos de
licencia solo se añaden a `/health`. La interfaz consume `/health/ready` en la
vista «Acerca del modelo» (HU-079).

## Atribución del dataset en la interfaz

El pie de `frontend/src/App.tsx` atribuye el dataset con enlace a
<https://huggingface.co/datasets/51ddhesh/PPE_Detection> y el texto «con licencia
CC-BY-4.0.». La licencia del código se muestra junto al enlace al repositorio:
«Licencia AGPL-3.0-only». No se modifica la licencia del dataset ni se añade una
atribución duplicada en el backend.

## Verificación

```bash
uv run pytest -o addopts="" -q tests/test_agpl_despliegue.py
```

Las cuatro pruebas cubren la URL del código y el commit (AC-01), la atribución
de la SPA (AC-02) y la documentación en OpenAPI junto con la respuesta (AC-03).
