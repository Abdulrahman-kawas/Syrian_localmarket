"""Conversations, messages, and user blocking."""

from __future__ import annotations

import uuid

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.core.errors import bad_request, forbidden, not_found
from app.models.chat import Conversation, Message
from app.models.user import Block, User
from app.services.moderation_service import sanitize_text


def _ordered_pair(a: uuid.UUID, b: uuid.UUID) -> tuple[uuid.UUID, uuid.UUID]:
    """Stable ordering so each user pair maps to exactly one conversation row."""
    return (a, b) if str(a) <= str(b) else (b, a)


def is_blocked(db: Session, a: uuid.UUID, b: uuid.UUID) -> bool:
    return (
        db.query(Block)
        .filter(
            or_(
                and_(Block.blocker_id == a, Block.blocked_id == b),
                and_(Block.blocker_id == b, Block.blocked_id == a),
            )
        )
        .first()
        is not None
    )


def get_or_create_conversation(
    db: Session, user_id: uuid.UUID, participant_id: uuid.UUID
) -> Conversation:
    if participant_id == user_id:
        raise bad_request("Cannot start a conversation with yourself")
    if db.get(User, participant_id) is None:
        raise not_found("Participant not found")
    if is_blocked(db, user_id, participant_id):
        raise forbidden("Conversation not permitted")

    p1, p2 = _ordered_pair(user_id, participant_id)
    convo = (
        db.query(Conversation)
        .filter(Conversation.participant1_id == p1, Conversation.participant2_id == p2)
        .one_or_none()
    )
    if convo is None:
        convo = Conversation(participant1_id=p1, participant2_id=p2)
        db.add(convo)
        db.commit()
        db.refresh(convo)
    return convo


def _require_participant(
    db: Session, user_id: uuid.UUID, conversation_id: uuid.UUID
) -> Conversation:
    convo = db.get(Conversation, conversation_id)
    if convo is None:
        raise not_found("Conversation not found")
    if user_id not in (convo.participant1_id, convo.participant2_id):
        raise forbidden("Not a participant in this conversation")
    return convo


def list_messages(db: Session, user_id: uuid.UUID, conversation_id: uuid.UUID) -> list[Message]:
    _require_participant(db, user_id, conversation_id)
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )


def post_message(
    db: Session, user_id: uuid.UUID, conversation_id: uuid.UUID, content: str
) -> Message:
    convo = _require_participant(db, user_id, conversation_id)
    other = convo.participant2_id if convo.participant1_id == user_id else convo.participant1_id
    if is_blocked(db, user_id, other):
        raise forbidden("Messaging not permitted")

    clean = sanitize_text(content)
    if not clean:
        raise bad_request("Message cannot be empty")
    message = Message(conversation_id=conversation_id, sender_id=user_id, content=clean)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def block_user(db: Session, blocker_id: uuid.UUID, blocked_id: uuid.UUID) -> None:
    if blocker_id == blocked_id:
        raise bad_request("Cannot block yourself")
    existing = (
        db.query(Block)
        .filter(Block.blocker_id == blocker_id, Block.blocked_id == blocked_id)
        .first()
    )
    if existing is None:
        db.add(Block(blocker_id=blocker_id, blocked_id=blocked_id))
        db.commit()


def other_participant(convo: Conversation, user_id: uuid.UUID) -> uuid.UUID:
    return convo.participant2_id if convo.participant1_id == user_id else convo.participant1_id


def list_conversations(
    db: Session, user_id: uuid.UUID
) -> list[tuple[Conversation, uuid.UUID, Message | None]]:
    """Return the user's conversations with the other participant id and last
    message, newest activity first."""
    convos = (
        db.query(Conversation)
        .filter(
            or_(
                Conversation.participant1_id == user_id,
                Conversation.participant2_id == user_id,
            )
        )
        .all()
    )
    rows: list[tuple[Conversation, uuid.UUID, Message | None]] = []
    for convo in convos:
        last = (
            db.query(Message)
            .filter(Message.conversation_id == convo.id)
            .order_by(Message.created_at.desc())
            .first()
        )
        rows.append((convo, other_participant(convo, user_id), last))

    rows.sort(
        key=lambda row: (row[2].created_at if row[2] else row[0].created_at),
        reverse=True,
    )
    return rows
