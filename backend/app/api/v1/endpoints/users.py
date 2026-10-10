from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.db.session import get_db
from app.models.user import User as UserModel
from app.schemas.user import User, UserUpdate

router = APIRouter()


@router.get("/me", response_model=User)
async def read_user_me(current_user: UserModel = Depends(deps.get_current_active_user)) -> Any:
    return current_user


@router.put("/me", response_model=User)
async def update_user_me(*, db: AsyncSession = Depends(get_db), user_in: UserUpdate, current_user: UserModel = Depends(deps.get_current_active_user)) -> Any:
    current_user.full_name = user_in.full_name or current_user.full_name
    current_user.bio = user_in.bio or current_user.bio
    current_user.avatar_url = user_in.avatar_url or current_user.avatar_url
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.get("/{user_id}", response_model=User)
async def read_user(*, db: AsyncSession = Depends(get_db), user_id: int) -> Any:
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=List[User])
async def read_users(*, db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    result = await db.execute(select(UserModel).offset(skip).limit(limit))
    return result.scalars().all()
