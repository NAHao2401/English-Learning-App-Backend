import hashlib
import logging
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import firebase_admin
from firebase_admin import credentials, messaging
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.logging import setup_logging
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.device_token import DeviceToken
from app.models.review_notification_state import ReviewNotificationState
from app.models.user_vocabulary import UserVocabulary

logger = logging.getLogger(__name__)
JOB_LOCK_ID = 1480674649
REVIEW_ACTIVITY_COOLDOWN = timedelta(minutes=5)


def _initialize_firebase() -> None:
    try:
        firebase_admin.get_app()
    except ValueError:
        credential = (
            credentials.Certificate(settings.firebase_credentials_path)
            if settings.firebase_credentials_path
            else None
        )
        firebase_admin.initialize_app(credential)


def _build_signature(vocabulary_ids: list[int]) -> str:
    raw_ids = ",".join(str(vocabulary_id) for vocabulary_id in vocabulary_ids)
    return hashlib.sha256(raw_ids.encode("ascii")).hexdigest()


def _get_due_vocabularies_by_user(db: Session) -> dict[int, list[int]]:
    rows = db.execute(
        select(
            UserVocabulary.user_id,
            UserVocabulary.vocabulary_id,
        )
        .where(
            UserVocabulary.mastery_level > 0,
            UserVocabulary.next_review_at.isnot(None),
            UserVocabulary.next_review_at <= func.now(),
        )
        .order_by(UserVocabulary.user_id, UserVocabulary.vocabulary_id)
    ).all()

    due_by_user: dict[int, list[int]] = defaultdict(list)
    for user_id, vocabulary_id in rows:
        due_by_user[user_id].append(vocabulary_id)
    return due_by_user


def _send_review_reminder(token: str, due_count: int) -> None:
    messaging.send(
        messaging.Message(
            token=token,
            data={
                "type": "vocabulary_review",
                "due_count": str(due_count),
            },
            android=messaging.AndroidConfig(priority="high"),
        )
    )


def send_due_review_notifications(db: Session) -> None:
    lock_acquired = db.execute(
        select(func.pg_try_advisory_xact_lock(JOB_LOCK_ID))
    ).scalar_one()
    if not lock_acquired:
        logger.info("Another review notification job is already running")
        return

    due_by_user = _get_due_vocabularies_by_user(db)
    if not due_by_user:
        logger.info("No vocabulary review notifications are due")
        return

    tokens = (
        db.query(DeviceToken)
        .filter(DeviceToken.user_id.in_(due_by_user))
        .order_by(DeviceToken.user_id, DeviceToken.updated_at.desc())
        .all()
    )
    if not tokens:
        logger.info("No registered device tokens found for due vocabulary reviews")
        return

    _initialize_firebase()

    states = {
        state.user_id: state
        for state in db.query(ReviewNotificationState)
        .filter(ReviewNotificationState.user_id.in_(due_by_user))
        .all()
    }
    tokens_by_user: dict[int, list[DeviceToken]] = defaultdict(list)
    for device_token in tokens:
        tokens_by_user[device_token.user_id].append(device_token)

    now = datetime.now(timezone.utc)
    sent_count = 0
    removed_count = 0
    for user_id, due_vocabulary_ids in due_by_user.items():
        state = states.get(user_id)
        if state is not None and state.last_review_activity_at is not None:
            last_review_activity_at = state.last_review_activity_at
            if last_review_activity_at.tzinfo is None:
                last_review_activity_at = last_review_activity_at.replace(tzinfo=timezone.utc)
            if now - last_review_activity_at < REVIEW_ACTIVITY_COOLDOWN:
                continue

        signature = _build_signature(due_vocabulary_ids)
        if state is not None and state.last_review_signature == signature:
            continue

        for device_token in tokens_by_user[user_id]:
            try:
                _send_review_reminder(device_token.token, len(due_vocabulary_ids))
            except messaging.UnregisteredError:
                db.delete(device_token)
                removed_count += 1
                logger.info("Removed unregistered FCM token id=%s", device_token.id)
            except Exception:
                logger.exception("Unable to send FCM reminder to token id=%s", device_token.id)
                break
            else:
                if state is None:
                    state = ReviewNotificationState(user_id=user_id)
                    db.add(state)
                    states[user_id] = state
                state.last_review_signature = signature
                state.last_notified_at = now
                sent_count += 1
                break

    db.commit()
    logger.info(
        "Vocabulary review notification job complete: sent=%s removed_tokens=%s",
        sent_count,
        removed_count,
    )


def main() -> None:
    setup_logging()
    db = SessionLocal()
    try:
        send_due_review_notifications(db)
    except Exception:
        db.rollback()
        logger.exception("Vocabulary review notification job failed")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
