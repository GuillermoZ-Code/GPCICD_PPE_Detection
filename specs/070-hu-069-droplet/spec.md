# Feature Specification: HU-069 — Aprovisionar el Droplet

**Feature Branch**: `docs/070-hu-069-spec`

**Created**: 2026-11-27

**Status**: Reconstruida (issue #125 cerrada)

**Input**: Issue #125 — «HU-069 — Aprovisionar el Droplet: Docker, usuario y
firewall». Épica `ep-07`, 3 SP, 12 pruebas objetivo. Depende de —.

> Esta spec reconstruye el artefacto que faltaba al cerrar #125. El script y sus
> pruebas ya están en `develop`; aquí se documentan los AC, las decisiones y la
> trazabilidad que exige la compuerta `Matriz`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Servidor listo para desplegar (Priority: P0)

Como operador, quiero un servidor con Docker, un usuario de despliegue y un firewall
mínimo, para alojar el sistema sin abrir puertos innecesarios ni permitir acceso
como root.

**Why this priority**: sin un servidor preparado no existe despliegue posible; el
pipeline de HU-070 necesita SSH, Docker y los puertos 80/443.

**Independent Test**: se ejecuta `deploy/droplet/provision.sh` en una máquina
Ubuntu limpia y se comprueba el usuario, SSH, UFW, fail2ban y Docker.

**Acceptance Scenarios** (AC de la issue #125):

1. **AC-01**: **Dado** un servidor nuevo, **Cuando** se aprovisiona, **Entonces**
   existe el usuario `deploy` sin contraseña, con llave SSH, y root por SSH queda
   deshabilitado.
2. **AC-02**: **Dado** el servidor aprovisionado, **Cuando** se revisa el firewall,
   **Entonces** UFW solo permite 22, 80 y 443, y fail2ban está activo.
3. **AC-03**: **Dado** el mismo servidor, **Cuando** se ejecuta el script otra vez,
   **Entonces** no duplica usuarios, reglas ni directorios.

### Edge Cases

- Falta `DEPLOY_PUBKEY`: el script termina con código 64 y un mensaje claro.
- Docker ya instalado: no se vuelve a descargar el instalador.
- Usuario `deploy` existente: no se recrea ni se borra su `authorized_keys`.
- Reinicio del servidor: UFW y fail2ban quedan habilitados.
- Directorio `/opt/ppe` existente: se conserva y se asegura la carpeta de modelos.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El script MUST crear `deploy` sin contraseña (`passwd -l`) y con
  `authorized_keys` en modo 0600.
- **FR-002**: El script MUST escribir `PermitRootLogin no` y
  `PasswordAuthentication no` en `sshd_config.d`.
- **FR-003**: UFW MUST tener política de entrada denegada y permitir solo 22, 80 y
  443/tcp.
- **FR-004**: fail2ban MUST quedar habilitado para `sshd`.
- **FR-005**: El script MUST ser idempotente para usuario, Docker y directorios.
- **FR-006**: El script MUST crear `/opt/ppe` y `/opt/ppe/models`.
- **FR-007**: La llave pública MUST recibirse por `DEPLOY_PUBKEY`; no se versiona.
- **FR-008**: No se MUST abrir ningún puerto adicional ni usar contraseñas SSH.

### Key Entities

- **Droplet**: servidor Ubuntu 24.04 LTS del curso.
- **Usuario `deploy`**: cuenta sin contraseña, solo por llave, en el grupo `docker`.
- **UFW/fail2ban**: firewall y protección de fuerza bruta.
- **`/opt/ppe`**: directorio de trabajo para compose, Caddyfile y modelo.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 Usuario y root | `tests/test_deploy.py::test_provision_creates_a_passwordless_deploy_user`, `tests/test_deploy.py::test_provision_disables_root_and_password_login` |
| AC-02 Firewall y fail2ban | `tests/test_deploy.py::test_firewall_allows_only_ssh_http_and_https`, `tests/test_deploy.py::test_fail2ban_is_enabled` |
| AC-03 Idempotencia y directorios | `tests/test_deploy.py::test_provision_is_idempotent`, `tests/test_deploy.py::test_provision_creates_the_work_directory` |

## Success Criteria *(mandatory)*

- **SC-001**: El script se ejecuta una vez y deja el servidor listo para HU-070.
- **SC-002**: Los seis AC se verifican con pruebas estáticas sin servidor real.
- **SC-003**: El script es idempotente y no contiene secretos.
- **SC-004**: `make check` y `make specs-check` quedan en verde.

## Out of Scope

- Crear el Droplet en el proveedor (lo hace el operador).
- Instalar Caddy o el compose de producción (HU-071).
- Configurar el dominio o el certificado HTTPS (HU-041).
- Guardar la llave privada; solo se usa la pública.

## Assumptions

- El servidor es Ubuntu 24.04 LTS y se entra como root la primera vez.
- La llave pública se pasa por entorno y no se versiona.
- El pipeline de HU-070 llega por SSH con el usuario `deploy`.
- El modelo se copia después a `/opt/ppe/models` y se monta `:ro`.
