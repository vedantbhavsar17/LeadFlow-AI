"""Lead activity model."""

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import BaseModel


class LeadActivity(BaseModel):
    """A timeline event attached to a lead."""

    __tablename__ = "lead_activities"

    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    activity_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    channel: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    lead: Mapped["Lead"] = relationship("Lead", back_populates="activities")

    __table_args__ = (
        Index("ix_lead_activities_lead_type", "lead_id", "activity_type"),
    )

    # Examples: email_sent, email_received, followup_created,
    # meeting_booked, status_changed.
