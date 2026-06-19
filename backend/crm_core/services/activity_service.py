"""Lead activity service."""

from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from crm_core.repositories.activity_repository import ActivityRepository
from crm_core.repositories.lead_repository import LeadRepository
from crm_core.services.exceptions import NotFoundError, ValidationError
from database.models import LeadActivity

logger = logging.getLogger(__name__)

ACTIVITY_TYPES = {
    "email_sent",
    "email_received",
    "lead_created",
    "status_changed",
    "followup_created",
    "meeting_booked",
    "converted",
}


class ActivityService:
    """Business service for recording lead timeline events."""

    def __init__(
        self,
        activity_repository: ActivityRepository | None = None,
        lead_repository: LeadRepository | None = None,
        session: Session | None = None,
    ) -> None:
        """Create an activity service with injectable repositories."""
        self.activity_repository = activity_repository or ActivityRepository(session=session)
        self.lead_repository = lead_repository or LeadRepository(session=self.activity_repository.session)
        self.session = self.activity_repository.session

    def create_activity(
        self,
        *,
        lead_id: int,
        activity_type: str,
        channel: str | None = None,
        note: str | None = None,
    ) -> LeadActivity:
        """Create one lead activity after validating lead ownership."""
        normalized_type = self._normalize_activity_type(activity_type)
        if not self.lead_repository.get_by_id(lead_id):
            raise NotFoundError(f"Lead {lead_id} was not found.")

        activity = self.activity_repository.create(
            lead_id=lead_id,
            activity_type=normalized_type,
            channel=self._clean_optional(channel),
            note=self._clean_optional(note),
        )
        logger.info("Created lead activity id=%s lead_id=%s type=%s", activity.id, lead_id, normalized_type)
        return activity

    def get_lead_timeline(self, lead_id: int, *, limit: int = 100, offset: int = 0) -> list[LeadActivity]:
        """Return activities for one lead ordered newest first."""
        if not self.lead_repository.get_by_id(lead_id):
            raise NotFoundError(f"Lead {lead_id} was not found.")

        statement = (
            select(LeadActivity)
            .where(LeadActivity.lead_id == lead_id)
            .order_by(LeadActivity.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.session.scalars(statement).all())

    def list_recent_activities(self, *, limit: int = 50, offset: int = 0) -> list[LeadActivity]:
        """Return recent activities across all leads."""
        statement = select(LeadActivity).order_by(LeadActivity.created_at.desc()).offset(offset).limit(limit)
        return list(self.session.scalars(statement).all())

    def _normalize_activity_type(self, activity_type: str) -> str:
        """Validate and normalize an activity type."""
        normalized = str(activity_type or "").strip().lower()
        if normalized not in ACTIVITY_TYPES:
            raise ValidationError(f"Unsupported activity type: {activity_type}")
        return normalized

    @staticmethod
    def _clean_optional(value: str | None) -> str | None:
        """Return stripped text or None."""
        if value is None:
            return None
        cleaned = str(value).strip()
        return cleaned or None

    # TODO: Add actor/user attribution when authentication exists.
