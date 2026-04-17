"""
API Pública (:8000) — Endpoints para el frontend.

Endpoints:
  - GET  /health                → estado del servicio
  - POST /auth/login            → autenticación JWT
  - POST /chat                  → chat RAG con moderación (delega al ia-service)
  - GET  /dashboard/kpis        → KPIs para dashboard
  - GET  /dashboard/series      → serie temporal para gráfica
"""

import logging
from datetime import datetime

import httpx
from fastapi import APIRouter, HTTPException, Depends

from app.config import get_settings
from app.models import LoginRequest, ChatRequest
from app.auth import create_token
from app.password import verify_password
from app.db.connection import fetch_one, execute
from app.services.data_service import DataService, get_data_service

logger = logging.getLogger(__name__)
router = APIRouter(tags=["public"])


# Endpoints frontend
@router.get("/health")
def health_check():
    s = get_settings()
    return {"status": "ok", "nom_user_id": s.nom_user_id}


@router.post("/auth/login")
def auth_login(request: LoginRequest):
    """
    Autentica contra la tabla `deportedata_users`:
      1. Busca usuario por username_user.
      2. Verifica password con bcrypt (hash guardado vs texto plano recibido).
      3. Si coincide: actualiza last_login_user y devuelve JWT.
    """
    s = get_settings()

    if not request.username or not request.password:
        raise HTTPException(
            status_code=400,
            detail="Faltan datos: username y password son obligatorios",
        )

    # Buscar usuario en la BD
    try:
        user = fetch_one(
            f"""
            SELECT id_user, username_user, password_user, role_user
            FROM `{s.name_table_users}`
            WHERE username_user = %s
            """,
            (request.username,),
        )
    except Exception as e:
        logger.error("Error consultando usuario: %s", e)
        raise HTTPException(status_code=500, detail="Error accediendo a la base de datos")

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar contraseña (bcrypt compara el texto plano con el hash)
    if not verify_password(request.password, user["password_user"]):
        raise HTTPException(status_code=401, detail="Contraseña errónea")

    # Actualizar last_login_user
    try:
        execute(
            f"UPDATE `{s.name_table_users}` SET last_login_user = %s WHERE id_user = %s",
            (datetime.utcnow(), user["id_user"]),
        )
    except Exception as e:
        # No bloqueamos el login si falla el update; solo logueamos.
        logger.warning("No se pudo actualizar last_login_user: %s", e)

    # Emitir JWT
    token = create_token({
        "sub": user["id_user"],
        "name": user["username_user"],
        "role": user["role_user"],
        "id_user": user["id_user"],
    })

    return {
        "username": user["username_user"],
        "role": user["role_user"],
        "token": token,
    }


# ─── /chat: proxy estricto al ia-service ─────────────────────────────
@router.post("/chat")
def chat(request: ChatRequest):
    """
    Contrato EXACTO del enunciado (sin añadir/renombrar campos):

        request:  { "message": "<pregunta>" }
        response: {
            "message": "<respuesta textual del modelo>",
            "has_toxic": <bool>,
            "key_words_toxic_classification": [ {word, categories[]}, ... ]
        }

    El backend NO procesa el mensaje: hace proxy puro al ia-service
    (Detoxify + RAG + Ollama), que ya devuelve ese JSON tal cual. Esto
    mantiene el backend tonto y concentra toda la lógica de IA en un
    único servicio.
    """
    s = get_settings()

    message = (request.message or "").strip()
    if not message:
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")

    url = f"{s.ia_service_url.rstrip('/')}/ia/chat"
    try:
        with httpx.Client(timeout=s.ia_service_timeout_seconds) as client:
            r = client.post(url, json={"message": message})
            r.raise_for_status()
            ia = r.json()
    except httpx.HTTPError as exc:
        logger.exception("Error llamando al ia-service (%s): %s", url, exc)
        raise HTTPException(
            status_code=502,
            detail=f"IA service no disponible: {exc}",
        )

    # Devolvemos solo los tres campos del contrato.
    return {
        "message": ia.get("message", ""),
        "has_toxic": bool(ia.get("has_toxic", False)),
        "key_words_toxic_classification": ia.get("key_words_toxic_classification", []),
    }


@router.get("/dashboard/kpis")
def get_dashboard_kpis(data_service: DataService = Depends(get_data_service)):
    return data_service.dashboard_kpis()


@router.get("/dashboard/series")
def get_dashboard_series(data_service: DataService = Depends(get_data_service)):
    return data_service.dashboard_series()
