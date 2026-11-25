"""Pruebas del job Docker + Trivy en CI (HU-083, issue #139)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
RUNBOOK = ROOT / "docs" / "operacion" / "docker.md"


def _workflow() -> str:
    """Devuelve el contenido del workflow de CI."""
    return WORKFLOW.read_text(encoding="utf-8")


def _job() -> str:
    """Devuelve el bloque del job `docker`, sin los jobs anteriores."""
    return _workflow().split("  docker:\n", 1)[1]


def test_job_construye_imagen_runtime_ac_01() -> None:
    """AC-01: el job existe, tiene nombre propio y construye el target runtime."""
    # Arrange / Act
    texto = _workflow()
    bloque = _job()

    # Assert
    assert "  docker:\n" in texto
    assert "name: Docker y Trivy" in bloque
    assert "docker build --target runtime -t gpcicd-ppe-detection:ci ." in bloque


def test_smoke_no_monta_modelo_ac_01() -> None:
    """AC-01: el smoke no monta volúmenes ni define PPE_MODEL_PATH."""
    # Arrange
    bloque = _job()
    smoke = bloque.split("- name: Smoke sin modelo", 1)[1].split("- name:", 1)[0]

    # Act / Assert
    assert "docker run --rm --entrypoint python gpcicd-ppe-detection:ci" in smoke
    assert "-v" not in smoke
    assert "PPE_MODEL_PATH" not in smoke


def test_smoke_construye_la_api_sin_pesos_ac_01() -> None:
    """AC-01: el smoke crea la API sin arrancar el servidor ni cargar pesos."""
    # Arrange / Act
    bloque = _job()

    # Assert
    assert "--entrypoint python" in bloque
    assert "from ppe_detection.api import create_app" in bloque
    assert "app = create_app()" in bloque
    assert "app.version" in bloque


def test_trivy_escanea_la_imagen_del_job_ac_02() -> None:
    """AC-02: Trivy escanea exactamente la imagen construida en el job."""
    # Arrange / Act
    bloque = _job()

    # Assert
    assert "uses: aquasecurity/trivy-action@v0.33.0" in bloque
    assert "image-ref: gpcicd-ppe-detection:ci" in bloque


def test_trivy_reporta_high_y_critical_en_sarif_ac_02() -> None:
    """AC-02: el escaneo reporta HIGH/CRITICAL en SARIF sin fallar por hallazgos."""
    # Arrange / Act
    bloque = _job()

    # Assert
    assert "severity: HIGH,CRITICAL" in bloque
    assert "format: sarif" in bloque
    assert "output: trivy-results.sarif" in bloque
    assert "ignore-unfixed: true" in bloque
    assert "exit-code: '0'" in bloque


def test_reporte_se_publica_como_artefacto_ac_03() -> None:
    """AC-03: el SARIF se publica como artefacto y su ausencia es un error."""
    # Arrange / Act
    bloque = _job()

    # Assert
    assert "uses: actions/upload-artifact@v4" in bloque
    assert "name: trivy-sarif" in bloque
    assert "path: trivy-results.sarif" in bloque
    assert "if-no-files-found: error" in bloque


def test_job_tiene_permisos_para_artefactos_ac_03() -> None:
    """AC-03: el job puede publicar artefactos y solo leer el repositorio."""
    # Arrange
    bloque = _job()
    permissions = bloque.split("permissions:\n", 1)[1].split("\n    steps:", 1)[0]

    # Act / Assert
    assert "contents: read" in permissions
    assert "actions: write" in permissions


def test_runbook_documenta_el_escaneo_automatico_ac_03() -> None:
    """AC-03: el runbook explica el job y cómo descargar el reporte."""
    # Arrange / Act
    texto = RUNBOOK.read_text(encoding="utf-8")

    # Assert
    assert "Docker y Trivy" in texto
    assert "trivy-sarif" in texto
    assert "trivy-results.sarif" in texto
