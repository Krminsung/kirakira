from datetime import datetime, timedelta, timezone

def get_kst_today_start() -> datetime:
    """
    Returns the UTC datetime corresponding to the start of the current day in KST.
    Legacy Logic:
    - Get KST curret time
    - Truncate to midnight
    - Return as UTC
    """
    # KST is UTC+9
    kst_tz = timezone(timedelta(hours=9))
    
    # Current time in UTC
    now_utc = datetime.now(timezone.utc)
    
    # Convert to KST
    now_kst = now_utc.astimezone(kst_tz)
    
    # Truncate to start of day
    kst_start_of_day = now_kst.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Convert back to UTC
    return kst_start_of_day.astimezone(timezone.utc)
