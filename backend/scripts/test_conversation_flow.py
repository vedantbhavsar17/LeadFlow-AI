"""Validate conversation thread and message persistence plus matching."""

from __future__ import annotations

from _validation import app_context, cleanup_records, print_result, run_validation


def _check() -> list[str]:
    from conversation_engine.email_listener import EmailParser, EmailThreadMatcher
    from crm_core.repositories import ConversationMessageRepository, ConversationThreadRepository
    from crm_core.services import LeadService

    lead = None
    with app_context():
        try:
            lead = LeadService().create_lead(
                first_name="Validation",
                last_name="Conversation",
                email="validation.conversation@leadflow.test",
                company="LeadFlow",
                source="validation",
            )
            thread_repo = ConversationThreadRepository()
            message_repo = ConversationMessageRepository(session=thread_repo.session)
            thread = thread_repo.create(lead_id=lead.id, channel="email", status="active")
            outbound = message_repo.create(
                thread_id=thread.id,
                sender="system",
                message_text="Validation outreach.",
                message_type="email",
                external_message_id="<leadflow-validation-outbound@test>",
                to_email=lead.email,
                subject="LeadFlow Validation",
            )
            raw_reply = (
                "From: validation.conversation@leadflow.test\r\n"
                "To: team@leadflow.test\r\n"
                "Subject: Re: LeadFlow Validation\r\n"
                "Message-ID: <leadflow-validation-inbound@test>\r\n"
                f"In-Reply-To: {outbound.external_message_id}\r\n"
                "\r\n"
                "Validation reply."
            ).encode()
            incoming = EmailParser().parse(raw_reply)
            matched = EmailThreadMatcher().match(incoming)
            if matched is None or matched.id != thread.id:
                raise AssertionError("Thread matcher did not return the expected conversation thread.")
            inbound = message_repo.create(
                thread_id=matched.id,
                sender="customer",
                message_text=incoming.body,
                message_type="email",
                external_message_id=incoming.message_id,
                in_reply_to=incoming.in_reply_to,
                from_email=incoming.from_email,
                to_email=incoming.to_email,
                subject=incoming.subject,
            )
            if inbound.id is None:
                raise AssertionError("ConversationMessage creation did not produce an id.")
            return [
                f"ConversationThread created with id {thread.id}.",
                f"ConversationMessage created with id {inbound.id}.",
                f"Thread matcher returned thread id {matched.id}.",
            ]
        finally:
            cleanup_records(lead)


def run_check():
    return run_validation("Conversation", _check)


if __name__ == "__main__":
    print_result(run_check())

