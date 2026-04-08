from fastapi import FastAPI, HTTPException, Depends
import random

from app.models_request import LoginRequest, ChatRequest
from app.funciones import create_token, verify_token

app = FastAPI(
    title="DeporteData API",
    description="Backend API para DeporteData",
    version="0.2.0",
)

# Temporal hasta tener BD
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


# Endpoints públicos

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/login")
def login(request: LoginRequest):
    if not request.username or not request.password:
        raise HTTPException(status_code=400, detail="Faltan datos: username y password son obligatorios")

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


# Endpoints protegidos

@app.post("/getResponseChat")
def get_response_chat(request: ChatRequest):
    if not request.question:
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")

    return {
        "question": request.question,
        "answer": random.choice(RESPUESTAS_SIMULADAS),
    }


@app.get("/getDatosDashboard")
def get_datos_dashboard():
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