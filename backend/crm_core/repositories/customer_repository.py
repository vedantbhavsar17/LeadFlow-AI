"""Customer repository."""

from database.models import Customer

from crm_core.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    """Data access helper for Customer records."""

    model = Customer

    # TODO: Add lookup-by-lead helpers during conversion service implementation.
