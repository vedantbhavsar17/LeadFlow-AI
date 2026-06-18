# LeadFlow Backend

Python, Flask, and SQLAlchemy backend scaffold.

This directory is architecture-only in Phase 1. It defines module boundaries and placeholder classes but does not implement APIs, authentication, database models, CRM logic, AI logic, or external integrations.

## Modules

- `crm_core/`: future home for migrated CRM logic.
- `lead_ingestion/`: lead collection adapters.
- `ai_engine/`: provider abstraction and lead intelligence modules.
- `outreach/`: email, WhatsApp copy workflow, LinkedIn copy workflow, and scheduling boundaries.
- `followups/`: future follow-up rules and automation.
- `analytics/`: future conversion and engagement intelligence.
- `integrations/`: external service integration boundaries.
- `database/`: SQLAlchemy and migration-ready database layout.
- `api/`: placeholder route modules only.
- `utils/`: shared backend helpers.

