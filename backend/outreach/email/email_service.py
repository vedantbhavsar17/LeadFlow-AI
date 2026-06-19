"""Email communication service."""

from __future__ import annotations

import logging

from crm_core.repositories import ConversationMessageRepository, ConversationThreadRepository, LeadRepository
from crm_core.services import NotFoundError, ValidationError
from database.models import ConversationMessage, ConversationThread, Lead
from outreach.email.email_models import EmailCommunicationError
from outreach.email.email_templates import plain_text_email
from outreach.email.smtp_client import SMTPClient

logger = logging.getLogger(__name__)


class EmailService:
    """Send outbound emails and store them in conversation history."""

    def __init__(
        self,
        *,
        smtp_client: SMTPClient | None = None,
        lead_repository: LeadRepository | None = None,
        thread_repository: ConversationThreadRepository | None = None,
        message_repository: ConversationMessageRepository | None = None,
    ) -> None:
        """Create an email service with injectable dependencies."""
        self.smtp_client = smtp_client or SMTPClient()
        self.lead_repository = lead_repository or LeadRepository()
        self.thread_repository = thread_repository or ConversationThreadRepository(session=self.lead_repository.session)
        self.message_repository = message_repository or ConversationMessageRepository(session=self.lead_repository.session)

    def send_email(self, *, lead: Lead, subject: str, body: str) -> ConversationMessage:
        """Send an email to a lead and store the outbound conversation message."""
        if not lead.email:
            raise ValidationError("Lead email is required.")
        cleaned_subject = str(subject or "").strip()
        cleaned_body = plain_text_email(body)
        if not cleaned_subject:
            raise ValidationError("Email subject is required.")
        if not cleaned_body:
            raise ValidationError("Email body is required.")

        result = self.smtp_client.send_email(to_email=lead.email, subject=cleaned_subject, body=cleaned_body)
        if not result.success:
            raise EmailCommunicationError(result.error or "Email send failed.")

        thread = self._get_or_create_thread(lead)
        message = self.message_repository.create(
            thread_id=thread.id,
            sender="system",
            message_text=cleaned_body,
            message_type="email",
            external_message_id=result.message_id,
            in_reply_to=None,
            from_email=getattr(self.smtp_client, "from_address", None),
            to_email=lead.email,
            subject=cleaned_subject,
        )
        logger.info("Stored outbound email message_id=%s thread_id=%s", message.external_message_id, thread.id)
        return message

    def _get_or_create_thread(self, lead: Lead) -> ConversationThread:
        """Return an active email thread for a lead, creating one if needed."""
        persisted_lead = self.lead_repository.get_by_id(lead.id)
        if persisted_lead is None:
            raise NotFoundError(f"Lead {lead.id} was not found.")
        thread = self.thread_repository.get_active_by_lead_channel(lead_id=lead.id, channel="email")
        if thread:
            return thread
        return self.thread_repository.create(lead_id=lead.id, channel="email", status="active")

    # TODO: Add reply-to headers after tenant/domain email settings exist.
