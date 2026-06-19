"""Autopilot workflow execution."""

from __future__ import annotations

from conversation_engine.autopilot.autopilot_models import AUTOPILOT_MODES, AutopilotDraft, AutopilotResult, SafetyDecision


class AutopilotWorkflowEngine:
    """Decide how a generated reply should move through manual/suggested/automatic modes."""

    def resolve(self, *, requested_mode: str, draft: AutopilotDraft, safety_decision: SafetyDecision) -> AutopilotResult:
        """Resolve requested mode and safety state into workflow output."""
        mode = str(requested_mode or "").strip().lower()
        if mode not in AUTOPILOT_MODES:
            raise ValueError(f"Unsupported autopilot mode: {requested_mode}")

        if mode == "manual":
            return AutopilotResult(
                recommended_action=draft.recommended_action,
                generated_reply=draft.generated_reply,
                send_mode="manual",
                confidence=draft.confidence,
                human_review_required=False,
                safety_reasons=[],
            )

        if mode == "suggested" or not safety_decision.can_auto_send:
            return AutopilotResult(
                recommended_action=draft.recommended_action,
                generated_reply=draft.generated_reply,
                send_mode="suggested",
                confidence=draft.confidence,
                human_review_required=not safety_decision.can_auto_send,
                safety_reasons=safety_decision.reasons,
            )

        return AutopilotResult(
            recommended_action=draft.recommended_action,
            generated_reply=draft.generated_reply,
            send_mode="automatic",
            confidence=draft.confidence,
            human_review_required=False,
            safety_reasons=[],
        )

    # TODO: Add organization-level default mode selection when settings exist.
