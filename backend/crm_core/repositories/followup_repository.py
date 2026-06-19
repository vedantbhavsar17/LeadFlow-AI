"""Follow-up task repository."""

from database.models import FollowupTask

from crm_core.repositories.base_repository import BaseRepository


class FollowupRepository(BaseRepository[FollowupTask]):
    """Data access helper for FollowupTask records."""

    model = FollowupTask

    # TODO: Add due-task queries when scheduler behavior is implemented.
