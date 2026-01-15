import uuid
from typing import Any
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func
from datetime import datetime

class Base(AsyncAttrs, DeclarativeBase):
    pass
