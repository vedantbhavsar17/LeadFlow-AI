# LeadFlow Architecture

LeadFlow is an AI-powered Lead Conversion Operating System. CRM data and workflows are infrastructure, not the product boundary.

## Core Flow

```text
Lead
-> Qualified
-> Engaged
-> Followed Up
-> Meeting Booked
-> Converted
```

## System Boundaries

### Backend

The backend uses Flask and SQLAlchemy. It is organized by business capability instead of technical layer alone.

- `crm_core`: future migrated CRM infrastructure.
- `lead_ingestion`: source-specific lead collection boundaries.
- `ai_engine`: provider abstraction and intelligence workflows.
- `outreach`: message generation and communication workflow boundaries.
- `followups`: follow-up rules and automation boundaries.
- `analytics`: conversion intelligence and forecasting boundaries.
- `integrations`: external service adapters.
- `database`: SQLAlchemy, migrations, and seeders.
- `api`: future HTTP route modules.

### Frontend

The frontend uses Next.js 15, TypeScript, Tailwind CSS, shadcn/ui, and Recharts.

Phase 1 creates route and component boundaries only. Pages and UI behavior are deferred.

### AI Layer

NVIDIA NIM is the default provider. The provider abstraction must allow optional Gemini and Ollama support later.

No business logic or AI execution is implemented in Phase 1.

## Business Context Engine

Business Context is a first-class product capability. Future prompts must use structured context:

- Company Name
- Industry
- Services
- Ideal Customer Profile
- Target Market
- Common Pain Points
- Competitors
- Brand Tone
- Sales Goals

No model training is required. Context is configuration and prompt input.

## Database Direction

SQLite is the MVP database. PostgreSQL readiness is achieved through:

- SQLAlchemy models
- Configuration-driven database URLs
- Migration tooling in a later phase
- Avoiding SQLite-specific assumptions where practical

## Communication Strategy

MVP requirements:

- Email supported.
- WhatsApp message generation supported through copy-to-clipboard workflow.
- LinkedIn message generation supported.

MVP must not require Twilio, WhatsApp Business API, LinkedIn API, or paid messaging services.

