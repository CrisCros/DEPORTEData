from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import FRONTEND_ORIGINS
from app.funciones import create_token
from app.models_request import LoginRequest
from app.routes.chat import router as chat_router
from app.routes.dashboard import router as dashboard_router

app = FastAPI(
    title="DeporteData API",
    description="Backend API para DeporteData",
    version="0.3.1",
)

explicit_origins = [origin for origin in FRONTEND_ORIGINS if "*" not in origin]
has_vercel_wildcard = any(origin == "https://*.vercel.app" for origin in FRONTEND_ORIGINS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=explicit_origins,
    allow_origin_regex=r"https://.*\.vercel\.app" if has_vercel_wildcard else None,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
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


app.include_router(dashboard_router)
app.include_router(chat_router)
