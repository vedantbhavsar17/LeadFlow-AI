"""Analytics metric aggregation service."""

from __future__ import annotations

import logging
from datetime import datetime

from sqlalchemy import distinct, func, select
from sqlalchemy.orm import Session

from analytics.analytics_models import ConversionMetrics, FollowupMetrics, PredictionMetrics
from crm_core.repositories import (
    AIInsightRepository,
    ConversionPredictionRepository,
    FollowupRepository,
    LeadRepository,
)
from database.models import AIInsight, ConversationMessage, ConversationThread, ConversionPrediction, FollowupTask, Lead, LeadActivity
from database.session import get_session

logger = logging.getLogger(__name__)


class MetricsService:
    """Read-only aggregation service for dashboard and reporting metrics."""

    def __init__(
        self,
        *,
        lead_repository: LeadRepository | None = None,
        followup_repository: FollowupRepository | None = None,
        ai_insight_repository: AIInsightRepository | None = None,
        prediction_repository: ConversionPredictionRepository | None = None,
        session: Session | None = None,
    ) -> None:
        """Create a metrics service with injectable repositories."""
        self.session = session or get_session()
        self.lead_repository = lead_repository or LeadRepository(session=self.session)
        self.followup_repository = followup_repository or FollowupRepository(session=self.session)
        self.ai_insight_repository = ai_insight_repository or AIInsightRepository(session=self.session)
        self.prediction_repository = prediction_repository or ConversionPredictionRepository(session=self.session)

    def total_leads(self) -> int:
        """Return total lead count."""
        return self._scalar_count(select(func.count(Lead.id)))

    def new_leads(self) -> int:
        """Return count of leads still in the new stage or status."""
        statement = select(func.count(Lead.id)).where((Lead.stage == "new") | (Lead.status == "new"))
        return self._scalar_count(statement)

    def converted_leads(self) -> int:
        """Return converted lead count."""
        statement = select(func.count(Lead.id)).where((Lead.converted_at.is_not(None)) | (Lead.status == "converted") | (Lead.stage == "converted"))
        return self._scalar_count(statement)

    def lost_leads(self) -> int:
        """Return lost lead count."""
        statement = select(func.count(Lead.id)).where((Lead.lost_at.is_not(None)) | (Lead.status == "lost") | (Lead.stage == "lost"))
        return self._scalar_count(statement)

    def conversion_rate(self) -> float:
        """Return converted leads divided by total leads as a percentage."""
        total = self.total_leads()
        if total == 0:
            return 0.0
        return round((self.converted_leads() / total) * 100, 2)

    def followups_due(self) -> int:
        """Return pending follow-ups due now or earlier."""
        now = datetime.utcnow()
        statement = select(func.count(FollowupTask.id)).where(FollowupTask.status == "pending", FollowupTask.due_at <= now)
        return self._scalar_count(statement)

    def meetings_booked(self) -> int:
        """Return count of meeting booked activities."""
        statement = select(func.count(LeadActivity.id)).where(LeadActivity.activity_type == "meeting_booked")
        return self._scalar_count(statement)

    def average_conversion_score(self) -> float:
        """Return average score across stored conversion predictions."""
        value = self.session.scalar(select(func.avg(ConversionPrediction.score)))
        return round(float(value or 0), 2)

    def lead_source_breakdown(self) -> dict[str, int]:
        """Return lead counts grouped by source."""
        statement = select(Lead.source, func.count(Lead.id)).group_by(Lead.source).order_by(Lead.source.asc())
        return {source or "unknown": count for source, count in self.session.execute(statement).all()}

    def reply_rate(self) -> float:
        """Return percent of contacted leads that received a customer reply."""
        contacted_statement = (
            select(func.count(distinct(LeadActivity.lead_id)))
            .where(LeadActivity.activity_type.in_(("email_sent", "reply_sent")))
        )
        replied_statement = (
            select(func.count(distinct(Lead.id)))
            .join(Lead.conversation_threads)
            .join(ConversationThread.messages)
            .where(ConversationMessage.sender.in_(("lead", "customer")))
        )
        contacted = self._scalar_count(contacted_statement)
        replied = self._scalar_count(replied_statement)
        if contacted == 0:
            return 0.0
        return round((replied / contacted) * 100, 2)

    def outreach_generated_count(self) -> int:
        """Return number of stored outreach generation insights."""
        statement = select(func.count(AIInsight.id)).where(AIInsight.insight_type == "outreach")
        return self._scalar_count(statement)

    def ai_qualification_distribution(self) -> dict[str, int]:
        """Return AI qualification counts grouped by category."""
        distribution = {"hot": 0, "warm": 0, "cold": 0}
        statement = select(AIInsight.output).where(AIInsight.insight_type == "qualification")
        for output in self.session.scalars(statement).all():
            if isinstance(output, dict):
                category = str(output.get("category", "")).lower()
                if category in distribution:
                    distribution[category] += 1
        return distribution

    def lead_temperature_counts(self) -> dict[str, int]:
        """Return hot, warm, and cold lead counts from latest qualification insights."""
        return self.ai_qualification_distribution()

    def conversion_metrics(self) -> ConversionMetrics:
        """Return conversion-focused metric group."""
        return ConversionMetrics(
            converted_leads=self.converted_leads(),
            lost_leads=self.lost_leads(),
            conversion_rate=self.conversion_rate(),
            average_conversion_score=self.average_conversion_score(),
            prediction_distribution=self.prediction_distribution(),
        )

    def followup_metrics(self) -> FollowupMetrics:
        """Return follow-up metric group."""
        now = datetime.utcnow()
        pending_statement = select(func.count(FollowupTask.id)).where(FollowupTask.status == "pending")
        completed_statement = select(func.count(FollowupTask.id)).where(FollowupTask.status == "completed")
        overdue_statement = select(func.count(FollowupTask.id)).where(FollowupTask.status == "pending", FollowupTask.due_at < now)
        channel_statement = select(FollowupTask.channel, func.count(FollowupTask.id)).group_by(FollowupTask.channel)
        return FollowupMetrics(
            due=self.followups_due(),
            pending=self._scalar_count(pending_statement),
            completed=self._scalar_count(completed_statement),
            overdue=self._scalar_count(overdue_statement),
            by_channel={channel or "unknown": count for channel, count in self.session.execute(channel_statement).all()},
        )

    def prediction_metrics(self) -> PredictionMetrics:
        """Return prediction metric group."""
        distribution = self.prediction_distribution()
        return PredictionMetrics(
            total_predictions=self._scalar_count(select(func.count(ConversionPrediction.id))),
            average_score=self.average_conversion_score(),
            low_probability=distribution.get("low", 0),
            medium_probability=distribution.get("medium", 0),
            high_probability=distribution.get("high", 0),
        )

    def prediction_distribution(self) -> dict[str, int]:
        """Return prediction counts grouped by probability label."""
        distribution = {"low": 0, "medium": 0, "high": 0}
        statement = select(ConversionPrediction.probability_label, func.count(ConversionPrediction.id)).group_by(ConversionPrediction.probability_label)
        for label, count in self.session.execute(statement).all():
            normalized = str(label or "").lower()
            if normalized in distribution:
                distribution[normalized] = count
        return distribution

    def _scalar_count(self, statement) -> int:
        """Return an integer scalar count for a SQLAlchemy statement."""
        return int(self.session.scalar(statement) or 0)

    # TODO: Add date-range filters once dashboard API contracts include reporting periods.
