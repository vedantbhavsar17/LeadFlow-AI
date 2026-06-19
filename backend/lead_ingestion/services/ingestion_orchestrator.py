"""Lead ingestion orchestrator."""

from __future__ import annotations

from typing import TextIO

from database.models import Lead, RawLeadEvent
from lead_ingestion.csv import CSVImportResult, CSVIngestionService
from lead_ingestion.manual import ManualIngestionService


class IngestionOrchestrator:
    """Single entry point for supported lead ingestion sources."""

    def __init__(
        self,
        manual_ingestion_service: ManualIngestionService | None = None,
        csv_ingestion_service: CSVIngestionService | None = None,
    ) -> None:
        """Create an ingestion orchestrator."""
        self.manual_ingestion_service = manual_ingestion_service or ManualIngestionService()
        self.csv_ingestion_service = csv_ingestion_service or CSVIngestionService(
            lead_service=self.manual_ingestion_service.lead_service,
            raw_event_repository=self.manual_ingestion_service.raw_event_repository,
        )

    def create_manual_lead(
        self,
        *,
        name: str,
        email: str | None = None,
        phone: str | None = None,
        company: str | None = None,
        notes: str | None = None,
    ) -> tuple[Lead, RawLeadEvent]:
        """Ingest one manually entered lead."""
        return self.manual_ingestion_service.create_manual_lead(
            name=name,
            email=email,
            phone=phone,
            company=company,
            notes=notes,
        )

    def import_csv(self, csv_input: str | TextIO) -> CSVImportResult:
        """Ingest leads from CSV content."""
        return self.csv_ingestion_service.import_csv(csv_input)

    # TODO: Add Meta, Google, website form, and API source routing in future phases.
