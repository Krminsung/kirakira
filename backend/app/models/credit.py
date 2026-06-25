from datetime import datetime
from uuid import uuid4
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base_class import Base

class CreditTransaction(Base):
    """Credit transaction history"""
    __tablename__ = "credit_transactions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)  # Positive for earn, negative for spend
    transaction_type: Mapped[str] = mapped_column(String(20), nullable=False)  # 'earn', 'spend', 'daily', 'signup'
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    balance_after: Mapped[int] = mapped_column(Integer, nullable=False)  # Balance after this transaction
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
