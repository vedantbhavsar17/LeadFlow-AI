"""CSV parsing for lead ingestion."""

from __future__ import annotations

from dataclasses import dataclass, field
import csv
from io import StringIO
from typing import TextIO

from crm_core.services.exceptions import ValidationError
from lead_ingestion.normalization import LeadNormalizer, NormalizedLead


@dataclass(frozen=True)
class CSVRowError:
    """Validation error for one CSV row."""

    row_number: int
    message: str


@dataclass
class CSVParseResult:
    """Structured CSV parser result."""

    leads: list[NormalizedLead] = field(default_factory=list)
    errors: list[CSVRowError] = field(default_factory=list)
    duplicate_count: int = 0


class CSVLeadParser:
    """Parse CSV lead data into normalized lead objects."""

    required_fields = {"name", "email"}

    def __init__(self, normalizer: LeadNormalizer | None = None) -> None:
        """Create a CSV parser."""
        self.normalizer = normalizer or LeadNormalizer()

    def parse(self, csv_input: str | TextIO) -> CSVParseResult:
        """Parse CSV content and return normalized lead objects."""
        stream = StringIO(csv_input) if isinstance(csv_input, str) else csv_input
        reader = csv.DictReader(stream)
        result = CSVParseResult()

        if not reader.fieldnames:
            result.errors.append(CSVRowError(row_number=0, message="CSV header row is required."))
            return result

        normalized_headers = {header.strip().lower() for header in reader.fieldnames if header}
        missing = self.required_fields - normalized_headers
        if missing:
            result.errors.append(CSVRowError(row_number=0, message=f"Missing required columns: {', '.join(sorted(missing))}."))
            return result

        seen_keys: set[str] = set()
        for row_number, row in enumerate(reader, start=2):
            payload = self._normalize_row_keys(row)
            duplicate_key = self._duplicate_key(payload)
            if duplicate_key in seen_keys:
                result.duplicate_count += 1
                continue
            seen_keys.add(duplicate_key)

            try:
                result.leads.append(self.normalizer.normalize(payload, source="csv"))
            except ValidationError as exc:
                result.errors.append(CSVRowError(row_number=row_number, message=str(exc)))

        return result

    def _normalize_row_keys(self, row: dict[str, str | None]) -> dict[str, str | None]:
        """Normalize CSV headers for expected lead fields."""
        return {str(key or "").strip().lower(): value for key, value in row.items()}

    def _duplicate_key(self, row: dict[str, str | None]) -> str:
        """Return a stable duplicate key for one CSV row."""
        email = str(row.get("email") or "").strip().lower()
        if email:
            return f"email:{email}"
        name = str(row.get("name") or "").strip().lower()
        phone = str(row.get("phone") or "").strip()
        return f"name-phone:{name}:{phone}"

    # TODO: Support configurable column aliases after source mapping UI exists.
