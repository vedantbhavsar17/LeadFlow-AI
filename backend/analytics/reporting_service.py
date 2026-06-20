"""Reporting analytics service."""

from __future__ import annotations

from sqlalchemy.orm import Session

from analytics.analytics_models import ConversionMetrics, FollowupMetrics, PredictionMetrics
from analytics.metrics_service import MetricsService


class ReportingService:
    """Read-only reporting facade for analytics endpoints."""

    def __init__(self, *, metrics_service: MetricsService | None = None, session: Session | None = None) -> None:
        """Create a reporting service."""
        self.metrics_service = metrics_service or MetricsService(session=session)

    def lead_sources(self) -> dict[str, int]:
        """Return lead source breakdown."""
        return self.metrics_service.lead_source_breakdown()

    def conversions(self) -> ConversionMetrics:
        """Return conversion reporting metrics."""
        return self.metrics_service.conversion_metrics()

    def followups(self) -> FollowupMetrics:
        """Return follow-up reporting metrics."""
        return self.metrics_service.followup_metrics()

    def predictions(self) -> PredictionMetrics:
        """Return prediction reporting metrics."""
        return self.metrics_service.prediction_metrics()

    # TODO: Add export-ready tabular reports in a later reporting phase.

