# Benchmark de latencia CPU — HU-020

**Estado:** Completado.

**Fecha:** 2026-11-23.

**Responsable:** Hernán Estrada (`HestradaUAO`).

**Issue:** #76.

---

## 1. Pregunta

¿Qué combinación de modelo, `imgsz` y formato cumple el objetivo de **<100 ms** en CPU
para el servicio de detección de EPP?

## 2. Entorno y método

| Elemento | Valor |
|---|---|
| Python | 3.13.7 |
| Ultralytics | 8.4.202 |
| torch | 2.15.0+cpu |
| ONNX Runtime | 1.32.0, CPUExecutionProvider |
| CPU | Intel Core i5-1235U, 10 núcleos / 12 hilos |
| Plataforma | Windows 11 |
| `torch` threads | 10 |
| Imagen | sintética 640×640, generada con OpenCV |
| Warm-ups | 5 |
| Repeticiones | 20 |
| Batch | 1 |
| `conf` / `iou` | 0,25 / 0,7 |
| Medición | `model.predict()` completo (pre + inferencia + post) |

Los pesos están fuera de Git. El JSON completo está en
`dist/analisis/latencia/latency_yolo26.json`.

## 3. Modelos

| Nombre | Formato | Clases | Nota |
|---|---|---|---|
| YOLO11s clean | `.pt`, `.onnx` | 6 EPP | baseline productivo |
| YOLO26n clean | `.pt`, `.onnx` | 6 EPP | candidato |
| YOLO26s pretrained | `.pt`, `.onnx` | 80 COCO | solo latencia; sin fine-tuning EPP |

## 4. Resultados

### 4.1 p50 / p95 por modelo y formato

| Modelo | Formato | 640 p50 / p95 | 480 p50 / p95 | 416 p50 / p95 |
|---|---|---:|---:|---:|
| YOLO11s clean | PyTorch | 194,80 / 292,21 | 118,83 / 184,12 | 95,49 / 133,23 |
| YOLO11s clean | ONNX | 183,52 / 280,63 | 214,04 / 264,65 | 173,44 / 221,03 |
| **YOLO26n clean** | **PyTorch** | **80,42 / 109,68** | 86,33 / 95,21 | 72,32 / 83,30 |
| **YOLO26n clean** | **ONNX** | **53,92 / 88,05** | 49,76 / 57,22 | 61,33 / 75,55 |
| YOLO26s pretrained | PyTorch | 281,07 / 353,63 | 150,18 / 185,59 | 153,72 / 179,69 |
| YOLO26s pretrained | ONNX | 123,69 / 190,80 | 119,72 / 132,81 | 118,42 / 138,61 |

### 4.1.1 Revalidación controlada — 2026-11-24

Se repitió el caso **YOLO26n ONNX 640** con el proceso en primer plano, 10 hilos de
PyTorch, OpenCV sin hilos propios, 5 warm-ups y **50 repeticiones**:

| Modelo | Formato | 640 p50 / p95 | Condición |
|---|---|---:|---|
| **YOLO26n clean** | **ONNX** | **33,94 / 40,90 ms** | CPU, imagen sintética 640×640 |

El resultado confirma el objetivo de **<100 ms** y es aún mejor que la medición
original de 53,92 / 88,05 ms. La diferencia se explica por la fijación de hilos y por
una sesión sin carga concurrente; el JSON completo está en
`dist/analisis/latencia/latency_yolo26_onnx_640_2026-11-24.json`.

### 4.2 Cumplimiento de <100 ms

| Combinación | p50 <100 | p95 <100 | Lectura |
|---|---:|---:|---|
| YOLO26n ONNX 640 | ✅ 53,92 | ✅ 88,05 | **Cumple** |
| YOLO26n ONNX 480 | ✅ 49,76 | ✅ 57,22 | Cumple, con más margen |
| YOLO26n ONNX 416 | ✅ 61,33 | ✅ 75,55 | Cumple, sin ventaja sobre 480 |
| YOLO26n PyTorch 640 | ✅ 80,42 | ❌ 109,68 | p95 fuera del objetivo |
| YOLO11s ONNX 640 | ❌ 183,52 | ❌ 280,63 | No cumple |
| YOLO26s ONNX 640 | ❌ 123,69 | ❌ 190,80 | No cumple; preentrenado |

## 5. Recomendación

