"""Validate LeadFlow analytics metrics."""

from __future__ import annotations

from _validation import app_context, print_result, run_validation


def _check() -> list[str]:
    from analytics import DashboardService, MetricsService

    with app_context():
        dashboard = DashboardService().get_dashboard_metrics()
        conversion = MetricsService().conversion_metrics()
        prediction = MetricsService().prediction_metrics()
        dashboard_payload = dashboard.to_dict()
        conversion_payload = conversion.to_dict()
        prediction_payload = prediction.to_dict()
        for key in ("total_leads", "conversion_rate", "lead_source_breakdown"):
            if key not in dashboard_payload:
                raise AssertionError(f"Dashboard metrics missing {key}.")
        for key in ("converted_leads", "lost_leads", "prediction_distribution"):
            if key not in conversion_payload:
                raise AssertionError(f"Conversion metrics missing {key}.")
        for key in ("total_predictions", "average_score", "high_probability"):
            if key not in prediction_payload:
                raise AssertionError(f"Prediction metrics missing {key}.")
        return [
            "Dashboard metrics loaded.",
            "Conversion metrics loaded.",
            "Prediction metrics loaded.",
        ]


def run_check():
    return run_validation("Analytics", _check)


if __name__ == "__main__":
    print_result(run_check())

