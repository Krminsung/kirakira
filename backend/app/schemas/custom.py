from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional, List, Any

# Upload Schemas
class UploadRequest(BaseModel):
    file: str # Base64 string
    type: str = "profile"

# Chat Image Schemas
class ChatMessage(BaseModel):
    role: str
    content: str

class ImageGenerationRequest(BaseModel):
    messages: List[ChatMessage]
    character_name: str
    conversation_id: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )

