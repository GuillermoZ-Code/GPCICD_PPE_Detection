# Contrato de inferencia `ImageData → list[Detection]`

> Fuente única: [`src/ppe_detection/contracts.py`](../../src/ppe_detection/contracts.py).
> Decisión: [ADR 0005](../adr/0005-contract-first.md). Spec: [`specs/001-ta-contract-first`](../../specs/001-ta-contract-first/spec.md).

El contrato permite que la API (HU-006), la interfaz (HU-007) y gRPC (HU-010)
trabajen con `FakeDetector` mientras HU-002 implementa el detector real. Ninguna capa
puede duplicar estos tipos.

## Catálogo de clases

El orden es el del `data.yaml` del dataset y el del checkpoint entrenado:

| `class_id` | `class_name` canónico | Etiqueta de presentación |
|---:|---|---|
| 0 | `Gloves` | Guantes |
| 1 | `Vest` | Chaleco |
| 2 | `goggles` | Gafas |
| 3 | `helmet` | Casco |
| 4 | `mask` | Mascarilla |
| 5 | `safety_shoe` | Calzado de seguridad |

`class_name` se conserva tal como lo entrega el modelo; la capitalización y la
traducción son responsabilidad de la interfaz (HU-003/HU-007).

## `ImageData`

Imagen decodificada, inmutable.

| Campo | Tipo | Regla |
|---|---|---|
| `array` | `numpy.ndarray` | `uint8`, forma `(alto, ancho, 3)`, RGB |
| `width` | `int` | > 0 y coincide con `array.shape[1]` |
| `height` | `int` | > 0 y coincide con `array.shape[0]` |
| `format` | `str` | `jpeg` o `png` |
| `source` | `str` | ruta o etiqueta de origen (por ejemplo, `upload`) |

La construcción valida las reglas y lanza `ContractError` si no se cumplen.

## `Detection`

Detección individual, inmutable.

| Campo | Tipo | Regla |
|---|---|---|
| `class_id` | `int` | 0–5, índice del catálogo |
| `class_name` | `str` | debe coincidir con `CLASSES[class_id]` |
| `confidence` | `float` | finita y en `[0, 1]` |
| `bbox` | `tuple[float, float, float, float]` | `x1, y1, x2, y2` en píxeles; `x1 < x2`, `y1 < y2` y dentro de la imagen |
| `image_width` | `int` | > 0 |
| `image_height` | `int` | > 0 |

`bbox` usa `xyxy`. Si el modelo entrega coordenadas fuera de la imagen, el adaptador
debe recortarlas antes de construir la `Detection`.

## `Detector`

```python
class Detector(Protocol):
    def detect(self, image: ImageData) -> list[Detection]: ...
```

- Devuelve una lista, nunca `None`.
- Sin detecciones devuelve `[]`; no es un error.
- No entrena ni descarga pesos.

## `FakeDetector`

Implementación determinista para pruebas y desarrollo paralelo:

```python
from ppe_detection.contracts import FakeDetector

detector = FakeDetector()  # siempre []
detector = FakeDetector([detection])  # siempre la misma lista
```

No depende de GPU, dataset, pesos ni red.

## Errores

- `ContractError(ValueError)`: violación del contrato.
- `InvalidImageError(ValueError)`: archivo vacío, corrupto o de formato no admitido.
- `FileNotFoundError`: la ruta no existe.

## Carga de imágenes (HU-001)

```python
from ppe_detection.io import load_image, load_image_bytes

image = load_image("ruta/foto.png")
image = load_image_bytes(data, source="upload")
```

La carga decodifica a RGB, conserva las dimensiones originales y **no ejecuta
inferencia**.

## Validación de entrada (HU-005)

`validate_image_bytes(data, source="upload")` es la puerta de entrada para la API y la
interfaz. Aplica las mismas reglas que `load_image` y `load_image_bytes`:

- Acepta **JPEG o PNG** detectados por contenido, no por extensión.
- Rechaza archivos vacíos, corruptos o de más de **10 MB** (`MAX_IMAGE_BYTES`).
- Lanza `InvalidImageError` con un mensaje en español.
- No importa ni ejecuta `YoloDetector`: la validación ocurre antes de la inferencia.

La API de HU-006 puede capturar `InvalidImageError` y responder con un error de cliente
4xx sin duplicar la lógica.

## Detector real (HU-002)

`YoloDetector` adapta un artefacto Ultralytics al protocolo `Detector`:

