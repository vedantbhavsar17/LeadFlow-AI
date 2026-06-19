"""Lead ingestion REST API."""

from typing import Any

from flask import Blueprint, jsonify, request

from api.serializers import serialize_lead, serialize_raw_event
from crm_core.services import ValidationError
from lead_ingestion.services import IngestionOrchestrator

ingestion_bp = Blueprint("ingestion_api", __name__, url_prefix="/api/import")


def _json_payload() -> dict[str, Any]:
    """Return a JSON object payload or raise a validation error."""
    payload = request.get_json(silent=True)
    if payload is None:
        return {}
    if not isinstance(payload, dict):
        raise ValidationError("JSON payload must be an object.")
    return payload


@ingestion_bp.post("/manual")
def import_manual_lead():
    """Import one manually submitted lead."""
    payload = _json_payload()
    lead, raw_event = IngestionOrchestrator().create_manual_lead(
        name=payload.get("name", ""),
        email=payload.get("email"),
        phone=payload.get("phone"),
        company=payload.get("company"),
        notes=payload.get("notes"),
    )
    return jsonify({"lead": serialize_lead(lead), "raw_event": serialize_raw_event(raw_event)}), 201


@ingestion_bp.post("/csv")
def import_csv_leads():
    """Import leads from CSV text.

    Accepts either `text/csv` raw body content or JSON with a `csv` field.
    """
    if request.mimetype == "text/csv":
        csv_content = request.get_data(as_text=True)
    else:
        payload = _json_payload()
        csv_content = payload.get("csv") or payload.get("content")

    if not csv_content:
        raise ValidationError("CSV content is required.")

    result = IngestionOrchestrator().import_csv(str(csv_content))
    return jsonify(
        {
            "success_count": result.success_count,
            "failed_count": result.failed_count,
            "duplicate_count": result.duplicate_count,
            "raw_event_count": result.raw_event_count,
            "errors": result.errors,
        }
    ), 200
