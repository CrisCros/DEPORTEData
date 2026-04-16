"""
API Pública (:8000) — Endpoints para el frontend.

Endpoints:
  - GET  /health                → estado del servicio
  - POST /auth/login            → autenticación JWT
  - POST /chat                  → chat conectado al dataset limpio
  - GET  /dashboard/kpis        → KPIs para dashboard
  - GET  /dashboard/series      → serie temporal para gráfica
"""

import logging

from fastapi import APIRouter, HTTPException, Depends

from app.config import get_settings
from app.models import LoginRequest, ChatRequest
from app.auth import create_token
#from app.db.connection import fetch_all
#from app.s3_client import upload_bytes, list_keys
from app.services.data_service import DataService, get_data_service

logger = logging.getLogger(__name__)
router = APIRouter(tags=["public"])


# Datos temporales (hasta tener BD poblada)
TEST_USER = {
    "admin": {
        "name": "Administrador",
        "username": "admin",
        "password": "*admin1234",
        "role": "admin",
    }
}


# ══════════════════════════════════════════════
# Endpoints frontend
# ══════════════════════════════════════════════

@router.get("/health")
def health_check():
    s = get_settings()
    return {"status": "ok", "nom_user_id": s.nom_user_id}


@router.post("/auth/login")
def auth_login(request: LoginRequest):
    if not request.username or not request.password:
        raise HTTPException(
            status_code=400,
            detail="Faltan datos: username y password son obligatorios",
        )

    user = TEST_USER.get(request.username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if request.password != user["password"]:
        raise HTTPException(status_code=401, detail="Contraseña errónea")

    token = create_token({
        "sub": user["username"],
        "name": user["name"],
        "role": user["role"],
    })

    return {
        "name": user["name"],
        "username": user["username"],
        "role": user["role"],
        "token": token,
    }


@router.post("/chat")
def chat(request: ChatRequest, data_service: DataService = Depends(get_data_service)):
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")

    try:
        answer = data_service.answer_chat(message)
    except ValueError as error:
        logger.error("Error resolviendo chat: %s", error)
        raise HTTPException(status_code=500, detail=str(error)) from error

    return {
        "message": message,
        "answer": answer,
    }


@router.get("/dashboard/kpis")
def get_dashboard_kpis(data_service: DataService = Depends(get_data_service)):
    return data_service.dashboard_kpis()


@router.get("/dashboard/series")
def get_dashboard_series(data_service: DataService = Depends(get_data_service)):
    return data_service.dashboard_series()
