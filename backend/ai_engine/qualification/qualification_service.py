"""Lead qualification service."""

from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from ai_engine.qualification.prompt_builder import QualificationPromptBuilder
from ai_engine.qualification.qualification_models import QualificationError, QualificationResult
from ai_engine.qualification.response_parser import QualificationResponseParser
from ai_engine.services import AIService
from crm_core.repositories import AIInsightRepository, BusinessContextRepository, LeadRepository
from crm_core.services import NotFoundError
from database.models import AIInsight, BusinessContext, Lead

logger = logging.getLogger(__name__)

QUALIFICATION_INSIGHT_TYPE = "qualification"


class QualificationService:
    """Analyze leads and store structured qualification insights."""

    def __init__(
        self,
        *,
        ai_service: AIService | None = None,
        lead_repository: LeadRepository | None = None,
        business_context_repository: BusinessContextRepository | None = None,
        ai_insight_repository: AIInsightRepository | None = None,
        prompt_builder: QualificationPromptBuilder | None = None,
        response_parser: QualificationResponseParser | None = None,
        session: Session | None = None,
    ) -> None:
        """Create a qualification service with injectable dependencies."""
        self.lead_repository = lead_repository or LeadRepository(session=session)
        self.session = self.lead_repository.session
        self.business_context_repository = business_context_repository or BusinessContextRepository(session=self.session)
        self.ai_insight_repository = ai_insight_repository or AIInsightRepository(session=self.session)
        self.ai_service = ai_service or AIService()
        self.prompt_builder = prompt_builder or QualificationPromptBuilder()
        self.response_parser = response_parser or QualificationResponseParser()

    def qualify_lead(self, lead_id: int, *, business_context_id: int | None = None) -> AIInsight:
        """Qualify a lead and store the result as an AIInsight."""
        return self._qualify_and_store(lead_id=lead_id, business_context_id=business_context_id)

    def requalify_lead(self, lead_id: int, *, business_context_id: int | None = None) -> AIInsight:
        """Run qualification again and store a new AIInsight snapshot."""
        return self._qualify_and_store(lead_id=lead_id, business_context_id=business_context_id)

    def get_latest_qualification(self, lead_id: int) -> AIInsight | None:
        """Return the latest stored qualification insight for a lead."""
        if self.lead_repository.get_by_id(lead_id) is None:
            raise NotFoundError(f"Lead {lead_id} was not found.")
        return self.ai_insight_repository.get_latest_for_lead(
            lead_id=lead_id,
            insight_type=QUALIFICATION_INSIGHT_TYPE,
        )

    def _qualify_and_store(self, *, lead_id: int, business_context_id: int | None) -> AIInsight:
        """Run AI qualification and persist the validated result."""
        lead = self._get_lead(lead_id)
        business_context = self._get_business_context(business_context_id)
        prompt = self.prompt_builder.build(lead=lead, business_context=business_context)
        response = self.ai_service.generate_text(
            prompt=prompt,
            system_prompt=self.prompt_builder.system_prompt,
            temperature=0.2,
            max_tokens=700,
        )
        if not response.success:
            raise QualificationError(response.error or "AI qualification request failed.")

        result = self.response_parser.parse(response.content)
        insight = self._store_result(lead=lead, result=result, provider=response.provider, model=response.model)
        logger.info("Qualified lead_id=%s insight_id=%s score=%s", lead.id, insight.id, result.score)
        return insight

    def _store_result(self, *, lead: Lead, result: QualificationResult, provider: str, model: str | None) -> AIInsight:
        """Persist a qualification result."""
        confidence = result.score / 100
        return self.ai_insight_repository.create(
            lead_id=lead.id,
            insight_type=QUALIFICATION_INSIGHT_TYPE,
            provider=provider,
            model=model,
            output=result.to_dict(),
            confidence=confidence,
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

    # TODO: Add qualification versioning and prompt hash metadata to AIInsight output.
