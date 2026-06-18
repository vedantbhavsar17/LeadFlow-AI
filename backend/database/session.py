"""Database session utilities.

These helpers centralize session lifecycle behavior without introducing
repositories or business logic.
"""

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy.orm import Session

from database.extensions import db


def get_session() -> Session:
    """Return the current Flask-SQLAlchemy scoped session."""
    return db.session


@contextmanager
def session_scope() -> Iterator[Session]:
    """Provide a transactional session scope for scripts and future services.

    TODO: Prefer request-scoped sessions in API handlers and use this helper
    only for scripts, seeders, and CLI-style operations.
    """
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
