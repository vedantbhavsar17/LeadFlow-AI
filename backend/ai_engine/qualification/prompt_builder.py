"""Prompt builder for lead qualification."""

from database.models import BusinessContext, Lead


class QualificationPromptBuilder:
    """Build provider-neutral prompts for lead qualification."""

    system_prompt = (
        "You are LeadFlow's lead qualification engine. "
        "Analyze the lead using the business context. "
        "Return structured JSON only. Do not include markdown, comments, or prose outside JSON."
    )

    def build(self, *, lead: Lead, business_context: BusinessContext) -> str:
        """Build a prompt using a lead and business context."""
        lead_name = " ".join(part for part in [lead.first_name, lead.last_name] if part).strip()
        return f"""
Qualify this lead for the business below.

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

Return JSON only with this exact shape:
{{
  "score": 87,
  "category": "hot",
  "buying_intent": "high",
  "pain_points": ["poor lead quality", "manual followups"],
  "recommended_action": "schedule_demo",
  "reasoning": "Brief explanation."
}}

Validation rules:
- score must be an integer from 0 to 100.
- category must be one of: hot, warm, cold.
- buying_intent must be one of: high, medium, low.
- pain_points must be an array of strings.
- recommended_action must be a short snake_case action.
- reasoning must be concise.
""".strip()

    # TODO: Add prompt versioning before production evaluation begins.
