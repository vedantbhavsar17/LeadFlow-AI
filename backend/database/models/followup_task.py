"""Follow-up task model."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import BaseModel


class FollowupTask(BaseModel):
    """A scheduled or suggested follow-up action for a lead."""

    __tablename__ = "followup_tasks"

    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    channel: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)

    lead: Mapped["Lead"] = relationship("Lead", back_populates="followups")

    __table_args__ = (
        Index("ix_followup_tasks_lead_status", "lead_id", "status"),
        Index("ix_followup_tasks_status_due", "status", "due_at"),
    )

    # TODO: Connect to scheduler and automation services in a later phase.
