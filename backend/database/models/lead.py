"""Lead domain model.

The Lead model is the central record in LeadFlow's conversion data layer.
It intentionally stores operational state only; AI scoring, outreach, and
follow-up behavior live in separate models and services.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import BaseModel

if TYPE_CHECKING:
    from database.models.ai_insight import AIInsight
    from database.models.conversion_prediction import ConversionPrediction
    from database.models.customer import Customer
    from database.models.followup_task import FollowupTask
    from database.models.lead_activity import LeadActivity
    from database.models.conversation_thread import ConversationThread


class Lead(BaseModel):
    """A prospect moving through the LeadFlow conversion lifecycle."""

    __tablename__ = "leads"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    stage: Mapped[str] = mapped_column(String(50), nullable=False, default="new", index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="new", index=True)
    priority: Mapped[str] = mapped_column(String(30), nullable=False, default="normal", index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    assigned_to: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    external_source_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    campaign_name: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    last_contacted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)
    last_followup_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)
    converted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)
    lost_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)

    activities: Mapped[list["LeadActivity"]] = relationship(
        "LeadActivity",
        back_populates="lead",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    followups: Mapped[list["FollowupTask"]] = relationship(
        "FollowupTask",
        back_populates="lead",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    ai_insights: Mapped[list["AIInsight"]] = relationship(
        "AIInsight",
        back_populates="lead",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    customer: Mapped["Customer | None"] = relationship(
        "Customer",
        back_populates="lead",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin",
    )
    conversation_threads: Mapped[list["ConversationThread"]] = relationship(
        "ConversationThread",
        back_populates="lead",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    conversion_predictions: Mapped[list["ConversionPrediction"]] = relationship(
        "ConversionPrediction",
        back_populates="lead",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    __table_args__ = (
        Index("ix_leads_source_stage_status", "source", "stage", "status"),
        Index("ix_leads_external_source", "source", "external_source_id"),
    )

    # TODO: Move lifecycle constants to a dedicated domain contract module.
