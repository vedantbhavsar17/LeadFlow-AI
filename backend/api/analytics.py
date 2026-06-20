"""Analytics REST API."""

import logging

from flask import Blueprint, jsonify

from analytics import DashboardService, ReportingService

logger = logging.getLogger(__name__)

analytics_bp = Blueprint("analytics_api", __name__, url_prefix="/api/analytics")


@analytics_bp.get("/dashboard")
def get_dashboard_metrics():
    """Return dashboard analytics metrics."""
    metrics = DashboardService().get_dashboard_metrics()
    return jsonify({"dashboard": metrics.to_dict()}), 200


@analytics_bp.get("/lead-sources")
def get_lead_sources():
    """Return lead source breakdown."""
    return jsonify({"lead_sources": ReportingService().lead_sources()}), 200


@analytics_bp.get("/conversions")
def get_conversions():
    """Return conversion analytics."""
    metrics = ReportingService().conversions()
    return jsonify({"conversions": metrics.to_dict()}), 200


@analytics_bp.get("/followups")
def get_followups():
    """Return follow-up analytics."""
    metrics = ReportingService().followups()
    return jsonify({"followups": metrics.to_dict()}), 200


@analytics_bp.get("/predictions")
def get_predictions():
    """Return conversion prediction analytics."""
    metrics = ReportingService().predictions()
    return jsonify({"predictions": metrics.to_dict()}), 200

