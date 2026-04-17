#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

log()  { echo -e "\033[1;34m[deploy-model-service]\033[0m $*"; }
die()  { echo -e "\033[1;31m[ERROR]\033[0m $*" >&2; exit 1; }

# Checks 
[[ -f .env ]] || die "Falta .env en $SCRIPT_DIR (cp .env.example .env)"
[[ -f docker-compose.yml ]] || die "Falta docker-compose.yml en $SCRIPT_DIR"
[[ -d data_json ]] || log "WARN: no existe ./data_json — la ingesta fallará."

# Crecer el filesystem si el EBS ya se amplió
# En Nitro (t3) el disco es /dev/nvme0n1. En Xen antiguo sería /dev/xvda.
ROOT_DEV="$(findmnt -n -o SOURCE / | sed 's/[0-9]*$//')"
ROOT_PART="$(findmnt -n -o SOURCE /)"
if command -v growpart >/dev/null; then
  log "Intentando crecer partición raíz ($ROOT_DEV / $ROOT_PART)..."
  sudo growpart "$ROOT_DEV" 1 || true
  sudo resize2fs "$ROOT_PART" || sudo xfs_growfs / || true
fi
df -h /

# Instalar Docker + Compose si faltan
if ! command -v docker &>/dev/null; then
  log "Instalando Docker..."
  sudo apt-get update -y
  sudo apt-get install -y docker.io
  sudo systemctl enable --now docker
  sudo usermod -aG docker "$USER" || true
fi
if ! docker compose version &>/dev/null; then
  log "Instalando docker compose plugin..."
  sudo apt-get install -y docker-compose-plugin || {
    # Fallback manual
    sudo mkdir -p /usr/local/lib/docker/cli-plugins
    sudo curl -SL https://github.com/docker/compose/releases/download/v2.29.7/docker-compose-linux-x86_64 \
      -o /usr/local/lib/docker/cli-plugins/docker-compose
    sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
  }
fi

# Pull + up 
log "Descargando imágenes..."
sudo docker compose pull

log "Levantando servicios..."
sudo docker compose up -d

# Esperar a que Ollama y ChromaDB estén sanos
wait_healthy() {
  local name="$1" timeout="${2:-120}" elapsed=0
  while (( elapsed < timeout )); do
    status=$(sudo docker inspect --format='{{.State.Health.Status}}' "$name" 2>/dev/null || echo "starting")
    [[ "$status" == "healthy" ]] && { log "  $name → healthy"; return 0; }
    sleep 5; elapsed=$((elapsed+5))
  done
  die "$name no quedó healthy en ${timeout}s"
}
log "Esperando health..."
wait_healthy deportedata-ollama   180
wait_healthy deportedata-chromadb 120
wait_healthy deportedata-ia       180
wait_healthy deportedata-backend  120

# Descargar el modelo en Ollama (si no está)
MODEL="${OLLAMA_MODEL:-qwen2.5:3b-instruct-q4_K_M}"
if ! sudo docker exec deportedata-ollama ollama list | grep -q "${MODEL%:*}"; then
  log "Descargando modelo $MODEL (~2 GB, puede tardar 2-3 min)..."
  sudo docker exec deportedata-ollama ollama pull "$MODEL"
else
  log "Modelo $MODEL ya presente en Ollama."
fi

# Ingesta a ChromaDB (idempotente: recrea colección)
log "Ejecutando ingesta a ChromaDB..."
sudo docker exec deportedata-ia python -m app.ingest_chromadb

# Smoke test
log "Probando /health..."
curl -sf http://localhost:8000/health && echo

log "Probando /chat con un mensaje benigno..."
curl -s -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"¿Cuántas personas trabajaban en el deporte en España en 2024?"}' \
  | head -c 800
echo

log "Probando /chat con un mensaje tóxico..."
curl -s -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"eres un idiota"}' \
  | head -c 800
echo

log "Despliegue completado."
