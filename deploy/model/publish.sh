#!/bin/sh
# =============================================================================
# HU-024 — publica el artefacto del modelo en el Generic Package Registry.
#
# El peso no se versiona en Git: se sube una vez por versión y el pipeline lo
# descarga verificando el SHA256. Este script corre en la máquina de quien
# tiene el archivo a mano, no en CI (CI no puede producir los pesos).
#
# Uso:
#   GITLAB_TOKEN=<PAT con scope api> sh deploy/model/publish.sh <archivo> <version>
#
# Ejemplo:
#   GITLAB_TOKEN=<tu-token> sh deploy/model/publish.sh artifacts/best.pt yolo26n-clean
# =============================================================================

set -eu

file="${1:-}"
version="${2:-}"

if [ -z "$file" ] || [ -z "$version" ]; then
    echo "uso: publish.sh <archivo> <version>" >&2
    exit 64
fi

if [ ! -f "$file" ]; then
    echo "no existe el archivo $file" >&2
    exit 66
fi

: "${GITLAB_TOKEN:?falta GITLAB_TOKEN (personal access token con scope api)}"

project="${PPE_PROJECT_ID:-89281003}"
package="${PPE_MODEL_PACKAGE:-ppe-detection-models}"
name="$(basename "$file")"
url="https://gitlab.com/api/v4/projects/${project}/packages/generic/${package}/${version}/${name}"

echo "subiendo $name ($version) a $package…"
curl -fsSL --header "PRIVATE-TOKEN: $GITLAB_TOKEN" --upload-file "$file" "$url" > /dev/null

# Verificación: se descarga lo publicado y se compara con el archivo local.
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT
curl -fsSL --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$url" -o "$tmp"

local_sum="$(sha256sum "$file" | cut -d' ' -f1)"
remote_sum="$(sha256sum "$tmp" | cut -d' ' -f1)"

if [ "$local_sum" != "$remote_sum" ]; then
    echo "el SHA256 publicado no coincide: $local_sum != $remote_sum" >&2
    exit 1
fi

echo
echo "publicado y verificado"
echo "  url    $url"
echo "  sha256 $(echo "$local_sum" | tr '[:lower:]' '[:upper:]')"
echo
echo "models.lock:"
echo "  url = \"$url\""
echo "  sha256 = \"$(echo "$local_sum" | tr '[:lower:]' '[:upper:]')\""
