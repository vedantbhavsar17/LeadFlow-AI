"""REST API blueprint registration."""

from flask import Flask

from api.analytics import analytics_bp
from api.business_context import business_context_bp
from api.customers import customers_bp
from api.errors import register_error_handlers
from api.health import health_bp
from api.ingestion import ingestion_bp
from api.leads import leads_bp


def register_api(app: Flask) -> None:
    """Register LeadFlow REST API blueprints and error handlers."""
    register_error_handlers(app)
    app.register_blueprint(health_bp)
    app.register_blueprint(leads_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(business_context_bp)
    app.register_blueprint(ingestion_bp)
    app.register_blueprint(analytics_bp)

    # TODO: Register AI, outreach, and follow-up APIs in later phases.


__all__ = ["register_api"]
