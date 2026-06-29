
import json
import logging
import sqlite3
import threading
from datetime import datetime, timedelta

from app.core import config

log = logging.getLogger("cache")

CACHE_DB = config.CACHE_DB

# check_same_thread=False só é seguro com lock externo. Mantemos o LOCK.
LOCK = threading.Lock()


def _conn():
    # timeout para evitar "database is locked" sob concorrência
    return sqlite3.connect(CACHE_DB, timeout=10, isolation_level=None)


def init_cache():
    try:
        with _conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cache (
                    cache_key TEXT PRIMARY KEY,
                    response TEXT,
                    expires_at DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        log.info("[CACHE] Banco inicializado em %s", CACHE_DB)
    except Exception as e:
        log.exception("[CACHE] Falha ao inicializar (%s): %s", CACHE_DB, e)


def get_cache(cache_key):
    try:
        with LOCK, _conn() as conn:
            row = conn.execute(
                "SELECT response, expires_at FROM cache WHERE cache_key = ?",
                (cache_key,),
            ).fetchone()
    except Exception as e:
        log.warning("[CACHE GET ERROR] %s", e)
        return None

    if not row:
        return None

    response, expires_at = row

    if expires_at:
        try:
            expires_at_dt = datetime.fromisoformat(expires_at)
            if datetime.utcnow() > expires_at_dt:
                log.info("[CACHE EXPIRED] %s", cache_key)
                delete_cache(cache_key)
                return None
        except Exception as e:
            log.warning("[CACHE ERROR PARSE] %s", e)
            return None

    log.info("[CACHE HIT] %s", cache_key)

    try:
        return json.loads(response)
    except Exception as e:
        log.warning("[CACHE JSON ERROR] %s", e)
        return None


def set_cache(cache_key, response, ttl=86400):
    expires_at = (
        datetime.utcnow() + timedelta(seconds=ttl)
    ).isoformat()

    try:
        with LOCK, _conn() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO cache (cache_key, response, expires_at)
                VALUES (?, ?, ?)
                """,
                (cache_key, json.dumps(response), expires_at),
            )
        log.info("[CACHE SAVED] %s", cache_key)
    except Exception as e:
        log.warning("[CACHE SET ERROR] %s", e)


def delete_cache(cache_key):
    try:
        with LOCK, _conn() as conn:
            conn.execute(
                "DELETE FROM cache WHERE cache_key = ?",
                (cache_key,),
            )
        log.info("[CACHE REMOVED] %s", cache_key)
    except Exception as e:
        log.warning("[CACHE DELETE ERROR] %s", e)


def clear_cache():
    try:
        with LOCK, _conn() as conn:
            conn.execute("DELETE FROM cache")
        log.info("[CACHE CLEARED]")
    except Exception as e:
        log.warning("[CACHE CLEAR ERROR] %s", e)
