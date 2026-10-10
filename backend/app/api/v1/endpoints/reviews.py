from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.db.session import get_db
from app.models.review import Review as ReviewModel
from app.schemas.review import Review, ReviewCreate

router = APIRouter()


@router.post("/", response_model=Review)
async def create_review(*, db: AsyncSession = Depends(get_db), review_in: ReviewCreate, current_user=Depends(deps.get_current_active_user)) -> Any:
    if review_in.rating < 1 or review_in.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    result = await db.execute(select(ReviewModel).where(and_(ReviewModel.user_id == current_user.id, ReviewModel.event_id == review_in.event_id)))
    existing = result.scalar_one_or_none()
    if existing:
        existing.rating = review_in.rating
        existing.comment = review_in.comment
        db.add(existing)
        await db.commit()
        await db.refresh(existing)
        return existing
    db_review = ReviewModel(user_id=current_user.id, event_id=review_in.event_id, rating=review_in.rating, comment=review_in.comment)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review


@router.get("/event/{event_id}", response_model=List[Review])
async def read_event_reviews(*, db: AsyncSession = Depends(get_db), event_id: int) -> Any:
    result = await db.execute(select(ReviewModel).where(ReviewModel.event_id == event_id))
    return result.scalars().all()
