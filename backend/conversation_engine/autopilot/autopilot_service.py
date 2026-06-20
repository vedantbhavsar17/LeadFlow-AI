"""Autopilot service."""

from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from ai_engine.qualification.qualification_service import QUALIFICATION_INSIGHT_TYPE
from ai_engine.reply_analysis import REPLY_ANALYSIS_INSIGHT_TYPE
from conversation_engine.autopilot.autopilot_models import AUTOPILOT_INSIGHT_TYPE, AutopilotResult
from conversation_engine.autopilot.response_generator import AutopilotResponseGenerator
from conversation_engine.autopilot.safety_rules import AutopilotSafetyRules
from conversation_engine.autopilot.workflow_engine import AutopilotWorkflowEngine
from crm_core.repositories import (
    AIInsightRepository,
    BusinessContextRepository,
    ConversationMessageRepository,
    ConversationThreadRepository,
    LeadRepository,
)
from crm_core.services import ActivityService, NotFoundError
from database.models import BusinessContext, ConversationThread, Lead
from outreach.email import EmailService
from outreach.email.email_templates import reply_subject

logger = logging.getLogger(__name__)


class AutopilotService:
    """Generate, draft, and optionally send intelligent email replies."""

    def __init__(
        self,
        *,
        response_generator: AutopilotResponseGenerator | None = None,
        safety_rules: AutopilotSafetyRules | None = None,
        workflow_engine: AutopilotWorkflowEngine | None = None,
        email_service: EmailService | None = None,
        lead_repository: LeadRepository | None = None,
        business_context_repository: BusinessContextRepository | None = None,
        ai_insight_repository: AIInsightRepository | None = None,
        thread_repository: ConversationThreadRepository | None = None,
        message_repository: ConversationMessageRepository | None = None,
        activity_service: ActivityService | None = None,
        session: Session | None = None,
    ) -> None:
        """Create an autopilot service with injectable dependencies."""
        self.lead_repository = lead_repository or LeadRepository(session=session)
        self.session = self.lead_repository.session
        self.business_context_repository = business_context_repository or BusinessContextRepository(session=self.session)
        self.ai_insight_repository = ai_insight_repository or AIInsightRepository(session=self.session)
        self.thread_repository = thread_repository or ConversationThreadRepository(session=self.session)
        self.message_repository = message_repository or ConversationMessageRepository(session=self.session)
        self.activity_service = activity_service or ActivityService(session=self.session)
        self.email_service = email_service or EmailService(
            lead_repository=self.lead_repository,
            thread_repository=self.thread_repository,
            message_repository=self.message_repository,
        )
        self.response_generator = response_generator or AutopilotResponseGenerator()
        self.safety_rules = safety_rules or AutopilotSafetyRules()
        self.workflow_engine = workflow_engine or AutopilotWorkflowEngine()

    def process_thread(self, *, thread_id: int, mode: str = "suggested") -> AutopilotResult:
        """Generate and execute the requested autopilot workflow for a thread."""
        thread = self._get_thread(thread_id)
        lead = self._get_lead(thread.lead_id)
        context = self._get_business_context()
        qualification = self._latest_insight_output(lead.id, QUALIFICATION_INSIGHT_TYPE)
        reply_analysis = self._latest_insight_output(lead.id, REPLY_ANALYSIS_INSIGHT_TYPE)
        history = self.message_repository.list_by_thread(thread.id)

        draft = self.response_generator.generate(
            lead=lead,
            business_context=context,
            qualification=qualification,
            reply_analysis=reply_analysis,
            conversation_history=history,
            send_mode=mode,
        )
        safety = self.safety_rules.evaluate(reply_analysis=reply_analysis, confidence=draft.confidence)
        result = self.workflow_engine.resolve(requested_mode=mode, draft=draft, safety_decision=safety)

        self._store_autopilot_insight(lead=lead, thread=thread, result=result)
        self.activity_service.create_activity(
            lead_id=lead.id,
            activity_type="reply_generated",
            channel="email",
            note=f"Autopilot reply generated in {result.send_mode} mode.",
        )

        if result.send_mode == "manual":
            logger.info("Autopilot generated manual reply lead_id=%s thread_id=%s", lead.id, thread.id)
            return result

        if result.send_mode == "suggested":
            draft_message = self._store_draft(thread=thread, lead=lead, result=result)
            self.activity_service.create_activity(
                lead_id=lead.id,
                activity_type="human_review_required" if result.human_review_required else "reply_generated",
                channel="email",
                note="Autopilot draft stored for review.",
            )
            return self._with_draft_id(result, draft_message.id)

        sent_message = self.email_service.send_email(
            lead=lead,
            subject=reply_subject(history[-1].subject if history else None),
            body=result.generated_reply,
        )
        self.activity_service.create_activity(
            lead_id=lead.id,
            activity_type="reply_sent",
            channel="email",
            note="Autopilot reply sent automatically.",
        )
        return self._with_sent_id(result, sent_message.id)

    def _store_draft(self, *, thread: ConversationThread, lead: Lead, result: AutopilotResult):
        """Store a suggested reply draft in the conversation."""
        return self.message_repository.create(
            thread_id=thread.id,
            sender="system",
            message_text=result.generated_reply,
            message_type="draft_email",
            external_message_id=None,
            in_reply_to=None,
            from_email=None,
            to_email=lead.email,
            subject=reply_subject(None),
        )

    def _store_autopilot_insight(self, *, lead: Lead, thread: ConversationThread, result: AutopilotResult) -> None:
        """Store autopilot output as an AIInsight audit record."""
        output = result.to_dict()
        output["thread_id"] = thread.id
        self.ai_insight_repository.create(
            lead_id=lead.id,
            insight_type=AUTOPILOT_INSIGHT_TYPE,
            provider="workflow",
            model=None,
            output=output,
            confidence=result.confidence,
        )

    def _get_thread(self, thread_id: int) -> ConversationThread:
        """Return thread or raise."""
        thread = self.thread_repository.get_by_id(thread_id)
        if thread is None:
            raise NotFoundError(f"Conversation thread {thread_id} was not found.")
        return thread

    def _get_lead(self, lead_id: int) -> Lead:
        """Return lead or raise."""
        lead = self.lead_repository.get_by_id(lead_id)
        if lead is None:
            raise NotFoundError(f"Lead {lead_id} was not found.")
        return lead

    def _get_business_context(self) -> BusinessContext:
        """Return latest business context or raise."""
        context = self.business_context_repository.get_latest()
        if context is None:
            raise NotFoundError("Business context was not found.")
        return context

    def _latest_insight_output(self, lead_id: int, insight_type: str) -> dict:
        """Return latest insight output or raise."""
        insight = self.ai_insight_repository.get_latest_for_lead(lead_id=lead_id, insight_type=insight_type)
        if insight is None or not isinstance(insight.output, dict):
            raise NotFoundError(f"Latest {insight_type} insight for lead {lead_id} was not found.")
        return insight.output

    def _with_draft_id(self, result: AutopilotResult, draft_message_id: int) -> AutopilotResult:
        """Return result with draft id."""
        return AutopilotResult(**{**result.to_dict(), "draft_message_id": draft_message_id})

    def _with_sent_id(self, result: AutopilotResult, sent_message_id: int) -> AutopilotResult:
        """Return result with sent id."""
        return AutopilotResult(**{**result.to_dict(), "sent_message_id": sent_message_id})

    # TODO: Add approval workflow for suggested drafts when user accounts exist.
