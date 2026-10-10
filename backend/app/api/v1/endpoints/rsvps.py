from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.db.session import get_db
from app.models.rsvp import Rsvp as RsvpModel, RsvpStatus
from app.models.event import Event as EventModel
from app.schemas.rsvp import Rsvp, RsvpCreate, RsvpUpdate

router = APIRouter()


@router.post("/", response_model=Rsvp)
async def create_rsvp(*, db: AsyncSession = Depends(get_db), rsvp_in: RsvpCreate, current_user=Depends(deps.get_current_active_user)) -> Any:
    event = await db.get(EventModel, rsvp_in.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    result = await db.execute(select(RsvpModel).where(and_(RsvpModel.user_id == current_user.id, RsvpModel.event_id == rsvp_in.event_id)))
    existing = result.scalar_one_or_none()
    if existing:
        existing.status = rsvp_in.status
        db.add(existing)
        await db.commit()
        await db.refresh(existing)
        return existing
    db_rsvp = RsvpModel(user_id=current_user.id, event_id=rsvp_in.event_id, status=rsvp_in.status)
    db.add(db_rsvp)
    await db.commit()
    await db.refresh(db_rsvp)
    return db_rsvp


@router.get("/me", response_model=List[Rsvp])
async def read_my_rsvps(*, db: AsyncSession = Depends(get_db), current_user=Depends(deps.get_current_active_user)) -> Any:
    result = await db.execute(select(RsvpModel).where(RsvpModel.user_id == current_user.id))
    return result.scalars().all()
