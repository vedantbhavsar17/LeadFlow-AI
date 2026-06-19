"""Email communication exports."""

from outreach.email.email_models import EmailCommunicationError, EmailSendResult, IncomingEmail
from outreach.email.email_service import EmailService
from outreach.email.smtp_client import SMTPClient

EmailOutreachService = EmailService

__all__ = [
    "EmailCommunicationError",
    "EmailOutreachService",
    "EmailSendResult",
    "EmailService",
    "IncomingEmail",
    "SMTPClient",
]
