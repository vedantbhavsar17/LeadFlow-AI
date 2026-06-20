"""Conversion prediction repository."""

from sqlalchemy import select

from database.models import ConversionPrediction

from crm_core.repositories.base_repository import BaseRepository


class ConversionPredictionRepository(BaseRepository[ConversionPrediction]):
    """Data access helper for ConversionPrediction records."""

    model = ConversionPrediction

    def get_latest_for_lead(self, lead_id: int) -> ConversionPrediction | None:
        """Return the latest conversion prediction for a lead."""
        statement = (
            select(ConversionPrediction)
            .where(ConversionPrediction.lead_id == lead_id)
            .order_by(ConversionPrediction.created_at.desc())
            .limit(1)
        )
        return self.session.scalars(statement).first()

    def list_by_lead(self, lead_id: int, *, limit: int = 25) -> list[ConversionPrediction]:
        """Return recent conversion predictions for a lead."""
        statement = (
            select(ConversionPrediction)
            .where(ConversionPrediction.lead_id == lead_id)
            .order_by(ConversionPrediction.created_at.desc())
            .limit(limit)
        )
        return list(self.session.scalars(statement).all())

    # TODO: Add bulk trend queries for analytics dashboards.
