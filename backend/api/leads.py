"""Lead REST API."""

import logging
from typing import Any

from flask import Blueprint, jsonify, request
from sqlalchemy import select

from analytics.journey import LeadJourneyService
from api.serializers import serialize_activity, serialize_lead
from crm_core.services import ActivityService, LeadService, ValidationError

logger = logging.getLogger(__name__)

leads_bp = Blueprint("leads_api", __name__, url_prefix="/api/leads")


def _json_payload() -> dict[str, Any]:
    """Return a JSON object payload or raise a validation error."""
    payload = request.get_json(silent=True)
    if payload is None:
        return {}
    if not isinstance(payload, dict):
        raise ValidationError("JSON payload must be an object.")
    return payload


@leads_bp.get("")
def list_leads():
    """Return leads."""
    service = LeadService()
    leads = service.list_leads(
        limit=request.args.get("limit", default=100, type=int) or 100,
        offset=request.args.get("offset", default=0, type=int) or 0,
        source=request.args.get("source"),
        stage=request.args.get("stage"),
        status=request.args.get("status"),
        assigned_to=request.args.get("assigned_to"),
    )
    return jsonify({"leads": [serialize_lead(lead) for lead in leads]}), 200


@leads_bp.get("/<int:lead_id>")
def get_lead(lead_id: int):
    """Return one lead."""
    lead = LeadService().get_lead(lead_id)
    return jsonify({"lead": serialize_lead(lead)}), 200


@leads_bp.post("")
def create_lead():
    """Create one lead."""
    payload = _json_payload()
    for field in ["first_name", "last_name", "email", "company"]:
        if not payload.get(field):
            raise ValidationError(f"{field} is required.")
    if not payload.get("source"):
        payload["source"] = "manual"

    email = payload.get("email")
    if email:
        from database.extensions import db
        from database.models import Lead
        email_normalized = email.strip().lower()
        existing = db.session.query(Lead).filter(Lead.email == email_normalized).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()

    lead = LeadService().create_lead(**payload)
    logger.info("API created lead id=%s", lead.id)
    return jsonify({"lead": serialize_lead(lead)}), 201


@leads_bp.put("/<int:lead_id>")
def update_lead(lead_id: int):
    """Update one lead."""
    lead = LeadService().update_lead(lead_id, **_json_payload())
    return jsonify({"lead": serialize_lead(lead)}), 200


@leads_bp.patch("/<int:lead_id>/status")
def change_lead_status(lead_id: int):
    """Change a lead status."""
    payload = _json_payload()
    status = payload.get("status")
    if not status:
        raise ValidationError("status is required.")
    lead = LeadService().change_status(lead_id, status)
    return jsonify({"lead": serialize_lead(lead)}), 200


@leads_bp.patch("/<int:lead_id>/stage")
def change_lead_stage(lead_id: int):
    """Change a lead stage."""
    payload = _json_payload()
    stage = payload.get("stage")
    if not stage:
        raise ValidationError("stage is required.")
    lead = LeadService().change_stage(lead_id, stage)
    return jsonify({"lead": serialize_lead(lead)}), 200


@leads_bp.get("/<int:lead_id>/timeline")
def get_lead_timeline(lead_id: int):
    """Return one lead timeline."""
    activities = ActivityService().get_lead_timeline(
        lead_id,
        limit=request.args.get("limit", default=100, type=int) or 100,
        offset=request.args.get("offset", default=0, type=int) or 0,
    )
    return jsonify({"activities": [serialize_activity(activity) for activity in activities]}), 200


@leads_bp.get("/<int:lead_id>/journey")
def get_lead_journey(lead_id: int):
    """Return the canonical journey for one lead."""
    journey = LeadJourneyService().get_lead_journey(lead_id)
    return jsonify({"journey": journey.to_dict()}), 200


@leads_bp.get("/<int:lead_id>/stage-progress")
def get_lead_stage_progress(lead_id: int):
    """Return current lifecycle stage progress for one lead."""
    progress = LeadJourneyService().get_stage_progress(lead_id)
    return jsonify({"stage_progress": progress.to_dict()}), 200


@leads_bp.get("/<int:lead_id>/followups")
def list_lead_followups(lead_id: int):
    """Return follow-up tasks for one lead."""
    from database.extensions import db
    from database.models import FollowupTask
    session = db.session
    statement = select(FollowupTask).where(FollowupTask.lead_id == lead_id).order_by(FollowupTask.created_at.desc())
    tasks = session.scalars(statement).all()
    return jsonify({
        "followups": [
            {
                "id": str(t.id),
                "lead_id": t.lead_id,
                "channel": t.channel,
                "reason": t.reason,
                "due_at": t.due_at.isoformat() if t.due_at else None,
                "status": t.status,
                "completed_at": t.completed_at.isoformat() if t.completed_at else None,
                "created_at": t.created_at.isoformat() if t.created_at else None,
                # Test compatibility fields:
                "title": t.reason,
                "notes": t.reason,
                "due_date": t.due_at.isoformat() if t.due_at else None,
            }
            for t in tasks
        ]
      }), 200


