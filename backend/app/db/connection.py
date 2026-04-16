# Conexión a RDS MySQL con mysql-connector-python.


import mysql.connector
from app.config import get_settings


def get_connection(database: str | None = None):
    # Conexión a RDS MySQL.
    # Si `database` es None, usa la del .env (DB_NAME).
    # Si se pasa otra BD, conecta a esa (para endpoints admin).

    s = get_settings()
    return mysql.connector.connect(
        host=s.db_host,
        port=s.db_port,
        database=database if database is not None else s.db_name,
        user=s.db_user,
        password=s.db_password,
    )


def fetch_all(sql: str, params=None, database: str | None = None) -> list[dict]:
    # Ejecutar SELECT y devolver lista de dicts.
    conn = get_connection(database=database)
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        rows = cur.fetchall()
        cur.close()
        return rows
    finally:
        conn.close()


def fetch_one(sql: str, params=None, database: str | None = None) -> dict | None:
    # Ejecutar SELECT y devolver un solo dict o None.
    conn = get_connection(database=database)
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        row = cur.fetchone()
        cur.close()
        return row
    finally:
        conn.close()


def execute(sql: str, params=None, database: str | None = None) -> int:
    # Ejecutar INSERT / UPDATE / DELETE / CREATE / ALTER.
    # Hace commit y devuelve lastrowid (para INSERT con AUTO_INCREMENT) o rowcount (para UPDATE/DELETE).
    
    conn = get_connection(database=database)
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
        # lastrowid si fue INSERT con AUTO_INCREMENT; si no, rowcount
        result = cur.lastrowid if cur.lastrowid else cur.rowcount
        cur.close()
        return result
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
