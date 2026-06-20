"""Email template helpers."""


def plain_text_email(body: str) -> str:
    """Return a normalized plain-text email body."""
    return str(body or "").strip()


def reply_subject(subject: str | None) -> str:
    """Return a reply-friendly subject."""
    cleaned = str(subject or "").strip()
    if not cleaned:
        return "Re: LeadFlow conversation"
    return cleaned if cleaned.lower().startswith("re:") else f"Re: {cleaned}"

    # TODO: Add HTML templates only when frontend/email design is approved.
