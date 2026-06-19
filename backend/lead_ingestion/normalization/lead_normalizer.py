"""Lead normalization utilities."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any

from crm_core.services.exceptions import ValidationError

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class NormalizedLead:
    """Source-neutral lead payload ready for CRM lead creation."""

    first_name: str
    last_name: str | None
    email: str | None
    phone: str | None
    company: str | None
    source: str
    notes: str | None = None
    external_source_id: str | None = None
    campaign_name: str | None = None

    def to_lead_payload(self) -> dict[str, Any]:
        """Return a dictionary accepted by LeadService.create_lead."""
        return asdict(self)


class LeadNormalizer:
    """Convert source-specific payloads into NormalizedLead objects."""

    def normalize(self, payload: dict[str, Any], *, source: str) -> NormalizedLead:
        """Normalize a raw source payload into a lead creation payload."""
        normalized_source = self._clean_required(source, "source").lower()
        first_name, last_name = self._split_name(payload)
        email = self._normalize_email(payload.get("email"))
        phone = self._clean_optional(payload.get("phone"))

        if not email and not phone:
            raise ValidationError("Either email or phone is required.")

        return NormalizedLead(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            company=self._clean_optional(payload.get("company")),
            source=normalized_source,
            notes=self._clean_optional(payload.get("notes")),
            external_source_id=self._clean_optional(payload.get("external_source_id") or payload.get("external_id")),
            campaign_name=self._clean_optional(payload.get("campaign_name")),
        )

    def _split_name(self, payload: dict[str, Any]) -> tuple[str, str | None]:
        """Split a full name or first/last payload into first and last name."""
        first_name = self._clean_optional(payload.get("first_name"))
        last_name = self._clean_optional(payload.get("last_name"))
        full_name = self._clean_optional(payload.get("name"))

        if first_name:
            return first_name, last_name
        if not full_name:
            raise ValidationError("Lead name is required.")

        parts = full_name.split()
        return parts[0], " ".join(parts[1:]) or None

    def _normalize_email(self, value: Any) -> str | None:
        """Normalize and validate an optional email address."""
        email = self._clean_optional(value)
        if email is None:
            return None
        normalized = email.lower()
        if not EMAIL_PATTERN.match(normalized):
            raise ValidationError(f"Invalid email address: {value}")
        return normalized

    @staticmethod
    def _clean_required(value: Any, field_name: str) -> str:
        """Return stripped text or raise for missing required values."""
        cleaned = LeadNormalizer._clean_optional(value)
        if cleaned is None:
            raise ValidationError(f"{field_name} is required.")
        return cleaned

    @staticmethod
    def _clean_optional(value: Any) -> str | None:
        """Return stripped text or None."""
        if value is None:
            return None
        cleaned = str(value).strip()
        return cleaned or None

    # TODO: Add source-specific normalization strategies for Meta, Google, website, and API sources.
