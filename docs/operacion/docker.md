# Runbook — HU-011: sistema completo en contenedor Docker CPU

> Cómo construir, configurar e iniciar el sistema (REST + gRPC + SPA) en Docker
> sin GPU, sin Colab y sin reentrenar. Los pesos, datasets y credenciales viven
> **fuera de Git y fuera de la imagen**: se montan read-only al arrancar.

## 1. Requisitos previos

| Requisito | Valor esperado |
|-----------|----------------|
| Docker Desktop / Engine | ≥ 29 (con Compose v2) |
| Artefacto del modelo | `best.pt` entrenado (Colab) en una carpeta del host |
| SHA256 del artefacto | `96ba99a7fd04566c95c1dac1e188f197efe50b2f170e4b5c76ac81ac0448c828` |

Verifica el artefacto antes de arrancar (PowerShell):

```powershell
(Get-FileHash "C:\ruta\modelos-epp\best.pt" -Algorithm SHA256).Hash.ToLower()
```

## 2. Construcción de la imagen (AC-011.1)

```bash
make docker-build         # backend (target runtime): REST + gRPC
make docker-build-web     # SPA con nginx (target web)
# equivalentes:
docker build --target runtime -t gpcicd-ppe-detection:local .
docker build --target web -t gpcicd-ppe-frontend:local .
```

- Las dependencias salen **del `uv.lock`** (`uv sync --frozen`); no se usa `pip`
  ni `requirements.txt` (CONSTITUTION §4/§8).
- Torch se instala **CPU**: en Linux el `uv.lock` resuelve `torch 2.15.0+cpu`
  desde el índice `pytorch-cpu` (marcador `sys_platform == 'linux'`), así que la
  imagen no arrastra CUDA.
- Bibliotecas del sistema en Debian trixie: `libgl1`, `libglib2.0-0t64` y
  `libxcb1` (OpenCV headless); `libgomp1` y `libquadmath0` (torch CPU), con
  `--no-install-recommends`.
- `grpcio` + `protobuf` viajan como extra `grpc` (runtime del servidor gRPC de
  HU-010).
- Para demostrar un entorno limpio, construye con `docker build --no-cache`.

Comprobación dentro de la imagen (CPU only):

```bash
docker run --rm gpcicd-ppe-detection:local python -c \
  "import cv2, torch, ultralytics; print(torch.__version__, torch.cuda.is_available())"
# 2.15.0+cpu False
```

## 3. Arranque con el artefacto montado read-only (AC-011.3)

Un contenedor con **REST + gRPC** y el modelo montado read-only:

```powershell
docker run -d --name ppe-system --rm `
  -p 8000:8000 -p 9000:9000 `
  -v "C:\ruta\modelos-epp:/models:ro" `
  -e PPE_MODEL_PATH=/models/best.pt `
  -e PPE_SERVICES=rest,grpc `
  gpcicd-ppe-detection:local
```

```bash
docker run -d --name ppe-system --rm \
  -p 8000:8000 -p 9000:9000 \
  -v "/ruta/modelos-epp:/models:ro" \
  -e PPE_MODEL_PATH=/models/best.pt \
  -e PPE_SERVICES=rest,grpc \
  gpcicd-ppe-detection:local
```

- `:ro` impide escribir en el montaje; el contenedor **no** puede alterar el
  artefacto (`docker exec ppe-system touch /models/test` falla con
  `Read-only file system`).
- `PPE_MODEL_VERSION` se deriva del nombre del archivo (`best`); fíjala con
  `-e PPE_MODEL_VERSION=<versión>` si necesitas trazabilidad explícita.
- Sin `PPE_MODEL_PATH` válido: la API responde **503** y gRPC **UNAVAILABLE**
  (mismo contrato de HU-005/HU-006/HU-010); el log del contenedor advierte.

### Variables de entorno

| Variable | Por omisión | Uso |
|----------|-------------|-----|
| `PPE_SERVICES` | `rest,grpc` | `rest`, `grpc` o ambos procesos en el contenedor |
| `PPE_MODEL_PATH` | - | Ruta del artefacto **dentro** del contenedor (`/models/best.pt`) |
| `PPE_MODEL_VERSION` | nombre del archivo | Versión reportada en cada respuesta |
| `PPE_MODEL_SHA256` | calculado del archivo | SHA256 reportado; opcional para fijarlo explícitamente |
| `PPE_CONF` / `PPE_IOU` / `PPE_IMGSZ` / `PPE_DEVICE` | del detector | Umbrales y dispositivo (`cpu`) |
| `PPE_API_HOST` / `PPE_API_PORT` | `0.0.0.0` / `8000` | Escucha de la API REST |
| `PPE_GRPC_HOST` / `PPE_GRPC_PORT` | `0.0.0.0` / `9000` | Escucha de gRPC |
| `PPE_CORS_ORIGINS` | `http://localhost:5173` | Orígenes permitidos por la API |

