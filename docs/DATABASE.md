# Database Architecture

## MVP Database

SQLite is the primary MVP database.

Recommended development URL:

```text
sqlite:///leadflow.sqlite3
```

## PostgreSQL Readiness

The database layer must remain portable to PostgreSQL:

- Use SQLAlchemy as the ORM boundary.
- Configure database connections with `DATABASE_URL`.
- Use migrations once models exist.
- Avoid SQLite-only column types and query behavior unless isolated.
- Keep persistence access behind repositories or services where appropriate.

## Planned Areas

- Leads
- Lead Sources
- Business Context
- Qualification Results
- Outreach Messages
- Follow-up Tasks
- Replies
- Conversion Predictions
- Analytics Events
- User and organization settings

Phase 1 does not implement these models.

