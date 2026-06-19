"""Conversion prediction service."""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_engine.conversion_prediction.prediction_models import (
    CONVERSION_PREDICTION_INSIGHT_TYPE,
    ConversionPredictionError,
    ConversionPredictionResult,
)
from ai_engine.conversion_prediction.prompt_builder import ConversionPredictionPromptBuilder
from ai_engine.conversion_prediction.response_parser import ConversionPredictionResponseParser
from ai_engine.qualification.qualification_service import QUALIFICATION_INSIGHT_TYPE
from ai_engine.reply_analysis.reply_models import REPLY_ANALYSIS_INSIGHT_TYPE
from ai_engine.services import AIService
from crm_core.repositories import (
    AIInsightRepository,
    ActivityRepository,
    BusinessContextRepository,
    ConversationMessageRepository,
    ConversationThreadRepository,
    ConversionPredictionRepository,
    FollowupRepository,
    LeadRepository,
)
from crm_core.services import NotFoundError
from database.models import (
    AIInsight,
    BusinessContext,
    ConversationMessage,
    ConversionPrediction,
    FollowupTask,
    Lead,
    LeadActivity,
)

logger = logging.getLogger(__name__)


class ConversionPredictionService:
    """Predict and store lead conversion probability snapshots."""

    def __init__(
        self,
        *,
        ai_service: AIService | None = None,
        lead_repository: LeadRepository | None = None,
        business_context_repository: BusinessContextRepository | None = None,
        ai_insight_repository: AIInsightRepository | None = None,
        prediction_repository: ConversionPredictionRepository | None = None,
        thread_repository: ConversationThreadRepository | None = None,
        message_repository: ConversationMessageRepository | None = None,
        followup_repository: FollowupRepository | None = None,
        activity_repository: ActivityRepository | None = None,
        prompt_builder: ConversionPredictionPromptBuilder | None = None,
        response_parser: ConversionPredictionResponseParser | None = None,
        session: Session | None = None,
    ) -> None:
        """Create a conversion prediction service with injectable dependencies."""
        self.lead_repository = lead_repository or LeadRepository(session=session)
        self.session = self.lead_repository.session
        self.business_context_repository = business_context_repository or BusinessContextRepository(session=self.session)
        self.ai_insight_repository = ai_insight_repository or AIInsightRepository(session=self.session)
        self.prediction_repository = prediction_repository or ConversionPredictionRepository(session=self.session)
        self.thread_repository = thread_repository or ConversationThreadRepository(session=self.session)
        self.message_repository = message_repository or ConversationMessageRepository(session=self.session)
        self.followup_repository = followup_repository or FollowupRepository(session=self.session)
        self.activity_repository = activity_repository or ActivityRepository(session=self.session)
        self.ai_service = ai_service or AIService()
        self.prompt_builder = prompt_builder or ConversionPredictionPromptBuilder()
        self.response_parser = response_parser or ConversionPredictionResponseParser()

    def predict_conversion(self, lead_id: int, *, business_context_id: int | None = None) -> ConversionPrediction:
        """Predict conversion probability and store a new snapshot."""
        return self._predict_and_store(lead_id=lead_id, business_context_id=business_context_id)

    def refresh_prediction(self, lead_id: int, *, business_context_id: int | None = None) -> ConversionPrediction:
        """Re-run conversion prediction and store a new snapshot."""
        return self._predict_and_store(lead_id=lead_id, business_context_id=business_context_id)

    def get_latest_prediction(self, lead_id: int) -> ConversionPrediction | None:
        """Return the latest stored prediction for a lead."""
        if self.lead_repository.get_by_id(lead_id) is None:
            raise NotFoundError(f"Lead {lead_id} was not found.")
        return self.prediction_repository.get_latest_for_lead(lead_id)

    def _predict_and_store(self, *, lead_id: int, business_context_id: int | None) -> ConversionPrediction:
        """Build prediction inputs, invoke AI, and persist outputs."""
        lead = self._get_lead(lead_id)
        business_context = self._get_business_context(business_context_id)
        qualification = self._get_required_insight_payload(
            lead_id=lead.id,
            insight_type=QUALIFICATION_INSIGHT_TYPE,
            label="Latest qualification",
        )
        reply_analysis = self._get_optional_insight_payload(
            lead_id=lead.id,
            insight_type=REPLY_ANALYSIS_INSIGHT_TYPE,
        )
        conversation_history = self._get_conversation_history(lead.id)
        followup_history = self._get_followup_history(lead.id)
        activity_history = self._get_activity_history(lead.id)

        prompt = self.prompt_builder.build(
            business_context=business_context,
            lead=lead,
            qualification=qualification,
            reply_analysis=reply_analysis,
            conversation_history=conversation_history,
            followup_history=followup_history,
            activity_history=activity_history,
        )
        response = self.ai_service.generate_text(
            prompt=prompt,
            system_prompt=self.prompt_builder.system_prompt,
            temperature=0.2,
            max_tokens=800,
        )
        if not response.success:
            raise ConversionPredictionError(response.error or "AI conversion prediction request failed.")

        result = self.response_parser.parse(response.content)
        prediction = self._store_result(
            lead=lead,
            result=result,
            provider=response.provider,
            model=response.model,
        )
        logger.info(
            "Predicted conversion lead_id=%s prediction_id=%s score=%s",
            lead.id,
            prediction.id,
            result.score,
        )
        return prediction

    def _store_result(
        self,
        *,
        lead: Lead,
        result: ConversionPredictionResult,
        provider: str,
        model: str | None,
    ) -> ConversionPrediction:
        """Persist prediction output in AIInsight and ConversionPrediction."""
        output = result.to_dict()
        insight = self.ai_insight_repository.create(
            lead_id=lead.id,
            insight_type=CONVERSION_PREDICTION_INSIGHT_TYPE,
            provider=provider,
            model=model,
            output=output,
            confidence=result.confidence,
        )
        return self.prediction_repository.create(
            lead_id=lead.id,
            score=result.score,
            probability_label=result.probability_label,
            confidence=result.confidence,
            reasons=result.reasons,
            risk_factors=result.risk_factors,
            recommended_action=result.recommended_action,
            provider=provider,
            model=model,
            ai_insight_id=insight.id,
        )

    def _get_lead(self, lead_id: int) -> Lead:
        """Return a lead or raise."""
        lead = self.lead_repository.get_by_id(lead_id)
        if lead is None:
            raise NotFoundError(f"Lead {lead_id} was not found.")
        return lead

    def _get_business_context(self, business_context_id: int | None) -> BusinessContext:
        """Return the requested or latest business context."""
        if business_context_id is not None:
            context = self.business_context_repository.get_by_id(business_context_id)
        else:
            context = self.business_context_repository.get_latest()
        if context is None:
            raise NotFoundError("Business context was not found.")
        return context

    def _get_required_insight_payload(self, *, lead_id: int, insight_type: str, label: str) -> dict[str, Any]:
        """Return a required AI insight output payload."""
        payload = self._get_optional_insight_payload(lead_id=lead_id, insight_type=insight_type)
        if payload is None:
            raise NotFoundError(f"{label} for lead {lead_id} was not found.")
        return payload

    def _get_optional_insight_payload(self, *, lead_id: int, insight_type: str) -> dict[str, Any] | None:
        """Return an optional AI insight output payload."""
        insight = self.ai_insight_repository.get_latest_for_lead(lead_id=lead_id, insight_type=insight_type)
        if insight is None or not isinstance(insight.output, dict):
            return None
        return insight.output

    def _get_conversation_history(self, lead_id: int) -> list[ConversationMessage]:
        """Return recent conversation messages across all lead threads."""
        messages: list[ConversationMessage] = []
        for thread in self.thread_repository.list_by_lead(lead_id):
            messages.extend(self.message_repository.list_by_thread(thread.id, limit=50))
        return sorted(messages, key=lambda message: message.created_at)

    def _get_followup_history(self, lead_id: int) -> list[FollowupTask]:
        """Return recent follow-up tasks for a lead."""
        statement = (
            select(FollowupTask)
            .where(FollowupTask.lead_id == lead_id)
            .order_by(FollowupTask.created_at.desc())
            .limit(50)
        )
        return list(self.session.scalars(statement).all())

    def _get_activity_history(self, lead_id: int) -> list[LeadActivity]:
        """Return recent lead activity records."""
        statement = (
            select(LeadActivity)
            .where(LeadActivity.lead_id == lead_id)
            .order_by(LeadActivity.created_at.desc())
            .limit(75)
        )
        return list(self.session.scalars(statement).all())

    # TODO: Add non-AI fallback scoring once analytics calibration is available.
