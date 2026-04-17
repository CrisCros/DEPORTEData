"""
Schemas Pydantic para el ia-service.

El CHAT_RESPONSE_JSON_SCHEMA se pasa tal cual a Ollama en el parámetro `format`
para forzar decoding estructurado (Ollama >= 0.5). Esto garantiza que el modelo
NO pueda salirse del schema.
"""
from typing import List
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class ToxicWord(BaseModel):
    word: str
    categories: List[str]


class ChatResponse(BaseModel):
    message: str
    has_toxic: bool
    key_words_toxic_classification: List[ToxicWord] = Field(default_factory=list)


# JSON Schema que va a Ollama (structured outputs)
CHAT_RESPONSE_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
    },
    "required": ["message"],
}
