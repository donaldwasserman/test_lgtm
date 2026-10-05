from datetime import datetime

from pydantic import BaseModel


class RsvpBase(BaseModel):
    event_id: int
    status: str


class RsvpCreate(RsvpBase):
    pass


class RsvpUpdate(BaseModel):
    status: str


class Rsvp(RsvpBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
