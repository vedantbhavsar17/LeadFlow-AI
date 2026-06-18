"""Shared SQLAlchemy model base classes.

Only infrastructure-level columns live here. Domain fields belong in concrete
models during later phases.
"""

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from database.extensions import db


class TimestampMixin:
    """Reusable timestamp columns for persistent records."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class BaseModel(TimestampMixin, db.Model):
    """Abstract base model for future LeadFlow database tables.

    Provides a simple integer primary key and timestamp fields. This keeps MVP
    SQLite usage straightforward while remaining compatible with PostgreSQL.

    TODO: Add shared serialization or audit helpers only after real model
    needs emerge.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Generate a conservative default table name for subclasses."""
        return cls.__name__.lower()
