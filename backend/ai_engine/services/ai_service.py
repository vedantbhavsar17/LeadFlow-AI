"""Provider-neutral AI service."""

from __future__ import annotations

import logging
from typing import Any

from ai_engine.models import AIRequest, AIResponse
from ai_engine.providers import AIProviderFactory, BaseAIProvider

logger = logging.getLogger(__name__)


class AIService:
    """Single entry point for generic AI provider operations."""

    def __init__(self, provider: BaseAIProvider | None = None) -> None:
        """Create an AI service using the active provider by default."""
        self.provider = provider or AIProviderFactory.create()

    def generate_text(
        self,
        *,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 512,
    ) -> AIResponse:
        """Generate text from a prompt."""
        request = AIRequest(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        logger.info("AI text generation requested provider=%s", self.provider.provider_name)
        return self.provider.generate(request)

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.2,
        max_tokens: int = 512,
    ) -> AIResponse:
        """Generate a response from chat messages."""
        prompt = messages[-1].get("content", "") if messages else ""
        request = AIRequest(prompt=prompt, temperature=temperature, max_tokens=max_tokens)
        logger.info("AI chat requested provider=%s", self.provider.provider_name)
        return self.provider.chat(messages, request)

    def health_check(self) -> dict[str, Any]:
        """Return active provider health information."""
        return self.provider.health_check()

    # TODO: Add workflow-specific AI services on top of this generic provider layer.
