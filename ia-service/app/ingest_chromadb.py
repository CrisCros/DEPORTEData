"""
Ingesta a ChromaDB persistente desde los JSON ya pre-procesados en
`data-ia/data_json/*.json`.

Formato esperado de cada JSON (el que ya genera tu pipeline `ingesta_pdfs.py`):
{
  "archivo_origen": "dep_empleo.pdf",
  "total_chunks": 21,
  "chunks": [
     {"chunk_id": "...", "texto": "...", "fuente": "..."},
     ...
  ]
}

Uso dentro del contenedor (una sola vez o tras cambiar los JSON):
    docker exec -it deportedata-ia python -m app.ingest_chromadb
"""
from __future__ import annotations

import glob
import json
import logging
import os
import sys
from typing import List

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def _iter_chunks(paths: List[str]):
    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as exc:
            logger.error("No se pudo leer %s: %s", path, exc)
            continue
        for chunk in data.get("chunks", []):
            texto = chunk.get("texto")
            cid = chunk.get("chunk_id")
            fuente = chunk.get("fuente") or data.get("archivo_origen", "desconocido")
            if not texto or not cid:
                continue
            yield cid, texto, {"fuente": fuente}


def main() -> int:
    settings = get_settings()
    data_dir = settings.data_json_dir

    if not os.path.isdir(data_dir):
        logger.error("No existe el directorio %s", data_dir)
        return 1

    json_paths = sorted(glob.glob(os.path.join(data_dir, "*.json")))
    if not json_paths:
        logger.error("No hay JSON en %s", data_dir)
        return 1

    logger.info("Encontrados %s JSON", len(json_paths))

    client = chromadb.HttpClient(
        host=settings.chroma_host,
        port=settings.chroma_port,
        settings=ChromaSettings(anonymized_telemetry=False),
    )

    # Recreamos la colección desde cero para una ingesta limpia
    try:
        client.delete_collection(settings.chroma_collection)
        logger.info("Colección previa eliminada: %s", settings.chroma_collection)
    except Exception:
        pass

    coll = client.create_collection(name=settings.chroma_collection)

    # Batcheamos por rendimiento
    BATCH = 200
    ids_buf, docs_buf, meta_buf = [], [], []
    total = 0
    for cid, texto, meta in _iter_chunks(json_paths):
        ids_buf.append(cid)
        docs_buf.append(texto)
        meta_buf.append(meta)
        if len(ids_buf) >= BATCH:
            coll.add(ids=ids_buf, documents=docs_buf, metadatas=meta_buf)
            total += len(ids_buf)
            ids_buf, docs_buf, meta_buf = [], [], []
    if ids_buf:
        coll.add(ids=ids_buf, documents=docs_buf, metadatas=meta_buf)
        total += len(ids_buf)

    logger.info("Ingesta completada. Documentos totales en colección: %s", total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
