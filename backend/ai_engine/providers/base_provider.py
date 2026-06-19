"""Base AI provider interface."""

from abc import ABC, abstractmethod
from typing import Any

from ai_engine.models import AIRequest, AIResponse


class BaseAIProvider(ABC):
    """Abstract interface implemented by all AI providers."""

    provider_name: str = "base"

    @abstractmethod
    def generate(self, request: AIRequest) -> AIResponse:
        """Generate text from a single prompt."""

    @abstractmethod
    def chat(self, messages: list[dict[str, str]], request: AIRequest | None = None) -> AIResponse:
        """Generate text from chat messages."""

    @abstractmethod
    def health_check(self) -> dict[str, Any]:
        """Return provider health information."""

    # TODO: Add streaming support after synchronous provider calls are stable.
