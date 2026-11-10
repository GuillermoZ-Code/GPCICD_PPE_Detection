"""Punto de entrada para `python -m ppe_detection.api`."""

from __future__ import annotations

import os

import uvicorn


def main() -> None:
    """Levanta la API con uvicorn."""
    uvicorn.run(
        "ppe_detection.api.app:app",
        host=os.getenv("PPE_API_HOST", "0.0.0.0"),
        port=int(os.getenv("PPE_API_PORT", "8000")),
    )


if __name__ == "__main__":
    main()
