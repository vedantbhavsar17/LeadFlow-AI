"""Conversion prediction model."""

from sqlalchemy import Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import BaseModel
from database.extensions import db


class ConversionPrediction(BaseModel):
    """Stored probability snapshot for a lead conversion forecast."""

    __tablename__ = "conversion_predictions"

    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    probability_label: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    reasons: Mapped[list[str]] = mapped_column(db.JSON, nullable=False, default=list)
    risk_factors: Mapped[list[str]] = mapped_column(db.JSON, nullable=False, default=list)
    recommended_action: Mapped[str] = mapped_column(String(120), nullable=False)
    provider: Mapped[str] = mapped_column(String(80), nullable=False, default="nim", index=True)
    model: Mapped[str | None] = mapped_column(String(160), nullable=True)
    ai_insight_id: Mapped[int | None] = mapped_column(
        ForeignKey("ai_insights.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    lead: Mapped["Lead"] = relationship("Lead", back_populates="conversion_predictions")
    ai_insight: Mapped["AIInsight | None"] = relationship("AIInsight")

    __table_args__ = (
        Index("ix_conversion_predictions_lead_created", "lead_id", "created_at"),
        Index("ix_conversion_predictions_lead_score", "lead_id", "score"),
    )

    # TODO: Add calibration metadata after real conversion outcomes exist.
