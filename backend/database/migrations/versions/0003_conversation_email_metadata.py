"""add conversation email metadata

Revision ID: 0003_conversation_email_metadata
Revises: 0002_conversation_models
Create Date: 2026-06-19 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "0003_conversation_email_metadata"
down_revision = "0002_conversation_models"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("conversation_messages") as batch_op:
        batch_op.add_column(sa.Column("external_message_id", sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column("in_reply_to", sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column("from_email", sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column("to_email", sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column("subject", sa.String(length=255), nullable=True))
        batch_op.create_index("ix_conversation_messages_external_message_id", ["external_message_id"], unique=False)
        batch_op.create_index("ix_conversation_messages_in_reply_to", ["in_reply_to"], unique=False)
        batch_op.create_index("ix_conversation_messages_from_email", ["from_email"], unique=False)
        batch_op.create_index("ix_conversation_messages_to_email", ["to_email"], unique=False)
        batch_op.create_index("ix_conversation_messages_external_reply", ["external_message_id", "in_reply_to"], unique=False)


def downgrade():
    with op.batch_alter_table("conversation_messages") as batch_op:
        batch_op.drop_index("ix_conversation_messages_external_reply")
        batch_op.drop_index("ix_conversation_messages_to_email")
        batch_op.drop_index("ix_conversation_messages_from_email")
        batch_op.drop_index("ix_conversation_messages_in_reply_to")
        batch_op.drop_index("ix_conversation_messages_external_message_id")
        batch_op.drop_column("subject")
        batch_op.drop_column("to_email")
        batch_op.drop_column("from_email")
        batch_op.drop_column("in_reply_to")
        batch_op.drop_column("external_message_id")
