import os, getpass, psycopg2, psycopg2.extras
from contextlib import contextmanager

HOST = os.getenv("DB_HOST", "127.0.0.1")
PORT = int(os.getenv("DB_PORT", "5432"))
NAME = os.getenv("DB_NAME", "cities")
USER = os.getenv("DB_USER", "postgres")
_password_cache = None

def _password():
    global _password_cache
    if _password_cache is None:
        _password_cache = getpass.getpass(f"Password for user '{USER}': ")
    return _password_cache

def get_conn():
    return psycopg2.connect(host=HOST, port=PORT, dbname=NAME, user=USER, password=_password())

@contextmanager
def get_cursor(commit: bool = False):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            yield cur
            if commit:
                conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
