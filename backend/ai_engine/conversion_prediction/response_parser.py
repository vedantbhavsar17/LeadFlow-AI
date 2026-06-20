"""Response parser for conversion prediction."""

from __future__ import annotations

import json
import re
from typing import Any

from ai_engine.conversion_prediction.prediction_models import (
    ConversionPredictionParseError,
    ConversionPredictionResult,
)


class ConversionPredictionResponseParser:
    """Parse and validate structured conversion prediction JSON."""

    def parse(self, content: str | None) -> ConversionPredictionResult:
        """Parse provider content into a ConversionPredictionResult."""
        if not content:
            raise ConversionPredictionParseError("Conversion prediction response was empty.")

        payload = self._load_json(content)
        score = payload.get("score")
        confidence = payload.get("confidence")
        reasons = payload.get("reasons")
        risk_factors = payload.get("risk_factors")
        recommended_action = str(payload.get("recommended_action", "")).strip()

        if not isinstance(score, int) or score < 0 or score > 100:
            raise ConversionPredictionParseError("score must be an integer from 0 to 100.")
        if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
            raise ConversionPredictionParseError("confidence must be a number from 0 to 1.")
        if not isinstance(reasons, list) or not all(isinstance(item, str) for item in reasons):
            raise ConversionPredictionParseError("reasons must be an array of strings.")
        if not isinstance(risk_factors, list) or not all(isinstance(item, str) for item in risk_factors):
            raise ConversionPredictionParseError("risk_factors must be an array of strings.")
        if not recommended_action:
            raise ConversionPredictionParseError("recommended_action is required.")

        return ConversionPredictionResult(
            score=score,
            confidence=float(confidence),
            reasons=[item.strip() for item in reasons if item.strip()],
            risk_factors=[item.strip() for item in risk_factors if item.strip()],
            recommended_action=recommended_action,
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
            raise ConversionPredictionParseError(f"Invalid JSON conversion prediction response: {exc}") from exc

        if not isinstance(payload, dict):
            raise ConversionPredictionParseError("Conversion prediction response must be a JSON object.")
        return payload

    # TODO: Add schema-version validation if prediction output expands.
