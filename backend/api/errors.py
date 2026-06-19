"""REST API error handling helpers."""

from __future__ import annotations

import logging
from typing import Any

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from crm_core.services import CRMCoreError, ConversionError, DuplicateLeadError, NotFoundError, ValidationError

logger = logging.getLogger(__name__)


def error_response(message: str, status_code: int, *, details: Any | None = None):
    """Return a consistent JSON error response."""
    payload: dict[str, Any] = {"error": message}
    if details is not None:
        payload["details"] = details
    return jsonify(payload), status_code


def register_error_handlers(app: Flask) -> None:
    """Register REST API error handlers."""

    @app.errorhandler(ValidationError)
    def handle_validation_error(exc: ValidationError):
        return error_response(str(exc), 400)

    @app.errorhandler(DuplicateLeadError)
    def handle_duplicate_lead_error(exc: DuplicateLeadError):
        return error_response(str(exc), 409)

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(exc: NotFoundError):
        return error_response(str(exc), 404)

    @app.errorhandler(ConversionError)
    def handle_conversion_error(exc: ConversionError):
        return error_response(str(exc), 409)

    @app.errorhandler(CRMCoreError)
    def handle_crm_core_error(exc: CRMCoreError):
        return error_response(str(exc), 400)

    @app.errorhandler(HTTPException)
    def handle_http_error(exc: HTTPException):
        return error_response(exc.description, exc.code or 500)

    @app.errorhandler(Exception)
    def handle_unexpected_error(exc: Exception):
        logger.exception("Unhandled API error")
        return error_response("Internal server error.", 500)

