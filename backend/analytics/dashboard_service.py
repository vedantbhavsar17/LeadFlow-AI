"""Dashboard analytics service."""

from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from analytics.analytics_models import DashboardMetrics
from analytics.metrics_service import MetricsService

logger = logging.getLogger(__name__)


class DashboardService:
    """Build dashboard-ready analytics summaries."""

    def __init__(self, *, metrics_service: MetricsService | None = None, session: Session | None = None) -> None:
        """Create a dashboard service."""
        self.metrics_service = metrics_service or MetricsService(session=session)

    def get_dashboard_metrics(self) -> DashboardMetrics:
        """Return all primary dashboard metrics."""
        lead_temperature = self.metrics_service.lead_temperature_counts()
        metrics = DashboardMetrics(
            total_leads=self.metrics_service.total_leads(),
            new_leads=self.metrics_service.new_leads(),
            hot_leads=lead_temperature.get("hot", 0),
            warm_leads=lead_temperature.get("warm", 0),
            cold_leads=lead_temperature.get("cold", 0),
            converted_leads=self.metrics_service.converted_leads(),
            conversion_rate=self.metrics_service.conversion_rate(),
            followups_due=self.metrics_service.followups_due(),
            meetings_booked=self.metrics_service.meetings_booked(),
            average_conversion_score=self.metrics_service.average_conversion_score(),
            lead_source_breakdown=self.metrics_service.lead_source_breakdown(),
            reply_rate=self.metrics_service.reply_rate(),
            outreach_generated_count=self.metrics_service.outreach_generated_count(),
            ai_qualification_distribution=self.metrics_service.ai_qualification_distribution(),
        )
        logger.info("Generated dashboard analytics total_leads=%s", metrics.total_leads)
        return metrics

    # TODO: Add widget-level caching after API usage patterns are known.