### Modelo y formato

**YOLO26n + ONNX + `imgsz=640`** es la mejor combinación para producción:

- **p50: 53,92 ms** y **p95: 88,05 ms**.
- Cumple el objetivo de 100 ms en esta máquina.
- Es ~3,4× más rápido que YOLO11s ONNX 640.
- Mantiene la resolución 640, que es la misma usada en entrenamiento y evaluación.

Si se necesita más margen para la API, **480 px ONNX** baja a p50 49,76 / p95 57,22,
pero puede costar precisión en objetos pequeños. **416 px no ofrece ventaja** frente a
480 en esta medición.

### Lo que no recomiendo

- **YOLO26s**: p50 123,69 ms en ONNX 640; no cumple y no está fine-tuneado para EPP.
- **YOLO11s**: el baseline actual no cumple el objetivo en CPU.
- **PyTorch 640**: p95 109,68 ms, ligeramente fuera del objetivo; ONNX es necesario.

### Estado de la decisión

La comparación de calidad de HU-018/HU-019 y el ADR 0009 ya están cerrados. El smoke
local de REST/gRPC con ONNX también se completó. Falta el rollout en Docker/Droplet y
la comprobación de `/health` en ese entorno.

## 6. Límites

- La imagen es sintética; el benchmark mide latencia, no calidad.
- `YOLO26s` es preentrenado COCO; su latencia es de arquitectura, no del modelo EPP.
- La medición es de una máquina de desarrollo, no del Droplet.
- No incluye overhead de FastAPI, gRPC, red ni SPA.
- Los valores 416/480 tienen variabilidad; se reporta p50/p95, no una promesa exacta.

## 7. Reproducibilidad

Configuración fija:

```text
imgsz = 640, 480, 416
warmups = 5
iterations = 20 (original), 50 (revalidación 2026-11-24)
conf = 0.25
iou = 0.7
device = cpu
```

Modelos usados:

```text
artifacts/models/yolo11s_clean/weights/best.pt
artifacts/models/yolo11s_clean/weights/best.onnx
artifacts/models/yolo26n_clean/weights/best.pt
artifacts/models/yolo26n_clean/weights/best.onnx
artifacts/models/yolo26/yolo26s.pt
artifacts/models/yolo26/yolo26s.onnx
```

No se versionan pesos ni imágenes. El JSON de resultados se conserva en
`dist/analisis/latencia/latency_yolo26.json`.

## 8. Conclusión

**YOLO26n ONNX a 640 px cumple <100 ms en CPU** en el equipo de referencia. Es el
candidato técnico para reemplazar a YOLO11s, sujeto a la decisión de calidad de HU-019
y al ADR de HU-023.

## 9. Smoke de servicio — 2026-11-24

Docker no está disponible en este equipo, así que el smoke se ejecutó en proceso con
el artefacto real, usando `TestClient` para REST y un servidor gRPC efímero:

```text
PPE_MODEL_PATH=artifacts/models/yolo26n_clean/weights/best.pt
PPE_MODEL_FORMAT=onnx
PPE_MODEL_VERSION=yolo26n-clean
PPE_MODEL_SHA256=FEFB1F1A…0F27F9
```

| Comprobación | Resultado |
|---|---|
| `/health` | `model_version=yolo26n-clean`, SHA `FEFB1F1A…0F27F9` |
| `POST /predict` | 2 detecciones `Vest` |
| gRPC `Detect` | 2 detecciones `Vest`, 44,22 ms |
| Artefacto cargado | `best.onnx` |
| Evidencia | `dist/analisis/rollout/smoke_rest_grpc.json` |

El REST frío tardó 2.214,63 ms por la carga inicial del modelo; no es una medición de
inferencia en caliente. El smoke confirma que REST y gRPC devuelven las mismas clases
y que `/health` reporta la versión y el SHA correctos cuando las variables se fijan
explícitamente.

**Aviso de despliegue:** `compose.yml` todavía usa `PPE_MODEL_PATH=/models/best.pt` y
`PPE_MODEL_VERSION=best`, y no define `PPE_MODEL_FORMAT=onnx`. Para que el contenedor
reporte la identidad correcta y use ONNX, el compose debe montar `best.onnx` o fijar
las tres variables (`PPE_MODEL_PATH`, `PPE_MODEL_FORMAT` y `PPE_MODEL_VERSION`).
