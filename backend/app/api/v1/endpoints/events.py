from typing import Any, List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, desc, or_, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api import deps
from app.db.session import get_db
from app.models.event import Event as EventModel, EventStatus
from app.models.rsvp import Rsvp, RsvpStatus
from app.models.category import Tag
from app.schemas.event import Event, EventCreate, EventUpdate

router = APIRouter()


@router.get("/", response_model=List[Event])
async def read_events(
    *,
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[EventStatus] = EventStatus.published,
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    featured: Optional[bool] = Query(None),
) -> Any:
    query = select(EventModel).options(
        selectinload(EventModel.organizer),
        selectinload(EventModel.venue),
        selectinload(EventModel.category),
        selectinload(EventModel.tags),
    )
    if status:
        query = query.where(EventModel.status == status)
    if search:
        query = query.where(
            or_(
                EventModel.title.ilike(f"%{search}%"),
                EventModel.description.ilike(f"%{search}%"),
                EventModel.short_description.ilike(f"%{search}%"),
            )
        )
    if category_id:
        query = query.where(EventModel.category_id == category_id)
    if featured is not None:
        query = query.where(EventModel.is_featured == featured)
    query = query.order_by(desc(EventModel.start_date)).offset(skip).limit(limit)
    result = await db.execute(query)
    events = result.scalars().all()
    events_out = []
    for event in events:
        event_dict = Event.model_validate(event).model_dump()
        attendee_result = await db.execute(
            select(func.count()).select_from(Rsvp).where(Rsvp.event_id == event.id, Rsvp.status == RsvpStatus.attending)
        )
        event_dict["attendee_count"] = attendee_result.scalar() or 0
        events_out.append(event_dict)
    return events_out


@router.get("/{event_id}", response_model=Event)
async def read_event(*, db: AsyncSession = Depends(get_db), event_id: int) -> Any:
    query = select(EventModel).options(
        selectinload(EventModel.organizer),
        selectinload(EventModel.venue),
        selectinload(EventModel.category),
        selectinload(EventModel.tags),
    ).where(EventModel.id == event_id)
    result = await db.execute(query)
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event.view_count += 1
    db.add(event)
    await db.commit()
    await db.refresh(event)
    event_dict = Event.model_validate(event).model_dump()
    attendee_result = await db.execute(
        select(func.count()).select_from(Rsvp).where(Rsvp.event_id == event.id, Rsvp.status == RsvpStatus.attending)
    )
    event_dict["attendee_count"] = attendee_result.scalar() or 0
    return event_dict


@router.post("/", response_model=Event)
async def create_event(
    *,
    db: AsyncSession = Depends(get_db),
    event_in: EventCreate,
    current_user=Depends(deps.get_current_organizer),
) -> Any:
    from slugify import slugify  # simple slug
    import re

    slug_base = slugify(event_in.title)
    slug = slug_base or re.sub(r'[^a-z0-9]+', '-', event_in.title.lower())
    # ensure uniqueness
    i = 1
    base_slug = slug
    while True:
        check = await db.execute(select(EventModel).where(EventModel.slug == slug))
        if not check.scalar_one_or_none():
            break
        slug = f"{base_slug}-{i}"
        i += 1

    db_event = EventModel(
        title=event_in.title,
        slug=slug,
        description=event_in.description,
        short_description=event_in.short_description,
        organizer_id=current_user.id,
        venue_id=event_in.venue_id,
        category_id=event_in.category_id,
        start_date=event_in.start_date,
        end_date=event_in.end_date,
        timezone=event_in.timezone,
        max_attendees=event_in.max_attendees,
        price=event_in.price,
        is_virtual=event_in.is_virtual,
        virtual_link=event_in.virtual_link,
        cover_image_url=event_in.cover_image_url,
        status=EventStatus.draft,
    )
    if event_in.tag_ids:
        tags_result = await db.execute(select(Tag).where(Tag.id.in_(event_in.tag_ids)))
        db_event.tags = list(tags_result.scalars().all())
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    fresh = await db.execute(
        select(EventModel).options(
            selectinload(EventModel.organizer),
            selectinload(EventModel.venue),
            selectinload(EventModel.category),
            selectinload(EventModel.tags),
        ).where(EventModel.id == db_event.id)
    )
    created = fresh.scalar_one()
    event_dict = Event.model_validate(created).model_dump()
    event_dict["attendee_count"] = 0
    return event_dict
