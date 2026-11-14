# Runbook — MLflow local (HU-009)

> Registra las evaluaciones de HU-008 como runs y compara dos o más corridas.
> Los pesos y el dataset viven **fuera de Git**; MLflow guarda parámetros, métricas y
> los resúmenes de evaluación, no los pesos.

## 1. Requisitos

MLflow es un extra opcional para no cargar ~150 dependencias en el paquete base ni en
la CI:

```bash
uv sync --extra tracking
```

Si compartes el `.venv` con la demo de inferencia, sincroniza ambos extras:

```bash
uv sync --all-extras
```

> `uv run --extra tracking ...` sincroniza solo ese extra. Si después necesitas el
> detector, vuelve a sincronizar `inference`.

## 2. Backend local

El comando usa por defecto `sqlite:///mlflow.db`, con artefactos en `mlruns/`
(almacén local por omisión de MLflow).
Ambos están cubiertos por `.gitignore`:

```text
mlflow.db
mlruns/
mlartifacts/
```

También se acepta el backend de archivo con `--tracking-uri file:./mlruns`.

## 3. Registrar una evaluación

Cada `summary.json` de HU-008 se registra como un run. El comando añade
automáticamente el `summary.json` y su `summary.md`; los gráficos se pasan con
`--artifact`:

```bash
uv run --extra tracking python -m ppe_detection.tracking log \
  --summary artifacts/eval/hu008_test1094/summary.json \
  --run-name test1094 \
  --dataset-sha256 3D1AE47B7F1401B02A05A997E413765D8F15529FB1944F2A5B1ADF536E909432 \
  --artifact artifacts/eval/hu008_test1094/confusion_matrix.png
```

Salida esperada:

```text
run_id=00771caaba4f444685bdd65e2b67f87c
```

Opciones útiles:

| Opción | Uso |
|--------|-----|
| `--run-name` | Nombre legible; si se omite, `eval-<split>-<sha12>` |
| `--dataset-sha256` | SHA256 del ZIP del dataset (queda como tag) |
| `--artifact` | Artefacto extra; repetible |
| `--tracking-uri` | Backend de MLflow |
| `--experiment` | Experimento; por defecto `ppe-detection-eval` |

El payload registra `model_path`, `model_sha256`, `dataset_path`, `dataset_split`,
`dataset_yaml_sha256`, `imgsz`, `conf`, `iou`, `seed`, `device`, imágenes, instancias,
métricas globales y métricas por clase. La referencia del modelo es
`sha256:<hash>`; los pesos no se copian. Esa misma referencia se expone en REST y gRPC
como `model_reference` (HU-013), de modo que un run se correlaciona con la inferencia.

## 4. Consultar y comparar

```bash
uv run --extra tracking python -m ppe_detection.tracking compare \
  --run-id b4187e62c6784effbae5552abac02468 \
  --run-id 00771caaba4f444685bdd65e2b67f87c
```

La salida es una tabla Markdown con `run_id`, nombre, referencia del modelo,
configuración y métricas. Para explorar la interfaz web:

```bash
uv run --extra tracking --extra inference mlflow ui \
  --backend-store-uri sqlite:///mlflow.db
```

Abre <http://localhost:5000>, entra al experimento `ppe-detection-eval` y consulta los
runs por nombre o por `run_id`.

## 4.1 Medir una sesión de inferencia

La rúbrica del M3 pide runs **comparables** con calidad y latencia. El comando
`benchmark` mide latencia media, p95 y throughput sobre imágenes locales y registra
parámetros, métricas, tags y artefactos (`latency_samples.csv`, `summary.md`):

```bash
export PPE_MODEL_PATH=artifacts/drive/yolo11s_clean/weights/best.pt
uv run --extra tracking --extra inference python -m ppe_detection.tracking benchmark \
  --model "$PPE_MODEL_PATH" --images artifacts/samples \
  --iterations 30 --imgsz 640 --conf 0.25
```

Opciones: `--imgsz`, `--conf`, `--iou`, `--device`, `--iterations`, `--experiment`
(por omisión `ppe-detection-inference`) y `--run-name`. La medición excluye el
calentamiento y no depende de la red.

## 4.2 Registrar el modelo

`register` empaqueta la identidad del artefacto (SHA256, versión y ruta), la Model
Card y, opcionalmente, los pesos; lo adjunta al run y crea una versión en el Model
Registry con alias (`production` por omisión):

```bash
uv run --extra tracking python -m ppe_detection.tracking register \
  --run-id <run_id> \
  --model "$PPE_MODEL_PATH" \
  --model-card docs/model-card.md
```

