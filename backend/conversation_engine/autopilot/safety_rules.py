"""Autopilot safety rules."""

from __future__ import annotations

from typing import Any

from conversation_engine.autopilot.autopilot_models import SafetyDecision


class AutopilotSafetyRules:
    """Evaluate whether a generated reply may be sent automatically."""

    minimum_confidence = 0.75

    def evaluate(self, *, reply_analysis: dict[str, Any], confidence: float) -> SafetyDecision:
        """Return a safety decision for automatic sending."""
        reasons: list[str] = []
        intent = str(reply_analysis.get("intent") or "").strip().lower()
        sentiment = str(reply_analysis.get("sentiment") or "").strip().lower()
        objection = str(reply_analysis.get("objection") or "").strip().lower()
        reasoning_blob = " ".join(
            str(reply_analysis.get(key) or "").lower()
            for key in ("reasoning", "suggested_reply", "recommended_action", "objection")
        )

        if intent == "unsubscribe":
            reasons.append("unsubscribe intent")
        if "legal" in objection or "legal complaint" in reasoning_blob or "lawsuit" in reasoning_blob:
            reasons.append("legal complaint")
        if sentiment == "angry" or "angry" in reasoning_blob:
            reasons.append("angry sentiment")
        if confidence < self.minimum_confidence:
            reasons.append("confidence below 0.75")

        return SafetyDecision(can_auto_send=not reasons, reasons=reasons)

    # TODO: Add configurable compliance and brand safety rules per organization.
