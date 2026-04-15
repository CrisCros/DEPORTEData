"""
API Pública (:8000) — Endpoints para el frontend.

Endpoints migrados del original:
  - GET  /health                → estado del servicio
  - POST /login                 → autenticación JWT
  - POST /getResponseChat       → chat (simulado ahora, RAG en Sprint 4)
  - GET  /getDatosDashboard     → KPIs para dashboard

Endpoints de datos:
  - GET  /api/v1/empleo         → consulta empleo deportivo
  - GET  /api/v1/gasto          → consulta gasto hogares
  - POST /api/v1/upload/raw     → subir archivo a S3 (raw)
  - GET  /api/v1/s3/list        → listar keys en S3
"""

import random
import logging

from fastapi import APIRouter, UploadFile, File, Query, HTTPException

from app.config import get_settings
from app.models import LoginRequest, ChatRequest
from app.auth import create_token
from app.db.connection import fetch_all
from app.s3_client import upload_bytes, list_keys

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

RESPUESTAS_SIMULADAS = [
    "Según la previsión anual, el sector del deporte podría generar un aumento moderado de empleo.",
    "La estimación del modelo indica que la demanda de empleo deportivo podría crecer.",
    "La predicción sugiere que el empleo en el sector deportivo tendrá una evolución positiva.",
    "El modelo prevé que los puestos de trabajo en el ámbito deportivo podrían incrementarse.",
    "La previsión permite anticipar tendencias de empleo en el deporte.",
]


# ══════════════════════════════════════════════
# Endpoints migrados del original
# ══════════════════════════════════════════════

@router.get("/health")
def health_check():
    s = get_settings()
    return {"status": "ok", "nom_user_id": s.nom_user_id}


@router.post("/login")
def login(request: LoginRequest):
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


@router.post("/getResponseChat")
def get_response_chat(request: ChatRequest):
    """
    Chat público. Respuesta simulada por ahora.
    En Sprint 4 se conectará al RAG (Ollama + ChromaDB).
    """
    if not request.question:
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")

    # TODO Sprint 4: integrar RAG aquí
    return {
        "question": request.question,
        "answer": random.choice(RESPUESTAS_SIMULADAS),
    }


@router.get("/getDatosDashboard")
def get_datos_dashboard():
    """
    Dashboard KPIs. Intenta leer de RDS; si falla, devuelve datos demo.
    """
    try:
        rows = fetch_all(
            "SELECT periodo, ocupados_miles FROM empleo_deporte_trimestral "
            "ORDER BY periodo DESC LIMIT 4"
        )
        if rows:
            valores = [float(r["ocupados_miles"]) for r in rows]
            ultimo = valores[0]
            anterior = valores[-1] if len(valores) > 1 else ultimo
            variacion = round((ultimo - anterior) / anterior * 100, 1) if anterior else 0

            return {
                "kpis": {
                    "total_empleo_miles": ultimo,
                    "variacion_anual_pct": variacion,
                    "ratio_hombres_mujeres": 1.8,
                },
                "empleo_trimestral": [
                    {"periodo": r["periodo"], "valor": float(r["ocupados_miles"])}
                    for r in reversed(rows)
                ],
            }
    except Exception as e:
        logger.warning(f"RDS no disponible para dashboard, usando datos demo: {e}")

    # Fallback: datos demo
    return {
        "kpis": {
            "total_empleo_miles": 294.1,
            "variacion_anual_pct": 3.2,
            "ratio_hombres_mujeres": 1.8,
        },
        "empleo_trimestral": [
            {"periodo": "2025-1T", "valor": 254.7},
            {"periodo": "2025-2T", "valor": 246.9},
            {"periodo": "2025-3T", "valor": 285.1},
            {"periodo": "2025-4T", "valor": 294.1},
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
