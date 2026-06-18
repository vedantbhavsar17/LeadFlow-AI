# LeadFlow

LeadFlow is an AI-powered Lead Conversion Operating System.

Phase 1 is architecture only. This repository currently contains structure, documentation, placeholders, and TODOs for the production foundation. It intentionally does not implement business logic, AI logic, CRM features, frontend pages, APIs, database models, authentication, or external integrations.

## Product Vision

LeadFlow helps lead-driven businesses move leads through the conversion journey:

Lead -> Qualified -> Engaged -> Followed Up -> Meeting Booked -> Converted

LeadFlow is not a traditional CRM. CRM capabilities are infrastructure for a broader lead conversion engine.

## MVP Principles

- NVIDIA NIM is the primary AI provider.
- The platform must be able to operate with free AI services.
- SQLite is acceptable for MVP.
- The architecture must remain PostgreSQL-ready.
- WhatsApp API is optional.
- LinkedIn API is optional.
- Message generation is mandatory.
- Lead qualification is mandatory.
- Business Context Engine is mandatory.
- Conversion Prediction is mandatory.

## Repository Layout

```text
leadflow/
├── backend/
├── frontend/
├── docs/
├── prompts/
├── tests/
├── scripts/
├── legacy_crm/
├── README.md
├── .gitignore
└── .env.example
```

`legacy_crm/` is intentionally empty. Existing CRM code will be copied there later and should not be analyzed during Phase 1.

## Development Status

Current phase: Phase 1 Architecture Only.

Next phases are documented in [docs/ROADMAP.md](docs/ROADMAP.md).

