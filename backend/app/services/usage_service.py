import json
from datetime import datetime, timedelta
from typing import Any

from app.config import get_settings
from app.db.connection import execute, fetch_all, fetch_one


def _table_name() -> str:
    return get_settings().name_table_usage_events


def ensure_usage_events_table() -> None:
    table = _table_name()
    execute(
        f"""
        CREATE TABLE IF NOT EXISTS `{table}` (
            id_event BIGINT AUTO_INCREMENT PRIMARY KEY,
            event_type VARCHAR(80) NOT NULL,
            page VARCHAR(200) NULL,
            metadata_json JSON NULL,
            id_user INT NULL,
            username_user VARCHAR(100) NULL,
            user_role VARCHAR(50) NULL,
            ip_address VARCHAR(64) NULL,
            user_agent VARCHAR(255) NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_usage_event_type (event_type),
            INDEX idx_usage_created_at (created_at),
            INDEX idx_usage_user (id_user)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )


def record_usage_event(
    event_type: str,
    page: str | None,
    metadata: dict[str, Any] | None = None,
    user: dict[str, Any] | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> None:
    ensure_usage_events_table()
    table = _table_name()
    payload = json.dumps(metadata or {}, ensure_ascii=False)
    execute(
        f"""
        INSERT INTO `{table}`
            (event_type, page, metadata_json, id_user, username_user, user_role, ip_address, user_agent)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            event_type,
            page,
            payload,
            user.get("id_user") if user else None,
            user.get("name") if user else None,
            user.get("role") if user else None,
            ip_address,
            user_agent[:255] if user_agent else None,
        ),
    )


def get_usage_summary() -> dict:
    ensure_usage_events_table()
    table = _table_name()
    now = datetime.utcnow()
    since_24h = now - timedelta(hours=24)
    since_7d = now - timedelta(days=7)

    totals = fetch_one(
        f"""
        SELECT
            COUNT(*) AS total_events,
            SUM(created_at >= %s) AS events_24h,
            SUM(created_at >= %s) AS events_7d,
            COUNT(DISTINCT COALESCE(username_user, ip_address)) AS unique_actors
        FROM `{table}`
        """,
        (since_24h, since_7d),
    ) or {}

    by_type = fetch_all(
        f"""
        SELECT event_type, COUNT(*) AS count
        FROM `{table}`
        WHERE created_at >= %s
        GROUP BY event_type
        ORDER BY count DESC
        LIMIT 10
        """,
        (since_7d,),
    )

    recent_events = fetch_all(
        f"""
        SELECT id_event, event_type, page, username_user, user_role, created_at
        FROM `{table}`
        ORDER BY created_at DESC
        LIMIT 20
        """
    )

    chat_messages = fetch_one(
        f"""
        SELECT COUNT(*) AS count
        FROM `{table}`
        WHERE event_type = 'chat_message_sent'
          AND created_at >= %s
        """,
        (since_7d,),
    ) or {}

    admin_page_views = fetch_one(
        f"""
        SELECT COUNT(*) AS count
        FROM `{table}`
        WHERE event_type = 'admin_page_view'
          AND created_at >= %s
        """,
        (since_7d,),
    ) or {}

    return {
        "total_events": int(totals.get("total_events") or 0),
        "events_24h": int(totals.get("events_24h") or 0),
        "events_7d": int(totals.get("events_7d") or 0),
        "unique_actors": int(totals.get("unique_actors") or 0),
        "chat_messages_7d": int(chat_messages.get("count") or 0),
        "admin_page_views_7d": int(admin_page_views.get("count") or 0),
        "by_type": by_type,
        "recent_events": recent_events,
    }
