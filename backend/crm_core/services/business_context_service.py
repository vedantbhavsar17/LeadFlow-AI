"""Business context service."""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from crm_core.repositories.business_context_repository import BusinessContextRepository
from crm_core.services.exceptions import NotFoundError, ValidationError
from database.models import BusinessContext

logger = logging.getLogger(__name__)

REQUIRED_CONTEXT_FIELDS = {"company_name", "industry"}


class BusinessContextService:
    """Business service for company-specific AI context data."""

    def __init__(
        self,
        business_context_repository: BusinessContextRepository | None = None,
        session: Session | None = None,
    ) -> None:
        """Create a business context service with injectable dependencies."""
        self.business_context_repository = business_context_repository or BusinessContextRepository(session=session)
        self.session = self.business_context_repository.session

    def create_context(self, **data: Any) -> BusinessContext:
        """Create a business context after validation."""
        payload = self._normalize_context_payload(data)
        self.validate_context(payload)
        context = self.business_context_repository.create(**payload)
        logger.info("Created business context id=%s company=%s", context.id, context.company_name)
        return context

    def update_context(self, context_id: int, **data: Any) -> BusinessContext:
        """Update a business context after validation."""
        existing = self.get_context(context_id)
        payload = self._normalize_context_payload(data)
        merged = {
            "company_name": existing.company_name,
            "industry": existing.industry,
            "services": existing.services,
            "ideal_customer_profile": existing.ideal_customer_profile,
            "target_market": existing.target_market,
            "common_pain_points": existing.common_pain_points,
            "competitors": existing.competitors,
            "brand_tone": existing.brand_tone,
            "sales_goals": existing.sales_goals,
            **payload,
        }
        self.validate_context(merged)
        updated = self.business_context_repository.update(context_id, **payload)
        if updated is None:
            raise NotFoundError(f"Business context {context_id} was not found.")
        logger.info("Updated business context id=%s", context_id)
        return updated

    def get_context(self, context_id: int | None = None) -> BusinessContext:
        """Return a business context by id, or the most recently updated context."""
        if context_id is not None:
            context = self.business_context_repository.get_by_id(context_id)
        else:
            statement = select(BusinessContext).order_by(BusinessContext.updated_at.desc()).limit(1)
            context = self.session.scalars(statement).first()

        if context is None:
            raise NotFoundError("Business context was not found.")
        return context

    def validate_context(self, data: dict[str, Any]) -> None:
        """Validate required business context fields."""
        missing = [field for field in sorted(REQUIRED_CONTEXT_FIELDS) if not self._clean_optional(data.get(field))]
        if missing:
            raise ValidationError(f"Missing business context fields: {', '.join(missing)}.")

    def _normalize_context_payload(self, data: dict[str, Any]) -> dict[str, str | None]:
        """Normalize context text fields."""
        allowed_fields = [
            "company_name",
            "industry",
            "services",
            "ideal_customer_profile",
            "target_market",
            "common_pain_points",
            "competitors",
            "brand_tone",
            "sales_goals",
        ]
        return {field: self._clean_optional(data.get(field)) for field in allowed_fields if field in data}

    @staticmethod
    def _clean_optional(value: Any) -> str | None:
        """Return stripped text or None."""
        if value is None:
            return None
        cleaned = str(value).strip()
        return cleaned or None

    # TODO: Add one-active-context policy when organization settings exist.
