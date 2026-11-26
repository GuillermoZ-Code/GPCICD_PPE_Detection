# Detector de EPP — réplica en Hugging Face Spaces

Servicio público de detección de Equipos de Protección Personal (EPP) ejecutado
con el Docker SDK de **Hugging Face Spaces**. Es la segunda URL pública del
modelo: `<SPACE_URL>` (el dominio real se publica al crear el Space; no se inventa
uno aquí).

## Qué ofrece

- `POST /predict`: imagen JPEG/PNG de hasta 10 MB y parámetro opcional `conf`.
- `GET /health`, `/health/live` y `/health/ready`: estado del servicio y del modelo.
- `/docs`: documentación interactiva de la API.

La inferencia es CPU. Sin pesos configurados el servicio responde, pero
`/health` reporta el modelo como no cargado; los pesos nunca se incluyen en la
imagen.

## Cómo arrancar

El contenedor escucha en el puerto `7860`, que es el que expone Spaces. Las
variables sensibles se configuran en la sección *Secrets* del Space; no se
versionan ni se hornean en la imagen. El modelo se inyecta en ejecución mediante
`PPE_MODEL_PATH`, con su SHA-256 verificado (HU-026).

## Licencias y atribución

- Código: **AGPL-3.0-only**. Fuente:
  <https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection>.
- Dataset: <https://huggingface.co/datasets/51ddhesh/PPE_Detection>, con
  **licencia del dataset CC-BY-4.0**. La atribución se muestra aquí, en la
  tarjeta pública del Space.

El resultado no declara cumplimiento normativo: no hay clase `person` ni
`no-EPP`, solo seis categorías de EPP.

## Despliegue reproducible

La decisión, los límites y el runbook completo están en
`docs/maas/segunda-url.md` del repositorio fuente. La imagen se construye con
`uv sync --frozen` sobre `uv.lock`; no se usan secretos en el build.
