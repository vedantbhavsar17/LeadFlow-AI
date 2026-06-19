"""Gemini provider placeholder."""

from typing import Any

from ai_engine.models import AIRequest, AIResponse
from ai_engine.providers import BaseAIProvider


class GeminiProvider(BaseAIProvider):
    """Placeholder for optional future Gemini integration."""

    provider_name = "gemini"

    def generate(self, request: AIRequest) -> AIResponse:
        """Return an explicit not-implemented response."""
        return AIResponse.failed(provider=self.provider_name, model=None, error="Gemini provider is not implemented.")

    def chat(self, messages: list[dict[str, str]], request: AIRequest | None = None) -> AIResponse:
        """Return an explicit not-implemented response."""
        return AIResponse.failed(provider=self.provider_name, model=None, error="Gemini provider is not implemented.")

    def health_check(self) -> dict[str, Any]:
        """Return placeholder health state."""
        return {"provider": self.provider_name, "healthy": False, "error": "Gemini provider is not implemented."}


__all__ = ["GeminiProvider"]
