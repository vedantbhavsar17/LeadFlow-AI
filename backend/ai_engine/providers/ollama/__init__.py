"""Ollama provider placeholder."""

from typing import Any

from ai_engine.models import AIRequest, AIResponse
from ai_engine.providers import BaseAIProvider


class OllamaProvider(BaseAIProvider):
    """Placeholder for optional future local Ollama integration."""

    provider_name = "ollama"

    def generate(self, request: AIRequest) -> AIResponse:
        """Return an explicit not-implemented response."""
        return AIResponse.failed(provider=self.provider_name, model=None, error="Ollama provider is not implemented.")

    def chat(self, messages: list[dict[str, str]], request: AIRequest | None = None) -> AIResponse:
        """Return an explicit not-implemented response."""
        return AIResponse.failed(provider=self.provider_name, model=None, error="Ollama provider is not implemented.")

    def health_check(self) -> dict[str, Any]:
        """Return placeholder health state."""
        return {"provider": self.provider_name, "healthy": False, "error": "Ollama provider is not implemented."}


__all__ = ["OllamaProvider"]
