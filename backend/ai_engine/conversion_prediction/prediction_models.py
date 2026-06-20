"""Conversion prediction data models."""

from dataclasses import asdict, dataclass


CONVERSION_PREDICTION_INSIGHT_TYPE = "conversion_prediction"
VALID_PROBABILITY_LABELS = {"low", "medium", "high"}


@dataclass(frozen=True)
class ConversionPredictionResult:
    """Structured output from conversion prediction."""

    score: int
    confidence: float
    reasons: list[str]
    risk_factors: list[str]
    recommended_action: str

    @property
    def probability_label(self) -> str:
        """Return the probability bucket for the score."""
        if self.score <= 39:
            return "low"
        if self.score <= 69:
            return "medium"
        return "high"

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""
        payload = asdict(self)
        payload["probability_label"] = self.probability_label
        return payload


class ConversionPredictionError(Exception):
    """Raised when conversion prediction cannot be completed."""


class ConversionPredictionParseError(ConversionPredictionError):
    """Raised when an AI response cannot be parsed into a valid prediction."""
