"""Incoming email to conversation thread matcher."""

from __future__ import annotations

import logging

from sqlalchemy import select

from crm_core.repositories import ConversationMessageRepository, ConversationThreadRepository, LeadRepository
from database.models import ConversationThread, Lead
from outreach.email.email_models import IncomingEmail

logger = logging.getLogger(__name__)


class EmailThreadMatcher:
    """Match incoming emails to conversation threads."""

    def __init__(
        self,
        *,
        lead_repository: LeadRepository | None = None,
        thread_repository: ConversationThreadRepository | None = None,
        message_repository: ConversationMessageRepository | None = None,
    ) -> None:
        """Create an email thread matcher."""
        self.lead_repository = lead_repository or LeadRepository()
        self.thread_repository = thread_repository or ConversationThreadRepository(session=self.lead_repository.session)
        self.message_repository = message_repository or ConversationMessageRepository(session=self.lead_repository.session)
        self.session = self.lead_repository.session

    def match(self, incoming_email: IncomingEmail) -> ConversationThread | None:
        """Match by In-Reply-To, Message-ID, then sender email."""
        message = self.message_repository.get_by_in_reply_to(incoming_email.in_reply_to)
        if message:
            return message.thread

        message = self.message_repository.get_by_external_message_id(incoming_email.message_id)
        if message:
            return message.thread

        if incoming_email.from_email:
            lead = self._find_lead_by_email(incoming_email.from_email)
            if lead:
                thread = self.thread_repository.get_active_by_lead_channel(lead_id=lead.id, channel="email")
                if thread:
                    return thread
                return self.thread_repository.create(lead_id=lead.id, channel="email", status="active")

        logger.info("No email thread match for message_id=%s from=%s", incoming_email.message_id, incoming_email.from_email)
        return None

    def _find_lead_by_email(self, email_address: str) -> Lead | None:
        """Find a lead by email address."""
        statement = select(Lead).where(Lead.email == email_address.lower()).limit(1)
        return self.session.scalars(statement).first()

    # TODO: Add fuzzy contact matching only after privacy and dedupe rules are defined.
