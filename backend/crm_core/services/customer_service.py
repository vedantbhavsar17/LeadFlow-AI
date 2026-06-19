"""Customer business service."""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from crm_core.repositories.customer_repository import CustomerRepository
from crm_core.repositories.lead_repository import LeadRepository
from crm_core.services.exceptions import ConversionError, NotFoundError, ValidationError
from database.models import Customer

logger = logging.getLogger(__name__)


class CustomerService:
    """Business service for customer records."""

    def __init__(
        self,
        customer_repository: CustomerRepository | None = None,
        lead_repository: LeadRepository | None = None,
        session: Session | None = None,
    ) -> None:
        """Create a customer service with injectable repositories."""
        self.customer_repository = customer_repository or CustomerRepository(session=session)
        self.session = self.customer_repository.session
        self.lead_repository = lead_repository or LeadRepository(session=self.session)

    def create_customer(self, *, lead_id: int, name: str, email: str | None = None, phone: str | None = None, status: str = "active") -> Customer:
        """Create a customer linked to an existing lead."""
        if not self.lead_repository.get_by_id(lead_id):
            raise NotFoundError(f"Lead {lead_id} was not found.")
        if not str(name or "").strip():
            raise ValidationError("Customer name is required.")
        existing_customer = self.session.scalars(select(Customer).where(Customer.lead_id == lead_id)).first()
        if existing_customer:
            raise ConversionError(f"Lead {lead_id} already has customer {existing_customer.id}.")

        customer = self.customer_repository.create(
            lead_id=lead_id,
            name=str(name).strip(),
            email=self._clean_optional(email),
            phone=self._clean_optional(phone),
            status=str(status or "active").strip().lower(),
        )
        logger.info("Created customer id=%s lead_id=%s", customer.id, lead_id)
        return customer

    def get_customer(self, customer_id: int) -> Customer:
        """Return one customer by id."""
        customer = self.customer_repository.get_by_id(customer_id)
        if customer is None:
            raise NotFoundError(f"Customer {customer_id} was not found.")
        return customer

    def list_customers(self, *, limit: int = 100, offset: int = 0) -> list[Customer]:
        """Return customers with pagination."""
        return self.customer_repository.list(limit=limit, offset=offset)

    @staticmethod
    def _clean_optional(value: Any) -> str | None:
        """Return stripped text or None."""
        if value is None:
            return None
        cleaned = str(value).strip()
        return cleaned or None

    # TODO: Add customer status constants after lifecycle contracts settle.
