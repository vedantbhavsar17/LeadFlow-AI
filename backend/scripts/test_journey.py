"""Validate Lead Journey, Stage Progress, and Journey Summary generation."""

from __future__ import annotations

from _validation import app_context, cleanup_records, print_result, run_validation


def _check() -> list[str]:
    from analytics.journey import LeadJourneyService
    from crm_core.repositories import AIInsightRepository
    from crm_core.services import LeadService

    lead = None
    with app_context():
        try:
            lead = LeadService().create_lead(
                first_name="Validation",
                last_name="Journey",
                email="validation.journey@leadflow.test",
                source="validation",
            )
            LeadService().change_stage(lead.id, "qualified")
            AIInsightRepository().create(
                lead_id=lead.id,
                insight_type="qualification",
                provider="validation",
                model="validation",
                output={"score": 82, "category": "hot", "recommended_action": "schedule_demo"},
                confidence=0.82,
            )
            service = LeadJourneyService()
            journey = service.get_lead_journey(lead.id)
            progress = service.get_stage_progress(lead.id)
            summary = journey.to_dict()
            if not journey.events:
                raise AssertionError("Lead Journey did not include events.")
            if progress.current_stage != "qualified":
                raise AssertionError(f"Expected stage progress to be qualified, got {progress.current_stage!r}.")
            if summary["lead_id"] != lead.id or "events" not in summary or "stage_progress" not in summary:
                raise AssertionError("Journey Summary was missing expected fields.")
            return [
                f"Lead Journey generated with {len(journey.events)} event(s).",
                f"Stage Progress generated at {progress.progress_percent}%.",
                "Journey Summary generated.",
            ]
        finally:
            cleanup_records(lead)


def run_check():
    return run_validation("Journey", _check)


if __name__ == "__main__":
    print_result(run_check())

