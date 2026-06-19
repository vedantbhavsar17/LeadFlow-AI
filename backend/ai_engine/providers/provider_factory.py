"""AI provider factory."""

from __future__ import annotations

from os import getenv

from flask import current_app, has_app_context

from ai_engine.providers.base_provider import BaseAIProvider
from ai_engine.providers.nim_provider import NIMProvider


class AIProviderFactory:
    """Resolve the active AI provider from configuration."""

    @classmethod
    def create(cls, provider_name: str | None = None) -> BaseAIProvider:
        """Return the configured provider. Defaults to NVIDIA NIM."""
        selected_provider = (provider_name or cls._config_value("AI_PROVIDER", "nim")).strip().lower()
        if selected_provider == "nim":
            return NIMProvider()
        if selected_provider in {"gemini", "ollama"}:
            raise NotImplementedError(f"{selected_provider} provider is planned but not implemented.")
        raise ValueError(f"Unsupported AI provider: {selected_provider}")

    @staticmethod
    def _config_value(name: str, default: str) -> str:
        """Read config from Flask current_app when available, then environment."""
        if has_app_context():
            return str(current_app.config.get(name, getenv(name, default)))
        return str(getenv(name, default))

    # TODO: Register Gemini and Ollama providers when those integrations are implemented.
