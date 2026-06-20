"""Incoming email parser."""

from __future__ import annotations

from email import policy
from email.parser import BytesParser
from email.utils import getaddresses, parseaddr

from outreach.email.email_models import IncomingEmail


class EmailParser:
    """Parse raw RFC822 emails into IncomingEmail payloads."""

    def parse(self, raw_email: bytes) -> IncomingEmail:
        """Parse one raw email."""
        message = BytesParser(policy=policy.default).parsebytes(raw_email)
        body = self._extract_body(message)
        return IncomingEmail(
            message_id=self._clean_header(message.get("Message-ID")),
            in_reply_to=self._clean_header(message.get("In-Reply-To")),
            from_email=parseaddr(message.get("From", ""))[1].lower() or None,
            to_email=self._first_address(message.get("To", "")),
            subject=self._clean_header(message.get("Subject")),
            body=body,
            raw_headers={key: str(value) for key, value in message.items()},
        )

    def _extract_body(self, message) -> str:
        """Extract a text/plain body from an email message."""
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain" and not part.get_content_disposition():
                    return str(part.get_content()).strip()
            return ""
        return str(message.get_content()).strip()

    def _first_address(self, value: str) -> str | None:
        """Return the first parsed email address."""
        addresses = getaddresses([value])
        if not addresses:
            return None
        return addresses[0][1].lower() or None

    @staticmethod
    def _clean_header(value: str | None) -> str | None:
        """Return stripped header text."""
        if value is None:
            return None
        cleaned = str(value).strip()
        return cleaned or None
