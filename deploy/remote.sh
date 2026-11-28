#!/bin/sh
# =============================================================================
# HU-070 — despliegue desde la máquina del integrante, sin abrir un pipeline.
#
#   sh deploy/remote.sh deploy   (TAG=<sha>)
#   sh deploy/remote.sh verify
#
# Variables:
#   PPE_DEPLOY_HOST   IP o dominio del Droplet        (obligatoria)
#   PPE_DEPLOY_USER   usuario SSH                      (deploy)
#   PPE_SSH_KEY       llave privada                    (~/.ssh/ppe_deploy2)
#   PPE_DOCKERHUB_USER usuario de Docker Hub           (guillermozabala)
#   PPE_PUBLIC_URL    URL pública, para `verify`
#   PPE_CADDY_REPO    repo de la imagen de Caddy       (por omisión el espejo)
# =============================================================================

set -eu

action="${1:-}"
host="${PPE_DEPLOY_HOST:?falta PPE_DEPLOY_HOST}"
user="${PPE_DEPLOY_USER:-deploy}"
key="${PPE_SSH_KEY:-$HOME/.ssh/ppe_deploy2}"
hub="${PPE_DOCKERHUB_USER:-guillermozabala}"
dir="${PPE_COMPOSE_DIR:-/opt/ppe}"

remote() {
    ssh -i "$key" -o StrictHostKeyChecking=accept-new -o BatchMode=yes \
        "$user@$host" "$@"
}

case "$action" in
deploy)
    tag="${PPE_TAG:?falta TAG (SHA corto de 8 caracteres)}"
    scp -i "$key" -o StrictHostKeyChecking=accept-new \
        compose.prod.yml docker/Caddyfile deploy/deploy.sh "$user@$host:$dir/" >/dev/null
    remote "cd $dir && PPE_API_REPO=$hub/gpcicd-ppe-api \
        PPE_WEB_REPO=$hub/gpcicd-ppe-web \
        PPE_CADDY_REPO=$hub/gpcicd-ppe-caddy PPE_COMPOSE_DIR=$dir sh deploy.sh $tag"
    ;;
verify)
    url="${PPE_PUBLIC_URL:?falta PPE_PUBLIC_URL}"
    echo "salud:"
    curl -fsS "$url/health"
    echo
    echo "listo:"
    curl -fsS "$url/health/ready"
    echo
    ;;
*)
    echo "uso: remote.sh deploy|verify" >&2
    exit 64
    ;;
esac
