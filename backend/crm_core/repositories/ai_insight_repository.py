"""AI insight repository."""

from sqlalchemy import select

from database.models import AIInsight

from crm_core.repositories.base_repository import BaseRepository


class AIInsightRepository(BaseRepository[AIInsight]):
    """Data access helper for AIInsight records."""

    model = AIInsight

    def get_latest_for_lead(self, *, lead_id: int, insight_type: str) -> AIInsight | None:
        """Return the latest insight for a lead and insight type."""
        statement = (
            select(AIInsight)
            .where(AIInsight.lead_id == lead_id)
            .where(AIInsight.insight_type == insight_type)
            .order_by(AIInsight.created_at.desc())
            .limit(1)
        )
        return self.session.scalars(statement).first()

    # TODO: Add pruning/retention helpers if AI insight volume grows.
