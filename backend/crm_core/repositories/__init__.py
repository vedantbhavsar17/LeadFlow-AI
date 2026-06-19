"""CRM core repository exports."""

from crm_core.repositories.activity_repository import ActivityRepository
from crm_core.repositories.base_repository import BaseRepository
from crm_core.repositories.business_context_repository import BusinessContextRepository
from crm_core.repositories.customer_repository import CustomerRepository
from crm_core.repositories.followup_repository import FollowupRepository
from crm_core.repositories.lead_repository import LeadRepository
from crm_core.repositories.raw_lead_event_repository import RawLeadEventRepository

__all__ = [
    "ActivityRepository",
    "BaseRepository",
    "BusinessContextRepository",
    "CustomerRepository",
    "FollowupRepository",
    "LeadRepository",
    "RawLeadEventRepository",
]
