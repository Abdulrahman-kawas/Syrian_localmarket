"""Current-user router: profile-adjacent actions like location updates."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_verified_user
from app.db.postgis import make_point
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import LatLng
from app.schemas.interactions import OkResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.put("/me/location", response_model=OkResponse)
def update_my_location(
    payload: LatLng,
    db: Session = Depends(get_db),
    user: User = Depends(get_verified_user),
) -> OkResponse:
    """Store the caller's last-known location (used for proximity notifications)."""
    user.last_location = make_point(payload.latitude, payload.longitude)
    db.commit()
    return OkResponse()
