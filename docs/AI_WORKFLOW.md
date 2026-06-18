# AI Workflow Architecture

## Provider Strategy

Primary provider: NVIDIA NIM.

Optional future providers:

- Gemini
- Ollama

The provider layer must avoid hard dependency on paid services. Ollama support is useful for local and free workflows.

## Required AI Workflows

- Lead qualification
- Pain point detection
- Outreach generation
- Reply analysis
- Follow-up suggestion
- Conversion prediction

## Business Context Usage

All future prompts should receive Business Context:

- Company Name
- Industry
- Services
- Ideal Customer Profile
- Target Market
- Common Pain Points
- Competitors
- Brand Tone
- Sales Goals

## Phase 1 Constraints

Do not call AI providers.
Do not implement prompt execution.
Do not implement scoring logic.
Do not implement generated message logic.

