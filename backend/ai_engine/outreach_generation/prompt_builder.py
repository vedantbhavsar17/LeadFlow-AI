"""Prompt builder for AI outreach generation."""

import json
from typing import Any

from database.models import BusinessContext, Lead


class OutreachPromptBuilder:
    """Build provider-neutral prompts for personalized outreach."""

    system_prompt = (
        "You are LeadFlow's outreach generation engine. "
        "Write helpful, specific, human outreach. "
        "Never produce generic sales spam. "
        "Return structured JSON only with no markdown or extra prose."
    )

    def build(
        self,
        *,
        channel: str,
        lead: Lead,
        business_context: BusinessContext,
        qualification: dict[str, Any],
    ) -> str:
        """Build an outreach prompt for a supported channel."""
        lead_name = " ".join(part for part in [lead.first_name, lead.last_name] if part).strip()
        output_shape = self._output_shape(channel)
        return f"""
Generate personalized {channel} outreach for this lead.

Rules:
- Be specific to the lead and business context.
- Use the qualification result and pain points.
- Keep the tone aligned with the brand.
- Never produce generic sales spam.
- Do not invent facts not provided below.
- Return JSON only.

Business Context:
- Company Name: {business_context.company_name}
- Industry: {business_context.industry or ""}
- Services: {business_context.services or ""}
- Ideal Customer Profile: {business_context.ideal_customer_profile or ""}
- Target Market: {business_context.target_market or ""}
- Common Pain Points: {business_context.common_pain_points or ""}
- Brand Tone: {business_context.brand_tone or ""}
- Sales Goals: {business_context.sales_goals or ""}

Lead:
- Name: {lead_name}
- Company: {lead.company or ""}
- Notes: {lead.notes or ""}
- Source: {lead.source}

Latest Qualification:
{json.dumps(qualification, indent=2)}

Return JSON only with this exact shape:
{output_shape}
""".strip()

    def _output_shape(self, channel: str) -> str:
        """Return the required JSON shape for one channel."""
        if channel == "email":
            return '{\n  "subject": "Short specific subject",\n  "body": "Personalized email body"\n}'
        if channel == "whatsapp":
            return '{\n  "message": "Concise personalized WhatsApp message"\n}'
        if channel == "linkedin":
            return (
                "{\n"
                '  "connection_message": "Short connection request",\n'
                '  "followup_message": "Follow-up message after connection"\n'
                "}"
            )
        raise ValueError(f"Unsupported outreach channel: {channel}")

    # TODO: Add prompt versions and channel-specific length controls.
