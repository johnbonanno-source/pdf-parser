import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def _database_url_from_streamlit_secrets() -> str | None:
    try:
        import streamlit as st
    except Exception:
        return None

    try:
        value = st.secrets.get("DATABASE_URL")
    except Exception:
        return None

    if not value:
        return None
    return str(value)


def get_database_url() -> str:
    database_url = _database_url_from_streamlit_secrets() or os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not set. Configure it in your environment or Streamlit secrets."
        )
    return database_url


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    return create_engine(get_database_url(), pool_pre_ping=True)
