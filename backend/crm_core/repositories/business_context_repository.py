"""Business context repository."""

from database.models import BusinessContext

from crm_core.repositories.base_repository import BaseRepository


class BusinessContextRepository(BaseRepository[BusinessContext]):
    """Data access helper for BusinessContext records."""

    model = BusinessContext

    # TODO: Add active-context lookup after organization settings exist.
