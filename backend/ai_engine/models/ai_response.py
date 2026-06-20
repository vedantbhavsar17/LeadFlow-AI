"""Provider-neutral AI response model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AIResponse:
    """Text generation response returned by AI providers."""

    content: str | None
    provider: str
    model: str | None
    tokens_used: int | None = None
    success: bool = True
    error: str | None = None

    @classmethod
    def failed(cls, *, provider: str, model: str | None, error: str) -> "AIResponse":
        """Create a failed response."""
        return cls(
            content=None,
            provider=provider,
            model=model,
            tokens_used=None,
            success=False,
            error=error,
        )
