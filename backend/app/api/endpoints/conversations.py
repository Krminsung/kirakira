from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from app.api import deps
from app.models.chat import Conversation, Message
from app.models.character import Character
from app.schemas.chat import Conversation as ConversationSchema, ConversationCreate, Message as MessageSchema

router = APIRouter()

@router.get("/")

async def read_conversations(
    session: deps.SessionDep,
    current_user: deps.CurrentUser,
    skip: int = 0,
    limit: int = 20
) -> Any:
    """
    Retrieve conversations for current user.
    """
    query = select(Conversation).where(
        Conversation.user_id == current_user.id
    ).options(
        selectinload(Conversation.character).selectinload(Character.creator)
    ).order_by(desc(Conversation.created_at)).offset(skip).limit(limit)


    
    result = await session.execute(query)
    conversations = result.scalars().all()
    from app.schemas.chat import Conversation as ConversationSchema
    return {"conversations": [ConversationSchema.model_validate(c).model_dump(by_alias=True) for c in conversations]}


@router.post("/")

async def create_conversation(
    *,
    session: deps.SessionDep,
    conversation_in: ConversationCreate,
    current_user: deps.CurrentUser
) -> Any:
    """
    Create new conversation.
    """
    # Verify character exists
    result = await session.execute(select(Character).where(Character.id == conversation_in.character_id))
    character = result.scalars().first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    conversation = Conversation(
        **conversation_in.model_dump(),
        user_id=current_user.id
    )
    session.add(conversation)
    await session.commit()
    
    # Reload with relationships for Pydantic validation
    result = await session.execute(
        select(Conversation)
        .where(Conversation.id == conversation.id)
        .options(selectinload(Conversation.character).selectinload(Character.creator))
    )
    conversation = result.scalars().first()
    
    return {"conversation": ConversationSchema.model_validate(conversation).model_dump(by_alias=True)}



@router.delete("/{id}")

async def delete_conversation(
    id: str,
    session: deps.SessionDep,
    current_user: deps.CurrentUser
) -> Any:
    """
    Delete conversation.
    """
    result = await session.execute(select(Conversation).where(
        Conversation.id == id,
        Conversation.user_id == current_user.id
    ))
    conversation = result.scalars().first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    await session.delete(conversation)
    await session.commit()
    return {"status": "success", "message": "Conversation deleted"}



@router.get("/{id}/messages")

async def read_conversation_messages(
    id: str,
    session: deps.SessionDep,
    current_user: deps.CurrentUser
) -> Any:
    """
    Get messages for a conversation.
    """
    # Verify conversation ownership
    result = await session.execute(select(Conversation).where(
        Conversation.id == id,
        Conversation.user_id == current_user.id
    ))
    conversation = result.scalars().first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    # Get messages
    query = select(Message).where(
        Message.conversation_id == id
    ).order_by(Message.created_at)
    
    result = await session.execute(query)
    messages = result.scalars().all()
    from app.schemas.chat import Message as MessageSchema
    return {"messages": [MessageSchema.model_validate(m).model_dump(by_alias=True) for m in messages]}

