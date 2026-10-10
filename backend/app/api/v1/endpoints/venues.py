from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.db.session import get_db
from app.models.venue import Venue as VenueModel
from app.schemas.venue import Venue, VenueCreate, VenueUpdate

router = APIRouter()


@router.get("/", response_model=List[Venue])
async def read_venues(*, db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    result = await db.execute(select(VenueModel).offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/", response_model=Venue)
async def create_venue(*, db: AsyncSession = Depends(get_db), venue_in: VenueCreate, current_user=Depends(deps.get_current_organizer)) -> Any:
    db_venue = VenueModel(**venue_in.model_dump())
    db.add(db_venue)
    await db.commit()
    await db.refresh(db_venue)
    return db_venue
