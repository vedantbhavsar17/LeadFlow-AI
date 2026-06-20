"""Reply analysis data models."""

from dataclasses import asdict, dataclass

VALID_REPLY_INTENTS = {
    "interested",
    "needs_information",
    "pricing_objection",
    "competitor_objection",
    "follow_up_later",
    "meeting_request",
    "not_interested",
    "unsubscribe",
}

VALID_SENTIMENTS = {"positive", "neutral", "negative"}
REPLY_ANALYSIS_INSIGHT_TYPE = "reply_analysis"


@dataclass(frozen=True)
class ReplyAnalysisResult:
    """Structured output from reply analysis."""

    intent: str
    sentiment: str
    objection: str | None
    recommended_action: str
    suggested_reply: str
    confidence: float

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""
        return asdict(self)


class ReplyAnalysisError(Exception):
    """Raised when reply analysis cannot be completed."""


class ReplyAnalysisParseError(ReplyAnalysisError):
    """Raised when an AI response cannot be parsed into a valid result."""
