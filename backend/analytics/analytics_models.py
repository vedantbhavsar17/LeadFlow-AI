"""Analytics service response models."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class DashboardMetrics:
    """Dashboard-ready aggregate metrics."""

    total_leads: int
    new_leads: int
    hot_leads: int
    warm_leads: int
    cold_leads: int
    converted_leads: int
    conversion_rate: float
    followups_due: int
    meetings_booked: int
    average_conversion_score: float
    lead_source_breakdown: dict[str, int]
    reply_rate: float
    outreach_generated_count: int
    ai_qualification_distribution: dict[str, int]

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class ConversionMetrics:
    """Conversion-focused analytics metrics."""

    converted_leads: int
    lost_leads: int
    conversion_rate: float
    average_conversion_score: float
    prediction_distribution: dict[str, int]

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class FollowupMetrics:
    """Follow-up analytics metrics."""

    due: int
    pending: int
    completed: int
    overdue: int
    by_channel: dict[str, int]

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class PredictionMetrics:
    """Conversion prediction analytics metrics."""

    total_predictions: int
    average_score: float
    low_probability: int
    medium_probability: int
    high_probability: int

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""
        return asdict(self)


class AnalyticsError(Exception):
    """Raised when analytics cannot be generated."""