@leads_bp.post("/<int:lead_id>/followups")
def create_lead_followup(lead_id: int):
    """Create a follow-up task for a lead."""
    from followups.services import FollowupService
    from datetime import datetime
    payload = _json_payload()
    
    # Handle Z suffix in ISO dates for datetime.fromisoformat
    due_at_str = payload.get("due_at") or payload.get("due_date")
    if due_at_str and due_at_str.endswith("Z"):
        due_at_str = due_at_str[:-1] + "+00:00"
        
    due_at = datetime.fromisoformat(due_at_str) if due_at_str else datetime.utcnow()
    
    title = payload.get("title")
    notes = payload.get("notes")
    reason = payload.get("reason") or title or notes or "Follow up"
    
    followup = FollowupService().create_followup(
        lead_id=lead_id,
        channel=payload.get("channel", "email"),
        reason=reason,
        due_at=due_at
    )
    return jsonify({
        "followup": {
            "id": str(followup.id),
            "lead_id": followup.lead_id,
            "channel": followup.channel,
            "reason": followup.reason,
            "due_at": followup.due_at.isoformat() if followup.due_at else None,
            "status": followup.status,
            "created_at": followup.created_at.isoformat() if followup.created_at else None,
            # Test compatibility fields:
            "title": title or followup.reason,
            "notes": notes or followup.reason,
            "due_date": followup.due_at.isoformat() if followup.due_at else None,
        }
    }), 201


@leads_bp.patch("/followups/<int:followup_id>/complete")
def complete_lead_followup(followup_id: int):
    """Complete a follow-up task."""
    from followups.services import FollowupService
    followup = FollowupService().complete_followup(followup_id)
    return jsonify({
        "followup": {
            "id": str(followup.id),
            "lead_id": followup.lead_id,
            "channel": followup.channel,
            "reason": followup.reason,
            "due_at": followup.due_at.isoformat() if followup.due_at else None,
            "status": followup.status,
            "completed_at": followup.completed_at.isoformat() if followup.completed_at else None,
        }
    }), 200


@leads_bp.get("/<int:lead_id>/messages")
def list_lead_messages(lead_id: int):
    """Return all messages and AI suggested replies for a lead."""
    from database.extensions import db
    from database.models import ConversationThread, ConversationMessage, AIInsight
    session = db.session
    threads_stmt = select(ConversationThread).where(ConversationThread.lead_id == lead_id)
    threads = session.scalars(threads_stmt).all()
    
    all_messages = []
    suggested_reply = None
    
    for t in threads:
        msgs_stmt = select(ConversationMessage).where(ConversationMessage.thread_id == t.id).order_by(ConversationMessage.created_at.asc())
        msgs = session.scalars(msgs_stmt).all()
        
        insight_stmt = select(AIInsight).where(AIInsight.lead_id == lead_id).where(AIInsight.insight_type == "reply_analysis").order_by(AIInsight.created_at.desc()).limit(1)
        insight = session.scalars(insight_stmt).first()
        if insight and isinstance(insight.output, dict):
            suggested_reply = insight.output.get("suggested_reply") or insight.output.get("reply_suggestion")
        
        for m in msgs:
            all_messages.append({
                "id": str(m.id),
                "sender": m.sender,
                "content": m.message_text,
                "created_at": m.created_at.isoformat() if m.created_at else None
            })
            
    return jsonify({
        "messages": all_messages,
        "suggested_reply": suggested_reply
    }), 200


@leads_bp.post("/<int:lead_id>/messages")
def create_lead_message(lead_id: int):
    """Add a conversation message and log activity."""
    from database.extensions import db
    from database.models import ConversationThread, ConversationMessage
    session = db.session
    payload = _json_payload()
    sender = payload.get("sender", "user")
    content = payload.get("content", "")
    channel = payload.get("channel", "email")
    
    thread_stmt = select(ConversationThread).where(ConversationThread.lead_id == lead_id).where(ConversationThread.channel == channel).where(ConversationThread.status == "active").limit(1)
    thread = session.scalars(thread_stmt).first()
    
    if not thread:
        thread = ConversationThread(lead_id=lead_id, channel=channel, status="active")
        session.add(thread)
        session.flush()
        
    message = ConversationMessage(
        thread_id=thread.id,
        sender=sender,
        message_text=content,
        message_type="text"
    )
    session.add(message)
    
    from crm_core.services import ActivityService
    ActivityService(session=session).create_activity(
        lead_id=lead_id,
        activity_type="reply_received" if sender == "customer" else "outreach_sent",
        channel=channel,
        note=f"Message {sender}: {content[:60]}..."
    )
    
    session.commit()
    
    return jsonify({
        "message": {
            "id": str(message.id),
            "sender": message.sender,
            "content": message.message_text,
            "created_at": message.created_at.isoformat() if message.created_at else None
        }
    }), 201


@leads_bp.get("/conversations")
def list_all_conversations():
    """Return all conversation threads in the system."""
    from database.extensions import db
    from database.models import ConversationThread, ConversationMessage, Lead, AIInsight
    session = db.session
    threads_stmt = select(ConversationThread).order_by(ConversationThread.updated_at.desc())
    threads = session.scalars(threads_stmt).all()
    
    response_data = []
    
    for t in threads:
        lead = session.get(Lead, t.lead_id)
        if not lead:
            continue
            
        msgs_stmt = select(ConversationMessage).where(ConversationMessage.thread_id == t.id).order_by(ConversationMessage.created_at.asc())
        msgs = session.scalars(msgs_stmt).all()
        
        insight_stmt = select(AIInsight).where(AIInsight.lead_id == t.lead_id).where(AIInsight.insight_type == "reply_analysis").order_by(AIInsight.created_at.desc()).limit(1)
        insight = session.scalars(insight_stmt).first()
        suggested_reply = None
        if insight and isinstance(insight.output, dict):
            suggested_reply = insight.output.get("suggested_reply") or insight.output.get("reply_suggestion")
        
        response_data.append({
            "leadId": t.lead_id,
            "threadId": f"thread_{t.id}",
            "suggestedReply": suggested_reply,
            "messages": [
                {
                    "id": str(m.id),
                    "sender": m.sender,
                    "content": m.message_text,
                    "created_at": m.created_at.isoformat() if m.created_at else None
                }
                for m in msgs
            ]
        })
        
    return jsonify({"conversations": response_data}), 200
