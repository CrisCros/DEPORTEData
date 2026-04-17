"""
DEPORTEData — Configuración centralizada.
Lee variables de entorno (pasadas via docker run -e o .env).
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Identificación (nombre del grupo o proyecto)
    nom_user_id: str = "proyecto_deportedata"

    # Spark Master
    spark_master_ip: str = "CAMBIAR_AQUI"

    # RDS MySQL
    db_host: str = "CAMBIAR_AQUI"
    db_port: int = 3306
    db_user: str = "admin"
    db_password: str = "CAMBIAR_AQUI"
    db_name: str = "deportedata"
    # RDS MySQL: Tabla de usuarios MYSQL
    name_table_users: str = "deportedata_users"


    # S3
    s3_bucket_datalake: str = "deportedata-datalake"
    aws_region: str = "us-east-1"

    # Auth JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # Puertos
    public_api_port: int = 8000
    private_api_port: int = 8001

    # IA Service (nuevo) ─────────────────────────────────────────────
    ia_service_url: str = "http://ia-service:8100"
    ia_service_timeout_seconds: int = 120

    @property
    def spark_master_url(self) -> str:
        return f"spark://{self.spark_master_ip}:7077"

    @property
    def s3_prefix(self) -> str:
        return f"deportedata/{self.nom_user_id}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
