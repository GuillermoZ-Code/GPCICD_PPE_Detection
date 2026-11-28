#!/bin/sh
# =============================================================================
# HU-070 — despliegue con rollback por tag.
#
# Se ejecuta EN el servidor (el job lo copia por scp). Recibe el tag nuevo,
# guarda el par de imágenes desplegado y, si el smoke no pasa, vuelve al par
# anterior. No necesita credenciales del registry: se las pasa el job por
# entorno.
#
# Entorno:
#   PPE_API_REPO    registry.../api
#   PPE_WEB_REPO    registry.../web
#   PPE_CADDY_REPO  registry.../caddy (HU-054: imagen con rate_limit)
#   PPE_COMPOSE_DIR carpeta del compose en el servidor (por omisión /opt/ppe)
# =============================================================================

set -eu

tag="${1:-}"
if [ -z "$tag" ]; then
    echo "uso: deploy.sh <tag>" >&2
    exit 64
fi

compose_dir="${PPE_COMPOSE_DIR:-/opt/ppe}"
api_repo="${PPE_API_REPO:?falta PPE_API_REPO}"
web_repo="${PPE_WEB_REPO:?falta PPE_WEB_REPO}"
caddy_repo="${PPE_CADDY_REPO:?falta PPE_CADDY_REPO}"

cd "$compose_dir"

state=".deployed_env"
previous=""
if [ -f "$state" ]; then
    previous="$(cat "$state")"
fi

# Estado nuevo: las tres imágenes con el mismo tag.
tmp="$state.tmp"
{
    echo "PPE_API_IMAGE=$api_repo:$tag"
    echo "PPE_WEB_IMAGE=$web_repo:$tag"
    echo "PPE_CADDY_IMAGE=$caddy_repo:$tag"
} > "$tmp"
mv "$tmp" "$state"

# shellcheck disable=SC1090
set -a
. "./$state"
set +a

# Un servicio está sano cuando Docker lo reporta `healthy`.
all_healthy() {
    for service in api grpc web; do
        container="$(docker compose -f compose.prod.yml ps -q "$service" 2>/dev/null || true)"
        [ -n "$container" ] || return 1
        status="$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "$container" 2>/dev/null || echo unknown)"
        [ "$status" = "healthy" ] || return 1
    done
    # Caddy no trae HEALTHCHECK en la imagen: basta con que siga corriendo.
    caddy_container="$(docker compose -f compose.prod.yml ps -q caddy 2>/dev/null || true)"
    [ -n "$caddy_container" ] || return 1
    running="$(docker inspect --format '{{.State.Running}}' "$caddy_container" 2>/dev/null || echo false)"
    [ "$running" = "true" ] || return 1
    return 0
}

# Inferencia real: el contrato no está sano solo por responder /health.
smoke() {
    all_healthy || return 1
    docker compose -f compose.prod.yml exec -T api python -c \
        "import sys, urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health/ready', timeout=5).status == 200 else 1)"
}

wait_for_health() {
    intento=0
    while [ "$intento" -lt 36 ]; do
        if smoke; then
            return 0
        fi
        intento=$((intento + 1))
        sleep 5
    done
    return 1
}

start() {
    docker compose -f compose.prod.yml pull
    docker compose -f compose.prod.yml up -d --remove-orphans
}

echo "desplegando $tag"
if start && wait_for_health; then
    echo "deploy ok: $tag"
    exit 0
fi

echo "el despliegue de $tag falló; se intenta volver al anterior" >&2
docker compose -f compose.prod.yml logs --tail 80 >&2 || true

if [ -z "$previous" ]; then
    echo "no hay versión anterior registrada: no se puede revertir" >&2
    exit 1
fi

printf '%s\n' "$previous" > "$state"
# shellcheck disable=SC1090
set -a
. "./$state"
set +a

if start && wait_for_health; then
    echo "rollback ok" >&2
    # El job falla igual: el despliegue no quedó en el tag pedido.
    exit 1
fi

echo "el rollback también falló: revisar los logs del servidor" >&2
exit 1
