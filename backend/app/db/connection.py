"""
Conexión a RDS MySQL con mysql-connector-python.
"""

import mysql.connector
from app.config import get_settings


def get_connection():
    s = get_settings()
    return mysql.connector.connect(
        host=s.db_host,
        port=s.db_port,
        database=s.db_name,
        user=s.db_user,
        password=s.db_password,
    )


def fetch_all(sql: str, params=None) -> list[dict]:
    """Ejecutar SELECT y devolver lista de dicts."""
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        rows = cur.fetchall()
        cur.close()
        return rows
    finally:
        conn.close()


def fetch_one(sql: str, params=None) -> dict | None:
    """Ejecutar SELECT y devolver un solo dict o None."""
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        row = cur.fetchone()
        cur.close()
        return row
    finally:
        conn.close()
