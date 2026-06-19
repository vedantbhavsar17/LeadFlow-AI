"""Provider-neutral AI request model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AIRequest:
    """Text generation request shared by AI providers."""

    prompt: str
    system_prompt: str | None = None
    temperature: float = 0.2
    max_tokens: int = 512

    def validate(self) -> None:
        """Validate request values before provider execution."""
        if not str(self.prompt or "").strip():
            raise ValueError("prompt is required.")
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("temperature must be between 0 and 2.")
        if self.max_tokens <= 0:
            raise ValueError("max_tokens must be greater than zero.")

    # TODO: Add provider-specific options only after a real need appears.
