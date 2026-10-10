from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.db.session import get_db
from app.models.event import Event as EventModel, EventStatus
from app.models.rsvp import Rsvp, RsvpStatus
from app.models.user import User as UserModel

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(*, db: AsyncSession = Depends(get_db), current_user=Depends(deps.get_current_organizer)) -> Any:
    total_events = await db.execute(select(func.count()).select_from(EventModel).where(EventModel.organizer_id == current_user.id))
    published_events = await db.execute(
        select(func.count()).select_from(EventModel).where(
            EventModel.organizer_id == current_user.id, EventModel.status == EventStatus.published
        )
    )
    total_attendees = await db.execute(
        select(func.count()).select_from(Rsvp)
        .join(EventModel)
        .where(EventModel.organizer_id == current_user.id, Rsvp.status == RsvpStatus.attending)
    )
    return {
        "total_events": total_events.scalar() or 0,
        "published_events": published_events.scalar() or 0,
        "total_attendees": total_attendees.scalar() or 0,
    }