- Carga perezosa de `ultralytics`: las pruebas unitarias no requieren torch.
- `conf`, `iou`, `imgsz` y `device` configurables; la CLI los registra en `run.json`.
- Convierte la entrada RGB a BGR antes de `predict` (Ultralytics asume BGR en arrays
  NumPy).
- Exige que el catálogo del modelo sea exactamente `CLASSES`; un modelo COCO u otro
  catálogo de EPP se rechaza.
- Recorta las cajas a la imagen y descarta cajas degeneradas antes de construir
  `Detection`.
- Sin resultados devuelve `[]`.

### Manifiesto de la ejecución

Cada corrida de `python -m ppe_detection.detection.predict` escribe, junto a
`detections.csv`, un `run.json` con la procedencia de la inferencia:

| Bloque | Contenido |
|---|---|
| `generated_at` | fecha UTC de la ejecución |
| `code` | paquete, versión instalada y commit del repositorio |
| `model` | ruta, SHA256 y tamaño del artefacto |
| `parameters` | `conf`, `iou`, `imgsz`, `device` y `seed` |
| `images` | ruta, dimensiones, formato y número de detecciones por imagen |
| `totals` | imágenes procesadas, con detecciones y total de detecciones |

Con esto se cumple la regla de reproducibilidad de `CONSTITUTION.md` §6: semilla,
versión del modelo, tamaño de imagen y umbrales quedan registrados en cada
inferencia. Con `conf` e `iou` fijos la inferencia no tiene componentes estocásticos;
la semilla se registra para trazabilidad.

Instalación del extra:

```bash
uv sync --extra inference
```

Uso:

```python
from ppe_detection.detection import YoloDetector
from ppe_detection.io import load_image

detector = YoloDetector("artifacts/models/yolo11s_clean/weights/best.pt")
detections = detector.detect(load_image("foto.jpg"))
```

## Visualización (HU-003)

`draw_detections` convierte una lista de `Detection` en una imagen anotada:

```python
from ppe_detection.io import load_image
from ppe_detection.visualization import draw_detections

annotated = draw_detections(load_image("foto.jpg"), detections)
```

- Devuelve una `ImageData` nueva; **no** modifica la entrada.
- Cada detección se dibuja con su caja, la categoría en español y la confianza
  (`Casco 0.87`). Los nombres canónicos del contrato no cambian.
- La caja usa los píxeles de `Detection`. Si el lienzo tiene otro tamaño, las
  coordenadas se escalan proporcionalmente (AC-003.2).
- Sin detecciones devuelve la imagen intacta, sin cajas (AC-003.3).
- El grosor y la fuente crecen con el lado mayor de la imagen.

La CLI de inferencia puede guardar las anotaciones con `--annotated`:

```bash
uv run --extra inference python -m ppe_detection.detection.predict \
    --model artifacts/models/yolo11s_clean/weights/best.pt \
    --source artifacts/samples --annotated
# genera artifacts/predictions/demo/annotated/*.png
```

## Contrato de resultado vacío (HU-004)

`ppe_detection.results` clasifica la salida de la inferencia y fija el mensaje de
las respuestas sin objetos, para que API (HU-006), interfaz (HU-007) y gRPC
(HU-010) compartan la misma semántica:

- `InferenceResult`: envuelve `detections`, `is_empty`, `is_error` y `message`.
- `build_inference_result(detections)`: `_ → []` es éxito sin objetos
  (`is_empty=True`, `is_error=False`); `None` es error de contrato, no se
  normaliza a vacío.
- `build_error_result(error)`: fallos reales (imagen corrupta, artefacto ausente)
  se clasifican `is_error=True` y no comparten el mensaje vacío.
- `NO_DETECTIONS_MESSAGE = "No se detectaron objetos EPP en la imagen."`: su
  redacción es por detección; no afirma incumplimiento ni ausencia real de EPP.
- `RESPONSIBLE_USE_NOTE`: nota de uso responsable disponible para API/UI.
- Integración CLI (HU-004, FR-008): `format_summary` de
  `detection/predict.py` imprime `NO_DETECTIONS_MESSAGE` cuando la corrida no
  genera detecciones y sale con código 0; los fallos de carga reales se lanzan
  como excepciones (`InvalidImageError`, `FileNotFoundError`).

```python
from ppe_detection.results import build_inference_result

result = build_inference_result(detector.detect(load_image("foto.jpg")))
result.is_empty, result.message
# (True, 'No se detectaron objetos EPP en la imagen.')
```

Pruebas: `tests/test_results.py` (AC-004.1..AC-004.3, refs de issue #4).
