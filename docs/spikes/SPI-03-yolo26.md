# SPI-03 — Compatibilidad de YOLO26 con el entorno CPU

- **Fecha:** 2026-11-21
- **Estado:** Completado
- **Responsable:** Hernán Estrada (`HestradaUAO`)
- **Habilita:** HU-017, HU-018, HU-019, HU-021
- **Timebox:** 1 día
- **Issue:** #72

## 1. Pregunta

¿Cargan e infieren `yolo26n.pt` y `yolo26s.pt` con Python 3.13, Ultralytics y torch
CPU? ¿La latencia y la forma de salida permiten considerar YOLO26 como reemplazo del
modelo actual YOLO11s?

## 2. Método

- Entorno lockeado del proyecto:

  ```bash
  uv run --extra inference python
  ```

- Pesos preentrenados descargados desde Ultralytics Assets:
  - `yolo26n.pt`
  - `yolo26s.pt`
- Comparación: `artifacts/models/yolo11s_clean/weights/best.pt` (6 clases EPP).
- Imagen sintética 640×640 generada con OpenCV (formas geométricas; no es una imagen
  del dataset).
- 5 warm-ups y 20 inferencias por modelo.
- Configuración: `imgsz=640`, `conf=0.25`, `iou=0.7`, `device=cpu`, `verbose=False`.
- Hardware: Intel Core i5-1235U, 10 núcleos / 12 hilos, Windows 11.
- `torch.get_num_threads() = 10`.

> Los pesos están fuera de Git. Se registran SHA256 y tamaño, pero no se versionan.

## 3. Entorno

| Componente | Versión |
|---|---|
| Python | 3.13.7 |
| Ultralytics | 8.4.202 |
| torch | 2.15.0+cpu |
| OpenCV | instalada por el extra de inferencia |
| Plataforma | Windows 11 (10.0.26200) |
| CPU | Intel Core i5-1235U |

## 4. Resultados

### 4.1 Carga e inferencia

| Modelo | Parámetros | Clases | Carga | Cajas en la imagen sintética | Resultado |
|---|---:|---:|---:|---:|---|
| YOLO26n | 2,572 M | 80 (COCO) | 0,305 s | 1 (`sports ball`) | ✅ carga e infiere |
| YOLO26s | 10,010 M | 80 (COCO) | 0,298 s | 1 (`frisbee`) | ✅ carga e infiere |
| YOLO11s-clean | 9,430 M | 6 (EPP) | 0,202 s | 0 | ✅ carga e infiere |

**AC-01:** ambos modelos YOLO26 cargan e infieren en CPU sin error.

### 4.2 Latencia CPU

| Modelo | p50 | p95 | Mínimo | Máximo |
|---|---:|---:|---:|---:|
| YOLO26n | **159,88 ms** | **223,24 ms** | 128,92 ms | 243,53 ms |
| YOLO26s | **513,84 ms** | **800,50 ms** | 427,84 ms | 872,67 ms |
| YOLO11s-clean | **436,78 ms** | **552,32 ms** | 407,96 ms | 657,01 ms |

- **YOLO26n** es el único candidato razonable para CPU: es ~2,7× más rápido que
  YOLO26s y ~2,7× más rápido que el YOLO11s actual en esta medición.
- Ningún modelo cumple el objetivo de **<100 ms** por imagen.
- La latencia incluye preprocesamiento, inferencia y postprocesamiento de
  `model.predict()`; la API añade overhead adicional.
- La medición es orientativa: el equipo no está aislado y la imagen sintética no
  representa el dataset.

### 4.3 Diferencias de salida frente a YOLO11s

- **Clases:** YOLO26 preentrenado tiene 80 clases COCO; el modelo actual tiene las 6
  clases EPP del `data.yaml`. No se puede reemplazar sin fine-tuning.
- **Contrato:** ambos devuelven `Results` con `boxes.xyxy`, `boxes.conf` y
  `boxes.cls`; el adaptador actual puede consumir la salida, pero el mapeo de clases
  debe venir del modelo fine-tuneado.
- **Modo end-to-end:** en la carga estándar de los checkpoints,
  `model.model.end2end` reportó `False` para YOLO26n/s y YOLO11s. No se probó el
  export ONNX ni un modo NMS-free específico.
- **Parámetros:** YOLO26n es el más pequeño (2,57 M); YOLO26s (10,01 M) es similar a
  YOLO11s (9,43 M), pero mucho más lento en esta máquina.
- **Cajas:** la imagen sintética produjo detecciones distintas y no comparables; no
  se usa para evaluar calidad.

### 4.4 Integridad de los pesos

| Archivo | Tamaño | SHA256 |
|---|---:|---|
| `yolo26n.pt` | 5.544.453 B | `9B09CC8BF347F0FC8A5F7657480587F25DB09B34BF33B0652110FB03A8AD4FEF` |
| `yolo26s.pt` | 20.422.725 B | `646F8BC3FE0A656803D95C294F7852321748CB29D13466A1AF8862E2DB384A1B` |

## 5. Conclusión go/no-go

### GO para compatibilidad y fine-tuning

- YOLO26n y YOLO26s cargan e infieren con Python 3.13 + torch 2.15.0+cpu.
- No se requiere cambiar de Python ni de torch para el spike.
- YOLO26n es el candidato para HU-017/018/019 por tamaño y latencia.
- El contrato de salida es compatible con el adaptador actual.

### NO-GO para reemplazo directo en producción

- Los pesos preentrenados son COCO-80, no EPP-6; requieren fine-tuning.
- **YOLO26n no cumple <100 ms** (p50 160 ms; p95 223 ms).
- **YOLO26s es demasiado lento** para CPU (p50 514 ms; p95 801 ms).
- El modelo actual YOLO11s sigue siendo el fallback productivo.

### Decisión recomendada

1. Fine-tuning de **YOLO26n** primero; YOLO26s solo si la mejora de calidad justifica
   la latencia.
2. Mantener YOLO11s como modelo productivo hasta que HU-019 demuestre una mejora
   clara.
3. Medir ONNX y resoluciones 640/480/416 antes de fijar el modelo definitivo
   (HU-020/HU-022).
4. Registrar la decisión final en el ADR 0009 (HU-023).

## 6. Reproducibilidad

El script usado es efímero y no se versiona; el procedimiento es:

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")
for _ in range(5):
    model.predict(image, imgsz=640, device="cpu", verbose=False)
# medir 20 veces con time.perf_counter()
```

Comando base:

```bash
uv run --extra inference python <script>
```

## 7. Evidencia y límites

- Pesos descargados fuera de Git; no se versionan.
- Imagen sintética generada en memoria; no se versiona.
- No se usó dataset EPP, GPU ni red durante la inferencia (solo la descarga inicial de
  pesos).
- La latencia es de una máquina de desarrollo; no es una medición de producción.
- No se evaluó mAP ni calidad por clase; eso pertenece a HU-018/HU-019.

## 8. Referencias

- Issue #72 — HU-016.
- [SPI-01](SPI-01-compatibilidad-yolo.md) — compatibilidad de YOLO con Python 3.13.
- [SPI-02](SPI-02-baseline-evaluacion.md) — baseline de evaluación.
- [ADR 0001](../adr/0001-modelo-base.md) — detector especializado nivel 3.
- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics).
