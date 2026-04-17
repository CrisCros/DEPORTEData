# ia-service/Dockerfile
# Pre-descarga el modelo Detoxify en build time para que el contenedor
# arranque sin depender de internet (importante en Learner Lab con IP
# cambiante y créditos limitados).
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/opt/hf_cache \
    TRANSFORMERS_CACHE=/opt/hf_cache \
    TOKENIZERS_PARALLELISM=false

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential curl ca-certificates git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Pre-descarga del modelo multilingüe de Detoxify (~1.1 GB).
# Así evitamos que el primer arranque en EC2 tenga que descargarlo.
RUN python -c "from detoxify import Detoxify; Detoxify('multilingual')"

# Copiamos el código al final para aprovechar la cache
COPY app /app/app

EXPOSE 8100

# Un solo worker: el modelo está cargado en memoria y no queremos duplicarlo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8100", "--workers", "1"]
