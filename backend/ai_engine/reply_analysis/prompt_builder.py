"""Prompt builder for reply analysis."""

import json
from typing import Any

from database.models import BusinessContext, ConversationMessage, Lead


class ReplyAnalysisPromptBuilder:
    """Build provider-neutral prompts for customer reply analysis."""

    system_prompt = (
        "You are LeadFlow's reply analysis engine. "
        "Analyze customer replies for sales intent and next action. "
        "Return structured JSON only with no markdown or extra prose."
    )

    def build(
        self,
        *,
        business_context: BusinessContext,
        lead: Lead,
        qualification: dict[str, Any],
        conversation_history: list[ConversationMessage],
        latest_customer_reply: ConversationMessage,
    ) -> str:
        """Build a reply analysis prompt."""
        lead_name = " ".join(part for part in [lead.first_name, lead.last_name] if part).strip()
        history = [
            {
                "sender": message.sender,
                "message_type": message.message_type,
                "message_text": message.message_text,
                "created_at": message.created_at.isoformat() if message.created_at else None,
            }
            for message in conversation_history
        ]
        return f"""
Analyze the latest customer reply in this conversation.

Business Context:
- Company Name: {business_context.company_name}
- Industry: {business_context.industry or ""}
- Services: {business_context.services or ""}
- Ideal Customer Profile: {business_context.ideal_customer_profile or ""}
- Common Pain Points: {business_context.common_pain_points or ""}
- Sales Goals: {business_context.sales_goals or ""}

Lead:
- Name: {lead_name}
- Company: {lead.company or ""}
- Notes: {lead.notes or ""}
- Source: {lead.source}

Latest Qualification:
{json.dumps(qualification, indent=2)}

Conversation History:
{json.dumps(history, indent=2)}

Latest Customer Reply:
{latest_customer_reply.message_text}

Return JSON only with this exact shape:
{{
  "intent": "interested",
  "sentiment": "positive",
  "objection": null,
  "recommended_action": "schedule_demo",
  "suggested_reply": "Concise helpful reply.",
  "confidence": 0.91
}}

Validation rules:
- intent must be one of: interested, needs_information, pricing_objection, competitor_objection, follow_up_later, meeting_request, not_interested, unsubscribe.
- sentiment must be one of: positive, neutral, negative.
- objection may be null or a concise string.
- recommended_action must be a short snake_case action.
- suggested_reply must be helpful and must not claim that a message was sent.
- confidence must be a number from 0 to 1.
""".strip()

    # TODO: Add prompt versions and conversation truncation strategy.
