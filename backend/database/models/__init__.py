"""Database model registry.

Import model classes here so Flask-Migrate can discover SQLAlchemy metadata.
No API, AI, or business workflow behavior belongs in this package.
"""

from database.models.ai_insight import AIInsight
from database.models.business_context import BusinessContext
from database.models.customer import Customer
from database.models.followup_task import FollowupTask
from database.models.lead import Lead
from database.models.lead_activity import LeadActivity
from database.models.raw_lead_event import RawLeadEvent

__all__ = [
    "AIInsight",
    "BusinessContext",
    "Customer",
    "FollowupTask",
    "Lead",
    "LeadActivity",
    "RawLeadEvent",
]
