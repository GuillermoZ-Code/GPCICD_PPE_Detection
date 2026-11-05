"""Detección de EPP con YOLO."""

from ppe_detection.detection.yolo import (
    DEFAULT_CONF,
    DEFAULT_DEVICE,
    DEFAULT_IMGSZ,
    DEFAULT_IOU,
    YoloDetector,
)

__all__ = [
    "DEFAULT_CONF",
    "DEFAULT_DEVICE",
    "DEFAULT_IMGSZ",
    "DEFAULT_IOU",
    "YoloDetector",
]
