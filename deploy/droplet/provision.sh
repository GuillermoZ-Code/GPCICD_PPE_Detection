#!/bin/sh
# =============================================================================
# HU-069 — aprovisionamiento idempotente del Droplet (Ubuntu 24.04 LTS).
#
# Deja el servidor listo para el job `deploy` del pipeline:
#   - usuario `deploy` sin contraseña, solo con llave SSH
#   - root por SSH deshabilitado
#   - UFW con 22, 80 y 443; fail2ban activo
#   - Docker Engine y el plugin compose
#
# Uso (como root, una sola vez por servidor):
#   DEPLOY_PUBKEY="ssh-ed25519 AAAA... equipo" sh provision.sh
#
# Es idempotente: se puede volver a ejecutar sin duplicar usuarios ni reglas.
# =============================================================================

set -eu

pubkey="${DEPLOY_PUBKEY:-}"
if [ -z "$pubkey" ]; then
    echo "falta DEPLOY_PUBKEY con la llave pública del equipo" >&2
    exit 64
fi

export DEBIAN_FRONTEND=noninteractive

apt-get update -qq
apt-get install -y -qq --no-install-recommends ca-certificates curl ufw fail2ban

# --- Docker (script oficial; idempotente por sí mismo) ------------------------
if ! command -v docker >/dev/null 2>&1; then
    curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
    sh /tmp/get-docker.sh
    rm -f /tmp/get-docker.sh
fi

# --- usuario deploy: sin contraseña y solo por llave --------------------------
if ! id deploy >/dev/null 2>&1; then
    useradd --create-home --shell /bin/bash deploy
    passwd -l deploy
fi
groupadd -f docker
usermod -aG docker deploy

install -d -m 0700 -o deploy -g deploy /home/deploy/.ssh
printf '%s\n' "$pubkey" > /home/deploy/.ssh/authorized_keys
chown deploy:deploy /home/deploy/.ssh/authorized_keys
chmod 0600 /home/deploy/.ssh/authorized_keys

# --- sshd: sin root y sin contraseñas ----------------------------------------
cat > /etc/ssh/sshd_config.d/99-ppe.conf <<'EOF'
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
EOF
systemctl reload ssh 2>/dev/null || systemctl reload sshd

# --- UFW: solo 22, 80 y 443 ---------------------------------------------------
ufw default deny incoming >/dev/null
ufw default allow outgoing >/dev/null
for port in 22 80 443; do
    ufw allow "$port"/tcp >/dev/null
done
ufw --force enable >/dev/null

# --- fail2ban con el filtro de sshd ------------------------------------------
cat > /etc/fail2ban/jail.d/ppe.local <<'EOF'
[sshd]
enabled = true
maxretry = 5
bantime = 1h
EOF
systemctl enable --now fail2ban >/dev/null 2>&1 || true

# --- carpeta de trabajo: compose, Caddyfile y modelo --------------------------
install -d -m 0755 /opt/ppe
install -d -m 0755 /opt/ppe/models

echo "aprovisionamiento listo: usuario deploy, UFW y fail2ban"
echo "siguiente paso: copiar best.pt a /opt/ppe/models y crear /opt/ppe/.env"
