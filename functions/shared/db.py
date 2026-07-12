"""Shared database access for the Azure Functions timer jobs.

The functions reuse the backend ORM models (installed as the ``app`` package) so
schema stays in one place. DATABASE_URL is provided via app settings / Key Vault.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://localmarket:localmarket@localhost:5432/localmarket",
)

_engine = create_engine(_DATABASE_URL, pool_pre_ping=True, future=True)
_SessionLocal = sessionmaker(bind=_engine, future=True)


@contextmanager
def session_scope() -> Iterator[Session]:
    session = _SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
