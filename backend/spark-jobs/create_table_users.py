"""
Spark Job — Crear tabla deportedata_users en RDS vía JDBC.

NOTA: usar un job Spark para un CREATE TABLE es overkill — el endpoint
`POST /internal/db/create_table_users` ya lo hace en ~50ms con mysql-connector.
Este job existe como referencia / alternativa si se quiere versionar la
creación junto con los demás jobs.

Uso (desde el container del backend):
    spark-submit /opt/spark-apps/create_table_users.py

Lee las variables de entorno DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
(las mismas que usa el backend FastAPI).
"""

import os
import sys

from pyspark.sql import SparkSession
from py4j.java_gateway import java_import


TABLE_NAME = "deportedata_users"

CREATE_SQL = f"""
    CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
        id_user         INT AUTO_INCREMENT PRIMARY KEY,
        username_user   VARCHAR(100) NOT NULL UNIQUE,
        password_user   VARCHAR(255) NOT NULL,
        role_user       VARCHAR(50)  DEFAULT 'user',
        last_login_user DATETIME     NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""


def main():
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    if not all([db_host, db_name, db_user, db_password]):
        print("ERROR: faltan variables DB_HOST / DB_NAME / DB_USER / DB_PASSWORD")
        sys.exit(1)

    jdbc_url = f"jdbc:mysql://{db_host}:{db_port}/{db_name}"

    spark = (
        SparkSession.builder
        .appName("DEPORTEData_CreateTableUsers")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    print(f"[create_table_users] JDBC URL: {jdbc_url}")
    print(f"[create_table_users] Tabla:    {TABLE_NAME}")

    try:
        # Ejecutar DDL vía driver MySQL JDBC (no hay API nativa en Spark para DDL)
        java_import(spark._jvm, "java.sql.DriverManager")
        conn = spark._jvm.java.sql.DriverManager.getConnection(
            jdbc_url, db_user, db_password,
        )
        stmt = conn.createStatement()
        stmt.execute(CREATE_SQL)
        stmt.close()
        conn.close()
        print(f"[create_table_users] ✔ Tabla `{TABLE_NAME}` creada (o ya existía).")
    except Exception as e:
        print(f"[create_table_users] ✗ Error: {e}")
        sys.exit(1)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
