"""Lead journey service."""

from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from analytics.journey.journey_builder import LeadJourneyBuilder
from analytics.journey.journey_models import LeadJourney, StageProgress
from crm_core.repositories import (
    AIInsightRepository,
    ActivityRepository,
    ConversationMessageRepository,
    ConversationThreadRepository,
    ConversionPredictionRepository,
    FollowupRepository,
    LeadRepository,
)
from crm_core.services import NotFoundError
from database.models import AIInsight, ConversationMessage, ConversionPrediction, FollowupTask, Lead, LeadActivity
from database.session import get_session

logger = logging.getLogger(__name__)


class LeadJourneyService:
    """Canonical read service for a lead's complete lifecycle journey."""

    def __init__(
        self,
        *,
        lead_repository: LeadRepository | None = None,
        activity_repository: ActivityRepository | None = None,
        ai_insight_repository: AIInsightRepository | None = None,
        thread_repository: ConversationThreadRepository | None = None,
        message_repository: ConversationMessageRepository | None = None,
        followup_repository: FollowupRepository | None = None,
        prediction_repository: ConversionPredictionRepository | None = None,
        journey_builder: LeadJourneyBuilder | None = None,
        session: Session | None = None,
    ) -> None:
        """Create a lead journey service with injectable dependencies."""
        self.session = session or get_session()
        self.lead_repository = lead_repository or LeadRepository(session=self.session)
        self.activity_repository = activity_repository or ActivityRepository(session=self.session)
        self.ai_insight_repository = ai_insight_repository or AIInsightRepository(session=self.session)
        self.thread_repository = thread_repository or ConversationThreadRepository(session=self.session)
        self.message_repository = message_repository or ConversationMessageRepository(session=self.session)
        self.followup_repository = followup_repository or FollowupRepository(session=self.session)
        self.prediction_repository = prediction_repository or ConversionPredictionRepository(session=self.session)
        self.journey_builder = journey_builder or LeadJourneyBuilder()

    def get_lead_journey(self, lead_id: int) -> LeadJourney:
        """Return the complete canonical journey for a lead."""
        lead = self._get_lead(lead_id)
        events = self.journey_builder.build_events(
            lead=lead,
            activities=self._activities(lead.id),
            insights=self._insights(lead.id),
            messages=self._messages(lead.id),
            followups=self._followups(lead.id),
            predictions=self._predictions(lead.id),
        )
        progress = self.journey_builder.build_stage_progress(lead=lead, events=events)
        logger.info("Built lead journey lead_id=%s events=%s", lead.id, len(events))
        return LeadJourney(lead_id=lead.id, events=events, stage_progress=progress)

    def get_stage_progress(self, lead_id: int) -> StageProgress:
        """Return current lifecycle progress for a lead."""
        return self.get_lead_journey(lead_id).stage_progress

    def _get_lead(self, lead_id: int) -> Lead:
        """Return a lead or raise."""
        lead = self.lead_repository.get_by_id(lead_id)
        if lead is None:
            raise NotFoundError(f"Lead {lead_id} was not found.")
        return lead

    def _activities(self, lead_id: int) -> list[LeadActivity]:
        """Return all lead activities oldest first."""
        statement = select(LeadActivity).where(LeadActivity.lead_id == lead_id).order_by(LeadActivity.created_at.asc())
        return list(self.session.scalars(statement).all())

    def _insights(self, lead_id: int) -> list[AIInsight]:
        """Return all lead AI insights oldest first."""
        statement = select(AIInsight).where(AIInsight.lead_id == lead_id).order_by(AIInsight.created_at.asc())
        return list(self.session.scalars(statement).all())

    def _messages(self, lead_id: int) -> list[ConversationMessage]:
        """Return all lead conversation messages oldest first."""
        messages: list[ConversationMessage] = []
        for thread in self.thread_repository.list_by_lead(lead_id):
            messages.extend(self.message_repository.list_by_thread(thread.id, limit=500))
        return sorted(messages, key=lambda message: message.created_at)

    def _followups(self, lead_id: int) -> list[FollowupTask]:
        """Return all lead follow-up tasks oldest first."""
        statement = select(FollowupTask).where(FollowupTask.lead_id == lead_id).order_by(FollowupTask.created_at.asc())
        return list(self.session.scalars(statement).all())

    def _predictions(self, lead_id: int) -> list[ConversionPrediction]:
        """Return all lead conversion predictions oldest first."""
        statement = (
            select(ConversionPrediction)
            .where(ConversionPrediction.lead_id == lead_id)
            .order_by(ConversionPrediction.created_at.asc())
        )
        return list(self.session.scalars(statement).all())

    # TODO: Add event pagination once journeys become large.
