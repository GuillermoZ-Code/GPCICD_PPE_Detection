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

## Detector real (HU-002)

`YoloDetector` adapta un artefacto Ultralytics al protocolo `Detector`:

- Carga perezosa de `ultralytics`: las pruebas unitarias no requieren torch.
- `conf`, `iou`, `imgsz` y `device` configurables; la CLI los registra.
- Convierte la entrada RGB a BGR antes de `predict` (Ultralytics asume BGR en arrays
  NumPy).
- Exige que el catálogo del modelo sea exactamente `CLASSES`; un modelo COCO u otro
  catálogo de EPP se rechaza.
- Recorta las cajas a la imagen y descarta cajas degeneradas antes de construir
  `Detection`.
- Sin resultados devuelve `[]`.

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
