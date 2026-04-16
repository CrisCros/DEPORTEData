# DEPORTEData API — Punto de entrada.

# Levanta DOS servidores FastAPI:
#   - API Pública  (:8000) → Frontend, login, chat, dashboard, datos
#   - API Privada  (:8001) → Spark jobs, admin S3/RDS
# Uso:
#   python -m app.main

import asyncio
import logging
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.routes_public import router as public_router
from app.api.routes_private import router as private_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


# App pública (:8000)
public_app = FastAPI(
    title="DEPORTEData API",
    version="1.0.0",
    description="API pública — login, chat, dashboard, consulta de datos",
)

public_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

public_app.include_router(public_router)


# App privada (:8001)
private_app = FastAPI(
    title="DEPORTEData Admin API",
    version="1.0.0",
    description="API privada — Spark jobs, admin S3/RDS",
)

private_app.include_router(private_router)


# Arranque dual
async def main():
    s = get_settings()

    config_public = uvicorn.Config(
        public_app,
        host="0.0.0.0",
        port=s.public_api_port,
        log_level="info",
    )
    config_private = uvicorn.Config(
        private_app,
        host="0.0.0.0",
        port=s.private_api_port,
        log_level="info",
    )

    server_public = uvicorn.Server(config_public)
    server_private = uvicorn.Server(config_private)

    logger.info(f"NOM_USER_ID:   {s.nom_user_id}")
    logger.info(f"SPARK_MASTER: {s.spark_master_url}")
    logger.info(f"DB_HOST:      {s.db_host}")
    logger.info(f"S3_BUCKET:    {s.s3_bucket_datalake}")
    logger.info(f"API Pública   → :{s.public_api_port}")
    logger.info(f"API Privada   → :{s.private_api_port}")

    await asyncio.gather(
        server_public.serve(),
        server_private.serve(),
    )


if __name__ == "__main__":
    asyncio.run(main())
