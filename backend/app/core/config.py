from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = BASE_DIR / "data"
FALLBACK_DATA_DIR = BASE_DIR.parent / "docs" / "clean_data"

DATA_DIR = Path(os.getenv("DATA_DIR", str(DEFAULT_DATA_DIR))).resolve()

_raw_origins = os.getenv("FRONTEND_ORIGINS", "")
if _raw_origins.strip():
    FRONTEND_ORIGINS = [origin.strip() for origin in _raw_origins.split(",") if origin.strip()]
else:
    FRONTEND_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://deported-data-dindr.vercel.app",
        "https://*.vercel.app",
    ]
