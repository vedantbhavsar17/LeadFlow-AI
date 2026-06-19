"""Conversation thread repository."""

from sqlalchemy import select

from database.models import ConversationThread

from crm_core.repositories.base_repository import BaseRepository


class ConversationThreadRepository(BaseRepository[ConversationThread]):
    """Data access helper for ConversationThread records."""

    model = ConversationThread

    def list_by_lead(self, lead_id: int) -> list[ConversationThread]:
        """Return conversation threads for one lead."""
        statement = select(ConversationThread).where(ConversationThread.lead_id == lead_id).order_by(ConversationThread.created_at.desc())
        return list(self.session.scalars(statement).all())

    def get_active_by_lead_channel(self, *, lead_id: int, channel: str) -> ConversationThread | None:
        """Return the active thread for a lead/channel pair."""
        statement = (
            select(ConversationThread)
            .where(ConversationThread.lead_id == lead_id)
            .where(ConversationThread.channel == channel)
            .where(ConversationThread.status == "active")
            .order_by(ConversationThread.created_at.desc())
            .limit(1)
        )
        return self.session.scalars(statement).first()

    # TODO: Add external thread identifiers when provider APIs expose them.
