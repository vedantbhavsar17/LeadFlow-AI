"""Email communication models."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class EmailSendResult:
    """Result returned after an SMTP send attempt."""

    success: bool
    message_id: str | None
    error: str | None = None


@dataclass(frozen=True)
class IncomingEmail:
    """Parsed incoming email payload."""

    message_id: str | None
    in_reply_to: str | None
    from_email: str | None
    to_email: str | None
    subject: str | None
    body: str
    raw_headers: dict[str, str] = field(default_factory=dict)


class EmailCommunicationError(Exception):
    """Raised when email communication fails."""
