"""Validate NVIDIA NIM configuration and real generation."""

from __future__ import annotations

import os

from _validation import app_context, print_result, run_validation


EXPECTED_TEXT = "LeadFlow NIM Test Successful"


def _check() -> list[str]:
    from ai_engine.models import AIRequest
    from ai_engine.providers.provider_factory import AIProviderFactory

    if not os.getenv("NVIDIA_NIM_API_KEY"):
        raise AssertionError("NVIDIA_NIM_API_KEY is not configured.")

    with app_context():
        provider = AIProviderFactory.create("nim")
        response = provider.generate(
            AIRequest(
                prompt=f"Reply with exactly:\n{EXPECTED_TEXT}",
                system_prompt="Follow the user instruction exactly and output no extra text.",
                temperature=0,
                max_tokens=16,
            )
        )
        if not response.success:
            raise AssertionError(f"NIM generation failed: {response.error}")
        if EXPECTED_TEXT not in response.content:
            raise AssertionError(f"NIM response did not contain expected text. Response: {response.content!r}")
        return [
            "NVIDIA_NIM_API_KEY exists.",
            f"Provider loaded: {provider.__class__.__name__}.",
            f"Generation response contained: {EXPECTED_TEXT}",
        ]


def run_check():
    return run_validation("NIM", _check)


if __name__ == "__main__":
    print_result(run_check())

