"""Customer REST API."""

from typing import Any

from flask import Blueprint, jsonify, request

from api.serializers import serialize_customer
from crm_core.services import ConversionService, CustomerService, ValidationError

customers_bp = Blueprint("customers_api", __name__, url_prefix="/api")


def _json_payload() -> dict[str, Any]:
    """Return a JSON object payload or raise a validation error."""
    payload = request.get_json(silent=True)
    if payload is None:
        return {}
    if not isinstance(payload, dict):
        raise ValidationError("JSON payload must be an object.")
    return payload


@customers_bp.get("/customers")
def list_customers():
    """Return customers."""
    customers = CustomerService().list_customers(
        limit=request.args.get("limit", default=100, type=int) or 100,
        offset=request.args.get("offset", default=0, type=int) or 0,
    )
    return jsonify({"customers": [serialize_customer(customer) for customer in customers]}), 200


@customers_bp.get("/customers/<int:customer_id>")
def get_customer(customer_id: int):
    """Return one customer."""
    customer = CustomerService().get_customer(customer_id)
    return jsonify({"customer": serialize_customer(customer)}), 200


@customers_bp.post("/customers")
def create_customer():
    """Create one customer."""
    customer = CustomerService().create_customer(**_json_payload())
    return jsonify({"customer": serialize_customer(customer)}), 201


@customers_bp.post("/leads/<int:lead_id>/convert")
def convert_lead(lead_id: int):
    """Convert one lead to a customer."""
    customer = ConversionService().convert_lead_to_customer(lead_id)
    return jsonify({"customer": serialize_customer(customer)}), 201

