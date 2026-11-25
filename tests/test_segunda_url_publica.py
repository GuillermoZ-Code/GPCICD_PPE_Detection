"""Pruebas estructurales de la segunda URL pública MaaS (HU-053, #109)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "maas" / "segunda-url.md"
ALT_DIR = ROOT / "deploy" / "maas-alt"
DOCKERFILE = ALT_DIR / "Dockerfile"
DOCKERIGNORE = ALT_DIR / ".dockerignore"
CARD = ALT_DIR / "README.md"
REPO_URL = "https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection"
DATASET_URL = "https://huggingface.co/datasets/51ddhesh/PPE_Detection"


def _text(path: Path) -> str:
    """Arrange: contenido UTF-8 de un artefacto del despliegue alternativo."""
    return path.read_text(encoding="utf-8")


def test_decision_hf_spaces_justificada_ac_01() -> None:
    """AC-01: el runbook elige Spaces y compara con Cloud Run."""
    # Arrange / Act
    runbook = _text(RUNBOOK)

    # Assert
    assert "Hugging Face Spaces" in runbook
    assert "Cloud Run" in runbook
    assert "Elegida" in runbook
    assert "capa gratuita" in runbook


def test_space_card_identifica_destino_ac_01() -> None:
    """AC-01: la tarjeta identifica el destino y el puerto que publica."""
    # Arrange / Act
    card = _text(CARD)

    # Assert
    assert "Hugging Face Spaces" in card
    assert "Docker" in card
    assert "<SPACE_URL>" in card


def test_dockerfile_expone_puerto_spaces_ac_01() -> None:
    """AC-01: el contenedor escucha en el puerto que espera Spaces."""
    # Arrange / Act
    dockerfile = _text(DOCKERFILE)

    # Assert
    assert "EXPOSE 7860" in dockerfile
    assert "PORT=7860" in dockerfile
    assert "--host 0.0.0.0" in dockerfile
    assert "--port 7860" in dockerfile


def test_sin_dominio_inventado_ac_01() -> None:
    """AC-01: la URL se deja como plantilla hasta crear el Space."""
    # Arrange / Act
    runbook = _text(RUNBOOK)
    card = _text(CARD)

    # Assert
    assert "<SPACE_URL>" in runbook
    assert "<SPACE_URL>" in card
    assert "no se inventa" in runbook.lower()


def test_documento_registra_limitaciones_ac_01() -> None:
    """AC-01: se documentan CPU, tamaño y ausencia de pesos en la imagen."""
    # Arrange / Act
    runbook = _text(RUNBOOK)

    # Assert
    for dato in ("CPU", "10 MB", "pesos"):
        assert dato in runbook, f"falta documentar {dato}"


def test_secretos_como_variables_de_entorno_ac_01() -> None:
    """AC-01: los secretos se declaran como Secrets del Space, no en el repo."""
    # Arrange / Act
    runbook = _text(RUNBOOK)

    # Assert
    assert "HF_TOKEN" in runbook
    assert "Secrets" in runbook
    assert "no se versionan" in runbook


def test_card_atribuye_dataset_cc_by_ac_02() -> None:
    """AC-02: la tarjeta visible atribuye el dataset CC-BY-4.0."""
    # Arrange / Act
    card = _text(CARD)

    # Assert
    assert DATASET_URL in card
    assert "CC-BY-4.0" in card


def test_card_enlaza_codigo_agpl_ac_02() -> None:
    """AC-02: la tarjeta enlaza el código fuente bajo AGPL-3.0-only."""
    # Arrange / Act
    card = _text(CARD)

    # Assert
    assert REPO_URL in card
    assert "AGPL-3.0-only" in card


def test_doc_explica_atribucion_visible_ac_02() -> None:
    """AC-02: el runbook explica que el README del Space es público."""
    # Arrange / Act
    runbook = _text(RUNBOOK)

    # Assert
    assert "README.md" in runbook
    assert "Space" in runbook
    assert "CC-BY-4.0" in runbook


def test_licencias_no_se_relicencian_ac_02() -> None:
    """AC-02: CC-BY aplica al dataset y AGPL al código, sin relicenciar."""
    # Arrange / Act
    runbook = _text(RUNBOOK)
    card = _text(CARD)

    # Assert
    assert "licencia del dataset" in runbook
    assert "AGPL-3.0-only" in runbook
    assert "licencia del dataset" in card


def test_dockerfile_congela_lock_ac_03() -> None:
    """AC-03: la imagen instala dependencias con uv y lock congelado."""
    # Arrange / Act
    dockerfile = _text(DOCKERFILE)

    # Assert
    assert "uv sync --frozen" in dockerfile
    assert "COPY pyproject.toml uv.lock" in dockerfile
    assert "pip install" not in dockerfile


def test_dockerfile_no_copia_secretos_ac_03() -> None:
    """AC-03: el Dockerfile no hornea secretos ni claves."""
    # Arrange / Act
    dockerfile = _text(DOCKERFILE)

    # Assert
    for patron in (".env", "HF_TOKEN=", "API_KEY=", "token="):
        assert patron not in dockerfile, f"secreto potencial: {patron}"


def test_dockerignore_excluye_pesos_y_entorno_ac_03() -> None:
    """AC-03: el contexto excluye entornos, pesos, datos y secretos."""
    # Arrange / Act
    ignorados = _text(DOCKERIGNORE)

    # Assert
    for patron in ("*.pt", ".env", ".venv", "runs/", "data/"):
        assert patron in ignorados, f"falta excluir {patron}"


def test_runbook_incluye_build_y_arranque_ac_03() -> None:
    """AC-03: el runbook da comandos concretos de build y arranque."""
    # Arrange / Act
    runbook = _text(RUNBOOK)

    # Assert
    assert "docker build -f deploy/maas-alt/Dockerfile" in runbook
    assert "docker run" in runbook
    assert "PPE_MODEL_PATH" in runbook


def test_modelo_fuera_de_la_imagen_ac_03() -> None:
    """AC-03: los pesos se inyectan en ejecución, nunca se copian."""
    # Arrange / Act
    dockerfile = _text(DOCKERFILE)
    runbook = _text(RUNBOOK)

    # Assert
    assert "COPY" in dockerfile
    assert ".pt" not in dockerfile
    assert "PPE_MODEL_PATH" in runbook
    assert "fuera de la imagen" in runbook


def test_pasos_publicacion_reproducibles_ac_03() -> None:
    """AC-03: la publicación describe Space, Docker, Secrets y puerto."""
    # Arrange / Act
    runbook = _text(RUNBOOK)

    # Assert
    for dato in ("New Space", "Docker", "Secrets", "7860"):
        assert dato in runbook, f"falta el paso {dato}"
