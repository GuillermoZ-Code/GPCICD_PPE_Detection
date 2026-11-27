"""AC-01, AC-02 y AC-03 (HU-049): decisión de no exponer gRPC.

Pruebas estáticas: leen el ADR y la configuración desplegada sin red.
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ADR = REPO / "docs" / "adr" / "0010-exposicion-grpc.md"
COMPOSE = REPO / "compose.prod.yml"
CADDYFILE = REPO / "docker" / "Caddyfile"
PROVISION = REPO / "deploy" / "droplet" / "provision.sh"


def _read(path: Path) -> str:
    """Lee un archivo esperado; su ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


def test_ac_01_decision_con_riesgos_y_alternativa() -> None:
    """AC-01: el ADR 0010 decide, documenta riesgos y evalúa h2c + TLS."""
    adr = _read(ADR)

    assert "ADR 0010" in adr
    assert "Estado:** Aceptada" in adr
    assert "HU-049 (#105)" in adr
    assert "gRPC" in adr
    assert "permanece interno" in adr.lower()
    assert "Alternativas consideradas" in adr
    assert "Consecuencias" in adr
    assert "h2c" in adr
    assert "mTLS" in adr


def test_ac_02_puerto_9000_no_publicado() -> None:
    """AC-02: Compose expone 9000 a la red interna, nunca al host."""
    compose = _read(COMPOSE)

    grpc_block = compose.split("  grpc:", 1)[1].split("  web:", 1)[0]
    assert "expose:" in grpc_block
    assert '"9000"' in grpc_block
    assert "9000:9000" not in compose
    assert '- "9000:' not in compose


def test_ac_02_proxy_sin_ruta_grpc() -> None:
    """AC-02: Caddy no publica gRPC ni usa h2c."""
    caddyfile = _read(CADDYFILE)

    assert "h2c" not in caddyfile
    assert "/grpc" not in caddyfile
    assert "9000" not in caddyfile


def test_ac_03_firewall_coherente() -> None:
    """AC-03: UFW niega entrada salvo SSH, HTTP y HTTPS."""
    provision = _read(PROVISION)

    assert "ufw default deny incoming" in provision
    assert "for port in 22 80 443" in provision
    assert "ufw allow 9000" not in provision
