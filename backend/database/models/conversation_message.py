"""Conversation message model."""

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import BaseModel


class ConversationMessage(BaseModel):
    """One message in a conversation thread."""

    __tablename__ = "conversation_messages"

    thread_id: Mapped[int] = mapped_column(
        ForeignKey("conversation_threads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sender: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    message_text: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[str] = mapped_column(String(50), nullable=False, default="text", index=True)
    external_message_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    in_reply_to: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    from_email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    to_email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)

    thread: Mapped["ConversationThread"] = relationship("ConversationThread", back_populates="messages")

    __table_args__ = (
        Index("ix_conversation_messages_thread_created", "thread_id", "created_at"),
        Index("ix_conversation_messages_thread_sender", "thread_id", "sender"),
        Index("ix_conversation_messages_external_reply", "external_message_id", "in_reply_to"),
    )

    # TODO: Add attachment fields when integrations support file handling.
