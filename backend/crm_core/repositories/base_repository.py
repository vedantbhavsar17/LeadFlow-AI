"""Shared repository primitives for LeadFlow data access."""

from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.base import BaseModel
from database.session import get_session

ModelT = TypeVar("ModelT", bound=BaseModel)


class BaseRepository(Generic[ModelT]):
    """Small CRUD repository around a SQLAlchemy model.

    Repositories intentionally avoid business decisions. Validation,
    workflow transitions, AI calls, and integration behavior belong in
    services added during later phases.
    """

    model: type[ModelT]

    def __init__(self, session: Session | None = None) -> None:
        """Create a repository bound to a SQLAlchemy session."""
        self.session = session or get_session()

    def create(self, **data: Any) -> ModelT:
        """Create and persist one model instance."""
        record = self.model(**data)
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def update(self, record_id: int, **data: Any) -> ModelT | None:
        """Update a model instance by id."""
        record = self.get_by_id(record_id)
        if record is None:
            return None

        for field, value in data.items():
            if hasattr(record, field):
                setattr(record, field, value)

        self.session.commit()
        self.session.refresh(record)
        return record

    def get_by_id(self, record_id: int) -> ModelT | None:
        """Return one model instance by primary key."""
        return self.session.get(self.model, record_id)

    def delete(self, record_id: int) -> bool:
        """Delete one model instance by id."""
        record = self.get_by_id(record_id)
        if record is None:
            return False

        self.session.delete(record)
        self.session.commit()
        return True

    def list(self, *, limit: int = 100, offset: int = 0) -> list[ModelT]:
        """Return model instances with conservative pagination defaults."""
        statement = select(self.model).offset(offset).limit(limit)
        return list(self.session.scalars(statement).all())

    # TODO: Add explicit filtering methods per repository when API contracts exist.
