"""Validate SMTP login and outbound send."""

from __future__ import annotations

from email.message import EmailMessage
from email.utils import make_msgid
import smtplib
from datetime import datetime

from _validation import app_context, print_result, run_validation


TO_EMAIL = "vedantbhavsar05@gmail.com"


def _check() -> list[str]:
    from outreach.email import SMTPClient

    with app_context():
        client = SMTPClient()
        if not client.host:
            raise AssertionError("EMAIL_HOST is not configured.")
        if not client.username or not client.password:
            raise AssertionError("EMAIL_USERNAME and EMAIL_PASSWORD are required for SMTP login.")
        if not client.from_address:
            raise AssertionError("EMAIL_FROM_ADDRESS is not configured.")

        with smtplib.SMTP(client.host, client.port, timeout=30) as smtp:
            if client.use_tls:
                smtp.starttls()
            smtp.login(client.username, client.password)

        message = EmailMessage()
        message_id = make_msgid(domain="leadflow.validation")
        message["From"] = client.from_address
        message["To"] = TO_EMAIL
        message["Subject"] = "LeadFlow SMTP Validation"
        message["Message-ID"] = message_id
        message.set_content(f"LeadFlow SMTP validation sent at {datetime.utcnow().isoformat()} UTC.")

        with smtplib.SMTP(client.host, client.port, timeout=30) as smtp:
            if client.use_tls:
                smtp.starttls()
            smtp.login(client.username, client.password)
            smtp.send_message(message)

        return [
            f"SMTP login succeeded for {client.username}.",
            f"SMTP send succeeded to {TO_EMAIL} with Message-ID {message_id}.",
        ]


def run_check():
    return run_validation("SMTP", _check)


if __name__ == "__main__":
    print_result(run_check())

