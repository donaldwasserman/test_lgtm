import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Table, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EventStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    cancelled = "cancelled"
    completed = "completed"


event_tags_association = Table(
    "event_tags",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    short_description: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[EventStatus] = mapped_column(Enum(EventStatus), default=EventStatus.draft, nullable=False)
    organizer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    venue_id: Mapped[int] = mapped_column(Integer, ForeignKey("venues.id"), nullable=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)
    max_attendees: Mapped[int] = mapped_column(Integer, nullable=True)
    price: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_virtual: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    virtual_link: Mapped[str] = mapped_column(String(500), nullable=True)
    cover_image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    organizer = relationship("User", back_populates="events_organized")
    venue = relationship("Venue", back_populates="events")
    category = relationship("Category", back_populates="events")
    tags = relationship("Tag", secondary="event_tags", back_populates="events")
    rsvps = relationship("Rsvp", back_populates="event")
    reviews = relationship("Review", back_populates="event")
    wishlist_items = relationship("WishlistItem", back_populates="event")
    invitations = relationship("Invitation", back_populates="event")
