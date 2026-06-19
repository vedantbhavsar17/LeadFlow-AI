"""Lead business service."""

from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from crm_core.repositories.lead_repository import LeadRepository
from crm_core.services.activity_service import ActivityService
from crm_core.services.exceptions import DuplicateLeadError, NotFoundError, ValidationError
from database.models import Lead

logger = logging.getLogger(__name__)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

LEAD_STAGES = {
    "new",
    "qualified",
    "engaged",
    "follow_up_needed",
    "meeting_booked",
    "proposal_sent",
    "converted",
    "lost",
}

LEAD_STATUSES = {
    "new",
    "contacted",
    "no_response",
    "interested",
    "not_interested",
    "qualified",
    "unqualified",
    "meeting_booked",
    "converted",
    "lost",
}

LEAD_PRIORITIES = {"low", "normal", "high", "urgent"}


class LeadService:
    """Business service for core lead operations."""

    def __init__(
        self,
        lead_repository: LeadRepository | None = None,
        activity_service: ActivityService | None = None,
        session: Session | None = None,
    ) -> None:
        """Create a lead service with injectable dependencies."""
        self.lead_repository = lead_repository or LeadRepository(session=session)
        self.session = self.lead_repository.session
        self.activity_service = activity_service or ActivityService(session=self.session)

    def create_lead(self, **data: Any) -> Lead:
        """Create a lead and record a `lead_created` activity."""
        payload = self._normalize_lead_payload(data, require_required_fields=True)
        self._ensure_email_available(payload.get("email"))

        lead = self.lead_repository.create(**payload)
        self.activity_service.create_activity(
            lead_id=lead.id,
            activity_type="lead_created",
            channel="system",
            note="Lead created.",
        )
        logger.info("Created lead id=%s source=%s", lead.id, lead.source)
        return lead

    def update_lead(self, lead_id: int, **data: Any) -> Lead:
        """Update a lead and record status changes when they occur."""
        lead = self.get_lead(lead_id)
        original_status = lead.status
        payload = self._normalize_lead_payload(data, require_required_fields=False)

        if "email" in payload and payload["email"] != lead.email:
            self._ensure_email_available(payload.get("email"), exclude_lead_id=lead_id)

        updated = self.lead_repository.update(lead_id, **payload)
        if updated is None:
            raise NotFoundError(f"Lead {lead_id} was not found.")

        if "status" in payload and payload["status"] != original_status:
            self.activity_service.create_activity(
                lead_id=lead_id,
                activity_type="status_changed",
                channel="system",
                note=f"Status changed from {original_status} to {payload['status']}.",
            )

        logger.info("Updated lead id=%s", lead_id)
        return updated

    def get_lead(self, lead_id: int) -> Lead:
        """Return a lead by id."""
        lead = self.lead_repository.get_by_id(lead_id)
        if lead is None:
            raise NotFoundError(f"Lead {lead_id} was not found.")
        return lead

    def list_leads(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
        source: str | None = None,
        stage: str | None = None,
        status: str | None = None,
        assigned_to: str | None = None,
    ) -> list[Lead]:
        """Return leads with optional lightweight filters."""
        statement = select(Lead).order_by(Lead.created_at.desc()).offset(offset).limit(limit)
        if source:
            statement = statement.where(Lead.source == source)
        if stage:
            statement = statement.where(Lead.stage == stage)
        if status:
            statement = statement.where(Lead.status == status)
        if assigned_to:
            statement = statement.where(Lead.assigned_to == assigned_to)
        return list(self.session.scalars(statement).all())

    def change_stage(self, lead_id: int, stage: str) -> Lead:
        """Change a lead stage."""
        normalized_stage = self._validate_choice(stage, LEAD_STAGES, "stage")
        lead = self.lead_repository.update(lead_id, stage=normalized_stage)
        if lead is None:
            raise NotFoundError(f"Lead {lead_id} was not found.")

        self.activity_service.create_activity(
            lead_id=lead_id,
            activity_type="status_changed",
            channel="system",
            note=f"Stage changed to {normalized_stage}.",
        )
        logger.info("Changed lead id=%s stage=%s", lead_id, normalized_stage)
        return lead

    def change_status(self, lead_id: int, status: str) -> Lead:
        """Change a lead status."""
        normalized_status = self._validate_choice(status, LEAD_STATUSES, "status")
        lead = self.lead_repository.update(lead_id, status=normalized_status)
        if lead is None:
            raise NotFoundError(f"Lead {lead_id} was not found.")

        activity_type = "meeting_booked" if normalized_status == "meeting_booked" else "status_changed"
        self.activity_service.create_activity(
            lead_id=lead_id,
            activity_type=activity_type,
            channel="system",
            note=f"Status changed to {normalized_status}.",
        )
        logger.info("Changed lead id=%s status=%s", lead_id, normalized_status)
        return lead

    def assign_lead(self, lead_id: int, assigned_to: str | None) -> Lead:
        """Assign a lead to an owner identifier."""
        normalized_owner = self._clean_optional(assigned_to)
        lead = self.lead_repository.update(lead_id, assigned_to=normalized_owner)
        if lead is None:
            raise NotFoundError(f"Lead {lead_id} was not found.")
        logger.info("Assigned lead id=%s to=%s", lead_id, normalized_owner)
        return lead

    def mark_contacted(
        self,
        lead_id: int,
        *,
        channel: str | None = None,
        contacted_at: datetime | None = None,
    ) -> Lead:
        """Mark a lead as contacted and update contact timestamp."""
        timestamp = contacted_at or datetime.utcnow()
        lead = self.lead_repository.update(
            lead_id,
            status="contacted",
            stage="engaged",
            last_contacted_at=timestamp,
        )
        if lead is None:
            raise NotFoundError(f"Lead {lead_id} was not found.")

        self.activity_service.create_activity(
            lead_id=lead_id,
            activity_type="status_changed",
            channel=channel or "system",
            note="Lead marked as contacted.",
        )
        logger.info("Marked lead id=%s contacted_at=%s", lead_id, timestamp.isoformat())
        return lead

    def mark_followup(
        self,
        lead_id: int,
        *,
        channel: str | None = None,
        followup_at: datetime | None = None,
    ) -> Lead:
        """Mark a lead as needing follow-up and update follow-up timestamp."""
        timestamp = followup_at or datetime.utcnow()
        lead = self.lead_repository.update(
            lead_id,
            stage="follow_up_needed",
            status="no_response",
            last_followup_at=timestamp,
        )
        if lead is None:
            raise NotFoundError(f"Lead {lead_id} was not found.")

        self.activity_service.create_activity(
            lead_id=lead_id,
            activity_type="followup_created",
            channel=channel or "system",
            note="Lead marked for follow-up.",
        )
        logger.info("Marked lead id=%s followup_at=%s", lead_id, timestamp.isoformat())
        return lead

    def _normalize_lead_payload(self, data: dict[str, Any], *, require_required_fields: bool) -> dict[str, Any]:
        """Normalize and validate lead payload fields."""
        payload: dict[str, Any] = {}
        required = {"first_name", "source"} if require_required_fields else set()

        for field in required:
            if not self._clean_optional(data.get(field)):
                raise ValidationError(f"{field} is required.")

        text_fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "company",
            "source",
            "stage",
            "status",
            "priority",
            "notes",
            "assigned_to",
            "external_source_id",
            "campaign_name",
        ]
        for field in text_fields:
            if field in data:
                payload[field] = self._clean_optional(data.get(field))

        if "email" in payload and payload["email"]:
            payload["email"] = self._normalize_email(payload["email"])

        if "stage" in payload and payload["stage"]:
            payload["stage"] = self._validate_choice(payload["stage"], LEAD_STAGES, "stage")
        elif require_required_fields:
            payload["stage"] = "new"

        if "status" in payload and payload["status"]:
            payload["status"] = self._validate_choice(payload["status"], LEAD_STATUSES, "status")
        elif require_required_fields:
            payload["status"] = "new"

        if "priority" in payload and payload["priority"]:
            payload["priority"] = self._validate_choice(payload["priority"], LEAD_PRIORITIES, "priority")
        elif require_required_fields:
            payload["priority"] = "normal"

        for datetime_field in [
            "last_contacted_at",
            "last_followup_at",
            "converted_at",
            "lost_at",
        ]:
            if datetime_field in data:
                payload[datetime_field] = data[datetime_field]

        return payload

    def _ensure_email_available(self, email: str | None, *, exclude_lead_id: int | None = None) -> None:
        """Prevent duplicate leads by email."""
        if not email:
            return
        statement = select(Lead).where(Lead.email == self._normalize_email(email))
        if exclude_lead_id is not None:
            statement = statement.where(Lead.id != exclude_lead_id)
        existing = self.session.scalars(statement).first()
        if existing:
            raise DuplicateLeadError(f"Lead with email {email} already exists.")

    def _normalize_email(self, email: str) -> str:
        """Normalize and validate an email address."""
        normalized = str(email or "").strip().lower()
        if not EMAIL_PATTERN.match(normalized):
            raise ValidationError(f"Invalid email address: {email}")
        return normalized

    @staticmethod
    def _validate_choice(value: str, allowed_values: set[str], field_name: str) -> str:
        """Validate a string against an allowed value set."""
        normalized = str(value or "").strip().lower()
        if normalized not in allowed_values:
            allowed = ", ".join(sorted(allowed_values))
            raise ValidationError(f"{field_name} must be one of: {allowed}.")
        return normalized

    @staticmethod
    def _clean_optional(value: Any) -> str | None:
        """Return stripped text or None."""
        if value is None:
            return None
        cleaned = str(value).strip()
        return cleaned or None

    # TODO: Move duplicate policy into configurable lead matching rules.
