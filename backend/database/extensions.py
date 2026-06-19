"""Database extension instances and initialization helpers.

This module owns Flask extension objects only. It must stay free of domain
models, API routes, and business behavior so the database layer remains easy
to initialize in tests, CLI commands, and future production entrypoints.
"""

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(session_options={"expire_on_commit": False})
"""Shared SQLAlchemy extension instance.

The configured session avoids expiring objects after commit because service
layers often need stable values for response serialization after persistence.
"""

migrate = Migrate()
"""Shared Flask-Migrate extension instance.

TODO: Generate initial migrations only after Phase 3 schema decisions are
approved and concrete domain models exist.
"""


def init_database(app: Flask) -> None:
    """Initialize SQLAlchemy and Flask-Migrate for a Flask application.

    SQLite is the MVP database through `DATABASE_URL`, while SQLAlchemy keeps
    the project ready for PostgreSQL-compatible migrations later.
    """
    db.init_app(app)
    import database.models  # noqa: F401

    migrate.init_app(
        app,
        db,
        directory=app.config.get("MIGRATIONS_DIRECTORY", "database/migrations"),
    )
