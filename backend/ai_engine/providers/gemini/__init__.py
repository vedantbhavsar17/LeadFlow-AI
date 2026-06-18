"""Gemini provider placeholder."""

from backend.ai_engine.providers import AIProvider


class GeminiProvider(AIProvider):
    """Placeholder for optional Gemini integration."""

    provider_name = "gemini"

    # TODO: Implement optional Gemini adapter only if needed.
    pass

