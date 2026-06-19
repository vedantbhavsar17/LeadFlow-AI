"""Response parser for AI outreach generation."""

from __future__ import annotations

import json
import re
from typing import Any

from ai_engine.outreach_generation.outreach_models import (
    SUPPORTED_OUTREACH_CHANNELS,
    OutreachParseError,
    OutreachResult,
)


class OutreachResponseParser:
    """Parse and validate structured outreach JSON."""

    required_fields = {
        "email": {"subject", "body"},
        "whatsapp": {"message"},
        "linkedin": {"connection_message", "followup_message"},
    }

    def parse(self, *, channel: str, content: str | None) -> OutreachResult:
        """Parse provider content into an OutreachResult."""
        normalized_channel = str(channel or "").strip().lower()
        if normalized_channel not in SUPPORTED_OUTREACH_CHANNELS:
            raise OutreachParseError(f"Unsupported outreach channel: {channel}")
        if not content:
            raise OutreachParseError("Outreach response was empty.")

        payload = self._load_json(content)
        required = self.required_fields[normalized_channel]
        missing = [field for field in sorted(required) if not self._clean_text(payload.get(field))]
        if missing:
            raise OutreachParseError(f"Missing outreach fields: {', '.join(missing)}.")

        parsed = {field: self._clean_text(payload[field]) for field in sorted(required)}
        return OutreachResult(channel=normalized_channel, content=parsed)

    def _load_json(self, content: str) -> dict[str, Any]:
        """Load JSON, tolerating fenced JSON blocks if returned."""
        cleaned = content.strip()
        fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, flags=re.DOTALL | re.IGNORECASE)
        if fenced:
            cleaned = fenced.group(1).strip()

        try:
            payload = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise OutreachParseError(f"Invalid JSON outreach response: {exc}") from exc

        if not isinstance(payload, dict):
            raise OutreachParseError("Outreach response must be a JSON object.")
        return payload

    @staticmethod
    def _clean_text(value: Any) -> str:
        """Return stripped string content."""
        return str(value or "").strip()

    # TODO: Add channel-specific anti-spam linting before production use.
