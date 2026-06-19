"""CSV lead ingestion service."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import logging
from typing import Any, TextIO

from crm_core.repositories.raw_lead_event_repository import RawLeadEventRepository
from crm_core.services.exceptions import DuplicateLeadError, ValidationError
from crm_core.services.lead_service import LeadService
from database.models import Lead, RawLeadEvent
from lead_ingestion.csv.csv_parser import CSVLeadParser, CSVParseResult
from lead_ingestion.interfaces import BaseIngestionService
from lead_ingestion.normalization import NormalizedLead

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CSVImportResult:
    """Summary of a CSV import operation."""

    success_count: int
    failed_count: int
    duplicate_count: int
    raw_event_count: int
    errors: list[str]


class CSVIngestionService(BaseIngestionService):
    """Ingest leads from CSV content."""

    source = "csv"

    def __init__(
        self,
        lead_service: LeadService | None = None,
        raw_event_repository: RawLeadEventRepository | None = None,
        parser: CSVLeadParser | None = None,
    ) -> None:
        """Create a CSV ingestion service with injectable dependencies."""
        self.lead_service = lead_service or LeadService()
        self.raw_event_repository = raw_event_repository or RawLeadEventRepository(session=self.lead_service.session)
        self.parser = parser or CSVLeadParser()

    def import_csv(self, csv_input: str | TextIO) -> CSVImportResult:
        """Read, validate, normalize, and import CSV leads."""
        parse_result = self.parser.parse(csv_input)
        success_count = 0
        failed_count = len(parse_result.errors)
        duplicate_count = parse_result.duplicate_count
        raw_event_count = 0
        errors = [f"row {error.row_number}: {error.message}" for error in parse_result.errors]

        for normalized in parse_result.leads:
            raw_event = self.create_raw_event(normalized.to_lead_payload(), normalized)
            raw_event_count += 1
            try:
                lead = self.create_lead(normalized)
            except DuplicateLeadError as exc:
                duplicate_count += 1
                errors.append(str(exc))
                logger.info("CSV lead skipped as duplicate email=%s", normalized.email)
                continue
            except ValidationError as exc:
                failed_count += 1
                errors.append(str(exc))
                logger.warning("CSV lead failed validation email=%s error=%s", normalized.email, exc)
                continue

            self.raw_event_repository.update(
                raw_event.id,
                is_processed=True,
                processed_at=datetime.utcnow(),
                normalized_payload=normalized.to_lead_payload(),
            )
            success_count += 1
            logger.info("CSV lead ingested lead_id=%s raw_event_id=%s", lead.id, raw_event.id)

        return CSVImportResult(
            success_count=success_count,
            failed_count=failed_count,
            duplicate_count=duplicate_count,
            raw_event_count=raw_event_count,
            errors=errors,
        )

    def validate(self, payload: str | TextIO) -> None:
        """Validate CSV input by parsing it."""
        parse_result = self.parser.parse(payload)
        if parse_result.errors:
            raise ValidationError(parse_result.errors[0].message)

    def normalize(self, payload: dict[str, Any]) -> NormalizedLead:
        """Return a normalized lead from a row-like payload."""
        return self.parser.normalizer.normalize(payload, source=self.source)

    def create_raw_event(self, payload: dict[str, Any], normalized: NormalizedLead | None = None) -> RawLeadEvent:
        """Store one raw CSV lead event."""
        return self.raw_event_repository.create(
            source=self.source,
            external_id=normalized.email if normalized else None,
            raw_payload=payload,
            normalized_payload=normalized.to_lead_payload() if normalized else None,
            is_processed=False,
            processed_at=None,
        )

    def create_lead(self, normalized: NormalizedLead) -> Lead:
        """Create a CRM lead from normalized CSV input."""
        return self.lead_service.create_lead(**normalized.to_lead_payload())

    # TODO: Add per-row source line tracking if CSV imports become user-visible audit logs.
