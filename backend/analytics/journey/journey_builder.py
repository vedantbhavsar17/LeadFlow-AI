"""Build normalized lead journey timelines."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from analytics.journey.journey_models import JourneyEvent, LEAD_STAGE_ORDER, StageProgress
from database.models import AIInsight, ConversationMessage, ConversionPrediction, FollowupTask, Lead, LeadActivity


class LeadJourneyBuilder:
    """Convert LeadFlow records into a single canonical lead journey."""

    activity_event_map = {
        "lead_created": ("Lead Created", "lead"),
        "email_sent": ("Email Sent", "outreach"),
        "email_received": ("Customer Replied", "conversation"),
        "followup_created": ("Follow-up Scheduled", "followup"),
        "meeting_booked": ("Meeting Booked", "conversion"),
        "status_changed": ("Lead Status Changed", "lead"),
        "converted": ("Converted", "conversion"),
        "reply_generated": ("AI Suggested Response", "ai"),
        "reply_sent": ("AI Reply Sent", "outreach"),
        "human_review_required": ("Human Review Required", "ai"),
    }

    def build_events(
        self,
        *,
        lead: Lead,
        activities: list[LeadActivity],
        insights: list[AIInsight],
        messages: list[ConversationMessage],
        followups: list[FollowupTask],
        predictions: list[ConversionPrediction],
    ) -> list[JourneyEvent]:
        """Build a sorted list of lead journey events."""
        events = [self._lead_created_event(lead)]
        events.extend(self._activity_events(activities))
        events.extend(self._insight_events(insights))
        events.extend(self._message_events(messages))
        events.extend(self._followup_events(followups))
        events.extend(self._prediction_events(predictions))

        if lead.converted_at:
            events.append(JourneyEvent(timestamp=lead.converted_at, event="Converted", type="conversion", source="lead"))
        if lead.lost_at:
            events.append(JourneyEvent(timestamp=lead.lost_at, event="Lost", type="lead", source="lead"))

        deduped = self._dedupe(events)
        return sorted(deduped, key=lambda event: event.timestamp)

    def build_stage_progress(self, *, lead: Lead, events: list[JourneyEvent]) -> StageProgress:
        """Build current lifecycle progress from lead state and journey events."""
        current_stage = self._infer_current_stage(lead=lead, events=events)
        index = LEAD_STAGE_ORDER.index(current_stage)
        completed = LEAD_STAGE_ORDER[: index + 1]
        progress_percent = int(round((index / (len(LEAD_STAGE_ORDER) - 1)) * 100))
        return StageProgress(
            current_stage=current_stage,
            progress_percent=progress_percent,
            completed_stages=completed,
        )

    def _lead_created_event(self, lead: Lead) -> JourneyEvent:
        """Return the lead creation event."""
        return JourneyEvent(
            timestamp=lead.created_at,
            event="Lead Created",
            type="lead",
            source="lead",
            metadata={"source": lead.source},
        )

    def _activity_events(self, activities: list[LeadActivity]) -> list[JourneyEvent]:
        """Return journey events from lead activities."""
        events: list[JourneyEvent] = []
        for activity in activities:
            label, event_type = self.activity_event_map.get(
                activity.activity_type,
                (self._title_from_token(activity.activity_type), "activity"),
            )
            events.append(
                JourneyEvent(
                    timestamp=activity.created_at,
                    event=label,
                    type=event_type,
                    source="activity",
                    metadata={
                        "activity_type": activity.activity_type,
                        "channel": activity.channel,
                        "note": activity.note,
                    },
                )
            )
        return events

    def _insight_events(self, insights: list[AIInsight]) -> list[JourneyEvent]:
        """Return journey events from AI insights."""
        events: list[JourneyEvent] = []
        for insight in insights:
            output = insight.output if isinstance(insight.output, dict) else {}
            event = self._insight_label(insight.insight_type, output)
            events.append(
                JourneyEvent(
                    timestamp=insight.created_at,
                    event=event,
                    type="ai",
                    source="ai_insight",
                    metadata={
                        "insight_type": insight.insight_type,
                        "confidence": insight.confidence,
                        "provider": insight.provider,
                        "summary": self._insight_summary(insight.insight_type, output),
                    },
                )
            )
            if insight.insight_type == "qualification" and output.get("pain_points"):
                events.append(
                    JourneyEvent(
                        timestamp=insight.created_at,
                        event="Pain Points Identified",
                        type="ai",
                        source="ai_insight",
                        metadata={"pain_points": output.get("pain_points")},
                    )
                )
        return events

    def _message_events(self, messages: list[ConversationMessage]) -> list[JourneyEvent]:
        """Return journey events from conversation messages."""
        events: list[JourneyEvent] = []
        for message in messages:
            if message.sender in {"lead", "customer"}:
                event = "Customer Replied"
                event_type = "conversation"
            elif message.message_type == "draft_email":
                event = "AI Suggested Response"
                event_type = "ai"
            elif message.sender == "system" and message.message_type in {"email", "text"}:
                event = "Email Sent" if message.subject or message.to_email else "System Message Sent"
                event_type = "outreach"
            else:
                event = self._title_from_token(message.message_type)
                event_type = "conversation"
            events.append(
                JourneyEvent(
                    timestamp=message.created_at,
                    event=event,
                    type=event_type,
                    source="conversation_message",
                    metadata={
                        "thread_id": message.thread_id,
                        "sender": message.sender,
                        "message_type": message.message_type,
                        "subject": message.subject,
                    },
                )
            )
        return events

    def _followup_events(self, followups: list[FollowupTask]) -> list[JourneyEvent]:
        """Return journey events from follow-up tasks."""
        events: list[JourneyEvent] = []
        for followup in followups:
            status_label = "Follow-up Completed" if followup.status == "completed" else "Follow-up Scheduled"
            events.append(
                JourneyEvent(
                    timestamp=followup.completed_at or followup.created_at,
                    event=status_label,
                    type="followup",
                    source="followup_task",
                    metadata={
                        "channel": followup.channel,
                        "reason": followup.reason,
                        "due_at": followup.due_at.isoformat() if followup.due_at else None,
                        "status": followup.status,
                    },
                )
            )
        return events

    def _prediction_events(self, predictions: list[ConversionPrediction]) -> list[JourneyEvent]:
        """Return journey events from conversion predictions."""
        return [
            JourneyEvent(
                timestamp=prediction.created_at,
                event="Conversion Score Updated",
                type="ai",
                source="conversion_prediction",
                metadata={
                    "score": prediction.score,
                    "probability_label": prediction.probability_label,
                    "confidence": prediction.confidence,
                    "recommended_action": prediction.recommended_action,
                },
            )
            for prediction in predictions
        ]

    def _infer_current_stage(self, *, lead: Lead, events: list[JourneyEvent]) -> str:
        """Infer lifecycle stage from lead fields and canonical journey events."""
        if lead.lost_at or lead.status == "lost" or lead.stage == "lost":
            return "lost"
        if lead.converted_at or lead.status == "converted" or lead.stage == "converted":
            return "converted"
        if lead.stage in LEAD_STAGE_ORDER:
            return lead.stage

        names = {event.event for event in events}
        if "Meeting Booked" in names or "Meeting Requested" in names:
            return "meeting_booked"
        if "Follow-up Scheduled" in names:
            return "follow_up_needed"
        if "Customer Replied" in names or "Email Sent" in names:
            return "engaged"
        if "AI Qualified Lead" in names or "Lead Qualified" in names:
            return "qualified"
        return "new"

    def _insight_label(self, insight_type: str, output: dict[str, Any]) -> str:
        """Return human-readable event label for an AI insight."""
        if insight_type == "qualification":
            return "AI Qualified Lead"
        if insight_type == "outreach":
            return "Outreach Generated"
        if insight_type == "reply_analysis":
            action = output.get("recommended_action")
            if action == "meeting_request" or output.get("intent") == "meeting_request":
                return "Meeting Requested"
            return "Reply Analyzed"
        if insight_type == "autopilot_reply":
            return "AI Suggested Response"
        if insight_type == "conversion_prediction":
            return "Conversion Score Updated"
        return self._title_from_token(insight_type)

    def _insight_summary(self, insight_type: str, output: dict[str, Any]) -> dict[str, Any]:
        """Return compact insight metadata for journey consumers."""
        if insight_type == "qualification":
            return {
                "score": output.get("score"),
                "category": output.get("category"),
                "buying_intent": output.get("buying_intent"),
                "recommended_action": output.get("recommended_action"),
            }
        if insight_type == "conversion_prediction":
            return {
                "score": output.get("score"),
                "probability_label": output.get("probability_label"),
                "recommended_action": output.get("recommended_action"),
            }
        return {"recommended_action": output.get("recommended_action")}

    def _dedupe(self, events: list[JourneyEvent]) -> list[JourneyEvent]:
        """Remove obvious duplicate lifecycle events from overlapping sources."""
        seen: set[tuple[datetime, str, str]] = set()
        unique: list[JourneyEvent] = []
        for event in events:
            key = (event.timestamp, event.event, event.type)
            if key in seen:
                continue
            seen.add(key)
            unique.append(event)
        return unique

    @staticmethod
    def _title_from_token(value: str | None) -> str:
        """Convert snake_case tokens to display labels."""
        return str(value or "Event").replace("_", " ").strip().title()

    # TODO: Add event severity/importance ordering for dense lead histories.

