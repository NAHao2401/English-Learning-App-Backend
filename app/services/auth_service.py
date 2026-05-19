from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import AuthResponse, ChangePasswordRequest, LoginRequest, RegisterRequest


def register_user(db: Session, data: RegisterRequest) -> AuthResponse:
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise ValueError("Email already exists")

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully",
    }


def login_user(db: Session, data: LoginRequest) -> AuthResponse:
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise ValueError("Invalid email or password")

    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user
    )

def change_user_password(
    db: Session,
    user: User,
    data: ChangePasswordRequest
) -> dict:
    if not verify_password(data.current_password, user.password_hash):
        raise ValueError("Current password is incorrect")

    if verify_password(data.new_password, user.password_hash):
        raise ValueError("New password must be different from current password")

    user.password_hash = hash_password(data.new_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Password changed successfully"
    }