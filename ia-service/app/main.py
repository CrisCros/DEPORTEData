"""
FastAPI del ia-service.

Endpoints:
  - GET  /health
  - POST /ia/chat   → { message, has_toxic, key_words_toxic_classification }
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.chat_service import ChatService
from app.config import get_settings
from app.models import ChatRequest, ChatResponse
from app.moderator import Moderator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


# Estado global del servicio (cargado en el lifespan)
state: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info("Arrancando ia-service...")
    logger.info("  OLLAMA_URL=%s", settings.ollama_url)
    logger.info("  OLLAMA_MODEL=%s", settings.ollama_model)
    logger.info("  CHROMA=%s:%s/%s", settings.chroma_host, settings.chroma_port, settings.chroma_collection)

    moderator = Moderator(threshold=settings.toxic_threshold)
    chat_service = ChatService(settings=settings, moderator=moderator)
    state["chat_service"] = chat_service
    logger.info("ia-service listo en puerto %s", settings.port)

    yield

    await chat_service.close()
    state.clear()


app = FastAPI(
    title="DEPORTEData IA Service",
    version="1.0.0",
    description="Chat RAG + moderación de toxicidad",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "ia-service"}


@app.post("/ia/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    svc: ChatService | None = state.get("chat_service")
    if svc is None:
        raise HTTPException(status_code=503, detail="Servicio aún no inicializado")

    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")

    try:
        return await svc.answer(message)
    except Exception as exc:
        logger.exception("Error procesando /ia/chat: %s", exc)
        raise HTTPException(status_code=500, detail=f"Error interno: {exc}")
