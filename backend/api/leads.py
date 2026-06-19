"""Lead REST API."""

import logging
from typing import Any

from flask import Blueprint, jsonify, request

from analytics.journey import LeadJourneyService
from api.serializers import serialize_activity, serialize_lead
from crm_core.services import ActivityService, LeadService, ValidationError

logger = logging.getLogger(__name__)

leads_bp = Blueprint("leads_api", __name__, url_prefix="/api/leads")


def _json_payload() -> dict[str, Any]:
    """Return a JSON object payload or raise a validation error."""
    payload = request.get_json(silent=True)
    if payload is None:
        return {}
    if not isinstance(payload, dict):
        raise ValidationError("JSON payload must be an object.")
    return payload


@leads_bp.get("")
def list_leads():
    """Return leads."""
    service = LeadService()
    leads = service.list_leads(
        limit=request.args.get("limit", default=100, type=int) or 100,
        offset=request.args.get("offset", default=0, type=int) or 0,
        source=request.args.get("source"),
        stage=request.args.get("stage"),
        status=request.args.get("status"),
        assigned_to=request.args.get("assigned_to"),
    )
    return jsonify({"leads": [serialize_lead(lead) for lead in leads]}), 200


@leads_bp.get("/<int:lead_id>")
def get_lead(lead_id: int):
    """Return one lead."""
    lead = LeadService().get_lead(lead_id)
    return jsonify({"lead": serialize_lead(lead)}), 200


@leads_bp.post("")
def create_lead():
    """Create one lead."""
    lead = LeadService().create_lead(**_json_payload())
    logger.info("API created lead id=%s", lead.id)
    return jsonify({"lead": serialize_lead(lead)}), 201


@leads_bp.put("/<int:lead_id>")
def update_lead(lead_id: int):
    """Update one lead."""
    lead = LeadService().update_lead(lead_id, **_json_payload())
    return jsonify({"lead": serialize_lead(lead)}), 200


@leads_bp.patch("/<int:lead_id>/status")
def change_lead_status(lead_id: int):
    """Change a lead status."""
    payload = _json_payload()
    status = payload.get("status")
    if not status:
        raise ValidationError("status is required.")
    lead = LeadService().change_status(lead_id, status)
    return jsonify({"lead": serialize_lead(lead)}), 200


@leads_bp.patch("/<int:lead_id>/stage")
def change_lead_stage(lead_id: int):
    """Change a lead stage."""
    payload = _json_payload()
    stage = payload.get("stage")
    if not stage:
        raise ValidationError("stage is required.")
    lead = LeadService().change_stage(lead_id, stage)
    return jsonify({"lead": serialize_lead(lead)}), 200


@leads_bp.get("/<int:lead_id>/timeline")
def get_lead_timeline(lead_id: int):
    """Return one lead timeline."""
    activities = ActivityService().get_lead_timeline(
        lead_id,
        limit=request.args.get("limit", default=100, type=int) or 100,
        offset=request.args.get("offset", default=0, type=int) or 0,
    )
    return jsonify({"activities": [serialize_activity(activity) for activity in activities]}), 200


@leads_bp.get("/<int:lead_id>/journey")
def get_lead_journey(lead_id: int):
    """Return the canonical journey for one lead."""
    journey = LeadJourneyService().get_lead_journey(lead_id)
    return jsonify({"journey": journey.to_dict()}), 200


@leads_bp.get("/<int:lead_id>/stage-progress")
def get_lead_stage_progress(lead_id: int):
    """Return current lifecycle stage progress for one lead."""
    progress = LeadJourneyService().get_stage_progress(lead_id)
    return jsonify({"stage_progress": progress.to_dict()}), 200
