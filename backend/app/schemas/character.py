from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Any

from pydantic.alias_generators import to_camel

# Worldview Schemas
class CharacterCreator(BaseModel):
    id: str
    name: str
    avatar: Optional[str] = None
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel
    )

class WorldviewBase(BaseModel):

    title: str
    description: str

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )


class WorldviewCreate(WorldviewBase):
    pass

class Worldview(WorldviewBase):
    id: str
    creator_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel
    )


# Character Schemas
class CharacterBase(BaseModel):
    name: str
    description: str
    personality: Optional[str] = None
    greeting: str
    greetings: Optional[Any] = None
    secret: Optional[str] = None
    example_dialogs: Optional[Any] = None

    visibility: str = "PRIVATE"
    profile_image: Optional[str] = None
    album_images: Optional[str] = None
    worldview_id: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )


class CharacterCreate(CharacterBase):
    pass

class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    personality: Optional[str] = None
    greeting: Optional[str] = None
    greetings: Optional[Any] = None
    secret: Optional[str] = None
    example_dialogs: Optional[Any] = None
    visibility: Optional[str] = None
    profile_image: Optional[str] = None
    album_images: Optional[Any] = None
    worldview_id: Optional[str] = None

    
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )


class Character(CharacterBase):
    id: str
    creator_id: str
    chat_count: int
    like_count: int
    created_at: datetime
    updated_at: datetime
    creator: Optional[CharacterCreator] = None

    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel
    )

