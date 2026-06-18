# Backend Architecture

## Stack

- Python
- Flask
- SQLAlchemy

## App Factory

`backend/app.py` contains a minimal Flask app factory. Future phases should initialize extensions, register blueprints, and configure middleware there.

## Module Ownership

- `crm_core`: migrated CRM logic.
- `lead_ingestion`: lead source adapters.
- `ai_engine`: AI provider and workflow boundaries.
- `outreach`: email, WhatsApp, LinkedIn, and scheduling boundaries.
- `followups`: rules and automation boundaries.
- `analytics`: conversion intelligence.
- `integrations`: third-party adapters.
- `database`: SQLAlchemy and migration structure.
- `api`: route modules.
- `utils`: shared utilities.

## Phase 1 Constraints

No routes, models, authentication, integrations, or business behavior should be added in this phase.

