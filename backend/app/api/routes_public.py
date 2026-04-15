"""
API Pública (:8000) — Endpoints para el frontend.

Endpoints principales para frontend:
  - GET  /health                → estado del servicio
  - POST /auth/login            → autenticación JWT
  - POST /chat                  → chat conectado al dataset limpio
  - GET  /dashboard/kpis        → KPIs para dashboard
  - GET  /dashboard/series      → serie temporal para gráfica

Compatibilidad backward (legacy):
  - POST /login
  - POST /getResponseChat
  - GET  /getDatosDashboard

Endpoints de datos:
  - GET  /api/v1/empleo         → consulta empleo deportivo
  - GET  /api/v1/gasto          → consulta gasto hogares
  - POST /api/v1/upload/raw     → subir archivo a S3 (raw)
  - GET  /api/v1/s3/list        → listar keys en S3
"""

import logging

from fastapi import APIRouter, UploadFile, File, Query, HTTPException, Depends

from app.config import get_settings
from app.models import LoginRequest, ChatRequest
from app.auth import create_token
from app.db.connection import fetch_all
from app.s3_client import upload_bytes, list_keys
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
# Endpoints frontend (actuales)
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


# ══════════════════════════════════════════════
# Endpoints legacy para no romper clientes antiguos
# ══════════════════════════════════════════════

@router.post("/login")
def login_legacy(request: LoginRequest):
    return auth_login(request)


@router.post("/getResponseChat")
def get_response_chat_legacy(request: ChatRequest, data_service: DataService = Depends(get_data_service)):
    response = chat(request, data_service)
    return {
        "question": response["message"],
        "answer": response["answer"],
    }


@router.get("/getDatosDashboard")
def get_datos_dashboard_legacy(data_service: DataService = Depends(get_data_service)):
    kpis = data_service.dashboard_kpis()
    series = data_service.dashboard_series()

    return {
        "kpis": {
            "total_empleo_miles": kpis["empleo_total"],
            "variacion_anual_pct": kpis["growth_pct"],
            "ratio_hombres_mujeres": 1.8,
        },
        "empleo_trimestral": [
            {"periodo": f"{item['year']}", "valor": item["value"]}
            for item in series[-4:]
        ],
    }


# ══════════════════════════════════════════════
# Consultas directas a RDS
# ══════════════════════════════════════════════

@router.get("/api/v1/empleo")
def get_empleo(
    periodo: str | None = None,
    comunidad: str | None = None,
    limit: int = Query(default=100, le=1000),
):
    """Consulta datos de empleo deportivo trimestral."""
    conditions, params = [], []
    if periodo:
        conditions.append("periodo = %s")
        params.append(periodo)
    if comunidad:
        conditions.append("comunidad_autonoma = %s")
        params.append(comunidad)

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    query = f"""
        SELECT periodo, comunidad_autonoma, sexo, grupo_edad,
               tipo_jornada, ocupados_miles
        FROM empleo_deporte_trimestral
        {where}
        ORDER BY periodo DESC LIMIT %s
    """
    params.append(limit)
    try:
        rows = fetch_all(query, tuple(params))
        return {"count": len(rows), "data": rows}
    except Exception as e:
        raise HTTPException(500, f"Error consultando empleo: {e}")


@router.get("/api/v1/gasto")
def get_gasto(
    anio: int | None = None,
    comunidad: str | None = None,
    limit: int = Query(default=100, le=1000),
):
    """Consulta datos de gasto de hogares en deporte."""
    conditions, params = [], []
    if anio:
        conditions.append("anio = %s")
        params.append(anio)
    if comunidad:
        conditions.append("comunidad_autonoma = %s")
        params.append(comunidad)

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    query = f"""
        SELECT anio, comunidad_autonoma, tipo_gasto, importe_medio_euros
        FROM gasto_hogares_deporte
        {where}
        ORDER BY anio DESC LIMIT %s
    """
    params.append(limit)
    try:
        rows = fetch_all(query, tuple(params))
        return {"count": len(rows), "data": rows}
    except Exception as e:
        raise HTTPException(500, f"Error consultando gasto: {e}")


# ══════════════════════════════════════════════
# S3
# ══════════════════════════════════════════════

@router.post("/api/v1/upload/raw")
async def upload_raw(file: UploadFile = File(...), subfolder: str = "csv"):
    """Sube un archivo a S3 en la carpeta raw/."""
    try:
        content = await file.read()
        path = upload_bytes(content, f"raw/{subfolder}/{file.filename}", content_type="text/csv")
        return {"s3_path": path, "size": len(content)}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/api/v1/s3/list")
def s3_list(prefix: str = "raw/"):
    """Lista keys en el bucket S3."""
    return {"keys": list_keys(prefix)}
