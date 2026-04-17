# user_message -> Moderador (Detoxify + léxico)

from __future__ import annotations

import json
import logging

import chromadb
import httpx
from chromadb.config import Settings as ChromaSettings

from app.config import Settings
from app.models import ChatResponse, CHAT_RESPONSE_JSON_SCHEMA, ToxicWord
from app.moderator import Moderator

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = (
    "Eres un asistente experto en analítica del empleo vinculado al deporte "
    "en España. Responde en el mismo idioma de la pregunta del usuario "
    "(español o inglés). Usa EXCLUSIVAMENTE la información del CONTEXTO "
    "proporcionado. Si el contexto no contiene la respuesta, dilo "
    "explícitamente y no inventes datos ni cifras. Sé conciso y claro. "
    "Devuelve exclusivamente un objeto JSON con la clave 'message' que "
    "contenga tu respuesta en texto plano."
)

TOXIC_REPLY_ES = (
    "Lo sentimos, pero no permitimos ese tipo de lenguaje inapropiado. "
    "¿Puedo ayudarte con una pregunta sobre el empleo vinculado al deporte "
    "en España?"
)
TOXIC_REPLY_EN = (
    "We are sorry, but we do not allow that kind of inappropriate language. "
    "Can I help you with a question about sport-related employment in Spain?"
)


def _is_english(text: str) -> bool:
    """Heurística rápida ES/EN. Si no detecta nada claro, asume ES."""
    t = text.lower()
    en_hits = sum(
        w in t for w in (" the ", " is ", " are ", " you ", " what ", " how ")
    )
    es_hits = sum(
        w in t for w in (" el ", " la ", " de ", " qué ", " cómo ", " cuántos ", "¿")
    )
    return en_hits > es_hits


class ChatService:
    def __init__(self, settings: Settings, moderator: Moderator):
        self._settings = settings
        self._moderator = moderator
        self._chroma = chromadb.HttpClient(
            host=settings.chroma_host,
            port=settings.chroma_port,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        try:
            self._collection = self._chroma.get_or_create_collection(
                name=settings.chroma_collection
            )
            logger.info(
                "Conectado a ChromaDB (col=%s, docs=%s)",
                settings.chroma_collection,
                self._collection.count(),
            )
        except Exception as exc:
            logger.exception("No se pudo conectar a ChromaDB: %s", exc)
            self._collection = None

        self._http = httpx.AsyncClient(timeout=settings.ollama_timeout_seconds)

    async def close(self) -> None:
        await self._http.aclose()

    # ─── RAG ──────────────────────────────────────────────────────
    def _retrieve(self, query: str, k: int = 5) -> str:
        if self._collection is None:
            return ""
        try:
            res = self._collection.query(query_texts=[query], n_results=k)
            docs = res.get("documents", [[]])[0] if res else []
        except Exception as exc:
            logger.exception("Fallo en query ChromaDB: %s", exc)
            return ""
        if not docs:
            return ""
        return "\n\n--- Fragmento ---\n".join(docs)

    # ─── LLM ──────────────────────────────────────────────────────
    async def _generate(self, message: str, context: str) -> str:
        """Llama a Ollama con format=JSON schema. Devuelve solo el 'message'."""
        user_prompt = (
            f"CONTEXTO:\n{context if context else '(no hay contexto recuperado)'}\n\n"
            f"PREGUNTA DEL USUARIO: {message}\n\n"
            "Responde en JSON con la clave 'message'."
        )
        payload = {
            "model": self._settings.ollama_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "format": CHAT_RESPONSE_JSON_SCHEMA,  # structured outputs
            "stream": False,
            "options": {"temperature": self._settings.ollama_temperature},
        }
        url = f"{self._settings.ollama_url}/api/chat"
        r = await self._http.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
        content = data.get("message", {}).get("content", "")
        try:
            parsed = json.loads(content)
            return str(parsed.get("message", "")).strip() or (
                "No he podido generar una respuesta."
            )
        except json.JSONDecodeError:
            # Si por lo que sea el modelo no devuelve JSON válido, usamos el
            # texto tal cual como fallback para no romper la UI.
            logger.warning("Ollama devolvió JSON inválido, fallback a texto plano.")
            return content.strip() or "No he podido generar una respuesta."

    # ─── Pipeline ─────────────────────────────────────────────────
    async def answer(self, message: str) -> ChatResponse:
        mod = self._moderator.moderate(message)

        if mod.has_toxic:
            reply = TOXIC_REPLY_EN if _is_english(message) else TOXIC_REPLY_ES
            return ChatResponse(
                message=reply,
                has_toxic=True,
                key_words_toxic_classification=[
                    ToxicWord(**w) for w in mod.toxic_words
                ],
            )

        context = self._retrieve(message)
        text = await self._generate(message, context)
        return ChatResponse(
            message=text,
            has_toxic=False,
            key_words_toxic_classification=[],
        )
