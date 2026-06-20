"""AI outreach generation service."""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy.orm import Session

from ai_engine.outreach_generation.outreach_models import (
    OUTREACH_INSIGHT_TYPE,
    SUPPORTED_OUTREACH_CHANNELS,
    OutreachGenerationError,
    OutreachResult,
)
from ai_engine.outreach_generation.prompt_builder import OutreachPromptBuilder
from ai_engine.outreach_generation.response_parser import OutreachResponseParser
from ai_engine.qualification.qualification_service import QUALIFICATION_INSIGHT_TYPE
from ai_engine.services import AIService
from crm_core.repositories import AIInsightRepository, BusinessContextRepository, LeadRepository
from crm_core.services import NotFoundError, ValidationError
from database.models import AIInsight, BusinessContext, Lead

logger = logging.getLogger(__name__)


class OutreachGenerationService:
    """Generate personalized outreach and store it as AIInsight output."""

    message_length_limits = {
        "email": {"subject": 120, "body": 5000},
        "whatsapp": {"message": 1024},
        "linkedin": {"connection_message": 300, "followup_message": 1900},
    }

    def __init__(
        self,
        *,
        ai_service: AIService | None = None,
        lead_repository: LeadRepository | None = None,
        business_context_repository: BusinessContextRepository | None = None,
        ai_insight_repository: AIInsightRepository | None = None,
        prompt_builder: OutreachPromptBuilder | None = None,
        response_parser: OutreachResponseParser | None = None,
        session: Session | None = None,
    ) -> None:
        """Create an outreach generation service with injectable dependencies."""
        self.lead_repository = lead_repository or LeadRepository(session=session)
        self.session = self.lead_repository.session
        self.business_context_repository = business_context_repository or BusinessContextRepository(session=self.session)
        self.ai_insight_repository = ai_insight_repository or AIInsightRepository(session=self.session)
        self.ai_service = ai_service or AIService()
        self.prompt_builder = prompt_builder or OutreachPromptBuilder()
        self.response_parser = response_parser or OutreachResponseParser()

    def generate_email(self, lead_id: int, *, business_context_id: int | None = None) -> AIInsight:
        """Generate personalized email outreach."""
        return self._generate_channel("email", lead_id=lead_id, business_context_id=business_context_id)

    def generate_whatsapp(self, lead_id: int, *, business_context_id: int | None = None) -> AIInsight:
        """Generate personalized WhatsApp outreach copy."""
        return self._generate_channel("whatsapp", lead_id=lead_id, business_context_id=business_context_id)

    def generate_linkedin(self, lead_id: int, *, business_context_id: int | None = None) -> AIInsight:
        """Generate personalized LinkedIn connection and follow-up messages."""
        return self._generate_channel("linkedin", lead_id=lead_id, business_context_id=business_context_id)

    def generate_all_channels(self, lead_id: int, *, business_context_id: int | None = None) -> dict[str, AIInsight]:
        """Generate outreach for all supported channels."""
        return {
            "email": self.generate_email(lead_id, business_context_id=business_context_id),
            "whatsapp": self.generate_whatsapp(lead_id, business_context_id=business_context_id),
            "linkedin": self.generate_linkedin(lead_id, business_context_id=business_context_id),
        }

    def _generate_channel(self, channel: str, *, lead_id: int, business_context_id: int | None) -> AIInsight:
        """Generate and store outreach for one channel."""
        normalized_channel = self._validate_channel(channel)
        lead = self._get_lead(lead_id)
        business_context = self._get_business_context(business_context_id)
        qualification = self._get_latest_qualification_payload(lead_id)

        prompt = self.prompt_builder.build(
            channel=normalized_channel,
            lead=lead,
            business_context=business_context,
            qualification=qualification,
        )
        response = self.ai_service.generate_text(
            prompt=prompt,
            system_prompt=self.prompt_builder.system_prompt,
            temperature=0.4,
            max_tokens=900,
        )
        if not response.success:
            raise OutreachGenerationError(response.error or "AI outreach generation request failed.")

        result = self.response_parser.parse(channel=normalized_channel, content=response.content)
        self._validate_message_lengths(result)
        insight = self._store_result(lead=lead, result=result, provider=response.provider, model=response.model)
        logger.info("Generated outreach lead_id=%s channel=%s insight_id=%s", lead.id, normalized_channel, insight.id)
        return insight

    def _store_result(self, *, lead: Lead, result: OutreachResult, provider: str, model: str | None) -> AIInsight:
        """Persist outreach generation output."""
        return self.ai_insight_repository.create(
            lead_id=lead.id,
            insight_type=OUTREACH_INSIGHT_TYPE,
            provider=provider,
            model=model,
            output=result.to_dict(),
            confidence=None,
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

    def _get_latest_qualification_payload(self, lead_id: int) -> dict[str, Any]:
        """Return latest qualification output for the lead."""
        insight = self.ai_insight_repository.get_latest_for_lead(
            lead_id=lead_id,
            insight_type=QUALIFICATION_INSIGHT_TYPE,
        )
        if insight is None or not isinstance(insight.output, dict):
            raise NotFoundError(f"Latest qualification for lead {lead_id} was not found.")
        return insight.output

    @staticmethod
    def _validate_channel(channel: str) -> str:
        """Validate an outreach channel."""
        normalized = str(channel or "").strip().lower()
        if normalized not in SUPPORTED_OUTREACH_CHANNELS:
            raise ValidationError(f"Unsupported outreach channel: {channel}")
        return normalized

    @classmethod
    def _validate_message_lengths(cls, result: OutreachResult) -> None:
        """Reject generated outreach that exceeds channel UI limits."""
        limits = cls.message_length_limits.get(result.channel, {})
        too_long = []
        for field, max_length in limits.items():
            message_length = len(result.content.get(field, ""))
            if message_length > max_length:
                too_long.append(f"{field} ({message_length}/{max_length})")
        if too_long:
            raise OutreachGenerationError(
                f"Generated {result.channel} outreach exceeded length limits: {', '.join(too_long)}."
            )
