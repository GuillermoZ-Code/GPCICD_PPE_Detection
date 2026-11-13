"""Etiquetas y colores del overlay, y utilidades del lanzador (AC-003.1)."""

from __future__ import annotations

import pytest

from ppe_detection.contracts import CLASSES, Detection
from ppe_detection.tools import launcher
from ppe_detection.visualization.overlay import COLORS, format_label

EXPECTED_LABELS: dict[str, str] = {
    "Gloves": "Guantes",
    "Vest": "Chaleco",
    "goggles": "Gafas",
    "helmet": "Casco",
    "mask": "Mascarilla",
    "safety_shoe": "Calzado",
}


def _detection(class_id: int, class_name: str) -> Detection:
    return Detection(
        class_id=class_id,
        class_name=class_name,
        confidence=0.5,
        bbox=(1.0, 1.0, 5.0, 5.0),
        image_width=10,
        image_height=10,
    )


def test_format_label_translates_every_class() -> None:
    # Arrange
    assert set(EXPECTED_LABELS) == set(CLASSES)

    # Act / Assert
    for class_id, class_name in enumerate(CLASSES):
        label = format_label(_detection(class_id, class_name))
        assert label == f"{EXPECTED_LABELS[class_name]} 0.50"


def test_class_colors_are_distinct() -> None:
    # Arrange
    colors = [COLORS[name] for name in CLASSES]

    # Act / Assert
    assert len(set(colors)) == len(CLASSES)
    assert all(0 <= channel <= 255 for color in colors for channel in color)


def test_launcher_parse_args_defaults() -> None:
    # Arrange / Act
    args = launcher.parse_args([])

    # Assert
    assert args.model is None
    assert (args.host, args.api_port, args.web_port) == ("127.0.0.1", 8000, 5173)
    assert args.timeout == 60.0


def test_launcher_parse_args_accepts_overrides() -> None:
    # Arrange
    argv = [
        "--model",
        "artifacts/models/best.pt",
        "--host",
        "0.0.0.0",
        "--api-port",
        "9100",
        "--web-port",
        "4100",
        "--timeout",
        "5.5",
    ]

    # Act
    args = launcher.parse_args(argv)

    # Assert
    assert args.model == "artifacts/models/best.pt"
    assert (args.host, args.api_port, args.web_port) == ("0.0.0.0", 9100, 4100)
    assert args.timeout == 5.5


def test_web_env_points_frontend_to_api(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setenv("EXISTING_FLAG", "1")

    # Act
    env = launcher.web_env("http://127.0.0.1:8000")

    # Assert
    assert env["VITE_API_URL"] == "http://127.0.0.1:8000"
    assert env["EXISTING_FLAG"] == "1"
