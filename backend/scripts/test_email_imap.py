"""Validate IMAP login, inbox access, and message fetch."""

from __future__ import annotations

import imaplib

from _validation import app_context, print_result, run_validation


def _check() -> list[str]:
    from conversation_engine.email_listener import IMAPEmailListener

    with app_context():
        listener = IMAPEmailListener()
        if not listener.host:
            raise AssertionError("IMAP_HOST is not configured.")
        if not listener.username or not listener.password:
            raise AssertionError("IMAP_USERNAME and IMAP_PASSWORD are required.")

        connection_class = imaplib.IMAP4_SSL if listener.use_ssl else imaplib.IMAP4
        connection = connection_class(listener.host, listener.port)
        try:
            connection.login(listener.username, listener.password)
            status, _ = connection.select(listener.mailbox)
            if status != "OK":
                raise AssertionError(f"Could not select mailbox {listener.mailbox!r}: {status}")
            search_status, data = connection.search(None, "ALL")
            if search_status != "OK":
                raise AssertionError(f"Could not search mailbox {listener.mailbox!r}: {search_status}")
            message_ids = []
            for chunk in data or []:
                message_ids.extend(chunk.split())
            fetched = 0
            if message_ids:
                fetch_status, fetch_data = connection.fetch(message_ids[-1], "(RFC822.HEADER)")
                if fetch_status != "OK":
                    raise AssertionError(f"Could not fetch latest message header: {fetch_status}")
                fetched = sum(1 for item in fetch_data if isinstance(item, tuple) and item[1])
            return [
                f"IMAP login succeeded for {listener.username}.",
                f"Mailbox selected: {listener.mailbox}.",
                f"Message search returned {len(message_ids)} messages; fetched {fetched} latest header(s).",
            ]
        finally:
            try:
                connection.logout()
            except imaplib.IMAP4.error:
                pass


def run_check():
    return run_validation("IMAP", _check)


if __name__ == "__main__":
    print_result(run_check())

