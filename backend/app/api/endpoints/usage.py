from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from datetime import datetime, time, timezone

from app.api import deps
from app.models.usage import ApiUsageLog

router = APIRouter()

@router.get("")
async def read_usage(
    current_user: deps.CurrentUser,
    session: deps.SessionDep
) -> Any:
    """
    Get user API usage statistics.
    """
    # Start of today (UTC)
    now = datetime.now(timezone.utc)
    start_of_day = datetime.combine(now.date(), time.min, tzinfo=timezone.utc)
    
    # Query counts
    usage_stats = {
        "gemini-2.5-flash": 0,
        "gemini-3-flash": 0,
        "exaone-236b": 0
    }
    
    # Group by model
    query = (
        select(ApiUsageLog.model, func.count(ApiUsageLog.id))
        .where(ApiUsageLog.user_id == current_user.id)
        .where(ApiUsageLog.used_at >= start_of_day)
        .group_by(ApiUsageLog.model)
    )
    
    result = await session.execute(query)
    for model, count in result.all():
        # Lowercase and handle variants if any
        m_lower = model.lower()
        if m_lower in usage_stats:
            usage_stats[m_lower] = count
            
    return {
        "usage": {
            "gemini-2.5-flash": {
                "used": usage_stats["gemini-2.5-flash"], 
                "limit": 300,
                "remaining": max(0, 300 - usage_stats["gemini-2.5-flash"])
            },
            "gemini-3-flash": {
                "used": usage_stats["gemini-3-flash"],
                "limit": 30,
                "remaining": max(0, 30 - usage_stats["gemini-3-flash"])
            },
            "exaone-236b": {
                "used": usage_stats["exaone-236b"],
                "limit": 1000,
                "remaining": max(0, 1000 - usage_stats["exaone-236b"])
            }

        }
    }



