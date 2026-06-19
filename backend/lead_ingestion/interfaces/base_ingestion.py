"""Base ingestion interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from database.models import Lead, RawLeadEvent
from lead_ingestion.normalization import NormalizedLead


class BaseIngestionService(ABC):
    """Contract shared by all source ingestion services."""

    source: str

    @abstractmethod
    def validate(self, payload: Any) -> None:
        """Validate source input before persistence."""

    @abstractmethod
    def normalize(self, payload: Any) -> NormalizedLead:
        """Convert source input into a NormalizedLead."""

    @abstractmethod
    def create_raw_event(self, payload: Any, normalized: NormalizedLead | None = None) -> RawLeadEvent:
        """Persist raw source input for auditability and replay."""

    @abstractmethod
    def create_lead(self, normalized: NormalizedLead) -> Lead:
        """Create a CRM lead from normalized source input."""

    # TODO: Add a shared ingestion result protocol once async sources exist.
