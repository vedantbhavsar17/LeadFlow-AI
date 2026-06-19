"""Follow-up rule engine."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from database.models import ConversationMessage, Lead
from followups.models import FollowupRecommendation
from followups.rules.followup_rules import (
    INTERESTED_FOLLOWUP_DAYS,
    NO_REPLY_INTERVAL_DAYS,
    PRICING_OBJECTION_FOLLOWUP_DAYS,
    add_days,
    extract_suggested_date,
)


class FollowupRuleEngine:
    """Determine whether and how a lead should be followed up."""

    def evaluate(
        self,
        *,
        lead: Lead,
        qualification: dict[str, Any] | None = None,
        reply_analysis: dict[str, Any] | None = None,
        conversation_history: list[ConversationMessage] | None = None,
        now: datetime | None = None,
    ) -> FollowupRecommendation:
        """Evaluate follow-up rules and return a recommendation."""
        timestamp = now or datetime.utcnow()
        qualification = qualification or {}
        reply_analysis = reply_analysis or {}
        conversation_history = conversation_history or []

        intent = str(reply_analysis.get("intent") or "").strip().lower()
        if intent == "meeting_request":
            return self._recommend(
                due_date=timestamp,
                priority="high",
                reason="Lead requested a meeting.",
                suggested_message="Offer two specific meeting times and confirm the best option.",
            )
        if intent == "interested":
            return self._recommend(
                due_date=add_days(timestamp, INTERESTED_FOLLOWUP_DAYS),
                priority="high",
                reason="Lead showed interest.",
                suggested_message="Send a helpful follow-up with a clear next step.",
            )
        if intent == "follow_up_later":
            return self._recommend(
                due_date=extract_suggested_date(reply_analysis, now=timestamp),
                priority="normal",
                reason="Lead asked to follow up later.",
                suggested_message="Follow up at the requested time with context from the previous conversation.",
            )
        if intent == "pricing_objection":
            return self._recommend(
                due_date=add_days(timestamp, PRICING_OBJECTION_FOLLOWUP_DAYS),
                priority="high",
                reason="Lead raised a pricing objection.",
                suggested_message="Respond with value, outcomes, and a low-friction next step.",
            )
        if intent in {"not_interested", "unsubscribe"}:
            return FollowupRecommendation(
                followup_required=False,
                due_date=None,
                priority="low",
                reason=f"Lead intent is {intent}; no follow-up recommended.",
                suggested_message="",
            )

        no_reply_count = self._count_system_messages_since_customer_reply(conversation_history)
        if no_reply_count > 0:
            index = min(no_reply_count - 1, len(NO_REPLY_INTERVAL_DAYS) - 1)
            days = NO_REPLY_INTERVAL_DAYS[index]
            priority = "high" if days >= 14 else "normal"
            return self._recommend(
                due_date=add_days(timestamp, days),
                priority=priority,
                reason=f"No reply after outreach; schedule {days}-day follow-up.",
                suggested_message=self._no_reply_message_angle(qualification),
            )

        return FollowupRecommendation(
            followup_required=False,
            due_date=None,
            priority="low",
            reason="No follow-up rule matched.",
            suggested_message="",
        )

    def _recommend(self, *, due_date: datetime, priority: str, reason: str, suggested_message: str) -> FollowupRecommendation:
        """Build a positive follow-up recommendation."""
        return FollowupRecommendation(
            followup_required=True,
            due_date=due_date,
            priority=priority,
            reason=reason,
            suggested_message=suggested_message,
        )

    def _count_system_messages_since_customer_reply(self, messages: list[ConversationMessage]) -> int:
        """Count outbound/system messages after the latest customer reply."""
        count = 0
        for message in reversed(messages):
            if message.sender in {"lead", "customer"}:
                break
            if message.sender == "system":
                count += 1
        return count

    def _no_reply_message_angle(self, qualification: dict[str, Any]) -> str:
        """Return a suggested message angle for a no-reply follow-up."""
        pain_points = qualification.get("pain_points") if isinstance(qualification, dict) else None
        if isinstance(pain_points, list) and pain_points:
            return f"Reference their likely pain point around {pain_points[0]} and offer a simple next step."
        return "Send a concise follow-up that restates the value and asks one easy question."

    # TODO: Add configurable rule sets per organization after settings exist.
