"""Validate core LeadFlow REST API endpoints."""

from __future__ import annotations

import time

from _validation import app_context, cleanup_records, print_result, run_validation


ENDPOINTS = [
    "/api/health",
    "/api/leads",
    "/api/customers",
    "/api/business-context",
    "/api/analytics/dashboard",
]


def _check() -> list[str]:
    from crm_core.services import BusinessContextService

    details: list[str] = []
    context = None
    with app_context() as app:
        try:
            context = BusinessContextService().create_context(
                company_name="LeadFlow Validation",
                industry="Validation",
                services="Automated readiness checks",
            )
            client = app.test_client()
            for endpoint in ENDPOINTS:
                started = time.perf_counter()
                response = client.get(endpoint)
                elapsed_ms = (time.perf_counter() - started) * 1000
                details.append(f"GET {endpoint} -> {response.status_code} in {elapsed_ms:.2f} ms")
                if response.status_code < 200 or response.status_code >= 300:
                    body = response.get_data(as_text=True)
                    raise AssertionError(f"GET {endpoint} returned {response.status_code}: {body}")
        finally:
            cleanup_records(context)
    return details


def run_check():
    return run_validation("API", _check)


if __name__ == "__main__":
    print_result(run_check())

