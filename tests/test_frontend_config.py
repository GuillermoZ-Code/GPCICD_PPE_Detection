"""AC-02 (HU-072) — proxy de Vite para la ruta relativa `/api`.

Pruebas estáticas: leen `frontend/vite.config.ts` sin levantar Vite, Node ni la API.
"""

from __future__ import annotations

from pathlib import Path

VITE_CONFIG = Path("frontend/vite.config.ts")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


def test_vite_proxies_api_prefix_to_local_api() -> None:
    """AC-02: el servidor de desarrollo reenvía `/api` a la API local."""
    # Arrange / Act
    config = _read(VITE_CONFIG)

    # Assert
    assert "'/api':" in config
    assert "target: env.VITE_API_PROXY || 'http://localhost:8000'" in config
    assert "changeOrigin: true" in config


def test_vite_proxy_rewrites_api_prefix() -> None:
    """AC-02: el prefijo `/api` se elimina antes de llegar a FastAPI."""
    # Arrange / Act
    config = _read(VITE_CONFIG)

    # Assert
    assert "rewrite:" in config
    assert r"path.replace(/^\/api/, '')" in config
