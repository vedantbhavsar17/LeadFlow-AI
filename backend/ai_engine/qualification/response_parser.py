"""Response parser for lead qualification."""

from __future__ import annotations

import json
import re
from typing import Any

from ai_engine.qualification.qualification_models import (
    QualificationParseError,
    QualificationResult,
    VALID_BUYING_INTENTS,
    VALID_CATEGORIES,
)


class QualificationResponseParser:
    """Parse and validate qualification JSON from an AI provider."""

    def parse(self, content: str | None) -> QualificationResult:
        """Parse provider content into a QualificationResult."""
        if not content:
            raise QualificationParseError("Qualification response was empty.")

        payload = self._load_json(content)
        score = payload.get("score")
        category = str(payload.get("category", "")).strip().lower()
        buying_intent = str(payload.get("buying_intent", "")).strip().lower()
        pain_points = payload.get("pain_points")
        recommended_action = str(payload.get("recommended_action", "")).strip()
        reasoning = str(payload.get("reasoning", "")).strip()

        if not isinstance(score, int) or score < 0 or score > 100:
            raise QualificationParseError("score must be an integer from 0 to 100.")
        if category not in VALID_CATEGORIES:
            raise QualificationParseError("category must be one of: hot, warm, cold.")
        if buying_intent not in VALID_BUYING_INTENTS:
            raise QualificationParseError("buying_intent must be one of: high, medium, low.")
        if not isinstance(pain_points, list) or not all(isinstance(item, str) for item in pain_points):
            raise QualificationParseError("pain_points must be an array of strings.")
        if not recommended_action:
            raise QualificationParseError("recommended_action is required.")
        if not reasoning:
            raise QualificationParseError("reasoning is required.")

        return QualificationResult(
            score=score,
            category=category,
            buying_intent=buying_intent,
            pain_points=[item.strip() for item in pain_points if item.strip()],
            recommended_action=recommended_action,
            reasoning=reasoning,
        )

    def _load_json(self, content: str) -> dict[str, Any]:
        """Load JSON, tolerating fenced JSON blocks if a provider returns them."""
        cleaned = content.strip()
        fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, flags=re.DOTALL | re.IGNORECASE)
        if fenced:
            cleaned = fenced.group(1).strip()

        try:
            payload = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise QualificationParseError(f"Invalid JSON qualification response: {exc}") from exc

        if not isinstance(payload, dict):
            raise QualificationParseError("Qualification response must be a JSON object.")
        return payload

    # TODO: Add schema-version handling if qualification output evolves.
