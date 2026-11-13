# Stub manual de `ppe_pb2` para el análisis de tipos (ty).
#
# protobuf genera los mensajes con una metaclass: los atributos no son visibles
# estáticamente. Este .pyi describe la superficie pública que usa HU-010 y se
# mantiene junto a `ppe.proto`; la regeneración (`make protos`) no lo toca.
# Si cambia el contrato, actualiza ambos en el mismo commit.

from collections.abc import Sequence
from typing import Any


class BoundingBox:
    """Caja delimitadora xyxy en píxeles de la imagen original."""

    x1: float
    y1: float
    x2: float
    y2: float

    def __init__(
        self,
        *,
        x1: float = 0.0,
        y1: float = 0.0,
        x2: float = 0.0,
        y2: float = 0.0,
    ) -> None: ...


class Detection:
    """Una detección de EPP del catálogo canónico."""

    class_id: int
    class_name: str
    confidence: float
    bbox: BoundingBox
    image_width: int
    image_height: int

    def __init__(
        self,
        *,
        class_id: int = 0,
        class_name: str = "",
        confidence: float = 0.0,
        bbox: BoundingBox | None = None,
        image_width: int = 0,
        image_height: int = 0,
    ) -> None: ...


class PredictRequest:
    """Solicitud de inferencia: JPEG/PNG completo, hasta 10 MB."""

    image: bytes
    source: str

    def __init__(self, *, image: bytes = b"", source: str = "") -> None: ...

    @classmethod
    def FromString(cls, data: bytes) -> "PredictRequest": ...

    def SerializeToString(self) -> bytes: ...


class PredictResponse:
    """Respuesta estructurada espejo del esquema HTTP de HU-006."""

    DESCRIPTOR: Any
    detections: Sequence[Detection]
    image_width: int
    image_height: int
    model_version: str
    elapsed_ms: float
    message: str
    model_sha256: str
    model_artifact: str
    model_reference: str

    def __init__(
        self,
        *,
        detections: Sequence[Detection] = (),
        image_width: int = 0,
        image_height: int = 0,
        model_version: str = "",
        elapsed_ms: float = 0.0,
        message: str = "",
        model_sha256: str = "",
        model_artifact: str = "",
        model_reference: str = "",
    ) -> None: ...

    @classmethod
    def FromString(cls, data: bytes) -> "PredictResponse": ...

    def SerializeToString(self) -> bytes: ...
