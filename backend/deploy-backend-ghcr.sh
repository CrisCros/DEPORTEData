#!/bin/bash
# ============================================================
# deploy-backend-ghcr.sh — Despliega DEPORTEData Backend desde GHCR
#
# La versión de la imagen se lee del .env (VERSION_GHCR_BACKEND)
#
# REQUISITOS:
#   1. Rellenar ${HOME}/backend/.env
#   2. Hacer docker login a GHCR (una sola vez):
#      echo "TU_PAT" | sudo docker login ghcr.io -u TU_USUARIO --password-stdin
# ============================================================
set -euo pipefail

# ── Configuración fija ──
CONTAINER_NAME="deportedata-backend"
ENV_FILE="${HOME}/backend/.env"
# CAMBIA esto por tu repo real (minúsculas)
GHCR_REPO="ghcr.io/CrisCros/DEPORTEData/backend"

# ── Verificar .env ──
if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: No se encontró $ENV_FILE"
    echo "  cp ~/backend/.env.example ~/backend/.env"
    echo "  nano ~/backend/.env"
    exit 1
fi

# ── Leer versión del .env ──
# En el .env: VERSION_GHCR_BACKEND=backend_v1.0.0
# El CI extrae "v1.0.0" como tag de imagen (quita el prefijo "backend_")
VERSION_TAG=$(grep -E "^VERSION_GHCR_BACKEND=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '[:space:]')

if [ -z "$VERSION_TAG" ]; then
    echo "ERROR: VERSION_GHCR_BACKEND no definida en $ENV_FILE"
    exit 1
fi

# Extraer versión de imagen (quitar prefijo "backend_")
IMAGE_TAG="${VERSION_TAG#backend_}"
GHCR_IMAGE="${GHCR_REPO}:${IMAGE_TAG}"

echo "============================================"
echo " Desplegando DEPORTEData Backend desde GHCR"
echo " Versión .env: ${VERSION_TAG}"
echo " Imagen:       ${GHCR_IMAGE}"
echo " Env:          ${ENV_FILE}"
echo "============================================"

# ─── 1) Instalar Docker (si no está) ───
if ! command -v docker &> /dev/null; then
    echo "[1/4] Instalando Docker..."
    sudo apt-get update -y
    sudo apt-get install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker ubuntu
else
    echo "[1/4] Docker ya instalado"
fi

# ─── 2) Descargar imagen desde GHCR ───
echo "[2/4] Descargando imagen desde GHCR..."
sudo docker pull ${GHCR_IMAGE}

# ─── 3) Eliminar contenedor anterior ───
echo "[3/4] Eliminando contenedor anterior si existe..."
sudo docker rm -f ${CONTAINER_NAME} 2>/dev/null || true

# ─── 4) Arrancar contenedor ───
echo "[4/4] Arrancando contenedor..."
sudo docker run -d \
    --name ${CONTAINER_NAME} \
    --network host \
    --env-file ${ENV_FILE} \
    --restart unless-stopped \
    ${GHCR_IMAGE}

echo ""
echo "============================================"
echo " API desplegada. Verificar:"
echo "   curl http://localhost:8000/health"
echo "   curl http://localhost:8001/internal/health"
echo "   sudo docker logs ${CONTAINER_NAME}"
echo "============================================"
