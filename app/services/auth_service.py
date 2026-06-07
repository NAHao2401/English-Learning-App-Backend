
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import (
    AuthResponse,
    ChangePasswordRequest,
    GoogleLoginRequest,
    LoginRequest,
    RegisterRequest,
)


def _build_auth_response(user: User) -> AuthResponse:
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user,
    )


def register_user(db: Session, data: RegisterRequest) -> dict:
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

    if not user or not user.password_hash or not verify_password(data.password, user.password_hash):
        raise ValueError("Invalid email or password")

    return _build_auth_response(user)


def login_with_google(db: Session, data: GoogleLoginRequest) -> AuthResponse:
    try:
        token_info = id_token.verify_oauth2_token(
            data.id_token,
            google_requests.Request(),
            settings.google_client_id,
        )
    except Exception:
        raise ValueError("Invalid Google token")

    email = token_info.get("email")
    name = token_info.get("name")
    picture = token_info.get("picture")
    email_verified = token_info.get("email_verified")

    if not email:
        raise ValueError("Google account does not contain email")

    if email_verified is False:
        raise ValueError("Google email is not verified")

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        user = User(
            name=name or email.split("@")[0],
            email=email,
            password_hash=None,
            avatar_url=picture,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        updated = False

        if picture and user.avatar_url != picture:
            user.avatar_url = picture
            updated = True

        if name and user.name != name:
            user.name = name
            updated = True

        if updated:
            db.add(user)
            db.commit()
            db.refresh(user)

    return _build_auth_response(user)


def change_user_password(
    db: Session,
    user: User,
    data: ChangePasswordRequest
) -> dict:
    if not user.password_hash:
        raise ValueError("This account uses Google sign-in and has no password")

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