"""AI insight model."""

from sqlalchemy import Float, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import BaseModel
from database.extensions import db


class AIInsight(BaseModel):
    """Stored AI output associated with a lead."""

    __tablename__ = "ai_insights"

    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    insight_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(80), nullable=False, default="nim", index=True)
    model: Mapped[str | None] = mapped_column(String(160), nullable=True)
    output: Mapped[dict | str | None] = mapped_column(db.JSON, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    lead: Mapped["Lead"] = relationship("Lead", back_populates="ai_insights")

    __table_args__ = (
        Index("ix_ai_insights_lead_type", "lead_id", "insight_type"),
    )

    # Examples: qualification, pain_points, reply_analysis,
    # conversion_prediction.
