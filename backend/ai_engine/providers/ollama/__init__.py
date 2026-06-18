"""Ollama provider placeholder."""

from backend.ai_engine.providers import AIProvider


class OllamaProvider(AIProvider):
    """Placeholder for optional local Ollama integration."""

    provider_name = "ollama"

    # TODO: Implement local model adapter for free/offline AI workflows.
    pass

