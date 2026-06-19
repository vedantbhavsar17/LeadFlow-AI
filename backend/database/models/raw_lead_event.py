"""Raw lead event model."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import BaseModel
from database.extensions import db


class RawLeadEvent(BaseModel):
    """Raw incoming lead data before normalization into a Lead."""

    __tablename__ = "raw_lead_events"

    source: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    raw_payload: Mapped[dict | None] = mapped_column(db.JSON, nullable=True)
    normalized_payload: Mapped[dict | None] = mapped_column(db.JSON, nullable=True)
    is_processed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)

    __table_args__ = (
        Index("ix_raw_lead_events_source_external", "source", "external_id"),
        Index("ix_raw_lead_events_source_processed", "source", "is_processed"),
    )

    # TODO: Add ingestion error fields when source processors are implemented.
