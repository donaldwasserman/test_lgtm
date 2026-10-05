from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BadgeBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    icon_url: Optional[str] = None
    criteria: Optional[str] = None


class Badge(BadgeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
