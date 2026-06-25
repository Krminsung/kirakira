"""
Credit API Endpoints

Handles credit-related API requests:
- Get balance and info
- Claim daily free credits
- Get transaction history
"""

from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.api import deps
from app.services import credit_system
from app.models.user import User

router = APIRouter()


@router.get("")
async def get_credits(
    current_user: deps.CurrentUser,
    session: deps.SessionDep
) -> Any:
    """
    Get current credit balance and info
    """
    balance = await credit_system.get_user_balance(session, current_user.id)
    
    # Get user info for last daily claim
    result = await session.execute(
        select(User).where(User.id == current_user.id)
    )
    user = result.scalars().first()
    
    # Calculate next daily claim time
    from datetime import datetime, timedelta, timezone
    next_claim = None
    can_claim_daily = True
    
    if user and user.last_daily_credit:
        next_claim_time = user.last_daily_credit + timedelta(hours=24)
        next_claim = next_claim_time.isoformat()
        can_claim_daily = datetime.now(timezone.utc) >= next_claim_time
    
    return {
        "balance": balance,
        "max_balance": credit_system.MAX_CREDIT_BALANCE,
        "daily_free_amount": credit_system.DAILY_FREE_CREDITS,
        "can_claim_daily": can_claim_daily,
        "next_daily_claim": next_claim,
        "costs": {
            "gemini_2_5_flash": credit_system.CREDIT_COSTS["gemini-2.5-flash"],
            "gemini_3_flash": credit_system.CREDIT_COSTS["gemini-3-flash"],
            "exaone": credit_system.CREDIT_COSTS["exaone-236b"],
            "image_generation": credit_system.CREDIT_COSTS["image-generation"]
        }
    }


@router.post("/daily")
async def claim_daily_credits(
    current_user: deps.CurrentUser,
    session: deps.SessionDep
) -> Any:
    """
    Claim daily free credits
    """
    result = await credit_system.claim_daily_credits(session, current_user.id)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return {
        "success": True,
        "balance": result["balance"],
        "message": result["message"],
        "next_claim": result.get("next_claim")
    }


@router.get("/history")
async def get_credit_history(
    current_user: deps.CurrentUser,
    session: deps.SessionDep,
    limit: int = 50
) -> Any:
    """
    Get credit transaction history
    """
    history = await credit_system.get_credit_history(session, current_user.id, limit)
    
    return {
        "transactions": history,
        "total": len(history)
    }
