"""Lead journey response models."""

from dataclasses import asdict, dataclass
from datetime import datetime


LEAD_STAGE_ORDER = [
    "new",
    "qualified",
    "engaged",
    "follow_up_needed",
    "meeting_booked",
    "proposal_sent",
    "converted",
    "lost",
]


@dataclass(frozen=True)
class JourneyEvent:
    """One normalized event in a lead journey."""

    timestamp: datetime
    event: str
    type: str
    source: str
    metadata: dict | None = None

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""
        payload = asdict(self)
        payload["timestamp"] = self.timestamp.isoformat()
        return payload


@dataclass(frozen=True)
class StageProgress:
    """Current lifecycle progress for a lead."""

    current_stage: str
    progress_percent: int
    completed_stages: list[str]

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class LeadJourney:
    """Complete lead journey response."""

    lead_id: int
    events: list[JourneyEvent]
    stage_progress: StageProgress

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary."""
        return {
            "lead_id": self.lead_id,
            "events": [event.to_dict() for event in self.events],
            "stage_progress": self.stage_progress.to_dict(),
        }

