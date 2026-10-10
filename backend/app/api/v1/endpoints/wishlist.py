from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.db.session import get_db
from app.models.wishlist import WishlistItem as WishlistModel
from app.schemas.wishlist import WishlistItem

router = APIRouter()


@router.get("/me", response_model=List[WishlistItem])
async def read_wishlist(*, db: AsyncSession = Depends(get_db), current_user=Depends(deps.get_current_active_user)) -> Any:
    result = await db.execute(select(WishlistModel).where(WishlistModel.user_id == current_user.id))
    return result.scalars().all()


@router.post("/events/{event_id}")
async def add_to_wishlist(*, db: AsyncSession = Depends(get_db), event_id: int, current_user=Depends(deps.get_current_active_user)) -> Any:
    result = await db.execute(select(WishlistModel).where(and_(WishlistModel.user_id == current_user.id, WishlistModel.event_id == event_id)))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Already in wishlist")
    item = WishlistModel(user_id=current_user.id, event_id=event_id)
    db.add(item)
    await db.commit()
    return {"message": "added to wishlist"}


@router.delete("/events/{event_id}")
async def remove_from_wishlist(*, db: AsyncSession = Depends(get_db), event_id: int, current_user=Depends(deps.get_current_active_user)) -> Any:
    result = await db.execute(select(WishlistModel).where(and_(WishlistModel.user_id == current_user.id, WishlistModel.event_id == event_id)))
    existing = result.scalar_one_or_none()
    if not existing:
        raise HTTPException(status_code=404, detail="Not in wishlist")
    await db.delete(existing)
    await db.commit()
    return {"message": "removed from wishlist"}
