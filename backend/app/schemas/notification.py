from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NotificationBase(BaseModel):
    type: str
    title: str
    message: str


class Notification(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    data: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True