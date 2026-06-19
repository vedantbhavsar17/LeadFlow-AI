"""JSON serializers for REST API responses."""

from datetime import datetime
from typing import Any

from database.models import BusinessContext, Customer, Lead, LeadActivity, RawLeadEvent


def serialize_datetime(value: datetime | None) -> str | None:
    """Return an ISO formatted datetime value."""
    return value.isoformat() if value else None


def serialize_lead(lead: Lead) -> dict[str, Any]:
    """Serialize a Lead model."""
    return {
        "id": lead.id,
        "first_name": lead.first_name,
        "last_name": lead.last_name,
        "email": lead.email,
        "phone": lead.phone,
        "company": lead.company,
        "source": lead.source,
        "stage": lead.stage,
        "status": lead.status,
        "priority": lead.priority,
        "notes": lead.notes,
        "assigned_to": lead.assigned_to,
        "external_source_id": lead.external_source_id,
        "campaign_name": lead.campaign_name,
        "last_contacted_at": serialize_datetime(lead.last_contacted_at),
        "last_followup_at": serialize_datetime(lead.last_followup_at),
        "converted_at": serialize_datetime(lead.converted_at),
        "lost_at": serialize_datetime(lead.lost_at),
        "created_at": serialize_datetime(lead.created_at),
        "updated_at": serialize_datetime(lead.updated_at),
    }


def serialize_activity(activity: LeadActivity) -> dict[str, Any]:
    """Serialize a LeadActivity model."""
    return {
        "id": activity.id,
        "lead_id": activity.lead_id,
        "activity_type": activity.activity_type,
        "channel": activity.channel,
        "note": activity.note,
        "created_at": serialize_datetime(activity.created_at),
        "updated_at": serialize_datetime(activity.updated_at),
    }


def serialize_customer(customer: Customer) -> dict[str, Any]:
    """Serialize a Customer model."""
    return {
        "id": customer.id,
        "lead_id": customer.lead_id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "status": customer.status,
        "created_at": serialize_datetime(customer.created_at),
        "updated_at": serialize_datetime(customer.updated_at),
    }


def serialize_business_context(context: BusinessContext) -> dict[str, Any]:
    """Serialize a BusinessContext model."""
    return {
        "id": context.id,
        "company_name": context.company_name,
        "industry": context.industry,
        "services": context.services,
        "ideal_customer_profile": context.ideal_customer_profile,
        "target_market": context.target_market,
        "common_pain_points": context.common_pain_points,
        "competitors": context.competitors,
        "brand_tone": context.brand_tone,
        "sales_goals": context.sales_goals,
        "created_at": serialize_datetime(context.created_at),
        "updated_at": serialize_datetime(context.updated_at),
    }


def serialize_raw_event(raw_event: RawLeadEvent) -> dict[str, Any]:
    """Serialize a RawLeadEvent model."""
    return {
        "id": raw_event.id,
        "source": raw_event.source,
        "external_id": raw_event.external_id,
        "raw_payload": raw_event.raw_payload,
        "normalized_payload": raw_event.normalized_payload,
        "is_processed": raw_event.is_processed,
        "processed_at": serialize_datetime(raw_event.processed_at),
        "created_at": serialize_datetime(raw_event.created_at),
        "updated_at": serialize_datetime(raw_event.updated_at),
    }

