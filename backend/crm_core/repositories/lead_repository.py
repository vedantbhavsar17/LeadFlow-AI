"""Lead repository."""

from database.models import Lead

from crm_core.repositories.base_repository import BaseRepository


class LeadRepository(BaseRepository[Lead]):
    """Data access helper for Lead records."""

    model = Lead

    # TODO: Add lifecycle and source-specific query helpers after API design.
