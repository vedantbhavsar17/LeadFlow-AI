# Database

SQLAlchemy and Flask-Migrate database foundation.

SQLite is the MVP database. The architecture must remain PostgreSQL-ready through SQLAlchemy-compatible models, migrations, and configuration-driven connection strings.

## Files

- `extensions.py`: owns `db`, `migrate`, and initialization.
- `base.py`: abstract base model with `id`, `created_at`, and `updated_at`.
- `session.py`: session lifecycle helpers for scripts and future services.
- `models/`: future domain model registry.
- `migrations/`: future Flask-Migrate/Alembic migration directory.
- `seeders/`: future deterministic seed data.

Phase 3 does not define business/domain models.