La versión registrada apunta a `runs:/<run_id>/model` y lleva los tags
`model_reference`, `model_sha256` y `model_version`, de modo que coincide con lo que
publica `/health` y con lo que carga el backend.

## 5. Evidencia local (2026-11-13)

### 5.1 Sesiones de inferencia (2026-11-13)

Backend: `sqlite:///mlflow.db` · experimento: **`ppe-detection-inference`**.
Mismo modelo (`sha256:E51EB080…D7A9959`), 2 imágenes de `artifacts/samples`,
20 iteraciones por run.

| Run | `run_id` | `imgsz` | `conf` | Latencia media | p95 | Throughput |
|-----|----------|--------:|-------:|---------------:|----:|-----------:|
| `infer-640-conf0.25` | `bf930b6f1633487dbe6f645edd5adb44` | 640 | 0.25 | 82,37 ms | 90,32 ms | 12,14 fps |
| `infer-640-conf0.4` | `83827402ec2e4593aff298e7b28f8fa4` | 640 | 0.40 | 77,95 ms | 88,12 ms | 12,83 fps |
| `infer-416-conf0.25` | `f2eb13651ed14bf6bb827cebed7f7207` | 416 | 0.25 | 41,45 ms | 44,42 ms | 24,13 fps |

Cada run registra `latency_samples.csv` y `summary.md`. El run base contiene además el
paquete del modelo.

**Model Registry:** `ppe-detection` versión **1**, alias **`production`**, origen
`runs:/bf930b6f1633487dbe6f645edd5adb44/model`, con `model_identity.json`,
`MODEL_CARD.md`, `README.md` y `best.pt`. Tags: `model_reference`,
`model_sha256` y `model_version = yolo11s_clean`.

### 5.2 Evaluaciones históricas (2026-11-11)

Registradas en una base local anterior (no versionada). Se conservan como referencia
de las particiones evaluadas en HU-008.

| Run | `run_id` | Partición | Imágenes | P | R | mAP50 | mAP50-95 |
|-----|----------|-----------|---------:|---:|---:|---:|---:|
| `eval492` | `b4187e62c6784effbae5552abac02468` | eval sin fuga (492) | 492 | 0.8738 | 0.6445 | 0.7259 | 0.4239 |
| `test1094` | `00771caaba4f444685bdd65e2b67f87c` | test limpio (1.094) | 1.094 | 0.7998 | 0.7672 | 0.8101 | 0.5162 |

Ambos runs compartían el modelo y registraban `summary.json` y `summary.md` como
artefactos.

> La clave `dataset_split` es la del YAML de evaluación. El YAML del eval sin fuga
> mapea `test` a `test_original_sin_fuga`; por eso los dos runs muestran `test` ahí.
> El nombre del run y el número de imágenes (492 vs 1.094) los distinguen.

## 6. Política de artefactos

- **Los pesos no se versionan en Git.** El comando `log` rechaza `.pt`, `.pth`,
  `.onnx`, `.safetensors`, `.h5` y datasets `.zip`.
- El **Model Registry local** puede contener una copia del artefacto en el almacén
  local de MLflow (`mlruns/`, ignorado por Git) para que la versión registrada
  sea autocontenida; se omite con `--no-weights`.
- La referencia estable sigue siendo el SHA256; el backend carga los pesos desde
  `PPE_MODEL_PATH`, fuera del repositorio.
- Los resúmenes, muestras de latencia y gráficos sí se registran como artefactos.
- `mlflow.db`, `mlruns/` y `mlartifacts/` no se versionan.

## 7. Reproducción

1. Ejecuta la evaluación de HU-008 para generar `summary.json` y `summary.md`.
2. Registra cada partición con `python -m ppe_detection.tracking log`.
3. Compara los `run_id` con `compare` o consulta la UI.
4. Para repetir la evidencia, usa los mismos `summary.json` y el mismo backend local;
   los `run_id` cambiarán porque MLflow genera identificadores nuevos.

## 8. Problemas frecuentes

| Síntoma | Causa / solución |
|---------|------------------|
| `Falta mlflow` | `uv sync --extra tracking` o `uv run --extra tracking ...` |
| `database is locked` | Cierra la UI u otro proceso que use `mlflow.db` |
| La UI no ve los runs | Usa el mismo `--backend-store-uri` con el que registraste |
| `No se encontró el run` | Revisa el `run_id` y el backend; los IDs son locales |
