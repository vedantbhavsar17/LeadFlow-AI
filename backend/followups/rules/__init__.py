"""Follow-up rule exports."""

from followups.rules.followup_rule_engine import FollowupRuleEngine
from followups.rules.followup_rules import (
    INTERESTED_FOLLOWUP_DAYS,
    NO_REPLY_INTERVAL_DAYS,
    PRICING_OBJECTION_FOLLOWUP_DAYS,
)

FollowupRuleSet = FollowupRuleEngine

__all__ = [
    "FollowupRuleEngine",
    "FollowupRuleSet",
    "INTERESTED_FOLLOWUP_DAYS",
    "NO_REPLY_INTERVAL_DAYS",
    "PRICING_OBJECTION_FOLLOWUP_DAYS",
]
