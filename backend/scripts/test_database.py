"""Validate LeadFlow database connectivity and schema."""

from __future__ import annotations

from _validation import print_result, run_validation
from bootstrap import (
    REQUIRED_TABLES,
    app_context,
    database_diagnostics,
    existing_tables,
    migration_revision,
    verify_database_connection,
)


def _check() -> list[str]:
    with app_context(verify_schema=False):
        from flask import current_app

        verify_database_connection()
        tables = existing_tables()
        missing = sorted(REQUIRED_TABLES - tables)
        if missing:
            raise AssertionError(
                "Migrations have not been applied. "
                f"Missing tables: {', '.join(missing)}"
            )
        diagnostics = database_diagnostics(current_app)
        return [
            "Database connection succeeded.",
            f"DATABASE URI: {diagnostics['database_uri']}",
            f"database file path: {diagnostics['database_file_path'] or '(not a file-backed SQLite database)'}",
            f"migration revision: {migration_revision() or '(none)'}",
            f"All expected tables exist: {', '.join(sorted(REQUIRED_TABLES))}",
        ]


def run_check():
    return run_validation("Database", _check)


if __name__ == "__main__":
    print_result(run_check())
