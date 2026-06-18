# Repository Tree

```text
leadflow/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── pyproject.toml
│   ├── crm_core/
│   │   ├── models/
│   │   ├── services/
│   │   ├── repositories/
│   │   └── README.md
│   ├── lead_ingestion/
│   │   ├── meta/
│   │   ├── google/
│   │   ├── csv/
│   │   ├── website/
│   │   └── manual/
│   ├── ai_engine/
│   │   ├── providers/
│   │   │   ├── nim/
│   │   │   ├── gemini/
│   │   │   └── ollama/
│   │   ├── qualification/
│   │   ├── business_context/
│   │   ├── outreach_generation/
│   │   ├── reply_analysis/
│   │   └── conversion_prediction/
│   ├── outreach/
│   │   ├── email/
│   │   ├── whatsapp/
│   │   ├── linkedin/
│   │   └── scheduler/
│   ├── followups/
│   │   ├── rules/
│   │   ├── scheduler/
│   │   └── automation/
│   ├── analytics/
│   │   ├── dashboard/
│   │   ├── conversion/
│   │   ├── engagement/
│   │   └── forecasting/
│   ├── integrations/
│   │   ├── ai/
│   │   ├── resend/
│   │   ├── meta/
│   │   ├── google/
│   │   └── webhooks/
│   ├── database/
│   │   ├── models/
│   │   ├── migrations/
│   │   └── seeders/
│   ├── api/
│   │   ├── leads.py
│   │   ├── ai.py
│   │   ├── outreach.py
│   │   ├── followups.py
│   │   ├── analytics.py
│   │   └── settings.py
│   └── utils/
├── frontend/
│   ├── app/
│   │   ├── dashboard/
│   │   ├── leads/
│   │   ├── lead-details/
│   │   ├── pipeline/
│   │   ├── outreach/
│   │   ├── followups/
│   │   ├── analytics/
│   │   ├── business-context/
│   │   └── settings/
│   ├── components/
│   │   ├── layout/
│   │   ├── dashboard/
│   │   ├── leads/
│   │   ├── pipeline/
│   │   ├── analytics/
│   │   ├── forms/
│   │   └── ai/
│   ├── services/
│   ├── hooks/
│   ├── types/
│   ├── lib/
│   └── public/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── MVP.md
│   ├── ROADMAP.md
│   ├── DATABASE.md
│   ├── AI_WORKFLOW.md
│   ├── FRONTEND.md
│   ├── BACKEND.md
│   └── REPOSITORY_TREE.md
├── prompts/
│   ├── qualification/
│   ├── outreach/
│   ├── followup/
│   ├── reply_analysis/
│   ├── conversion_prediction/
│   └── business_context/
├── tests/
├── scripts/
├── legacy_crm/
├── README.md
├── .gitignore
└── .env.example
```

## Folder Creation Commands

The canonical folder creation reference is [scripts/create_structure.ps1](../scripts/create_structure.ps1).

Run it from inside `leadflow/` in a clean environment:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\create_structure.ps1
```

`legacy_crm/` must remain empty until existing CRM code is copied in a later phase.

