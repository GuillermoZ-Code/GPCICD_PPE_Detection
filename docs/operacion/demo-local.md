# Runbook — demo local API + frontend con el modelo real

> Para la sustentación del M3. Los pesos, el dataset y las anotaciones viven **fuera de
> Git**; este documento explica cómo obtenerlos y cómo levantar el sistema completo.

## 1. Artefactos (fuera de Git)

Descarga la carpeta compartida con `gdown`:

```bash
uv run --with gdown gdown --folder \
  "https://drive.google.com/drive/folders/1sUvUScA2vjGgrBwcYbfrpa9z5_5mBXap" \
  -O artifacts/drive
```

Contenido esperado:

| Ruta | Uso |
|------|-----|
| `yolo11s_clean/weights/best.pt` | modelo real (HU-002), SHA256 `e51eb080…7a9959` |
| `yolo11s_clean/weights/best.onnx` | export para latencia |
| `yolov11/summary.md` | métricas de evaluación del modelo |
| `yolov8n_clean/weights/best.pt` | modelo pequeño alternativo |
| `ds_base.zip` | dataset limpio (para sacar muestras) |

`.gitignore` ya cubre `artifacts/`, `data/`, `weights/`, `*.pt`, `*.pth`, `*.onnx` y
`*.zip`. **Nada de esto se sube al repositorio.**

Para extraer una muestra del dataset:

```bash
uv run python -c "import zipfile; z=zipfile.ZipFile('artifacts/drive/ds_base.zip'); \
name=[n for n in z.namelist() if '/test/images/' in n][0]; \
open('artifacts/samples/muestra.jpg','wb').write(z.read(name))"
```

## 2. API REST (HU-006)

```powershell
$env:PPE_MODEL_PATH = "artifacts/drive/yolo11s_clean/weights/best.pt"
$env:PPE_MODEL_VERSION = "yolo11s_clean"
# PPE_MODEL_SHA256 es opcional; si no se define, se calcula del .pt.
uv run --extra inference python -m ppe_detection.api
```

- Escucha en `http://127.0.0.1:8000` (`PPE_API_HOST` y `PPE_API_PORT` lo cambian).
- **Primera petición:** ~27 s, porque carga torch y los pesos.
- **Peticiones siguientes:** ~78 ms en CPU con `imgsz=640`.
- OpenAPI interactivo: <http://127.0.0.1:8000/docs>.
- `/health` todavía no existe: llega con HU-015.

Prueba rápida:

```bash
curl -X POST http://127.0.0.1:8000/predict -F "file=@artifacts/samples/muestra.jpg"
```

Respuesta real de la demo:

```json
{
  "detections": [
    {
      "class_id": 1,
      "class_name": "Vest",
      "confidence": 0.739,
      "bbox": [363.15, 166.1, 504.89, 444.77],
      "image_width": 640,
      "image_height": 640
    }
  ],
  "image_width": 640,
  "image_height": 640,
  "model_version": "yolo11s_clean",
  "model_sha256": "E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959",
  "model_artifact": "artifacts/drive/yolo11s_clean/weights/best.pt",
  "model_reference": "sha256:E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959",
  "elapsed_ms": 77.84
}
```

> `model_sha256` se calcula del artefacto; `model_reference` usa el mismo formato
> `sha256:<hash>` que el tag de MLflow (HU-009).

## 3. Frontend (HU-007)

```powershell
cd frontend
$env:VITE_API_URL = "http://127.0.0.1:8000"
npm run dev
```

- Abre <http://localhost:5173>.
- Sin `VITE_API_URL`, la app usa el **cliente simulado** y no necesita backend.
- CORS de la API permite `http://localhost:5173` por defecto (`PPE_CORS_ORIGINS`).

## 4. Flujo verificado

1. Subir un JPEG de `ds_base/test/images`.
2. La SPA hace `POST /predict` con `multipart/form-data`.
3. La API valida la imagen, ejecuta el detector y devuelve las detecciones.
4. La SPA dibuja las cajas y la tabla con categoría y confianza.

Resultado de la prueba: `Chaleco 74 %` sobre
`00011_jpg.rf.1f418e35dcb50e032e52d5ae301c5a6e.jpg`, con la caja sobre la persona.

## 5. Notas

- Los pesos se descargan por máquina y se guardan en `artifacts/`; no se versionan.
- Métricas del modelo `yolo11s_clean`: mAP50 **0.726**, mAP50-95 **0.424**
  (`yolov11/summary.md`).
- Latencia en caliente medida aquí: **77.84 ms**. SPI-01 había medido 136–158 ms en
  otro equipo; conviene repetir la medición en el hardware de la sustentación.
- HU-015 añadirá `/health` y registros técnicos sin secretos.
