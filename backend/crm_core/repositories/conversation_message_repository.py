"""Conversation message repository."""

from sqlalchemy import select

from database.models import ConversationMessage

from crm_core.repositories.base_repository import BaseRepository


class ConversationMessageRepository(BaseRepository[ConversationMessage]):
    """Data access helper for ConversationMessage records."""

    model = ConversationMessage

    def list_by_thread(self, thread_id: int, *, limit: int = 100) -> list[ConversationMessage]:
        """Return messages for a thread in chronological order."""
        statement = (
            select(ConversationMessage)
            .where(ConversationMessage.thread_id == thread_id)
            .order_by(ConversationMessage.created_at.asc())
            .limit(limit)
        )
        return list(self.session.scalars(statement).all())

    def get_latest_customer_reply(self, thread_id: int) -> ConversationMessage | None:
        """Return the latest lead/customer-authored message in a thread."""
        statement = (
            select(ConversationMessage)
            .where(ConversationMessage.thread_id == thread_id)
            .where(ConversationMessage.sender.in_(("lead", "customer")))
            .order_by(ConversationMessage.created_at.desc())
            .limit(1)
        )
        return self.session.scalars(statement).first()

    def get_by_external_message_id(self, external_message_id: str | None) -> ConversationMessage | None:
        """Return one message by provider Message-ID."""
        if not external_message_id:
            return None
        statement = (
            select(ConversationMessage)
            .where(ConversationMessage.external_message_id == external_message_id)
            .order_by(ConversationMessage.created_at.desc())
            .limit(1)
        )
        return self.session.scalars(statement).first()

    def get_by_in_reply_to(self, in_reply_to: str | None) -> ConversationMessage | None:
        """Return the original message referenced by an In-Reply-To header."""
        if not in_reply_to:
            return None
        return self.get_by_external_message_id(in_reply_to)

    def exists_external_message_id(self, external_message_id: str | None) -> bool:
        """Return True when a provider Message-ID has already been stored."""
        return self.get_by_external_message_id(external_message_id) is not None

    # TODO: Add pagination cursor support when conversation histories grow.
