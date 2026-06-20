"""Conversation thread model."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import BaseModel

if TYPE_CHECKING:
    from database.models.conversation_message import ConversationMessage
    from database.models.lead import Lead


class ConversationThread(BaseModel):
    """A channel-specific conversation attached to a lead."""

    __tablename__ = "conversation_threads"

    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    channel: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

    lead: Mapped["Lead"] = relationship("Lead", back_populates="conversation_threads")
    messages: Mapped[list["ConversationMessage"]] = relationship(
        "ConversationMessage",
        back_populates="thread",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    __table_args__ = (
        Index("ix_conversation_threads_lead_channel", "lead_id", "channel"),
        Index("ix_conversation_threads_status_channel", "status", "channel"),
    )

    # TODO: Add external thread identifiers when email/LinkedIn/WhatsApp integrations exist.
