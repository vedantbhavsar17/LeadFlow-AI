"""Sample data seeder for the Phase 4 data layer.

Run from `leadflow/backend` after applying migrations:

    python -m database.seeders.sample_data

The seeder is intentionally conservative: it inserts sample rows only when no
Lead records exist and does not delete existing data.
"""

from datetime import datetime, timedelta

from sqlalchemy import inspect

from app import create_app
from database.extensions import db
from database.models import (
    AIInsight,
    BusinessContext,
    Customer,
    FollowupTask,
    Lead,
    LeadActivity,
    RawLeadEvent,
)


def _tables_exist() -> bool:
    """Return True when the Phase 4 tables are present."""
    inspector = inspect(db.engine)
    required_tables = {
        "ai_insights",
        "business_contexts",
        "customers",
        "followup_tasks",
        "lead_activities",
        "leads",
        "raw_lead_events",
    }
    return required_tables.issubset(set(inspector.get_table_names()))


def seed_sample_data() -> None:
    """Insert a minimal sample dataset for development verification."""
    if not _tables_exist():
        raise RuntimeError("Phase 4 tables are missing. Run database migrations before seeding.")

    if Lead.query.first():
        print("Sample data skipped because leads already exist.")
        return

    business_context = BusinessContext(
        company_name="LeadFlow Demo Co",
        industry="B2B Services",
        services="Lead qualification, outreach planning, follow-up automation",
        ideal_customer_profile="Small teams that receive inbound leads and need faster follow-up",
        target_market="Lead-driven agencies, consultants, SaaS teams, and service businesses",
        common_pain_points="Slow response time, poor lead prioritization, inconsistent follow-up",
        competitors="Traditional CRMs and manual spreadsheets",
        brand_tone="Helpful, clear, practical",
        sales_goals="Increase meeting bookings and improve lead-to-customer conversion",
    )

    raw_event = RawLeadEvent(
        source="manual",
        external_id="sample-manual-001",
        raw_payload={
            "first_name": "Avery",
            "last_name": "Shah",
            "email": "avery@example.com",
            "source": "manual",
        },
        normalized_payload={
            "first_name": "Avery",
            "last_name": "Shah",
            "email": "avery@example.com",
            "source": "manual",
            "stage": "qualified",
        },
        is_processed=True,
        processed_at=datetime.utcnow(),
    )

    lead = Lead(
        first_name="Avery",
        last_name="Shah",
        email="avery@example.com",
        phone="+1-555-0100",
        company="Northstar Growth",
        source="manual",
        stage="qualified",
        status="interested",
        priority="high",
        notes="Sample lead for validating the Phase 4 data layer.",
        assigned_to="demo-owner",
        external_source_id="sample-manual-001",
        campaign_name="Phase 4 Sample",
        last_contacted_at=datetime.utcnow(),
    )

    db.session.add_all([business_context, raw_event, lead])
    db.session.flush()

    activity = LeadActivity(
        lead_id=lead.id,
        activity_type="status_changed",
        channel="system",
        note="Sample lead marked as qualified.",
    )
    followup = FollowupTask(
        lead_id=lead.id,
        channel="email",
        reason="Send first personalized follow-up.",
        due_at=datetime.utcnow() + timedelta(days=1),
        status="pending",
    )
    ai_insight = AIInsight(
        lead_id=lead.id,
        insight_type="qualification",
        provider="nim",
        model="placeholder",
        output={"summary": "Sample qualification insight placeholder."},
        confidence=0.8,
    )
    customer = Customer(
        lead_id=lead.id,
        name="Avery Shah",
        email="avery@example.com",
        phone="+1-555-0100",
        status="prospective",
    )

    db.session.add_all([activity, followup, ai_insight, customer])
    db.session.commit()
    print("Sample data inserted.")


def main() -> None:
    """Run the sample data seeder inside the Flask app context."""
    app = create_app()
    with app.app_context():
        seed_sample_data()


if __name__ == "__main__":
    main()
