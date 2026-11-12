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

El comando usa por defecto `sqlite:///mlflow.db`, con artefactos en `mlartifacts/`.
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
`sha256:<hash>`; los pesos no se copian.

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

## 5. Evidencia local (2026-11-11)

Backend: `sqlite:///mlflow.db` · experimento: `ppe-detection-eval`.

| Run | `run_id` | Partición | Imágenes | P | R | mAP50 | mAP50-95 |
|-----|----------|-----------|---------:|---:|---:|---:|---:|
| `eval492` | `b4187e62c6784effbae5552abac02468` | eval sin fuga (492) | 492 | 0.8738 | 0.6445 | 0.7259 | 0.4239 |
| `test1094` | `00771caaba4f444685bdd65e2b67f87c` | test limpio (1.094) | 1.094 | 0.7998 | 0.7672 | 0.8101 | 0.5162 |

Ambos runs comparten el modelo
`sha256:E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959` y registran
solo `summary.json` y `summary.md` como artefactos. La consulta con
`MlflowClient.list_artifacts` devolvió esos dos archivos y ningún `.pt`.

> La clave `dataset_split` es la del YAML de evaluación. El YAML del eval sin fuga
> mapea `test` a `test_original_sin_fuga`; por eso los dos runs muestran `test` ahí.
> El nombre del run y el número de imágenes (492 vs 1.094) los distinguen.

## 6. Política de artefactos

- **No se registran pesos** (`.pt`, `.pth`, `.onnx`, `.safetensors`, `.h5`) ni datasets
  (`.zip`). `log` los rechaza antes de llamar a MLflow.
- La referencia del modelo es el SHA256 y su ruta; los pesos siguen fuera de Git y de
  MLflow.
- Los resúmenes y gráficos sí se registran como artefactos del run.
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
