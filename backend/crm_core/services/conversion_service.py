"""Lead conversion service."""

from __future__ import annotations

import logging
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from crm_core.repositories.customer_repository import CustomerRepository
from crm_core.repositories.lead_repository import LeadRepository
from crm_core.services.activity_service import ActivityService
from crm_core.services.exceptions import ConversionError, NotFoundError
from database.models import Customer

logger = logging.getLogger(__name__)


class ConversionService:
    """Business service for converting leads into customers."""

    def __init__(
        self,
        lead_repository: LeadRepository | None = None,
        customer_repository: CustomerRepository | None = None,
        activity_service: ActivityService | None = None,
        session: Session | None = None,
    ) -> None:
        """Create a conversion service with injectable dependencies."""
        self.lead_repository = lead_repository or LeadRepository(session=session)
        self.session = self.lead_repository.session
        self.customer_repository = customer_repository or CustomerRepository(session=self.session)
        self.activity_service = activity_service or ActivityService(session=self.session)

    def convert_lead_to_customer(self, lead_id: int, *, converted_at: datetime | None = None) -> Customer:
        """Convert a lead into a customer and record the conversion activity."""
        lead = self.lead_repository.get_by_id(lead_id)
        if lead is None:
            raise NotFoundError(f"Lead {lead_id} was not found.")

        existing_customer = self.session.scalars(select(Customer).where(Customer.lead_id == lead_id)).first()
        if existing_customer:
            raise ConversionError(f"Lead {lead_id} is already converted to customer {existing_customer.id}.")

        timestamp = converted_at or datetime.utcnow()
        full_name = " ".join(part for part in [lead.first_name, lead.last_name] if part).strip()
        customer = self.customer_repository.create(
            lead_id=lead.id,
            name=full_name or lead.email or f"Lead {lead.id}",
            email=lead.email,
            phone=lead.phone,
            status="active",
        )
        updated = self.lead_repository.update(
            lead.id,
            stage="converted",
            status="converted",
            converted_at=timestamp,
            lost_at=None,
        )
        if updated is None:
            raise ConversionError(f"Lead {lead_id} could not be updated after customer creation.")

        self.activity_service.create_activity(
            lead_id=lead.id,
            activity_type="converted",
            channel="system",
            note=f"Lead converted to customer {customer.id}.",
        )
        logger.info("Converted lead id=%s to customer id=%s", lead.id, customer.id)
        return customer

    # TODO: Wrap conversion in an explicit unit-of-work if repository transaction policy changes.
