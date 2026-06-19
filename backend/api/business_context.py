"""Business context REST API."""

from typing import Any

from flask import Blueprint, jsonify, request

from api.serializers import serialize_business_context
from crm_core.services import BusinessContextService, ValidationError

business_context_bp = Blueprint("business_context_api", __name__, url_prefix="/api/business-context")


def _json_payload() -> dict[str, Any]:
    """Return a JSON object payload or raise a validation error."""
    payload = request.get_json(silent=True)
    if payload is None:
        return {}
    if not isinstance(payload, dict):
        raise ValidationError("JSON payload must be an object.")
    return payload


@business_context_bp.get("")
def get_business_context():
    """Return the most recently updated business context."""
    context = BusinessContextService().get_context()
    return jsonify({"business_context": serialize_business_context(context)}), 200


@business_context_bp.post("")
def create_business_context():
    """Create a business context."""
    context = BusinessContextService().create_context(**_json_payload())
    return jsonify({"business_context": serialize_business_context(context)}), 201


@business_context_bp.put("")
def update_business_context():
    """Update the most recently updated business context."""
    service = BusinessContextService()
    existing = service.get_context()
    context = service.update_context(existing.id, **_json_payload())
    return jsonify({"business_context": serialize_business_context(context)}), 200

