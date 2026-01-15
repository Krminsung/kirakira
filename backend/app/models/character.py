from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.db.base_class import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Worldview(Base):
    __tablename__ = "Worldview"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    creator_id: Mapped[str] = mapped_column("creatorId", ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column("createdAt", DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column("updatedAt", DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    creator: Mapped["User"] = relationship(back_populates="worldviews")
    characters: Mapped[list["Character"]] = relationship(back_populates="worldview")


class Character(Base):
    __tablename__ = "Character"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    personality: Mapped[str | None] = mapped_column(Text, nullable=True)
    greeting: Mapped[str] = mapped_column(Text, nullable=False)
    greetings: Mapped[str | None] = mapped_column(Text, nullable=True) # JSON string or text
    secret: Mapped[str | None] = mapped_column(Text, nullable=True)
    example_dialogs: Mapped[str | None] = mapped_column("exampleDialogs", Text, nullable=True)
    visibility: Mapped[str] = mapped_column(String, default='PRIVATE') # 'PUBLIC', 'PRIVATE'
    profile_image: Mapped[str | None] = mapped_column("profileImage", String, nullable=True)
    album_images: Mapped[str | None] = mapped_column("albumImages", Text, nullable=True) # JSON string
    creator_id: Mapped[str] = mapped_column("creatorId", ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    worldview_id: Mapped[str | None] = mapped_column("worldviewId", ForeignKey("Worldview.id", ondelete="SET NULL"), nullable=True)
    chat_count: Mapped[int] = mapped_column("chatCount", Integer, default=0)
    like_count: Mapped[int] = mapped_column("likeCount", Integer, default=0)
    created_at: Mapped[datetime] = mapped_column("createdAt", DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column("updatedAt", DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    creator: Mapped["User"] = relationship(back_populates="characters")
    worldview: Mapped["Worldview"] = relationship(back_populates="characters")
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="character", cascade="all, delete-orphan")
