"""LeadFlow database foundation.

Exports database extension primitives without importing domain models.
"""

from database.base import BaseModel
from database.extensions import db, init_database, migrate
from database.session import get_session, session_scope

__all__ = [
    "BaseModel",
    "db",
    "get_session",
    "init_database",
    "migrate",
    "session_scope",
]
