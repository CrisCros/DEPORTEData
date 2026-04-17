#!/usr/bin/env bash
# ============================================================
# build-and-push.sh — Construye ia-service y lo sube a GHCR
#
# Antes de ejecutar:
#   1. Crea un PAT de GitHub con scope `write:packages`
#   2. Exporta: export GHCR_USER=tu-usuario  GHCR_PAT=ghp_xxx
#   3. Lanza: bash build-and-push.sh v1.0.0
#
# El tag se le pasa como argumento. Por defecto: latest
# ============================================================
set -euo pipefail

TAG="${1:-latest}"
GHCR_USER="${GHCR_USER:?Define GHCR_USER=tu-usuario}"
GHCR_PAT="${GHCR_PAT:?Define GHCR_PAT=<PAT con write:packages>}"

IMAGE="ghcr.io/${GHCR_USER}/deportedata/ia-service"
FULL="${IMAGE}:${TAG}"

echo "[1/3] Login a GHCR..."
echo "$GHCR_PAT" | docker login ghcr.io -u "$GHCR_USER" --password-stdin

echo "[2/3] Build: ${FULL}"
docker build -t "$FULL" -t "${IMAGE}:latest" .

echo "[3/3] Push: ${FULL}"
docker push "$FULL"
docker push "${IMAGE}:latest"

echo "Listo: ${FULL}"
echo ""
echo "Recuerda hacer pública la imagen en GitHub (Packages) o autenticar"
echo "en EC2-5: echo \$GHCR_PAT | sudo docker login ghcr.io -u \$GHCR_USER --password-stdin"
