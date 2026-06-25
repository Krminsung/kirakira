"""
Credit Management Service

Handles all credit-related operations including:
- Balance checking
- Credit deduction
- Credit addition
- Daily free credits
- Transaction history
"""

from datetime import datetime, timedelta, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.credit import CreditTransaction
from uuid import uuid4

# Credit costs per message
CREDIT_COSTS = {
    "gemini-2.5-flash": 3,
    "gemini-3-flash": 5,
    "exaone-236b": 1,
    "cukee-ai": 1,
    "image-generation": 10,
}

# Daily credit settings
DAILY_FREE_CREDITS = 50
MAX_CREDIT_BALANCE = 200
INITIAL_SIGNUP_CREDITS = 100


async def get_user_balance(session: AsyncSession, user_id: str) -> int:
    """Get current credit balance for user"""
    result = await session.execute(
        select(User.kira_balance).where(User.id == user_id)
    )
    balance = result.scalar()
    return balance if balance is not None else 0


async def check_sufficient_credits(session: AsyncSession, user_id: str, amount: int) -> bool:
    """Check if user has sufficient credits"""
    balance = await get_user_balance(session, user_id)
    return balance >= amount


async def deduct_credits(
    session: AsyncSession, 
    user_id: str, 
    amount: int, 
    description: str = "메시지 전송"
) -> dict:
    """
    Deduct credits from user balance
    Returns: {"success": bool, "balance": int, "message": str}
    """
    # Get current balance
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()
    
    if not user:
        return {"success": False, "balance": 0, "message": "사용자를 찾을 수 없습니다"}
    
    if user.kira_balance < amount:
        return {
            "success": False, 
            "balance": user.kira_balance, 
            "message": f"크레딧이 부족합니다. 필요: {amount}, 보유: {user.kira_balance}"
        }
    
    # Deduct credits
    new_balance = user.kira_balance - amount
    await session.execute(
        update(User)
        .where(User.id == user_id)
        .values(kira_balance=new_balance)
    )
    
    # Log transaction
    transaction = CreditTransaction(
        id=str(uuid4()),
        user_id=user_id,
        amount=-amount,  # Negative for spending
        transaction_type="spend",
        description=description,
        balance_after=new_balance
    )
    session.add(transaction)
    await session.commit()
    
    return {
        "success": True, 
        "balance": new_balance, 
        "message": f"{amount} 크레딧 차감됨"
    }


async def add_credits(
    session: AsyncSession, 
    user_id: str, 
    amount: int, 
    transaction_type: str = "earn",
    description: str = "크레딧 추가"
) -> dict:
    """
    Add credits to user balance
    Returns: {"success": bool, "balance": int, "message": str}
    """
    # Get current balance
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()
    
    if not user:
        return {"success": False, "balance": 0, "message": "사용자를 찾을 수 없습니다"}
    
    # Add credits
    new_balance = user.kira_balance + amount
    await session.execute(
        update(User)
        .where(User.id == user_id)
        .values(kira_balance=new_balance)
    )
    
    # Log transaction
    transaction = CreditTransaction(
        id=str(uuid4()),
        user_id=user_id,
        amount=amount,  # Positive for earning
        transaction_type=transaction_type,
        description=description,
        balance_after=new_balance
    )
    session.add(transaction)
    await session.commit()
    
    return {
        "success": True, 
        "balance": new_balance, 
        "message": f"{amount} 크레딧 추가됨"
    }


async def claim_daily_credits(session: AsyncSession, user_id: str) -> dict:
    """
    Claim daily free credits
    Returns: {"success": bool, "balance": int, "message": str, "next_claim": datetime}
    """
    # Get user
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()
    
    if not user:
        return {"success": False, "balance": 0, "message": "사용자를 찾을 수 없습니다"}
    
    now = datetime.now(timezone.utc)
    
    # Check if already claimed today
    if user.last_daily_credit:
        time_since_last = now - user.last_daily_credit
        if time_since_last < timedelta(hours=24):
            next_claim = user.last_daily_credit + timedelta(hours=24)
            hours_left = (next_claim - now).total_seconds() / 3600
            return {
                "success": False,
                "balance": user.kira_balance,
                "message": f"오늘 이미 받았습니다. 다음 수령까지 {hours_left:.1f}시간 남음",
                "next_claim": next_claim
            }
    
    # Check max balance limit
    if user.kira_balance >= MAX_CREDIT_BALANCE:
        return {
            "success": False,
            "balance": user.kira_balance,
            "message": f"최대 보유량({MAX_CREDIT_BALANCE} 키라)에 도달했습니다. 먼저 사용해주세요!"
        }
    
    # Calculate credits to give (don't exceed max)
    credits_to_give = min(DAILY_FREE_CREDITS, MAX_CREDIT_BALANCE - user.kira_balance)
    new_balance = user.kira_balance + credits_to_give
    
    # Update user
    await session.execute(
        update(User)
        .where(User.id == user_id)
        .values(
            kira_balance=new_balance,
            last_daily_credit=now
        )
    )
    
    # Log transaction
    transaction = CreditTransaction(
        id=str(uuid4()),
        user_id=user_id,
        amount=credits_to_give,
        transaction_type="daily",
        description="일일 무료 크레딧",
        balance_after=new_balance
    )
    session.add(transaction)
    await session.commit()
    
    next_claim = now + timedelta(hours=24)
    return {
        "success": True,
        "balance": new_balance,
        "message": f"일일 크레딧 {credits_to_give}개를 받았습니다!",
        "next_claim": next_claim
    }


async def get_credit_history(
    session: AsyncSession, 
    user_id: str, 
    limit: int = 50
) -> list[dict]:
    """Get credit transaction history"""
    result = await session.execute(
        select(CreditTransaction)
        .where(CreditTransaction.user_id == user_id)
        .order_by(CreditTransaction.created_at.desc())
        .limit(limit)
    )
    transactions = result.scalars().all()
    
    return [
        {
            "id": t.id,
            "amount": t.amount,
            "type": t.transaction_type,
            "description": t.description,
            "balance_after": t.balance_after,
            "created_at": t.created_at.isoformat()
        }
        for t in transactions
    ]


def get_model_cost(model_name: str) -> int:
    """Get credit cost for a model"""
    # Normalize model name
    model_lower = model_name.lower()
    
    if "exaone" in model_lower:
        return CREDIT_COSTS["exaone-236b"]
    elif "cukee" in model_lower:
        return CREDIT_COSTS["cukee-ai"]
    elif "3" in model_lower and "flash" in model_lower:
        return CREDIT_COSTS["gemini-3-flash"]
    else:
        return CREDIT_COSTS["gemini-2.5-flash"]
