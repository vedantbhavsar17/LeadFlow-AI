"""Follow-up rule constants and helpers."""

from __future__ import annotations

from datetime import datetime, timedelta
import re
from typing import Any


NO_REPLY_INTERVAL_DAYS = (3, 7, 14)
INTERESTED_FOLLOWUP_DAYS = 2
PRICING_OBJECTION_FOLLOWUP_DAYS = 3


def add_days(now: datetime, days: int) -> datetime:
    """Return a datetime offset by whole days."""
    return now + timedelta(days=days)


def extract_suggested_date(reply_analysis: dict[str, Any], *, now: datetime) -> datetime:
    """Extract a suggested follow-up date or fall back to seven days.

    The reply-analysis model currently stores free-form structured output. This
    helper accepts optional future fields such as `suggested_followup_at` or
    `followup_date` without requiring a schema migration.
    """
    for key in ("suggested_followup_at", "followup_date", "due_date"):
        raw_value = reply_analysis.get(key)
        if not raw_value:
            continue
        parsed = _parse_datetime(str(raw_value))
        if parsed:
            return parsed
    return add_days(now, 7)


def _parse_datetime(value: str) -> datetime | None:
    """Parse an ISO-ish datetime value."""
    normalized = value.strip()
    if not normalized:
        return None
    try:
        return datetime.fromisoformat(normalized.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        pass

    date_match = re.fullmatch(r"\d{4}-\d{2}-\d{2}", normalized)
    if date_match:
        try:
            return datetime.fromisoformat(f"{normalized}T09:00:00")
        except ValueError:
            return None
    return None

    # TODO: Add natural-language date parsing only when product UX requires it.
