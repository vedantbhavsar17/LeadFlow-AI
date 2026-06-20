"""Autopilot workflow models."""

from dataclasses import asdict, dataclass, field

AUTOPILOT_MODES = {"manual", "suggested", "automatic"}
AUTOPILOT_INSIGHT_TYPE = "autopilot_reply"


@dataclass(frozen=True)
class AutopilotDraft:
    """Generated response before workflow execution."""

    recommended_action: str
    generated_reply: str
    send_mode: str
    confidence: float

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class AutopilotResult:
    """Autopilot workflow result."""

    recommended_action: str
    generated_reply: str
    send_mode: str
    confidence: float
    draft_message_id: int | None = None
    sent_message_id: int | None = None
    human_review_required: bool = False
    safety_reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class SafetyDecision:
    """Safety decision for an autopilot-generated reply."""

    can_auto_send: bool
    reasons: list[str]


class AutopilotError(Exception):
    """Raised when autopilot workflow cannot be completed."""


class AutopilotParseError(AutopilotError):
    """Raised when generated autopilot output is invalid."""
