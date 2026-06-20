"""Follow-up scheduler helpers."""

from __future__ import annotations

from datetime import datetime

from crm_core.repositories import FollowupRepository
from database.models import FollowupTask


class FollowupScheduler:
    """Read due follow-up tasks from storage."""

    def __init__(self, followup_repository: FollowupRepository | None = None) -> None:
        """Create a scheduler with injectable repository."""
        self.followup_repository = followup_repository or FollowupRepository()

    def get_due_followups(self, *, due_before: datetime | None = None) -> list[FollowupTask]:
        """Return pending follow-ups due by a timestamp."""
        return self.followup_repository.get_due(due_before=due_before)

    # TODO: Add background execution only after product scheduling behavior is approved.
