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
- Documentación Swagger: `http://localhost:8000/docs`

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Health check |

## Tests
```bash
pytest tests/ -v
```

## Docker
```bash
docker build -t deportedata-backend .
docker run -p 8000:8000 deportedata-backend
```