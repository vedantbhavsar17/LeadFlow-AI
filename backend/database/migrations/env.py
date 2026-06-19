"""Alembic migration environment for LeadFlow."""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from flask import current_app

from database.extensions import db
import database.models  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = db.metadata


def get_engine():
    """Return the SQLAlchemy engine from the active Flask app."""
    try:
        return current_app.extensions["migrate"].db.get_engine()
    except (TypeError, AttributeError):
        return current_app.extensions["migrate"].db.engine


def get_engine_url() -> str:
    """Return a string database URL safe for Alembic configuration."""
    return str(get_engine().url).replace("%", "%%")


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""
    url = get_engine_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""

    def process_revision_directives(context, revision, directives):
        # TODO: Keep generated migrations reviewable as model count grows.
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
