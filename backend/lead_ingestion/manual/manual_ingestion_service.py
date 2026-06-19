"""Manual lead ingestion service."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from crm_core.repositories.raw_lead_event_repository import RawLeadEventRepository
from crm_core.services.lead_service import LeadService
from database.models import Lead, RawLeadEvent
from lead_ingestion.interfaces import BaseIngestionService
from lead_ingestion.normalization import LeadNormalizer, NormalizedLead

logger = logging.getLogger(__name__)


class ManualIngestionService(BaseIngestionService):
    """Ingest leads entered manually by a user or internal process."""

    source = "manual"

    def __init__(
        self,
        lead_service: LeadService | None = None,
        raw_event_repository: RawLeadEventRepository | None = None,
        normalizer: LeadNormalizer | None = None,
    ) -> None:
        """Create a manual ingestion service with injectable dependencies."""
        self.lead_service = lead_service or LeadService()
        self.raw_event_repository = raw_event_repository or RawLeadEventRepository(session=self.lead_service.session)
        self.normalizer = normalizer or LeadNormalizer()

    def create_manual_lead(
        self,
        *,
        name: str,
        email: str | None = None,
        phone: str | None = None,
        company: str | None = None,
        notes: str | None = None,
    ) -> tuple[Lead, RawLeadEvent]:
        """Create a lead from manual input and store the raw event."""
        payload = {
            "name": name,
            "email": email,
            "phone": phone,
            "company": company,
            "notes": notes,
        }
        self.validate(payload)
        normalized = self.normalize(payload)
        raw_event = self.create_raw_event(payload, normalized)
        lead = self.create_lead(normalized)
        self.raw_event_repository.update(
            raw_event.id,
            is_processed=True,
            processed_at=datetime.utcnow(),
            normalized_payload=normalized.to_lead_payload(),
        )
        logger.info("Manual lead ingested lead_id=%s raw_event_id=%s", lead.id, raw_event.id)
        return lead, raw_event

    def validate(self, payload: dict[str, Any]) -> None:
        """Validate manual lead input."""
        self.normalizer.normalize(payload, source=self.source)

    def normalize(self, payload: dict[str, Any]) -> NormalizedLead:
        """Normalize manual lead input."""
        return self.normalizer.normalize(payload, source=self.source)

    def create_raw_event(self, payload: dict[str, Any], normalized: NormalizedLead | None = None) -> RawLeadEvent:
        """Store a raw manual lead event."""
        return self.raw_event_repository.create(
            source=self.source,
            external_id=None,
            raw_payload=payload,
            normalized_payload=normalized.to_lead_payload() if normalized else None,
            is_processed=False,
            processed_at=None,
        )

    def create_lead(self, normalized: NormalizedLead) -> Lead:
        """Create a CRM lead from normalized manual input."""
        return self.lead_service.create_lead(**normalized.to_lead_payload())

    # TODO: Add actor attribution after authentication exists.
