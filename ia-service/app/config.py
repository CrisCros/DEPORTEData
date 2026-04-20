# Configuración centralizada del ia-service.
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Ollama
    ollama_url: str = "http://ollama:11434"
    ollama_model: str = "qwen2.5:3b-instruct-q4_K_M"
    ollama_temperature: float = 0.2
    ollama_timeout_seconds: int = 300

    # ChromaDB
    chroma_host: str = "chromadb"
    chroma_port: int = 8000
    chroma_collection: str = "deportedata_docs"

    # Moderador toxicidad
    toxic_threshold: float = 0.5

    # Servidor
    port: int = 8100

    # Ingesta
    data_json_dir: str = "/data_json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
