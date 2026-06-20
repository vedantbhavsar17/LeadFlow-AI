"""Reply analysis service."""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy.orm import Session

from ai_engine.qualification.qualification_service import QUALIFICATION_INSIGHT_TYPE
from ai_engine.reply_analysis.prompt_builder import ReplyAnalysisPromptBuilder
from ai_engine.reply_analysis.reply_models import (
    REPLY_ANALYSIS_INSIGHT_TYPE,
    ReplyAnalysisError,
    ReplyAnalysisResult,
)
from ai_engine.reply_analysis.response_parser import ReplyAnalysisResponseParser
from ai_engine.services import AIService
from crm_core.repositories import (
    AIInsightRepository,
    BusinessContextRepository,
    ConversationMessageRepository,
    ConversationThreadRepository,
    LeadRepository,
)
from crm_core.services import NotFoundError
from database.models import AIInsight, BusinessContext, ConversationMessage, ConversationThread, Lead

logger = logging.getLogger(__name__)


class ReplyAnalysisService:
    """Analyze customer replies and store structured AI insights."""

    def __init__(
        self,
        *,
        ai_service: AIService | None = None,
        lead_repository: LeadRepository | None = None,
        business_context_repository: BusinessContextRepository | None = None,
        ai_insight_repository: AIInsightRepository | None = None,
        thread_repository: ConversationThreadRepository | None = None,
        message_repository: ConversationMessageRepository | None = None,
        prompt_builder: ReplyAnalysisPromptBuilder | None = None,
        response_parser: ReplyAnalysisResponseParser | None = None,
        session: Session | None = None,
    ) -> None:
        """Create a reply analysis service with injectable dependencies."""
        self.lead_repository = lead_repository or LeadRepository(session=session)
        self.session = self.lead_repository.session
        self.business_context_repository = business_context_repository or BusinessContextRepository(session=self.session)
        self.ai_insight_repository = ai_insight_repository or AIInsightRepository(session=self.session)
        self.thread_repository = thread_repository or ConversationThreadRepository(session=self.session)
        self.message_repository = message_repository or ConversationMessageRepository(session=self.session)
        self.ai_service = ai_service or AIService()
        self.prompt_builder = prompt_builder or ReplyAnalysisPromptBuilder()
        self.response_parser = response_parser or ReplyAnalysisResponseParser()

    def analyze_reply(
        self,
        *,
        thread_id: int,
        latest_message_id: int | None = None,
        business_context_id: int | None = None,
    ) -> AIInsight:
        """Analyze the latest customer reply in a conversation thread."""
        thread = self._get_thread(thread_id)
        lead = self._get_lead(thread.lead_id)
        business_context = self._get_business_context(business_context_id)
        qualification = self._get_latest_qualification_payload(lead.id)
        history = self.message_repository.list_by_thread(thread.id)
        latest_reply = self._get_latest_reply(thread_id=thread.id, latest_message_id=latest_message_id)

        prompt = self.prompt_builder.build(
            business_context=business_context,
            lead=lead,
            qualification=qualification,
            conversation_history=history,
            latest_customer_reply=latest_reply,
        )
        response = self.ai_service.generate_text(
            prompt=prompt,
            system_prompt=self.prompt_builder.system_prompt,
            temperature=0.2,
            max_tokens=800,
        )
        if not response.success:
            raise ReplyAnalysisError(response.error or "AI reply analysis request failed.")

        result = self.response_parser.parse(response.content)
        insight = self._store_result(
            lead=lead,
            thread=thread,
            latest_reply=latest_reply,
            result=result,
            provider=response.provider,
            model=response.model,
        )
        logger.info("Analyzed reply lead_id=%s thread_id=%s insight_id=%s", lead.id, thread.id, insight.id)
        return insight

    def _store_result(
        self,
        *,
        lead: Lead,
        thread: ConversationThread,
        latest_reply: ConversationMessage,
        result: ReplyAnalysisResult,
        provider: str,
        model: str | None,
    ) -> AIInsight:
        """Persist reply analysis output."""
        output = result.to_dict()
        output["thread_id"] = thread.id
        output["latest_message_id"] = latest_reply.id
        return self.ai_insight_repository.create(
            lead_id=lead.id,
            insight_type=REPLY_ANALYSIS_INSIGHT_TYPE,
            provider=provider,
            model=model,
            output=output,
            confidence=result.confidence,
        )

    def _get_thread(self, thread_id: int) -> ConversationThread:
        """Return a conversation thread or raise."""
        thread = self.thread_repository.get_by_id(thread_id)
        if thread is None:
            raise NotFoundError(f"Conversation thread {thread_id} was not found.")
        return thread

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

    def _get_latest_reply(self, *, thread_id: int, latest_message_id: int | None) -> ConversationMessage:
        """Return the explicit or latest customer reply message."""
        if latest_message_id is not None:
            message = self.message_repository.get_by_id(latest_message_id)
            if message is None or message.thread_id != thread_id:
                raise NotFoundError(f"Conversation message {latest_message_id} was not found in thread {thread_id}.")
            if message.sender not in {"lead", "customer"}:
                raise ReplyAnalysisError("Latest reply must be from lead or customer.")
            return message

        message = self.message_repository.get_latest_customer_reply(thread_id)
        if message is None:
            raise NotFoundError(f"No customer reply found for conversation thread {thread_id}.")
        return message

    # TODO: Add conversation history summarization before very long threads are supported.
