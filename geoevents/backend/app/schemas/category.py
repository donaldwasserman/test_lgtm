from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    slug: str
    icon: Optional[str] = None


class Category(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Tag(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
