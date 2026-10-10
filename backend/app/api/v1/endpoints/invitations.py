from datetime import datetime, timedelta, timezone
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.db.session import get_db
from app.models.invitation import Invitation as InvitationModel, InvitationStatus
from app.schemas.invitation import Invitation, InvitationCreate

router = APIRouter()


@router.post("/", response_model=Invitation)
async def create_invitation(*, db: AsyncSession = Depends(get_db), inv_in: InvitationCreate, current_user=Depends(deps.get_current_organizer)) -> Any:
    db_inv = InvitationModel(
        event_id=inv_in.event_id,
        inviter_id=current_user.id,
        invitee_email=inv_in.invitee_email,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )
    db.add(db_inv)
    await db.commit()
    await db.refresh(db_inv)
    return db_inv


@router.get("/me", response_model=List[Invitation])
async def read_my_invitations(*, db: AsyncSession = Depends(get_db), current_user=Depends(deps.get_current_active_user)) -> Any:
    result = await db.execute(select(InvitationModel).where(InvitationModel.invitee_email == current_user.email))
    return result.scalars().all()
