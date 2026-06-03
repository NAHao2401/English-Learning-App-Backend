from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.device_token import DeviceToken


def register_device_token(db: Session, user_id: int, token: str, platform: str) -> None:
    statement = insert(DeviceToken).values(user_id=user_id, token=token, platform=platform)
    statement = statement.on_conflict_do_update(
        index_elements=[DeviceToken.token],
        set_={
            "user_id": statement.excluded.user_id,
            "platform": statement.excluded.platform,
            "updated_at": func.now(),
        },
    )
    db.execute(statement)
    db.commit()


def unregister_device_token(db: Session, user_id: int, token: str) -> None:
    db.query(DeviceToken).filter(
        DeviceToken.user_id == user_id,
        DeviceToken.token == token,
    ).delete(synchronize_session=False)
    db.commit()
