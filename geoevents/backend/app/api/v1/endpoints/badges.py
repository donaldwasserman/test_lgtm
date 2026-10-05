from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.db.session import get_db
from app.models.badge import Badge as BadgeModel, user_badges_association
from app.schemas.badge import Badge

router = APIRouter()


@router.get("/", response_model=List[Badge])
async def read_badges(*, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(BadgeModel))
    return result.scalars().all()


@router.get("/me", response_model=List[Badge])
async def read_my_badges(*, db: AsyncSession = Depends(get_db), current_user=Depends(deps.get_current_active_user)) -> Any:
    result = await db.execute(
        select(BadgeModel).join(user_badges_association).where(user_badges_association.c.user_id == current_user.id)
    )
    return result.scalars().all()
