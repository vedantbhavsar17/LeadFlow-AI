"""Lead qualification data models."""

from dataclasses import asdict, dataclass


VALID_CATEGORIES = {"hot", "warm", "cold"}
VALID_BUYING_INTENTS = {"high", "medium", "low"}


@dataclass(frozen=True)
class QualificationResult:
    """Structured output from lead qualification."""

    score: int
    category: str
    buying_intent: str
    pain_points: list[str]
    recommended_action: str
    reasoning: str

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""
        return asdict(self)


class QualificationError(Exception):
    """Raised when lead qualification cannot be completed."""


class QualificationParseError(QualificationError):
    """Raised when an AI response cannot be parsed into a valid result."""
