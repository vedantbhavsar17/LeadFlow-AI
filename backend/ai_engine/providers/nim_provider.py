"""NVIDIA NIM AI provider implementation."""

from __future__ import annotations

import json
import logging
from os import getenv
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from flask import current_app, has_app_context

from ai_engine.models import AIRequest, AIResponse
from ai_engine.providers.base_provider import BaseAIProvider

logger = logging.getLogger(__name__)


class NIMProvider(BaseAIProvider):
    """NVIDIA NIM provider using the OpenAI-compatible chat completions API."""

    provider_name = "nim"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout_seconds: float | None = None,
    ) -> None:
        """Create a NIM provider from explicit values, Flask config, or environment."""
        self.api_key = api_key if api_key is not None else self._config_value("NVIDIA_NIM_API_KEY", "")
        self.base_url = (base_url if base_url is not None else self._config_value("NVIDIA_NIM_BASE_URL", "https://integrate.api.nvidia.com/v1")).rstrip("/")
        self.model = model if model is not None else self._config_value("NVIDIA_NIM_MODEL", "")
        self.timeout_seconds = float(timeout_seconds if timeout_seconds is not None else self._config_value("NVIDIA_NIM_TIMEOUT_SECONDS", 30))

    def generate(self, request: AIRequest) -> AIResponse:
        """Generate text from a single prompt."""
        request.validate()
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})
        return self.chat(messages, request)

    def chat(self, messages: list[dict[str, str]], request: AIRequest | None = None) -> AIResponse:
        """Generate text from chat messages."""
        if not messages:
            return AIResponse.failed(provider=self.provider_name, model=self.model, error="messages are required.")
        if not self.api_key:
            return AIResponse.failed(provider=self.provider_name, model=self.model, error="NVIDIA_NIM_API_KEY is not configured.")
        if not self.model:
            return AIResponse.failed(provider=self.provider_name, model=self.model, error="NVIDIA_NIM_MODEL is not configured.")

        generation_request = request or AIRequest(prompt=messages[-1].get("content", ""))
        try:
            payload = self._build_chat_payload(messages, generation_request)
            response_payload = self._post_json("/chat/completions", payload)
            content = self._extract_content(response_payload)
            tokens_used = self._extract_tokens_used(response_payload)
            return AIResponse(
                content=content,
                provider=self.provider_name,
                model=str(response_payload.get("model") or self.model),
                tokens_used=tokens_used,
                success=True,
                error=None,
            )
        except (TimeoutError, HTTPError, URLError, ValueError, OSError) as exc:
            logger.warning("NIM provider request failed: %s", exc)
            return AIResponse.failed(provider=self.provider_name, model=self.model, error=str(exc))

    def health_check(self) -> dict[str, Any]:
        """Return NIM provider configuration and connectivity status."""
        if not self.api_key:
            return {"provider": self.provider_name, "healthy": False, "error": "NVIDIA_NIM_API_KEY is not configured."}
        if not self.model:
            return {"provider": self.provider_name, "healthy": False, "error": "NVIDIA_NIM_MODEL is not configured."}

        response = self.generate(AIRequest(prompt="ping", system_prompt="Reply with ok.", temperature=0, max_tokens=4))
        return {
            "provider": self.provider_name,
            "healthy": response.success,
            "model": self.model,
            "error": response.error,
        }

    def _build_chat_payload(self, messages: list[dict[str, str]], request: AIRequest) -> dict[str, Any]:
        """Build the NIM chat completions payload."""
        return {
            "model": self.model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }

    def _post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """POST JSON to the NIM API and return decoded JSON."""
        url = f"{self.base_url}{path}"
        body = json.dumps(payload).encode("utf-8")
        request = Request(
            url,
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        with urlopen(request, timeout=self.timeout_seconds) as response:
            raw_body = response.read().decode("utf-8")
        decoded = json.loads(raw_body)
        if not isinstance(decoded, dict):
            raise ValueError("NIM response was not a JSON object.")
        return decoded

    def _extract_content(self, response_payload: dict[str, Any]) -> str:
        """Extract assistant content from a NIM response."""
        choices = response_payload.get("choices") or []
        if not choices:
            raise ValueError("NIM response did not include choices.")
        message = choices[0].get("message") or {}
        content = message.get("content")
        if content is None:
            raise ValueError("NIM response did not include message content.")
        return str(content)

    @staticmethod
    def _extract_tokens_used(response_payload: dict[str, Any]) -> int | None:
        """Extract total token usage when provided."""
        usage = response_payload.get("usage") or {}
        total_tokens = usage.get("total_tokens")
        return int(total_tokens) if total_tokens is not None else None

    @staticmethod
    def _config_value(name: str, default: Any) -> Any:
        """Read config from Flask current_app when available, then environment."""
        if has_app_context():
            return current_app.config.get(name, getenv(name, default))
        return getenv(name, default)

    # TODO: Add retries/backoff only after observing provider failure modes.
