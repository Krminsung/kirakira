from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from pydantic.alias_generators import to_camel

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str | None = None

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    password: str | None = None
    avatar: str | None = None
    
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )

class UserInDBBase(UserBase):
    id: str
    avatar: str | None = None
    name_changed: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel
    )

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password: str | None = None

class UserUpdateName(BaseModel):
    name: str

class UserUpdateAvatar(BaseModel):
    imageData: str
