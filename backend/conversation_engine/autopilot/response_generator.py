"""Autopilot response generation."""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from ai_engine.services import AIService
from conversation_engine.autopilot.autopilot_models import AutopilotDraft, AutopilotParseError
from database.models import BusinessContext, ConversationMessage, Lead

logger = logging.getLogger(__name__)


class AutopilotResponseGenerator:
    """Generate intelligent email replies from conversation context."""

    system_prompt = (
        "You are LeadFlow's email autopilot response generator. "
        "Generate helpful draft email replies. "
        "Do not claim an email was sent. "
        "Return structured JSON only with no markdown or extra prose."
    )

    def __init__(self, ai_service: AIService | None = None) -> None:
        """Create a response generator."""
        self.ai_service = ai_service or AIService()

    def generate(
        self,
        *,
        lead: Lead,
        business_context: BusinessContext,
        qualification: dict[str, Any],
        reply_analysis: dict[str, Any],
        conversation_history: list[ConversationMessage],
        send_mode: str,
    ) -> AutopilotDraft:
        """Generate and parse an autopilot reply."""
        prompt = self._build_prompt(
            lead=lead,
            business_context=business_context,
            qualification=qualification,
            reply_analysis=reply_analysis,
            conversation_history=conversation_history,
            send_mode=send_mode,
        )
        response = self.ai_service.generate_text(
            prompt=prompt,
            system_prompt=self.system_prompt,
            temperature=0.3,
            max_tokens=700,
        )
        if not response.success:
            raise AutopilotParseError(response.error or "AI autopilot response generation failed.")
        draft = self._parse(response.content)
        logger.info("Generated autopilot draft mode=%s confidence=%s", draft.send_mode, draft.confidence)
        return draft

    def _build_prompt(
        self,
        *,
        lead: Lead,
        business_context: BusinessContext,
        qualification: dict[str, Any],
        reply_analysis: dict[str, Any],
        conversation_history: list[ConversationMessage],
        send_mode: str,
    ) -> str:
        """Build a generic email response prompt."""
        lead_name = " ".join(part for part in [lead.first_name, lead.last_name] if part).strip()
        history = [
            {
                "sender": message.sender,
                "message_type": message.message_type,
                "message_text": message.message_text,
                "subject": message.subject,
            }
            for message in conversation_history
        ]
        return f"""
Generate an intelligent email response for this conversation.

Autopilot Mode Requested: {send_mode}

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

Qualification:
{json.dumps(qualification, indent=2)}

Reply Analysis:
{json.dumps(reply_analysis, indent=2)}

Conversation History:
{json.dumps(history, indent=2)}

Return JSON only with this exact shape:
{{
  "recommended_action": "schedule_demo",
  "generated_reply": "Helpful email reply body.",
  "send_mode": "{send_mode}",
  "confidence": 0.91
}}
""".strip()

    def _parse(self, content: str | None) -> AutopilotDraft:
        """Parse generated JSON into an AutopilotDraft."""
        if not content:
            raise AutopilotParseError("Autopilot response was empty.")
        cleaned = content.strip()
        fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, flags=re.DOTALL | re.IGNORECASE)
        if fenced:
            cleaned = fenced.group(1).strip()
        try:
            payload = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise AutopilotParseError(f"Invalid autopilot JSON response: {exc}") from exc
        if not isinstance(payload, dict):
            raise AutopilotParseError("Autopilot response must be a JSON object.")

        recommended_action = str(payload.get("recommended_action") or "").strip()
        generated_reply = str(payload.get("generated_reply") or "").strip()
        send_mode = str(payload.get("send_mode") or "").strip().lower()
        confidence = payload.get("confidence")
        if not recommended_action:
            raise AutopilotParseError("recommended_action is required.")
        if not generated_reply:
            raise AutopilotParseError("generated_reply is required.")
        if send_mode not in {"manual", "suggested", "automatic"}:
            raise AutopilotParseError("send_mode is invalid.")
        if not isinstance(confidence, int | float) or confidence < 0 or confidence > 1:
            raise AutopilotParseError("confidence must be a number from 0 to 1.")

        return AutopilotDraft(
            recommended_action=recommended_action,
            generated_reply=generated_reply,
            send_mode=send_mode,
            confidence=float(confidence),
        )

    # TODO: Add channel-specific response generators if WhatsApp/LinkedIn APIs are introduced.
