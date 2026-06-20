"""Business context repository."""

from sqlalchemy import select

from database.models import BusinessContext

from crm_core.repositories.base_repository import BaseRepository


class BusinessContextRepository(BaseRepository[BusinessContext]):
    """Data access helper for BusinessContext records."""

    model = BusinessContext

    def get_latest(self) -> BusinessContext | None:
        """Return the most recently updated business context."""
        statement = select(BusinessContext).order_by(BusinessContext.updated_at.desc()).limit(1)
        return self.session.scalars(statement).first()

    # TODO: Add active-context lookup after organization settings exist.
