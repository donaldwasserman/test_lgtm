from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class InvitationBase(BaseModel):
    event_id: int
    invitee_email: EmailStr


class InvitationCreate(InvitationBase):
    pass


class Invitation(InvitationBase):
    id: int
    inviter_id: int
    status: str
    created_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True
