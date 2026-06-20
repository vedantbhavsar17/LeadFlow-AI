"""Health check API."""

from flask import Blueprint, jsonify

health_bp = Blueprint("health_api", __name__, url_prefix="/api")


@health_bp.get("/health")
def get_health():
    """Return service health."""
    return jsonify({"status": "healthy"}), 200

