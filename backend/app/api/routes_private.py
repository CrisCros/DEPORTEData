"""
API Privada (:8001) — Administración, Spark jobs, subida S3, gestión BD.

Endpoints:
  - GET  /internal/health                    → estado
  - POST /internal/jobs/curation             → Job 1: limpieza CSV → Parquet
  - POST /internal/jobs/analytics            → Job 2: analítica + forecast
  - POST /internal/jobs/test                 → Job Test: Pi (verificar cluster)
  - POST /internal/upload/csv                → subir CSV a S3
  - POST /internal/upload/s3                 → subir archivo genérico a S3
  - GET  /internal/rds/tables                → listar tablas en la BD del .env
  - GET  /internal/s3/list                   → listar keys en S3
  - GET  /internal/db/mostrar_tables         → tablas de una BD indicada
  - GET  /internal/db/mostrar_table          → filas de una tabla indicada
  - POST /internal/db/create_table_users     → crea tabla deportedata_users
  - POST /internal/db/add_user               → inserta un usuario (password hasheado)
"""

import os
import re
import subprocess
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Query

from app.config import get_settings
from app.db.connection import fetch_all, execute
from app.s3_client import upload_bytes, list_keys
from app.models import AddUserRequest
from app.password import hash_password

logger = logging.getLogger(__name__)
router = APIRouter(tags=["private"])


# Regex para validar identificadores MySQL (BD / tabla)
# y evitar SQL injection en endpoints que interpolan nombres.
IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def _validate_identifier(name: str, kind: str) -> str:
    """Valida que `name` sea un identificador MySQL seguro."""
    if not name or not IDENTIFIER_RE.match(name):
        raise HTTPException(
            status_code=400,
            detail=f"{kind} inválido: solo se permiten letras, números, '_' y '-'.",
        )
    return name


# Spark Submit helper
def _spark_submit(job_file: str, timeout: int = 600) -> dict:
    """Ejecuta spark-submit contra el master remoto."""
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
    """Job Test — Calcula Pi para verificar conexión al clúster Spark."""
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
    """Lista las tablas de la BD indicada en .env (DB_NAME)."""
    try:
        return {"tables": fetch_all("SHOW TABLES")}
    except Exception as e:
        raise HTTPException(500, f"Error consultando RDS: {e}")


@router.get("/internal/s3/list")
def s3_list(prefix: str = ""):
    """Lista keys en S3 (raw/, processed/, analytics/)."""
    return {"keys": list_keys(prefix)}


# Endpoints nuevos — gestión BD
@router.get("/internal/db/mostrar_tables")
def mostrar_tables(nom_database: str = Query(..., description="Nombre de la base de datos")):
    """
    Lista las tablas de una BD especificada.
    Ejemplo: GET /internal/db/mostrar_tables?nom_database=deportedata
    """
    db = _validate_identifier(nom_database, "nom_database")
    try:
        # No se puede parametrizar un identificador con %s → interpolación
        # segura tras validación regex + backticks.
        rows = fetch_all(f"SHOW TABLES FROM `{db}`")
        # SHOW TABLES devuelve dicts tipo {"Tables_in_<db>": "nombre"}
        tables = [list(r.values())[0] for r in rows]
        return {"database": db, "count": len(tables), "tables": tables}
    except Exception as e:
        raise HTTPException(500, f"Error listando tablas de '{db}': {e}")


@router.get("/internal/db/mostrar_table")
def mostrar_table(
    nom_database: str = Query(..., description="Nombre de la base de datos"),
    nom_table: str = Query(..., description="Nombre de la tabla"),
    limit: int = Query(default=100, ge=1, le=1000),
):
    """
    Muestra el contenido de una tabla específica.
    Ejemplo: GET /internal/db/mostrar_table?nom_database=deportedata&nom_table=deportedata_users&limit=50
    """
    db = _validate_identifier(nom_database, "nom_database")
    tbl = _validate_identifier(nom_table, "nom_table")
    try:
        rows = fetch_all(
            f"SELECT * FROM `{db}`.`{tbl}` LIMIT %s",
            (limit,),
        )
        return {
            "database": db,
            "table": tbl,
            "count": len(rows),
            "rows": rows,
        }
    except Exception as e:
        raise HTTPException(500, f"Error consultando '{db}.{tbl}': {e}")


@router.post("/internal/db/create_table_users")
def create_table_users():
    # Crea la tabla `deportedata_users` en la BD del .env (DB_NAME).
    # Esquema:
    #   - id_user         INT AUTO_INCREMENT PRIMARY KEY
    #   - username_user   VARCHAR(100) NOT NULL UNIQUE
    #   - password_user   VARCHAR(255) NOT NULL   ← hash bcrypt (60 chars)
    #   - role_user       VARCHAR(50)  DEFAULT 'user'
    #   - last_login_user DATETIME     NULL


    s = get_settings()
    
    sql = f"""
        CREATE TABLE IF NOT EXISTS `{s.name_table_users}` (
            id_user         INT AUTO_INCREMENT PRIMARY KEY,
            username_user   VARCHAR(100) NOT NULL UNIQUE,
            password_user   VARCHAR(255) NOT NULL,
            role_user       VARCHAR(50)  DEFAULT 'user',
            last_login_user DATETIME     NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    try:
        execute(sql)
        return {
            "status": "ok",
            "database": s.db_name,
            "table": s.name_table_users,
            "message": f"Tabla `{s.name_table_users}` creada (o ya existía).",
        }
    except Exception as e:
        raise HTTPException(500, f"Error creando tabla: {e}")


@router.post("/internal/db/add_user")
def add_user(request: AddUserRequest):
    """
    Inserta un usuario en `deportedata_users`.
    La contraseña se hashea con bcrypt antes de guardarse.

    Body JSON:
      {"username": "pepe", "pwd": "secreto123", "role": "admin"}
    """
    s = get_settings()

    username = request.username.strip()
    if not username:
        raise HTTPException(400, "username no puede estar vacío")

    hashed = hash_password(request.pwd)

    sql = f"""
        INSERT INTO `{s.name_table_users}`
            (username_user, password_user, role_user)
        VALUES (%s, %s, %s)
    """
    try:
        new_id = execute(sql, (username, hashed, request.role))
        return {
            "status": "created",
            "id_user": new_id,
            "username_user": username,
            "role_user": request.role,
        }
    except Exception as e:
        # Error 1062 = duplicado (UNIQUE en username_user)
        if "1062" in str(e) or "Duplicate" in str(e):
            raise HTTPException(409, f"El usuario '{username}' ya existe")
        raise HTTPException(500, f"Error insertando usuario: {e}")
