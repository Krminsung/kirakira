from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from pydantic.alias_generators import to_camel
from app.schemas.character import Character as CharacterDetail


# Message Schemas
class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(BaseModel):
    character_id: Optional[str] = None
    conversation_id: Optional[str] = None
    message: Optional[str] = None
    content: Optional[str] = None
    model: Optional[str] = "Gemini 2.5 Flash"
    
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )

class Message(MessageBase):
    id: str
    conversation_id: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel
    )

# Conversation Schemas
class ConversationBase(BaseModel):
    title: Optional[str] = None

class ConversationCreate(ConversationBase):
    character_id: str
    
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )

class Conversation(ConversationBase):
    id: str
    user_id: str
    character_id: str
    created_at: datetime
    updated_at: datetime
    character: Optional[CharacterDetail] = None


    # Include character info briefly if needed for sidebar
    # But current models don't have this nested in basic schema
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel
    )

class ConversationWithDetails(Conversation):
    messages: List[Message] = []
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel
    )
