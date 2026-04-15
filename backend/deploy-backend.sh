#!/bin/bash
# ============================================================
# deploy-backend.sh — Despliega DEPORTEData Backend en EC2-5
#
# REQUISITO: rellenar ~/backend/.env antes de ejecutar
# ============================================================
set -euo pipefail

IMAGE_NAME="deportedata-backend:latest"
ENV_FILE="${HOME}/backend/.env"

# Verificar que .env existe
if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: No se encontró $ENV_FILE"
    echo "Copia .env.example → .env y rellena los valores reales:"
    echo "  cp ~/backend/.env.example ~/backend/.env"
    echo "  nano ~/backend/.env"
    exit 1
fi

echo "============================================"
echo " Desplegando DEPORTEData Backend (EC2)"
echo " Usando: $ENV_FILE"
echo "============================================"

# ─── 1) Instalar Docker ───
echo "[1/4] Instalando Docker..."
sudo apt-get update -y
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# ─── 2) Construir imagen ───
echo "[2/4] Construyendo imagen Docker (5-8 min la primera vez)..."
cd ~/backend
sudo docker build -t ${IMAGE_NAME} .

# ─── 3) Eliminar contenedor anterior ───
echo "[3/4] Eliminando contenedor anterior si existe..."
sudo docker rm -f deportedata-backend 2>/dev/null || true

# ─── 4) Arrancar contenedor ───
echo "[4/4] Arrancando contenedor..."
sudo docker run -d \
    --name deportedata-backend \
    --network host \
    --env-file ${ENV_FILE} \
    --restart unless-stopped \
    ${IMAGE_NAME}

echo ""
echo "============================================"
echo " API desplegada. Verificar:"
echo "   curl http://localhost:8000/health"
echo "   curl http://localhost:8001/internal/health"
echo "   sudo docker logs deportedata-backend"
echo "============================================"
