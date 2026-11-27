"""Pruebas del catálogo de errores de API e interfaz (HU-059)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs" / "manual" / "errores.md"


def _catalog_text() -> str:
    return CATALOG.read_text(encoding="utf-8")


def test_catalogo_documenta_codigos_http_api_ac_01() -> None:
    """AC-01: cada código HTTP usado por la API está documentado."""
    text = _catalog_text()
    for code in ["200", "400", "401", "413", "415", "422", "503"]:
        assert f"| {code} |" in text or f"| {code} " in text, code


def test_catalogo_documenta_estados_grpc_ac_01() -> None:
    """AC-01: cada estado gRPC usado por el servicio está documentado."""
    text = _catalog_text()
    for status in ["OK", "INVALID_ARGUMENT", "UNAVAILABLE", "INTERNAL"]:
        assert status in text, status


def test_catalogo_documenta_mensajes_ui_ac_02() -> None:
    """AC-02: los mensajes visibles de la UI están enlazados a causa/solución."""
    text = _catalog_text()
    ui_messages = [
        "La API respondió con estado",
        "No fue posible analizar la imagen.",
        "No fue posible cargar la información del modelo.",
        "No se detectaron EPP en la imagen.",
        "La confianza más alta fue",
        "La inferencia está tardando más de lo habitual.",
    ]
    for message in ui_messages:
        assert message in text, message
    for heading in ["Causa", "Solución", "Causa probable", "Acción recomendada"]:
        assert heading in text, heading


def test_catalogo_cubre_todos_los_codigos_api_ac_03() -> None:
    """AC-03: todos los códigos HTTP y estados gRPC de la API están en el catálogo."""
    text = _catalog_text()

    api_app = (ROOT / "src" / "ppe_detection" / "api" / "app.py").read_text(encoding="utf-8")
    http_codes = ["200", "400", "401", "413", "415", "422", "503"]
    # Verifica que los códigos explícitos del app estén contemplados.
    for explicit in ["400", "401", "413", "415", "503"]:
        assert f"status_code={explicit}" in api_app or explicit in api_app
    for code in http_codes:
        assert code in text, code

    servicer = (ROOT / "src" / "ppe_detection" / "grpc" / "servicer.py").read_text(encoding="utf-8")
    grpc_statuses = ["OK", "INVALID_ARGUMENT", "UNAVAILABLE", "INTERNAL"]
    for status in grpc_statuses:
        if status != "OK":
            assert f"StatusCode.{status}" in servicer
        assert status in text, status
