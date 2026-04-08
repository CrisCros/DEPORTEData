# Backend - DeporteData API

API REST desarrollada con FastAPI.

## Requisitos

- Python 3.12+
- pip

## Instalación local
```bash
cd backend/
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

Para desactivar el entorno virtual una vez terminado:
```bash
deactivate
```

## Ejecución
```bash
uvicorn app.main:app --reload --port 8000
```

Endpoints disponibles:

- Health check: `http://localhost:8000/health`
- Documentación Swagger: `http://localhost:8000/endpoints`

## Endpoints

| Método | Ruta | Protegido | Descripción |
|--------|------|-----------|-------------|
| GET | `/health` | No | Health check |
| POST | `/login` | No | Autenticación, devuelve JWT |
| POST | `/getResponseChat` | Sí | Chat RAG simulado |
| GET | `/getDatosDashboard` | Sí | Datos y KPIs para dashboard |

Los endpoints protegidos requieren la cabecera: Authorization: Bearer <token>
El token se obtiene llamando a `/login` con:
```json
{
  "username": "admin",
  "password": "*admin1234"
}
```

## Estructura del módulo
backend/app/
├── init.py
├── main.py              # Definición de endpoints
├── funciones.py         # Lógica JWT y utilidades
└── models_request.py    # Modelos Pydantic de request


## Tests
```bash
pytest tests/ -v
```

## Docker
```bash
docker build -t deportedata-backend .
docker run -p 8000:8000 deportedata-backend
```