"""Follow-up service."""

from __future__ import annotations

import logging
from datetime import datetime

from sqlalchemy.orm import Session

from ai_engine.qualification.qualification_service import QUALIFICATION_INSIGHT_TYPE
from ai_engine.reply_analysis import REPLY_ANALYSIS_INSIGHT_TYPE
from crm_core.repositories import (
    AIInsightRepository,
    ConversationMessageRepository,
    ConversationThreadRepository,
    FollowupRepository,
    LeadRepository,
)
from crm_core.services import ActivityService, NotFoundError, ValidationError
from database.models import FollowupTask, Lead
from followups.models import FOLLOWUP_STATUSES, FollowupRecommendation
from followups.rules import FollowupRuleEngine
from followups.scheduler import FollowupScheduler

logger = logging.getLogger(__name__)


class FollowupService:
    """Business service for follow-up recommendations and tasks."""

    def __init__(
        self,
        *,
        followup_repository: FollowupRepository | None = None,
        lead_repository: LeadRepository | None = None,
        ai_insight_repository: AIInsightRepository | None = None,
        thread_repository: ConversationThreadRepository | None = None,
        message_repository: ConversationMessageRepository | None = None,
        activity_service: ActivityService | None = None,
        rule_engine: FollowupRuleEngine | None = None,
        scheduler: FollowupScheduler | None = None,
        session: Session | None = None,
    ) -> None:
        """Create a follow-up service with injectable dependencies."""
        self.followup_repository = followup_repository or FollowupRepository(session=session)
        self.session = self.followup_repository.session
        self.lead_repository = lead_repository or LeadRepository(session=self.session)
        self.ai_insight_repository = ai_insight_repository or AIInsightRepository(session=self.session)
        self.thread_repository = thread_repository or ConversationThreadRepository(session=self.session)
        self.message_repository = message_repository or ConversationMessageRepository(session=self.session)
        self.activity_service = activity_service or ActivityService(session=self.session)
        self.rule_engine = rule_engine or FollowupRuleEngine()
        self.scheduler = scheduler or FollowupScheduler(followup_repository=self.followup_repository)

    def create_followup(
        self,
        *,
        lead_id: int,
        channel: str,
        reason: str,
        due_at: datetime,
        status: str = "pending",
    ) -> FollowupTask:
        """Create a follow-up task and record a lead activity."""
        self._get_lead(lead_id)
        normalized_status = self._validate_status(status)
        if not str(channel or "").strip():
            raise ValidationError("channel is required.")
        if not str(reason or "").strip():
            raise ValidationError("reason is required.")

        followup = self.followup_repository.create(
            lead_id=lead_id,
            channel=str(channel).strip().lower(),
            reason=str(reason).strip(),
            due_at=due_at,
            status=normalized_status,
            completed_at=None,
        )
        self.activity_service.create_activity(
            lead_id=lead_id,
            activity_type="followup_created",
            channel=followup.channel,
            note=followup.reason,
        )
        logger.info("Created follow-up id=%s lead_id=%s due_at=%s", followup.id, lead_id, due_at.isoformat())
        return followup

    def get_due_followups(self, *, due_before: datetime | None = None) -> list[FollowupTask]:
        """Return pending follow-ups due by a timestamp."""
        return self.scheduler.get_due_followups(due_before=due_before)

    def complete_followup(self, followup_id: int, *, completed_at: datetime | None = None) -> FollowupTask:
        """Mark a follow-up task complete."""
        timestamp = completed_at or datetime.utcnow()
        followup = self.followup_repository.update(
            followup_id,
            status="completed",
            completed_at=timestamp,
        )
        if followup is None:
            raise NotFoundError(f"Follow-up {followup_id} was not found.")
        self.activity_service.create_activity(
            lead_id=followup.lead_id,
            activity_type="status_changed",
            channel=followup.channel,
            note=f"Follow-up {followup.id} completed.",
        )
        logger.info("Completed follow-up id=%s", followup.id)
        return followup

    def generate_followup_recommendation(self, lead_id: int, *, now: datetime | None = None) -> FollowupRecommendation:
        """Generate a follow-up recommendation from stored lead intelligence."""
        lead = self._get_lead(lead_id)
        qualification = self._latest_insight_output(lead_id, QUALIFICATION_INSIGHT_TYPE)
        reply_analysis = self._latest_insight_output(lead_id, REPLY_ANALYSIS_INSIGHT_TYPE)
        conversation_history = []
        for thread in self.thread_repository.list_by_lead(lead_id):
            conversation_history.extend(self.message_repository.list_by_thread(thread.id))

        recommendation = self.rule_engine.evaluate(
            lead=lead,
            qualification=qualification,
            reply_analysis=reply_analysis,
            conversation_history=conversation_history,
            now=now,
        )
        logger.info(
            "Generated follow-up recommendation lead_id=%s required=%s priority=%s",
            lead_id,
            recommendation.followup_required,
            recommendation.priority,
        )
        return recommendation

    def _latest_insight_output(self, lead_id: int, insight_type: str) -> dict | None:
        """Return latest AI insight output if present."""
        insight = self.ai_insight_repository.get_latest_for_lead(lead_id=lead_id, insight_type=insight_type)
        return insight.output if insight and isinstance(insight.output, dict) else None

    def _get_lead(self, lead_id: int) -> Lead:
        """Return a lead or raise."""
        lead = self.lead_repository.get_by_id(lead_id)
        if lead is None:
            raise NotFoundError(f"Lead {lead_id} was not found.")
        return lead

    @staticmethod
    def _validate_status(status: str) -> str:
        """Validate follow-up status."""
        normalized = str(status or "").strip().lower()
        if normalized not in FOLLOWUP_STATUSES:
            raise ValidationError(f"status must be one of: {', '.join(sorted(FOLLOWUP_STATUSES))}.")
        return normalized

    # TODO: Persist recommendation priority/message if FollowupTask schema is expanded.
