# API pública de detección de EPP (MaaS)

Esta guía permite consumir el modelo como **MaaS** (*Model as a Service*) sin leer
el código. La documentación interactiva generada por FastAPI está en `/docs` y el
esquema OpenAPI en `/openapi.json`.

> **URL pública (HU-053 pendiente):** la URL definitiva aún no está asignada.
> Exporte `PPE_MAAS_URL=<URL_PUBLICA>` con la base del despliegue y sustituya
> `<URL_PUBLICA>` en los ejemplos. No se publica un dominio inventado.

## Endpoints

| Método | Ruta | Uso |
|--------|------|-----|
| `GET` | `/health` | Estado del servicio, identidad del modelo, origen del código y commit desplegado (HU-060). |
| `GET` | `/health/live` | Liveness: responde `{"status":"ok"}` sin cargar el modelo. |
| `GET` | `/health/ready` | Readiness: `200` si el modelo está cargado, `503` si no. |
| `POST` | `/predict` | Inferencia sobre una imagen; devuelve detecciones e identidad del modelo. |

## Límites y contrato de entrada

- **Formatos:** JPEG y PNG; el contenido debe comenzar con su cabecera mágica.
- **Tamaño:** máximo **10 MB** por imagen; se rechaza un archivo vacío.
- **`conf`:** parámetro de formulario opcional entre **0.01** y **0.99**; si se omite,
  se aplica el default del despliegue. Ejemplo documentado: `0.25`.
- **Salida:** `detections` (clase, confianza, bbox y tamaño de imagen), `image_width`,
  `image_height`, `model_version`, `model_sha256`, `model_artifact`,
  `model_reference` y `elapsed_ms`.
- **Clases:** `Gloves`, `Vest`, `goggles`, `helmet`, `mask`, `safety_shoe`. No existe
  la clase `person` ni `no-EPP`: la respuesta **no** evalúa cumplimiento de EPP.
- **Errores:** `400` para imagen inválida o parámetros fuera de rango; `503` cuando
  el modelo no está cargado. Ambos devuelven `{"detail": "..."}` y están documentados
  con ejemplos en OpenAPI (AC-01).

## Ejemplo con curl

```bash
export PPE_MAAS_URL=<URL_PUBLICA>
curl -sS -X POST "$PPE_MAAS_URL/predict" \
  -F "file=@/ruta/a/imagen.jpg;type=image/jpeg" \
  -F "conf=0.25"
```

Consulta del estado antes de inferir:

```bash
curl -sS "$PPE_MAAS_URL/health"
curl -sS -o /dev/null -w "%{http_code}\n" "$PPE_MAAS_URL/health/ready"
```

## Ejemplo con Python

Sin dependencias ajenas a la instalación estándar:

```python
import os
import urllib.request
from urllib.parse import urlencode

base = os.environ["PPE_MAAS_URL"]
with open("imagen.jpg", "rb") as fh:
    image = fh.read()

boundary = "----ppe-example"
body = (
    f"--{boundary}\r\n"
    'Content-Disposition: form-data; name="file"; filename="imagen.jpg"\r\n'
    "Content-Type: image/jpeg\r\n\r\n"
).encode() + image + (
    f"\r\n--{boundary}\r\n"
    'Content-Disposition: form-data; name="conf"\r\n\r\n0.25\r\n'
    f"--{boundary}--\r\n"
).encode()

request = urllib.request.Request(
    f"{base}/predict",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    method="POST",
)
with urllib.request.urlopen(request, timeout=30) as response:
    print(response.read().decode("utf-8"))
```

`urlencode` se importa solo como referencia de codificación de parámetros; el
cuerpo `multipart/form-data` se construye explícitamente porque incluye bytes.

## Ejemplo de respuesta 200

```json
{
  "detections": [
    {
      "class_id": 3,
      "class_name": "helmet",
      "confidence": 0.93,
      "bbox": [12.0, 8.0, 96.0, 84.0],
      "image_width": 640,
      "image_height": 480
    }
  ],
  "image_width": 640,
  "image_height": 480,
  "model_version": "yolo11s-clean",
  "model_sha256": null,
  "model_artifact": null,
  "model_reference": "artifacts/drive/yolo11s_clean/weights/best.pt",
  "elapsed_ms": 42.5
}
```

El mismo ejemplo está publicado en `/openapi.json` dentro de
`paths./predict.post.responses.200` (AC-03).

## Funcionalidad pendiente

- **HU-051:** clave de API opcional; hoy no se exige `Authorization` ni `X-API-Key`.
- **HU-053:** segunda URL pública y dominio definitivo.
- **HU-054:** límite de peticiones por cliente; hoy no hay rate limit.

No asuma autenticación ni cuotas hasta que esas HU se fusionen. El código fuente
está disponible en <https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection>
(AGPL-3.0-only) y el dataset en
<https://huggingface.co/datasets/51ddhesh/PPE_Detection> (CC-BY-4.0).
