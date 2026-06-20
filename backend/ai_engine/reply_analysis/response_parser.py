"""Response parser for reply analysis."""

from __future__ import annotations

import json
import re
from typing import Any

from ai_engine.reply_analysis.reply_models import (
    ReplyAnalysisParseError,
    ReplyAnalysisResult,
    VALID_REPLY_INTENTS,
    VALID_SENTIMENTS,
)


class ReplyAnalysisResponseParser:
    """Parse and validate structured reply analysis JSON."""

    def parse(self, content: str | None) -> ReplyAnalysisResult:
        """Parse provider content into a ReplyAnalysisResult."""
        if not content:
            raise ReplyAnalysisParseError("Reply analysis response was empty.")

        payload = self._load_json(content)
        intent = str(payload.get("intent", "")).strip().lower()
        sentiment = str(payload.get("sentiment", "")).strip().lower()
        objection = payload.get("objection")
        recommended_action = str(payload.get("recommended_action", "")).strip()
        suggested_reply = str(payload.get("suggested_reply", "")).strip()
        confidence = payload.get("confidence")

        if intent not in VALID_REPLY_INTENTS:
            raise ReplyAnalysisParseError("intent is invalid.")
        if sentiment not in VALID_SENTIMENTS:
            raise ReplyAnalysisParseError("sentiment is invalid.")
        if objection is not None and not isinstance(objection, str):
            raise ReplyAnalysisParseError("objection must be null or a string.")
        if not recommended_action:
            raise ReplyAnalysisParseError("recommended_action is required.")
        if not suggested_reply:
            raise ReplyAnalysisParseError("suggested_reply is required.")
        if not isinstance(confidence, int | float) or confidence < 0 or confidence > 1:
            raise ReplyAnalysisParseError("confidence must be a number from 0 to 1.")

        return ReplyAnalysisResult(
            intent=intent,
            sentiment=sentiment,
            objection=objection.strip() if isinstance(objection, str) and objection.strip() else None,
            recommended_action=recommended_action,
            suggested_reply=suggested_reply,
            confidence=float(confidence),
        )

    def _load_json(self, content: str) -> dict[str, Any]:
        """Load JSON, tolerating fenced JSON blocks if returned."""
        cleaned = content.strip()
        fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, flags=re.DOTALL | re.IGNORECASE)
        if fenced:
            cleaned = fenced.group(1).strip()

        try:
            payload = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ReplyAnalysisParseError(f"Invalid JSON reply analysis response: {exc}") from exc

        if not isinstance(payload, dict):
            raise ReplyAnalysisParseError("Reply analysis response must be a JSON object.")
        return payload

    # TODO: Add stricter action taxonomy validation after sales workflow contracts settle.
