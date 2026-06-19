"""Tests for LeadFlow ingestion foundation."""

import pytest

from app import create_app
from database.extensions import db
import database.models
from database.models import Lead, LeadActivity, RawLeadEvent
from lead_ingestion.csv import CSVLeadParser
from lead_ingestion.services import IngestionOrchestrator


@pytest.fixture()
def app_context():
    """Create an in-memory database context for ingestion tests."""
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    ctx = app.app_context()
    ctx.push()
    db.create_all()
    try:
        yield app
    finally:
        db.session.remove()
        db.drop_all()
        ctx.pop()


def test_manual_ingestion_creates_raw_event_lead_and_activity(app_context):
    """Manual ingestion should persist the full raw-to-lead flow."""
    orchestrator = IngestionOrchestrator()

    lead, raw_event = orchestrator.create_manual_lead(
        name="Avery Shah",
        email="avery@example.com",
        phone="+1-555-0100",
        company="Northstar Growth",
        notes="Interested in faster follow-up.",
    )

    assert lead.id is not None
    assert lead.first_name == "Avery"
    assert lead.last_name == "Shah"
    assert raw_event.id is not None
    assert raw_event.source == "manual"
    assert RawLeadEvent.query.count() == 1
    assert Lead.query.count() == 1
    assert LeadActivity.query.count() == 1


def test_csv_parser_validates_duplicate_rows(app_context):
    """CSV parser should skip duplicate rows in the uploaded file."""
    csv_content = "name,email,phone,company\nAvery Shah,avery@example.com,123,Northstar\nAvery Again,AVERY@example.com,456,Northstar\n"
    result = CSVLeadParser().parse(csv_content)

    assert len(result.leads) == 1
    assert result.duplicate_count == 1
    assert result.errors == []


def test_csv_ingestion_imports_valid_rows_and_counts_duplicates(app_context):
    """CSV ingestion should create leads and report duplicates."""
    orchestrator = IngestionOrchestrator()
    csv_content = (
        "name,email,phone,company\n"
        "Avery Shah,avery@example.com,123,Northstar\n"
        "Blair Chen,blair@example.com,456,Atlas\n"
        "Avery Again,avery@example.com,789,Northstar\n"
    )

    result = orchestrator.import_csv(csv_content)

    assert result.success_count == 2
    assert result.failed_count == 0
    assert result.duplicate_count == 1
    assert Lead.query.count() == 2
    assert RawLeadEvent.query.count() == 2
    assert LeadActivity.query.count() == 2
