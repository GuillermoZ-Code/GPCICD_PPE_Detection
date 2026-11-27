"""HU-070 y HU-069 — despliegue con rollback y aprovisionamiento.

Pruebas estáticas: leen el pipeline y los scripts sin conectarse al servidor.
"""

from __future__ import annotations

from pathlib import Path

PIPELINE = Path(".gitlab-ci.yml")
DEPLOY = Path("deploy/deploy.sh")
PROVISION = Path("deploy/droplet/provision.sh")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------- HU-070 · AC-01


def test_deploy_job_runs_after_the_image_is_published() -> None:
    """AC-01: el despliegue usa la imagen que construyó el pipeline."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "deploy:" in pipeline
    assert "needs:\n    - build_image" in pipeline
    assert "- deploy" in pipeline


def test_ssh_key_comes_from_a_file_variable_and_is_protected() -> None:
    """AC-01: la llave no vive en el repositorio y se restringe a 600."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert 'chmod 600 "$SSH_KEY"' in pipeline
    assert "ssh-ed25519" not in pipeline
    assert "PRIVATE KEY" not in pipeline


def test_deploy_copies_compose_caddyfile_and_script() -> None:
    """AC-01: el servidor recibe los archivos versionados, no los inventa."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "compose.prod.yml docker/Caddyfile deploy/deploy.sh" in pipeline
    assert "scp -i" in pipeline


def test_deploy_pulls_and_recreates_with_compose() -> None:
    """AC-01: `docker compose pull` y `up -d` en el servidor."""
    # Arrange
    script = _read(DEPLOY)

    # Assert
    assert "docker compose -f compose.prod.yml pull" in script
    assert "up -d --remove-orphans" in script


# --------------------------------------------------------------- HU-070 · AC-02


def test_script_keeps_the_previous_tag_for_rollback() -> None:
    """AC-02: sin el estado anterior no se puede revertir."""
    # Arrange
    script = _read(DEPLOY)

    # Assert
    assert ".deployed_env" in script
    assert "previous" in script
    assert "rollback ok" in script


def test_smoke_waits_for_healthy_services() -> None:
    """AC-02: el despliegue no se declara bueno sin healthchecks en verde."""
    # Arrange
    script = _read(DEPLOY)

    # Assert
    assert "State.Health.Status" in script
    assert "healthy" in script
    assert "wait_for_health" in script


def test_smoke_proves_a_real_inference() -> None:
    """AC-02: `/health/ready` dentro del contenedor, no solo el puerto abierto."""
    # Arrange
    script = _read(DEPLOY)

    # Assert
    assert "health/ready" in script
    assert "exec -T api python -c" in script


def test_failed_deploy_returns_non_zero() -> None:
    """AC-02: un despliegue fallido no puede terminar en verde."""
    # Arrange
    script = _read(DEPLOY)

    # Assert
    assert script.count("exit 1") >= 2


# --------------------------------------------------------------- HU-070 · AC-03


def test_deploy_is_serialized_and_skipped_without_a_server() -> None:
    """AC-03: `resource_group` serializa y sin host el job no se crea."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "resource_group: production" in pipeline
    assert "$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH && $DEPLOY_HOST" in pipeline


def test_deploy_job_has_an_environment() -> None:
    """AC-03: GitLab registra el entorno de producción y su URL."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "name: production" in pipeline
    assert "url: https://$PPE_DOMAIN" in pipeline


# --------------------------------------------------------------- HU-069 · AC-01


def test_provision_creates_a_passwordless_deploy_user() -> None:
    """AC-01: usuario `deploy` sin contraseña, solo con llave."""
    # Arrange
    script = _read(PROVISION)

    # Assert
    assert "useradd --create-home --shell /bin/bash deploy" in script
    assert "passwd -l deploy" in script
    assert "authorized_keys" in script


def test_provision_disables_root_and_password_login() -> None:
    """AC-01: root por SSH y las contraseñas quedan fuera."""
    # Arrange
    script = _read(PROVISION)

    # Assert
    assert "PermitRootLogin no" in script
    assert "PasswordAuthentication no" in script


# --------------------------------------------------------------- HU-069 · AC-02


def test_firewall_allows_only_ssh_http_and_https() -> None:
    """AC-02: UFW deja 22, 80 y 443; nada más."""
    # Arrange
    script = _read(PROVISION)

    # Assert
    assert "for port in 22 80 443" in script
    assert "ufw default deny incoming" in script


def test_fail2ban_is_enabled() -> None:
    """AC-02: fail2ban activo para el servicio sshd."""
    # Arrange
    script = _read(PROVISION)

    # Assert
    assert "fail2ban" in script
    assert "systemctl enable --now fail2ban" in script


# --------------------------------------------------------------- HU-069 · AC-03


def test_provision_is_idempotent() -> None:
    """AC-03: volver a ejecutarlo no duplica usuarios ni reglas."""
    # Arrange
    script = _read(PROVISION)

    # Assert
    assert "if ! id deploy" in script
    assert "if ! command -v docker" in script


def test_provision_creates_the_work_directory() -> None:
    """AC-03: el compose y el modelo tienen dónde vivir."""
    # Arrange
    script = _read(PROVISION)

    # Assert
    assert "install -d -m 0755 /opt/ppe" in script
    assert "install -d -m 0755 /opt/ppe/models" in script
