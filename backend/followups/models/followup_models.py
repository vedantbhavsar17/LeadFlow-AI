"""Follow-up recommendation models."""

from dataclasses import asdict, dataclass
from datetime import datetime


FOLLOWUP_PRIORITIES = {"low", "normal", "high", "urgent"}
FOLLOWUP_STATUSES = {"pending", "completed", "cancelled"}


@dataclass(frozen=True)
class FollowupRecommendation:
    """Structured follow-up recommendation."""

    followup_required: bool
    due_date: datetime | None
    priority: str
    reason: str
    suggested_message: str
    channel: str = "email"

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""
        payload = asdict(self)
        payload["due_date"] = self.due_date.isoformat() if self.due_date else None
        return payload


class FollowupError(Exception):
    """Raised when follow-up operations fail."""


class FollowupRuleError(FollowupError):
    """Raised when follow-up rule evaluation fails."""
