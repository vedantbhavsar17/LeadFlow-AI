"""SMTP client for outbound email."""

from __future__ import annotations

import logging
from email.message import EmailMessage
from email.utils import make_msgid
import smtplib
from os import getenv

from flask import current_app, has_app_context

from outreach.email.email_models import EmailCommunicationError, EmailSendResult

logger = logging.getLogger(__name__)


class SMTPClient:
    """Small SMTP client with environment/config based settings."""

    def __init__(
        self,
        *,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        use_tls: bool | None = None,
        from_address: str | None = None,
    ) -> None:
        """Create an SMTP client."""
        self.host = host if host is not None else self._config_value("EMAIL_HOST", "")
        self.port = int(port if port is not None else self._config_value("EMAIL_PORT", 587))
        self.username = username if username is not None else self._config_value("EMAIL_USERNAME", "")
        self.password = password if password is not None else self._config_value("EMAIL_PASSWORD", "")
        self.use_tls = self._coerce_bool(use_tls if use_tls is not None else self._config_value("EMAIL_USE_TLS", True))
        self.from_address = from_address if from_address is not None else self._config_value("EMAIL_FROM_ADDRESS", self.username)

    def send_email(self, *, to_email: str, subject: str, body: str) -> EmailSendResult:
        """Send one plain-text email."""
        if not self.host:
            return EmailSendResult(success=False, message_id=None, error="EMAIL_HOST is not configured.")
        if not self.from_address:
            return EmailSendResult(success=False, message_id=None, error="EMAIL_FROM_ADDRESS is not configured.")
        if not to_email:
            return EmailSendResult(success=False, message_id=None, error="Recipient email is required.")

        message_id = make_msgid(domain="leadflow.local")
        message = EmailMessage()
        message["From"] = self.from_address
        message["To"] = to_email
        message["Subject"] = subject
        message["Message-ID"] = message_id
        message.set_content(body)

        try:
            with smtplib.SMTP(self.host, self.port, timeout=30) as smtp:
                if self.use_tls:
                    smtp.starttls()
                if self.username and self.password:
                    smtp.login(self.username, self.password)
                smtp.send_message(message)
        except (OSError, smtplib.SMTPException) as exc:
            logger.warning("SMTP email send failed: %s", exc)
            return EmailSendResult(success=False, message_id=message_id, error=str(exc))

        logger.info("SMTP email sent to=%s message_id=%s", to_email, message_id)
        return EmailSendResult(success=True, message_id=message_id)

    @staticmethod
    def _config_value(name: str, default):
        """Read config from Flask current_app when available, then environment."""
        if has_app_context():
            return current_app.config.get(name, getenv(name, default))
        return getenv(name, default)

    @staticmethod
    def _coerce_bool(value) -> bool:
        """Convert common config/env truthy values to bool."""
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in {"1", "true", "yes", "on"}

    # TODO: Add provider-specific clients such as Resend behind the same service boundary.
