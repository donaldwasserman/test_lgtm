from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.db.session import get_db
from app.models.notification import Notification as NotificationModel

router = APIRouter()


@router.get("/me", response_model=List[NotificationModel])
async def read_my_notifications(*, db: AsyncSession = Depends(get_db), current_user=Depends(deps.get_current_active_user), skip: int = 0, limit: int = 100) -> Any:
    result = await db.execute(select(NotificationModel).where(NotificationModel.user_id == current_user.id).order_by(NotificationModel.created_at.desc()).offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/{notification_id}/read")
async def mark_read(*, db: AsyncSession = Depends(get_db), notification_id: int, current_user=Depends(deps.get_current_active_user)) -> Any:
    notif = await db.get(NotificationModel, notification_id)
    if not notif or notif.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif.is_read = True
    db.add(notif)
    await db.commit()
    return {"message": "marked as read"}
