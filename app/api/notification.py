from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.notification import DeviceTokenRequest
from app.services.notification_service import register_device_token, unregister_device_token

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post("/device-tokens", status_code=status.HTTP_204_NO_CONTENT)
def register_token(
    request: DeviceTokenRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    register_device_token(db, current_user.id, request.token, request.platform)


@router.delete("/device-tokens", status_code=status.HTTP_204_NO_CONTENT)
def unregister_token(
    request: DeviceTokenRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    unregister_device_token(db, current_user.id, request.token)
