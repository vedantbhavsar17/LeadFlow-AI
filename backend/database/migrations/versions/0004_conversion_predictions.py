"""create conversion prediction model

Revision ID: 0004_conversion_predictions
Revises: 0003_conversation_email_metadata
Create Date: 2026-06-19 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "0004_conversion_predictions"
down_revision = "0003_conversation_email_metadata"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "conversion_predictions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("probability_label", sa.String(length=50), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("reasons", sa.JSON(), nullable=False),
        sa.Column("risk_factors", sa.JSON(), nullable=False),
        sa.Column("recommended_action", sa.String(length=120), nullable=False),
        sa.Column("provider", sa.String(length=80), nullable=False),
        sa.Column("model", sa.String(length=160), nullable=True),
        sa.Column("ai_insight_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["ai_insight_id"], ["ai_insights.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_conversion_predictions_ai_insight_id", "conversion_predictions", ["ai_insight_id"], unique=False)
    op.create_index("ix_conversion_predictions_lead_created", "conversion_predictions", ["lead_id", "created_at"], unique=False)
    op.create_index("ix_conversion_predictions_lead_id", "conversion_predictions", ["lead_id"], unique=False)
    op.create_index("ix_conversion_predictions_lead_score", "conversion_predictions", ["lead_id", "score"], unique=False)
    op.create_index("ix_conversion_predictions_probability_label", "conversion_predictions", ["probability_label"], unique=False)
    op.create_index("ix_conversion_predictions_provider", "conversion_predictions", ["provider"], unique=False)
    op.create_index("ix_conversion_predictions_score", "conversion_predictions", ["score"], unique=False)


def downgrade():
    op.drop_index("ix_conversion_predictions_score", table_name="conversion_predictions")
    op.drop_index("ix_conversion_predictions_provider", table_name="conversion_predictions")
    op.drop_index("ix_conversion_predictions_probability_label", table_name="conversion_predictions")
    op.drop_index("ix_conversion_predictions_lead_score", table_name="conversion_predictions")
    op.drop_index("ix_conversion_predictions_lead_id", table_name="conversion_predictions")
    op.drop_index("ix_conversion_predictions_lead_created", table_name="conversion_predictions")
    op.drop_index("ix_conversion_predictions_ai_insight_id", table_name="conversion_predictions")
    op.drop_table("conversion_predictions")
