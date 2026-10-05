from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class VenueBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    address: str = Field(..., max_length=500)
    city: str = Field(..., max_length=100)
    country: str = Field(..., max_length=100)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    capacity: Optional[int] = None
    image_url: Optional[str] = None


class VenueCreate(VenueBase):
    pass


class VenueUpdate(VenueBase):
    pass


class VenueInDB(VenueBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Venue(VenueInDB):
    pass
