"""Raw lead event repository."""

from database.models import RawLeadEvent

from crm_core.repositories.base_repository import BaseRepository


class RawLeadEventRepository(BaseRepository[RawLeadEvent]):
    """Data access helper for RawLeadEvent records."""

    model = RawLeadEvent

    # TODO: Add source/external-id lookup helpers when ingestion dedupe rules mature.
