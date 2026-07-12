"""Chat router: conversations, messages, blocking."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_verified_user
from app.db.session import get_db
from app.models.seller import Seller
from app.models.user import User
from app.schemas.interactions import (
    ConversationCreate,
    ConversationOut,
    ConversationSummary,
    MessageCreate,
    MessageList,
    MessageOut,
    OkResponse,
    ParticipantOut,
)
from app.services import chat_service

router = APIRouter(tags=["chat"])


def _participant_name(db: Session, user_id: uuid.UUID) -> str:
    """Display name: shop name if the user is a seller, else masked phone."""
    seller = db.query(Seller).filter(Seller.user_id == user_id).one_or_none()
    if seller is not None:
        return seller.shop_name
    user = db.get(User, user_id)
    if user and user.phone:
        return f"User {user.phone[-4:]}"
    return "User"


@router.post("/conversations", response_model=ConversationOut)
def create_conversation(
    payload: ConversationCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_verified_user),
) -> ConversationOut:
    convo = chat_service.get_or_create_conversation(db, user.id, payload.participant_id)
    other = chat_service.other_participant(convo, user.id)
    return ConversationOut(
        id=convo.id,
        participant=ParticipantOut(id=other, name=_participant_name(db, other)),
    )


@router.get("/conversations", response_model=list[ConversationSummary])
def list_conversations(
    db: Session = Depends(get_db),
    user: User = Depends(get_verified_user),
) -> list[ConversationSummary]:
    rows = chat_service.list_conversations(db, user.id)
    return [
        ConversationSummary(
            id=convo.id,
            participant=ParticipantOut(id=other, name=_participant_name(db, other)),
            last_message=last.content if last else "",
            last_message_time=last.created_at if last else convo.created_at,
        )
        for convo, other, last in rows
    ]


@router.get("/conversations/{conversation_id}/messages", response_model=MessageList)
def list_messages(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_verified_user),
) -> MessageList:
    rows = chat_service.list_messages(db, user.id, conversation_id)
    return MessageList(items=[MessageOut.model_validate(m) for m in rows])


@router.post("/conversations/{conversation_id}/messages", response_model=MessageOut)
def post_message(
    conversation_id: uuid.UUID,
    payload: MessageCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_verified_user),
) -> MessageOut:
    message = chat_service.post_message(db, user.id, conversation_id, payload.content)
    return MessageOut.model_validate(message)


@router.post("/blocks/{blocked_id}", response_model=OkResponse)
def block(
    blocked_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_verified_user),
) -> OkResponse:
    chat_service.block_user(db, user.id, blocked_id)
    return OkResponse()
