from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.db.base_class import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "User"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str | None] = mapped_column(String, nullable=True) # Null for OAuth
    avatar: Mapped[str | None] = mapped_column(String, nullable=True)
    name_changed: Mapped[bool] = mapped_column("nameChanged", Boolean, default=False)
    # google_id removed to match existing DB
    created_at: Mapped[datetime] = mapped_column("createdAt", DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column("updatedAt", DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    characters: Mapped[list["Character"]] = relationship(back_populates="creator", cascade="all, delete-orphan")
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    worldviews: Mapped[list["Worldview"]] = relationship(back_populates="creator", cascade="all, delete-orphan")
