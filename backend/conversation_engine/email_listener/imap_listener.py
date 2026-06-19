"""IMAP listener for incoming email."""

from __future__ import annotations

import imaplib
import logging
from os import getenv
from typing import Iterable

from flask import current_app, has_app_context

from conversation_engine.email_listener.email_parser import EmailParser
from conversation_engine.email_listener.thread_matcher import EmailThreadMatcher
from crm_core.repositories import ConversationMessageRepository
from database.models import ConversationMessage, ConversationThread

logger = logging.getLogger(__name__)


class IMAPEmailListener:
    """Fetch incoming emails over IMAP and store matched replies."""

    def __init__(
        self,
        *,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        use_ssl: bool | None = None,
        mailbox: str | None = None,
        parser: EmailParser | None = None,
        thread_matcher: EmailThreadMatcher | None = None,
        message_repository: ConversationMessageRepository | None = None,
    ) -> None:
        """Create an IMAP email listener."""
        self.host = host if host is not None else self._config_value("IMAP_HOST", "")
        self.port = int(port if port is not None else self._config_value("IMAP_PORT", 993))
        self.username = username if username is not None else self._config_value("IMAP_USERNAME", "")
        self.password = password if password is not None else self._config_value("IMAP_PASSWORD", "")
        self.use_ssl = self._coerce_bool(use_ssl if use_ssl is not None else self._config_value("IMAP_USE_SSL", True))
        self.mailbox = mailbox if mailbox is not None else self._config_value("IMAP_MAILBOX", "INBOX")
        self.parser = parser or EmailParser()
        self.thread_matcher = thread_matcher or EmailThreadMatcher()
        self.message_repository = message_repository or ConversationMessageRepository(session=self.thread_matcher.session)

    def fetch_new_emails(self) -> list[tuple[ConversationThread, ConversationMessage]]:
        """Fetch unseen emails, match them to threads, and store customer messages."""
        raw_messages = self._fetch_unseen_raw_messages()
        stored: list[tuple[ConversationThread, ConversationMessage]] = []
        for raw_message in raw_messages:
            incoming = self.parser.parse(raw_message)
            if self.message_repository.exists_external_message_id(incoming.message_id):
                continue
            thread = self.thread_matcher.match(incoming)
            if thread is None:
                continue
            message = self.message_repository.create(
                thread_id=thread.id,
                sender="customer",
                message_text=incoming.body,
                message_type="email",
                external_message_id=incoming.message_id,
                in_reply_to=incoming.in_reply_to,
                from_email=incoming.from_email,
                to_email=incoming.to_email,
                subject=incoming.subject,
            )
            stored.append((thread, message))
            logger.info("Stored incoming email message_id=%s thread_id=%s", incoming.message_id, thread.id)
        return stored

    def _fetch_unseen_raw_messages(self) -> list[bytes]:
        """Fetch unseen raw emails from the configured mailbox."""
        if not self.host:
            raise ValueError("IMAP_HOST is not configured.")
        if not self.username or not self.password:
            raise ValueError("IMAP_USERNAME and IMAP_PASSWORD are required.")

        connection_class = imaplib.IMAP4_SSL if self.use_ssl else imaplib.IMAP4
        connection = connection_class(self.host, self.port)
        try:
            connection.login(self.username, self.password)
            connection.select(self.mailbox)
            status, data = connection.search(None, "UNSEEN")
            if status != "OK":
                return []
            raw_messages: list[bytes] = []
            for message_id in self._iter_message_ids(data):
                fetch_status, fetch_data = connection.fetch(message_id, "(RFC822)")
                if fetch_status != "OK":
                    continue
                for item in fetch_data:
                    if isinstance(item, tuple) and item[1]:
                        raw_messages.append(item[1])
            return raw_messages
        finally:
            try:
                connection.logout()
            except imaplib.IMAP4.error:
                pass

    def _iter_message_ids(self, data) -> Iterable[bytes]:
        """Yield message ids from an IMAP search response."""
        for chunk in data or []:
            for message_id in chunk.split():
                yield message_id

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

    # TODO: Move polling to a scheduler after deployment architecture is defined.
