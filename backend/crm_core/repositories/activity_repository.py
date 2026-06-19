"""Lead activity repository."""

from database.models import LeadActivity

from crm_core.repositories.base_repository import BaseRepository


class ActivityRepository(BaseRepository[LeadActivity]):
    """Data access helper for LeadActivity records."""

    model = LeadActivity

    # TODO: Add lead timeline queries when lead detail APIs are implemented.
