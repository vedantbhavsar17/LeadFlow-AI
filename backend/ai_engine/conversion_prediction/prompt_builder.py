"""Prompt builder for conversion prediction."""

import json
from typing import Any

from database.models import BusinessContext, ConversationMessage, FollowupTask, Lead, LeadActivity


class ConversionPredictionPromptBuilder:
    """Build provider-neutral prompts for lead conversion prediction."""

    system_prompt = (
        "You are LeadFlow's conversion prediction engine. "
        "Estimate conversion probability from lead, conversation, follow-up, and AI insight signals. "
        "Return structured JSON only with no markdown or extra prose."
    )

    def build(
        self,
        *,
        business_context: BusinessContext,
        lead: Lead,
        qualification: dict[str, Any],
        reply_analysis: dict[str, Any] | None,
        conversation_history: list[ConversationMessage],
        followup_history: list[FollowupTask],
        activity_history: list[LeadActivity],
    ) -> str:
        """Build a conversion prediction prompt."""
        lead_name = " ".join(part for part in [lead.first_name, lead.last_name] if part).strip()
        conversations = [
            {
                "sender": message.sender,
                "message_type": message.message_type,
                "message_text": message.message_text,
                "created_at": message.created_at.isoformat() if message.created_at else None,
            }
            for message in conversation_history
        ]
        followups = [
            {
                "channel": followup.channel,
                "reason": followup.reason,
                "due_at": followup.due_at.isoformat() if followup.due_at else None,
                "status": followup.status,
                "completed_at": followup.completed_at.isoformat() if followup.completed_at else None,
            }
            for followup in followup_history
        ]
        activities = [
            {
                "activity_type": activity.activity_type,
                "channel": activity.channel,
                "note": activity.note,
                "created_at": activity.created_at.isoformat() if activity.created_at else None,
            }
            for activity in activity_history
        ]

        return f"""
Predict the probability that this lead will convert.

Business Context:
- Company Name: {business_context.company_name}
- Industry: {business_context.industry or ""}
- Services: {business_context.services or ""}
- Ideal Customer Profile: {business_context.ideal_customer_profile or ""}
- Target Market: {business_context.target_market or ""}
- Common Pain Points: {business_context.common_pain_points or ""}
- Sales Goals: {business_context.sales_goals or ""}

Lead:
- Name: {lead_name}
- Company: {lead.company or ""}
- Email: {lead.email or ""}
- Phone: {lead.phone or ""}
- Source: {lead.source}
- Stage: {lead.stage}
- Status: {lead.status}
- Priority: {lead.priority}
- Notes: {lead.notes or ""}
- Last Contacted At: {lead.last_contacted_at.isoformat() if lead.last_contacted_at else ""}
- Last Followup At: {lead.last_followup_at.isoformat() if lead.last_followup_at else ""}

Latest Qualification:
{json.dumps(qualification, indent=2)}

Latest Reply Analysis:
{json.dumps(reply_analysis or {}, indent=2)}

Conversation History:
{json.dumps(conversations, indent=2)}

Follow-up History:
{json.dumps(followups, indent=2)}

Activity History:
{json.dumps(activities, indent=2)}

Return JSON only with this exact shape:
{{
  "score": 87,
  "confidence": 0.91,
  "reasons": [
    "Responded to outreach",
    "Requested more information",
    "Multiple interactions"
  ],
  "risk_factors": [
    "Slow response time"
  ],
  "recommended_action": "schedule_demo"
}}

Scoring:
- 0-39 means low conversion probability.
- 40-69 means medium conversion probability.
- 70-100 means high conversion probability.

Validation rules:
- score must be an integer from 0 to 100.
- confidence must be a number from 0 to 1.
- reasons and risk_factors must be arrays of concise strings.
- recommended_action must be a short snake_case action.
""".strip()

    # TODO: Add feature weighting metadata once analytics has measured outcomes.
