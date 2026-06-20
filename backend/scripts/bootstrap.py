"""Bootstrap helpers for LeadFlow validation scripts."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import os
import sys
from typing import Iterator

from sqlalchemy import inspect, text


BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BACKEND_DIR.parent

for path in (str(BACKEND_DIR), str(PROJECT_DIR)):
    if path not in sys.path:
        sys.path.insert(0, path)


REQUIRED_TABLES = {
    "leads",
    "lead_activities",
    "customers",
    "business_contexts",
    "raw_lead_events",
    "followup_tasks",
    "ai_insights",
    "conversation_threads",
    "conversation_messages",
    "conversion_predictions",
}


class MigrationsNotAppliedError(RuntimeError):
    """Raised when validation points at a database without required tables."""


def load_dotenv() -> None:
    """Load simple KEY=VALUE pairs from .env files without overriding env vars."""
    for env_path in (PROJECT_DIR / ".env", PROJECT_DIR / ".env.local"):
        if not env_path.exists():
            continue
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                os.environ.setdefault(key, value)


def create_validation_app():
    """Create the Flask app through the same factory used by production."""
    load_dotenv()
    from app import create_app

    return create_app()


def database_diagnostics(app) -> dict[str, str | None]:
    """Return configured and resolved database location details."""
    from database.extensions import db

    engine_url = db.engine.url
    database_path = engine_url.database
    resolved_path = None
    if database_path and engine_url.drivername.startswith("sqlite"):
        resolved_path = str(Path(database_path).resolve())
    return {
        "database_uri": app.config.get("SQLALCHEMY_DATABASE_URI"),
        "engine_url": str(engine_url),
        "database_file_path": resolved_path,
    }


def verify_database_connection() -> None:
    """Verify the active database connection can execute a trivial query."""
    from database.extensions import db

    db.session.execute(text("SELECT 1"))


def existing_tables() -> set[str]:
    """Return tables in the active database."""
    from database.extensions import db

    return set(inspect(db.engine).get_table_names())


def verify_required_tables() -> None:
    """Verify all required tables exist before validations access services."""
    tables = existing_tables()
    missing = sorted(REQUIRED_TABLES - tables)
    if missing:
        raise MigrationsNotAppliedError(
            "Migrations have not been applied. "
            f"Missing tables: {', '.join(missing)}"
        )


def migration_revision() -> str | None:
    """Return current Alembic revision if the migration table exists."""
    from database.extensions import db

    if "alembic_version" not in existing_tables():
        return None
    return db.session.execute(text("SELECT version_num FROM alembic_version LIMIT 1")).scalar()


@contextmanager
def app_context(*, verify_schema: bool = True) -> Iterator:
    """Create app context, verify DB connection, and optionally verify schema."""
    from database.extensions import db
    import database.models  # noqa: F401

    app = create_validation_app()
    ctx = app.app_context()
    ctx.push()
    try:
        verify_database_connection()
        if verify_schema:
            verify_required_tables()
        yield app
    finally:
        db.session.remove()
        ctx.pop()


def startup_lines(app, *, include_revision: bool = True) -> list[str]:
    """Return human-readable database startup diagnostics."""
    diagnostics = database_diagnostics(app)
    lines = [
        f"DATABASE URI: {diagnostics['database_uri']}",
        f"database file path: {diagnostics['database_file_path'] or '(not a file-backed SQLite database)'}",
    ]
    if include_revision:
        revision = migration_revision()
        lines.append(f"migration revision: {revision or '(none)'}")
    return lines

