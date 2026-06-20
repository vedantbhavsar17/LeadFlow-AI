"""Validate the complete LeadFlow backend workflow with fake AI and email adapters."""

from __future__ import annotations

import json
from datetime import datetime, timedelta

from _validation import app_context, cleanup_records, print_result, run_validation


class StaticAIService:
    """Fake AI service returning a configured JSON payload."""

    def __init__(self, payload: dict):
        self.payload = payload

    def generate_text(self, *, prompt, system_prompt=None, temperature=0.2, max_tokens=512):
        from ai_engine.models import AIResponse

        return AIResponse(
            content=json.dumps(self.payload),
            provider="validation",
            model="validation-model",
            tokens_used=10,
            success=True,
        )


class FakeSMTPClient:
    """Fake SMTP adapter used to validate workflow without sending live mail."""

    from_address = "team@leadflow.test"

    def send_email(self, *, to_email, subject, body):
        from outreach.email import EmailSendResult

        return EmailSendResult(success=True, message_id="<leadflow-validation-e2e-outbound@test>")


def _check() -> list[str]:
    from ai_engine.conversion_prediction import ConversionPredictionService
    from ai_engine.outreach_generation import OutreachGenerationService
    from ai_engine.qualification import QualificationService
    from ai_engine.reply_analysis import ReplyAnalysisService
    from analytics.journey import LeadJourneyService
    from conversation_engine.email_listener import EmailParser, EmailThreadMatcher
    from crm_core.repositories import ConversationMessageRepository, ConversationThreadRepository
    from crm_core.services import BusinessContextService, LeadService
    from followups import FollowupService
    from outreach.email import EmailService

    lead = None
    context = None
    with app_context():
        try:
            lead = LeadService().create_lead(
                first_name="Validation",
                last_name="E2E",
                email="validation.e2e@leadflow.test",
                company="LeadFlow",
                source="validation",
                notes="Needs complete workflow validation.",
            )
            context = BusinessContextService().create_context(
                company_name="LeadFlow Validation",
                industry="B2B Services",
                services="Lead qualification and conversion workflows",
                ideal_customer_profile="Teams with inbound leads",
                common_pain_points="manual followups",
                sales_goals="Book qualified demos",
            )
            qualification = QualificationService(
                ai_service=StaticAIService(
                    {
                        "score": 88,
                        "category": "hot",
                        "buying_intent": "high",
                        "pain_points": ["manual followups"],
                        "recommended_action": "schedule_demo",
                        "reasoning": "Validation lead is a strong fit.",
                    }
                )
            ).qualify_lead(lead.id)
            outreach = OutreachGenerationService(
                ai_service=StaticAIService(
                    {
                        "subject": "LeadFlow validation outreach",
                        "body": "Hi Validation, this is an automated LeadFlow workflow check.",
                    }
                )
            ).generate_email(lead.id)
            outbound = EmailService(smtp_client=FakeSMTPClient()).send_email(
                lead=lead,
                subject=outreach.output["subject"],
                body=outreach.output["body"],
            )
            raw_reply = (
                "From: validation.e2e@leadflow.test\r\n"
                "To: team@leadflow.test\r\n"
                "Subject: Re: LeadFlow validation outreach\r\n"
                "Message-ID: <leadflow-validation-e2e-inbound@test>\r\n"
                f"In-Reply-To: {outbound.external_message_id}\r\n"
                "\r\n"
                "This looks useful. Can we see a demo?"
            ).encode()
            incoming = EmailParser().parse(raw_reply)
            thread = EmailThreadMatcher().match(incoming)
            if thread is None:
                raise AssertionError("Conversation Creation failed because no thread matched the reply.")
            reply = ConversationMessageRepository().create(
                thread_id=thread.id,
                sender="customer",
                message_text=incoming.body,
                message_type="email",
                external_message_id=incoming.message_id,
                in_reply_to=incoming.in_reply_to,
                from_email=incoming.from_email,
                to_email=incoming.to_email,
                subject=incoming.subject,
            )
            reply_analysis = ReplyAnalysisService(
                ai_service=StaticAIService(
                    {
                        "intent": "meeting_request",
                        "sentiment": "positive",
                        "objection": None,
                        "recommended_action": "schedule_demo",
                        "suggested_reply": "Happy to show you. Would Tuesday work?",
                        "confidence": 0.92,
                    }
                )
            ).analyze_reply(thread_id=thread.id, latest_message_id=reply.id)
            followup = FollowupService().create_followup(
                lead_id=lead.id,
                channel="email",
                reason="Schedule requested demo",
                due_at=datetime.utcnow() + timedelta(days=1),
            )
            prediction = ConversionPredictionService(
                ai_service=StaticAIService(
                    {
                        "score": 91,
                        "confidence": 0.9,
                        "reasons": ["Requested a demo", "Responded to outreach"],
                        "risk_factors": [],
                        "recommended_action": "schedule_demo",
                    }
                )
            ).predict_conversion(lead.id)
            journey = LeadJourneyService().get_lead_journey(lead.id)
            if qualification.output["category"] != "hot":
                raise AssertionError("Qualification step did not produce a hot lead.")
            if not outbound.external_message_id:
                raise AssertionError("Outreach Generation / send step did not create an outbound message id.")
            if reply_analysis.output["intent"] != "meeting_request":
                raise AssertionError("Reply Analysis step did not produce meeting_request intent.")
            if followup.id is None:
                raise AssertionError("Followup Generation step did not create a follow-up.")
            if prediction.score != 91:
                raise AssertionError("Conversion Prediction step did not produce expected score.")
            if not journey.events:
                raise AssertionError("Journey Generation step did not produce events.")
            if ConversationThreadRepository().get_by_id(thread.id) is None:
                raise AssertionError("Conversation Creation step did not persist a thread.")
            return [
                f"Lead Creation passed with lead id {lead.id}.",
                "Qualification passed.",
                "Outreach Generation passed.",
                f"Conversation Creation passed with thread id {thread.id}.",
                "Reply Analysis passed.",
                f"Followup Generation passed with follow-up id {followup.id}.",
                "Conversion Prediction passed.",
                f"Journey Generation passed with {len(journey.events)} event(s).",
            ]
        finally:
            cleanup_records(lead, context)


def run_check():
    return run_validation("E2E", _check)


if __name__ == "__main__":
    print_result(run_check())

