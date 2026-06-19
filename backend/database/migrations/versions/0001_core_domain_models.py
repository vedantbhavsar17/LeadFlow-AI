"""create core domain models

Revision ID: 0001_core_domain_models
Revises:
Create Date: 2026-06-19 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "0001_core_domain_models"
down_revision = None
branch_labels = None
depends_on = None


def _base_columns():
    """Return columns shared by all BaseModel-backed tables."""
    return [
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    ]


def upgrade():
    op.create_table(
        "business_contexts",
        *_base_columns(),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("industry", sa.String(length=120), nullable=True),
        sa.Column("services", sa.Text(), nullable=True),
        sa.Column("ideal_customer_profile", sa.Text(), nullable=True),
        sa.Column("target_market", sa.Text(), nullable=True),
        sa.Column("common_pain_points", sa.Text(), nullable=True),
        sa.Column("competitors", sa.Text(), nullable=True),
        sa.Column("brand_tone", sa.String(length=120), nullable=True),
        sa.Column("sales_goals", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_business_contexts_company_name", "business_contexts", ["company_name"], unique=False)
    op.create_index("ix_business_contexts_industry", "business_contexts", ["industry"], unique=False)

    op.create_table(
        "leads",
        *_base_columns(),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("company", sa.String(length=255), nullable=True),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("stage", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("priority", sa.String(length=30), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("assigned_to", sa.String(length=120), nullable=True),
        sa.Column("external_source_id", sa.String(length=255), nullable=True),
        sa.Column("campaign_name", sa.String(length=255), nullable=True),
        sa.Column("last_contacted_at", sa.DateTime(), nullable=True),
        sa.Column("last_followup_at", sa.DateTime(), nullable=True),
        sa.Column("converted_at", sa.DateTime(), nullable=True),
        sa.Column("lost_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_leads_assigned_to", "leads", ["assigned_to"], unique=False)
    op.create_index("ix_leads_campaign_name", "leads", ["campaign_name"], unique=False)
    op.create_index("ix_leads_email", "leads", ["email"], unique=False)
    op.create_index("ix_leads_external_source", "leads", ["source", "external_source_id"], unique=False)
    op.create_index("ix_leads_external_source_id", "leads", ["external_source_id"], unique=False)
    op.create_index("ix_leads_phone", "leads", ["phone"], unique=False)
    op.create_index("ix_leads_priority", "leads", ["priority"], unique=False)
    op.create_index("ix_leads_source", "leads", ["source"], unique=False)
    op.create_index("ix_leads_source_stage_status", "leads", ["source", "stage", "status"], unique=False)
    op.create_index("ix_leads_stage", "leads", ["stage"], unique=False)
    op.create_index("ix_leads_status", "leads", ["status"], unique=False)

    op.create_table(
        "raw_lead_events",
        *_base_columns(),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.Column("normalized_payload", sa.JSON(), nullable=True),
        sa.Column("is_processed", sa.Boolean(), nullable=False),
        sa.Column("processed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_raw_lead_events_external_id", "raw_lead_events", ["external_id"], unique=False)
    op.create_index("ix_raw_lead_events_is_processed", "raw_lead_events", ["is_processed"], unique=False)
    op.create_index("ix_raw_lead_events_source", "raw_lead_events", ["source"], unique=False)
    op.create_index("ix_raw_lead_events_source_external", "raw_lead_events", ["source", "external_id"], unique=False)
    op.create_index("ix_raw_lead_events_source_processed", "raw_lead_events", ["source", "is_processed"], unique=False)

    op.create_table(
        "ai_insights",
        *_base_columns(),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("insight_type", sa.String(length=80), nullable=False),
        sa.Column("provider", sa.String(length=80), nullable=False),
        sa.Column("model", sa.String(length=160), nullable=True),
        sa.Column("output", sa.JSON(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_insights_insight_type", "ai_insights", ["insight_type"], unique=False)
    op.create_index("ix_ai_insights_lead_id", "ai_insights", ["lead_id"], unique=False)
    op.create_index("ix_ai_insights_lead_type", "ai_insights", ["lead_id", "insight_type"], unique=False)
    op.create_index("ix_ai_insights_provider", "ai_insights", ["provider"], unique=False)

    op.create_table(
        "customers",
        *_base_columns(),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("lead_id"),
    )
    op.create_index("ix_customers_email", "customers", ["email"], unique=False)
    op.create_index("ix_customers_phone", "customers", ["phone"], unique=False)
    op.create_index("ix_customers_status", "customers", ["status"], unique=False)

    op.create_table(
        "followup_tasks",
        *_base_columns(),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("channel", sa.String(length=50), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("due_at", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_followup_tasks_channel", "followup_tasks", ["channel"], unique=False)
    op.create_index("ix_followup_tasks_due_at", "followup_tasks", ["due_at"], unique=False)
    op.create_index("ix_followup_tasks_lead_id", "followup_tasks", ["lead_id"], unique=False)
    op.create_index("ix_followup_tasks_lead_status", "followup_tasks", ["lead_id", "status"], unique=False)
    op.create_index("ix_followup_tasks_status", "followup_tasks", ["status"], unique=False)
    op.create_index("ix_followup_tasks_status_due", "followup_tasks", ["status", "due_at"], unique=False)

    op.create_table(
        "lead_activities",
        *_base_columns(),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("activity_type", sa.String(length=80), nullable=False),
        sa.Column("channel", sa.String(length=50), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_lead_activities_activity_type", "lead_activities", ["activity_type"], unique=False)
    op.create_index("ix_lead_activities_channel", "lead_activities", ["channel"], unique=False)
    op.create_index("ix_lead_activities_lead_id", "lead_activities", ["lead_id"], unique=False)
    op.create_index("ix_lead_activities_lead_type", "lead_activities", ["lead_id", "activity_type"], unique=False)


def downgrade():
    op.drop_index("ix_lead_activities_lead_type", table_name="lead_activities")
    op.drop_index("ix_lead_activities_lead_id", table_name="lead_activities")
    op.drop_index("ix_lead_activities_channel", table_name="lead_activities")
    op.drop_index("ix_lead_activities_activity_type", table_name="lead_activities")
    op.drop_table("lead_activities")

    op.drop_index("ix_followup_tasks_status_due", table_name="followup_tasks")
    op.drop_index("ix_followup_tasks_status", table_name="followup_tasks")
    op.drop_index("ix_followup_tasks_lead_status", table_name="followup_tasks")
    op.drop_index("ix_followup_tasks_lead_id", table_name="followup_tasks")
    op.drop_index("ix_followup_tasks_due_at", table_name="followup_tasks")
    op.drop_index("ix_followup_tasks_channel", table_name="followup_tasks")
    op.drop_table("followup_tasks")

    op.drop_index("ix_customers_status", table_name="customers")
    op.drop_index("ix_customers_phone", table_name="customers")
    op.drop_index("ix_customers_email", table_name="customers")
    op.drop_table("customers")

    op.drop_index("ix_ai_insights_provider", table_name="ai_insights")
    op.drop_index("ix_ai_insights_lead_type", table_name="ai_insights")
    op.drop_index("ix_ai_insights_lead_id", table_name="ai_insights")
    op.drop_index("ix_ai_insights_insight_type", table_name="ai_insights")
    op.drop_table("ai_insights")

    op.drop_index("ix_raw_lead_events_source_processed", table_name="raw_lead_events")
    op.drop_index("ix_raw_lead_events_source_external", table_name="raw_lead_events")
    op.drop_index("ix_raw_lead_events_source", table_name="raw_lead_events")
    op.drop_index("ix_raw_lead_events_is_processed", table_name="raw_lead_events")
    op.drop_index("ix_raw_lead_events_external_id", table_name="raw_lead_events")
    op.drop_table("raw_lead_events")

    op.drop_index("ix_leads_status", table_name="leads")
    op.drop_index("ix_leads_stage", table_name="leads")
    op.drop_index("ix_leads_source_stage_status", table_name="leads")
    op.drop_index("ix_leads_source", table_name="leads")
    op.drop_index("ix_leads_priority", table_name="leads")
    op.drop_index("ix_leads_phone", table_name="leads")
    op.drop_index("ix_leads_external_source_id", table_name="leads")
    op.drop_index("ix_leads_external_source", table_name="leads")
    op.drop_index("ix_leads_email", table_name="leads")
    op.drop_index("ix_leads_campaign_name", table_name="leads")
    op.drop_index("ix_leads_assigned_to", table_name="leads")
    op.drop_table("leads")

    op.drop_index("ix_business_contexts_industry", table_name="business_contexts")
    op.drop_index("ix_business_contexts_company_name", table_name="business_contexts")
    op.drop_table("business_contexts")
