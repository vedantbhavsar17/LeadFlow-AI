"""create conversation models

Revision ID: 0002_conversation_models
Revises: 0001_core_domain_models
Create Date: 2026-06-19 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "0002_conversation_models"
down_revision = "0001_core_domain_models"
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
        "conversation_threads",
        *_base_columns(),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("channel", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_conversation_threads_channel", "conversation_threads", ["channel"], unique=False)
    op.create_index("ix_conversation_threads_lead_channel", "conversation_threads", ["lead_id", "channel"], unique=False)
    op.create_index("ix_conversation_threads_lead_id", "conversation_threads", ["lead_id"], unique=False)
    op.create_index("ix_conversation_threads_status", "conversation_threads", ["status"], unique=False)
    op.create_index("ix_conversation_threads_status_channel", "conversation_threads", ["status", "channel"], unique=False)

    op.create_table(
        "conversation_messages",
        *_base_columns(),
        sa.Column("thread_id", sa.Integer(), nullable=False),
        sa.Column("sender", sa.String(length=50), nullable=False),
        sa.Column("message_text", sa.Text(), nullable=False),
        sa.Column("message_type", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(["thread_id"], ["conversation_threads.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_conversation_messages_message_type", "conversation_messages", ["message_type"], unique=False)
    op.create_index("ix_conversation_messages_sender", "conversation_messages", ["sender"], unique=False)
    op.create_index("ix_conversation_messages_thread_created", "conversation_messages", ["thread_id", "created_at"], unique=False)
    op.create_index("ix_conversation_messages_thread_id", "conversation_messages", ["thread_id"], unique=False)
    op.create_index("ix_conversation_messages_thread_sender", "conversation_messages", ["thread_id", "sender"], unique=False)


def downgrade():
    op.drop_index("ix_conversation_messages_thread_sender", table_name="conversation_messages")
    op.drop_index("ix_conversation_messages_thread_id", table_name="conversation_messages")
    op.drop_index("ix_conversation_messages_thread_created", table_name="conversation_messages")
    op.drop_index("ix_conversation_messages_sender", table_name="conversation_messages")
    op.drop_index("ix_conversation_messages_message_type", table_name="conversation_messages")
    op.drop_table("conversation_messages")

    op.drop_index("ix_conversation_threads_status_channel", table_name="conversation_threads")
    op.drop_index("ix_conversation_threads_status", table_name="conversation_threads")
    op.drop_index("ix_conversation_threads_lead_id", table_name="conversation_threads")
    op.drop_index("ix_conversation_threads_lead_channel", table_name="conversation_threads")
    op.drop_index("ix_conversation_threads_channel", table_name="conversation_threads")
    op.drop_table("conversation_threads")
