"""
API Privada (:8001) — Administración, Spark jobs, subida S3.

Endpoints:
  - GET  /internal/health               → estado
  - POST /internal/jobs/curation        → Job 1: limpieza CSV → Parquet (spark-submit)
  - POST /internal/jobs/analytics       → Job 2: analítica + forecast (spark-submit)
  - POST /internal/upload/csv           → subir CSV a S3
  - POST /internal/upload/s3            → subir archivo genérico a S3
  - GET  /internal/rds/tables           → listar tablas en RDS
  - GET  /internal/s3/list              → listar keys en S3
"""

import os
import subprocess
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.config import get_settings
from app.db.connection import fetch_all
from app.s3_client import upload_bytes, list_keys

logger = logging.getLogger(__name__)
router = APIRouter(tags=["private"])


# ──────────────────────────────────────────────
# Spark Submit helper
# ──────────────────────────────────────────────

def _spark_submit(job_file: str, timeout: int = 600) -> dict:
    """
    Ejecuta spark-submit contra el master remoto.
    Los jobs están en /opt/spark-apps/ (copiados en el Dockerfile).
    """
    s = get_settings()
    path = f"/opt/spark-apps/{job_file}"

    if not os.path.exists(path):
        raise HTTPException(404, f"Job no encontrado: {path}")

    cmd = [
        "spark-submit",
        "--master", s.spark_master_url,
        "--deploy-mode", "client",
        "--conf", "spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem",
        "--conf", "spark.hadoop.fs.s3a.aws.credentials.provider="
                  "com.amazonaws.auth.DefaultAWSCredentialsProviderChain",
        path,
    ]

    logger.info(f"spark-submit: {' '.join(cmd)}")

    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {
            "status": "completed" if r.returncode == 0 else "failed",
            "returncode": r.returncode,
            "stdout_tail": r.stdout[-3000:] if r.stdout else "",
            "stderr_tail": r.stderr[-2000:] if r.stderr else "",
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(504, f"Timeout ejecutando {job_file}")


# Endpoints
@router.get("/internal/health")
def health():
    s = get_settings()
    return {"status": "ok", "nom_user_id": s.nom_user_id}


@router.post("/internal/jobs/curation")
def job_curation():
    """Job 1 — Curación: CSVs raw → Parquet limpio en S3."""
    return {"job": "curation", **_spark_submit("job1_curation.py")}


@router.post("/internal/jobs/analytics")
def job_analytics():
    """Job 2 — Analítica: modelo estrella + forecast → S3 + RDS."""
    return {"job": "analytics", **_spark_submit("job2_analytics.py")}


@router.post("/internal/jobs/test")
def job_test():
    """Job Test — Calcula Pi para verificar conexión al clúster Spark. No necesita S3 ni RDS."""
    return {"job": "test", **_spark_submit("job_test.py", timeout=120)}


@router.post("/internal/upload/csv")
async def upload_csv(file: UploadFile = File(...), s3_prefix: str = "raw/"):
    """Sube un CSV al bucket data lake en S3."""
    s = get_settings()
    key = f"{s3_prefix.rstrip('/')}/{file.filename}"
    content = await file.read()
    try:
        path = upload_bytes(content, key, content_type="text/csv")
        return {"status": "uploaded", "s3_path": path, "size": len(content)}
    except Exception as e:
        raise HTTPException(500, f"Error subiendo a S3: {e}")


@router.post("/internal/upload/s3")
async def upload_s3(file: UploadFile = File(...), s3_key: str = "raw/manual/file.csv"):
    """Sube un archivo a S3 con una key específica."""
    content = await file.read()
    path = upload_bytes(content, s3_key)
    return {"s3_path": path, "size": len(content)}


@router.get("/internal/rds/tables")
def rds_tables():
    """Lista las tablas existentes en RDS."""
    try:
        return {"tables": fetch_all("SHOW TABLES")}
    except Exception as e:
        raise HTTPException(500, f"Error consultando RDS: {e}")


@router.get("/internal/s3/list")
def s3_list(prefix: str = ""):
    """Lista keys en S3 (raw/, processed/, analytics/)."""
    return {"keys": list_keys(prefix)}
