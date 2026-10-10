from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class EventBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    short_description: Optional[str] = Field(None, max_length=500)
    venue_id: Optional[int] = None
    category_id: Optional[int] = None
    start_date: datetime
    end_date: datetime
    timezone: str = Field(default="UTC", max_length=50)
    max_attendees: Optional[int] = None
    price: float = Field(default=0.0, ge=0)
    is_virtual: bool = False
    virtual_link: Optional[str] = None
    cover_image_url: Optional[str] = None


class EventCreate(EventBase):
    tag_ids: List[int] = []


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    status: Optional[str] = None
    venue_id: Optional[int] = None
    category_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_attendees: Optional[int] = None
    price: Optional[float] = None
    is_virtual: Optional[bool] = None
    virtual_link: Optional[str] = None
    cover_image_url: Optional[str] = None
    tag_ids: Optional[List[int]] = None


class EventInDB(EventBase):
    id: int
    slug: str
    status: str
    organizer_id: int
    is_featured: bool
    view_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Event(EventInDB):
    organizer: Optional[dict] = None
    venue: Optional[dict] = None
    category: Optional[dict] = None
    tags: List[dict] = []
    attendee_count: Optional[int] = None
