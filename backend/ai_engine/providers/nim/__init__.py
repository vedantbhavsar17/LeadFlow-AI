"""NVIDIA NIM provider placeholder.

NIM is the primary LeadFlow AI provider.
"""

from backend.ai_engine.providers import AIProvider


class NIMProvider(AIProvider):
    """Placeholder for NVIDIA NIM API integration."""

    provider_name = "nim"

    # TODO: Implement NIM request adapter in AI implementation phase.
    pass

