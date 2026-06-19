"""Outreach generation data models."""

from dataclasses import asdict, dataclass

SUPPORTED_OUTREACH_CHANNELS = {"email", "whatsapp", "linkedin"}
OUTREACH_INSIGHT_TYPE = "outreach"


@dataclass(frozen=True)
class OutreachResult:
    """Structured outreach generation result."""

    channel: str
    content: dict[str, str]

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""
        return {"channel": self.channel, **asdict(self)["content"]}


class OutreachGenerationError(Exception):
    """Raised when outreach generation cannot be completed."""


class OutreachParseError(OutreachGenerationError):
    """Raised when an AI response cannot be parsed into outreach content."""
