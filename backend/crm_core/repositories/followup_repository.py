"""Follow-up task repository."""

from datetime import datetime

from sqlalchemy import select

from database.models import FollowupTask

from crm_core.repositories.base_repository import BaseRepository


class FollowupRepository(BaseRepository[FollowupTask]):
    """Data access helper for FollowupTask records."""

    model = FollowupTask

    def get_due(self, *, due_before: datetime | None = None, status: str = "pending") -> list[FollowupTask]:
        """Return follow-up tasks due on or before a timestamp."""
        cutoff = due_before or datetime.utcnow()
        statement = (
            select(FollowupTask)
            .where(FollowupTask.status == status)
            .where(FollowupTask.due_at <= cutoff)
            .order_by(FollowupTask.due_at.asc())
        )
        return list(self.session.scalars(statement).all())

    # TODO: Add owner filtering after authentication and assignment semantics exist.