## 4. Inferencia con el servicio dentro del contenedor (AC-011.2)

Espera a que torch cargue el artefacto: la **primera** petición tarda
~30–60 s; las siguientes son rápidas (misma conducta que la demo local).

### REST (HU-006)

```bash
curl -X POST http://127.0.0.1:8000/predict -F "file=@muestra.jpg"
```

Respuesta conforme al contrato (`detections`, dimensiones, `model_version`,
`model_sha256`, `model_artifact`, `model_reference`, `elapsed_ms`; cada detección con
`class_id`, `class_name`, `confidence` en [0,1] y `bbox` xyxy):

```json
{
  "detections": [],
  "image_width": 640,
  "image_height": 480,
  "model_version": "best",
  "elapsed_ms": 41.53
}
```

Con una muestra del dataset (`docs/operacion/demo-local.md`) aparecen las clases
canónicas (`Gloves, Vest, goggles, helmet, mask, safety_shoe`).

### gRPC (HU-010)

```bash
uv run python -m ppe_detection.grpc.client --target 127.0.0.1:9000 --image muestra.jpg
```

El cliente imprime `message`, las detecciones y la cabecera
`Imagen <w>x<h> · modelo <versión> · <ms> ms`. Una solicitud inválida devuelve
`INVALID_ARGUMENT` y el servidor sigue disponible.

### SPA (HU-007) con nginx

Con compose (§5), la interfaz queda en <http://localhost:8080>; la API que la
SPA llama se hornea en el build (`VITE_API_URL`, por omisión
`http://localhost:8000`).

### Prueba automatizada

```bash
make docker-smoke
# o: PPE_DOCKER_SMOKE=1 PPE_DOCKER_MODEL=ruta/best.pt uv run pytest -m docker
```

Arranca un contenedor efímero, espera la carga del artefacto y verifica REST y
gRPC contra el contrato (AC-011.2). Sin Docker, imagen o artefacto, la prueba
se salta y el resto de la suite no depende de Docker.

## 5. Aplicación completa con compose

```powershell
$env:PPE_MODELS_DIR = "C:\ruta\modelos-epp"
make docker-up        # docker compose up -d --build
make docker-logs      # seguir registros
make docker-down      # detener y eliminar
```

| Servicio | URL | Qué corre |
|----------|-----|-----------|
| `api` | <http://localhost:8000> (docs: `/docs`) | API REST (HU-006) |
| `grpc` | `127.0.0.1:9000` | Servidor gRPC (HU-010) |
| `frontend` | <http://localhost:8080> | SPA React (HU-007) con nginx |

Los tres montan `${PPE_MODELS_DIR}:/models:ro` y comparten la imagen backend
(`gpcicd-ppe-detection:local`). Puertos alternos: `PPE_API_PORT`,
`PPE_GRPC_PORT`, `PPE_WEB_PORT`.

## 6. Solución de problemas

| Síntoma | Causa | Acción |
|---------|-------|--------|
| `503` en `/predict` o `UNAVAILABLE` en gRPC | Montaje ausente o `PPE_MODEL_PATH` mal apuntada | Revisa `docker logs`; monta `:ro` y redefine `PPE_MODEL_PATH` |
| Primera petición muy lenta | torch carga el artefacto (una vez) | Espera; las siguientes son rápidas |
| La SPA no llama a la API | `VITE_API_URL` horneado ≠ puerto de la API | Reconstruye `web` con `--build-arg VITE_API_URL=http://host:puerto` |
| Puerto ocupado | 8000/9000/8080 en uso | Cambia el mapeo (`-p`) o las variables de compose |
| `Read-only file system` al escribir en `/models` | Montaje `:ro` funcionando | Comportamiento esperado (AC-011.3) |

## 7. Criterios de la issue (#11)

| AC | Verificación |
|----|--------------|
| AC-011.1 | `docker build --no-cache` exitoso; `uv sync --frozen` desde `uv.lock`; libglib/libgomp instaladas |
| AC-011.2 | Contenedor sin GPU sirve `/predict` y `Detect` conforme al contrato (`make docker-smoke`) |
| AC-011.3 | Montaje `:ro`; `.gitignore` y `.dockerignore` bloquean pesos/datasets; sin Colab ni reentrenamiento |
| AC-011.4 | Este runbook + README (`Iniciar servicios → Docker`) |
