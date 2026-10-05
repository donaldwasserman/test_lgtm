from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.category import Category as CategoryModel, Tag
from app.schemas.category import Category, Tag as TagSchema

router = APIRouter()


@router.get("/", response_model=List[Category])
async def read_categories(*, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(CategoryModel))
    return result.scalars().all()


@router.get("/tags", response_model=List[TagSchema])
async def read_tags(*, db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(Tag))
    return result.scalars().all()
