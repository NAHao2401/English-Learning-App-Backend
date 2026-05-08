from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.progress import ReviewHistory, XpHistory
from app.models.user import User
from app.models.user_vocabulary import UserVocabulary
from app.models.vocabulary import Vocabulary

REVIEW_INTERVALS = {
    0: 0,
    1: 1,
    2: 2,
    3: 4,
    4: 8,
    5: 16,
}

RATING_TO_RESULT = {
    1: "unknown",
    3: "familiar",
    5: "mastered",
}

XP_BY_RATING = {
    1: 1,
    3: 3,
    5: 5,
}


def get_next_review_at(mastery_level: int, last_reviewed_at: datetime) -> datetime:
    days = REVIEW_INTERVALS.get(mastery_level, 1)
    return last_reviewed_at + timedelta(days=days)


def _normalize_datetime(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def rate_vocabulary(db: Session, user_id: int, vocabulary_id: int, rating: int) -> UserVocabulary:
    now = datetime.now(timezone.utc)

    vocabulary_exists = db.query(Vocabulary.id).filter(Vocabulary.id == vocabulary_id).first()
    if vocabulary_exists is None:
        raise ValueError("Vocabulary not found")

    user_vocab = (
        db.query(UserVocabulary)
        .filter(
            UserVocabulary.user_id == user_id,
            UserVocabulary.vocabulary_id == vocabulary_id,
        )
        .first()
    )

    if user_vocab is None:
        user_vocab = UserVocabulary(
            user_id=user_id,
            vocabulary_id=vocabulary_id,
            is_saved=False,
            mastery_level=rating,
            last_reviewed_at=now,
            review_count=1,
        )
        db.add(user_vocab)
    else:
        user_vocab.mastery_level = rating
        user_vocab.last_reviewed_at = now
        user_vocab.review_count += 1

    history = ReviewHistory(
        user_id=user_id,
        vocabulary_id=vocabulary_id,
        result=RATING_TO_RESULT[rating],
        reviewed_at=now,
    )
    db.add(history)

    xp = XpHistory(
        user_id=user_id,
        source="review",
        xp_amount=XP_BY_RATING[rating],
        created_at=now,
    )
    db.add(xp)

    user = db.query(User).filter(User.id == user_id).first()
    if user is not None:
        user.total_xp = (user.total_xp or 0) + XP_BY_RATING[rating]

    db.commit()
    db.refresh(user_vocab)

    if user_vocab.last_reviewed_at is not None:
        user_vocab.last_reviewed_at = _normalize_datetime(user_vocab.last_reviewed_at)
        user_vocab.__dict__["next_review_at"] = get_next_review_at(
            user_vocab.mastery_level,
            user_vocab.last_reviewed_at,
        )

    return user_vocab


def get_topic_progress_map(db: Session, user_id: int, topic_id: int) -> dict[int, UserVocabulary]:
    vocab_ids = [
        row.id
        for row in db.query(Vocabulary.id).filter(Vocabulary.topic_id == topic_id).all()
    ]
    if not vocab_ids:
        return {}

    records = (
        db.query(UserVocabulary)
        .filter(
            UserVocabulary.user_id == user_id,
            UserVocabulary.vocabulary_id.in_(vocab_ids),
        )
        .all()
    )
    return {record.vocabulary_id: record for record in records}


def get_new_words(db: Session, user_id: int, topic_id: int, limit: int = 20) -> list[Vocabulary]:
    seen_ids = (
        db.query(UserVocabulary.vocabulary_id)
        .filter(
            UserVocabulary.user_id == user_id,
            UserVocabulary.mastery_level > 0,
        )
        .subquery()
    )

    return (
        db.query(Vocabulary)
        .filter(
            Vocabulary.topic_id == topic_id,
            ~Vocabulary.id.in_(seen_ids),
        )
        .limit(limit)
        .all()
    )


def get_due_review_words(db: Session, user_id: int, topic_id: int) -> list[Vocabulary]:
    now = datetime.now(timezone.utc)

    user_vocabs = (
        db.query(UserVocabulary)
        .join(Vocabulary, Vocabulary.id == UserVocabulary.vocabulary_id)
        .filter(
            Vocabulary.topic_id == topic_id,
            UserVocabulary.user_id == user_id,
            UserVocabulary.mastery_level > 0,
            UserVocabulary.last_reviewed_at.isnot(None),
        )
        .all()
    )

    due_ids: list[int] = []
    for user_vocab in user_vocabs:
        reviewed_at = user_vocab.last_reviewed_at
        if reviewed_at is None:
            continue
        reviewed_at = _normalize_datetime(reviewed_at)
        interval = REVIEW_INTERVALS.get(user_vocab.mastery_level, 1)
        next_review = reviewed_at + timedelta(days=interval)
        if next_review <= now:
            due_ids.append(user_vocab.vocabulary_id)

    if not due_ids:
        return []

    return db.query(Vocabulary).filter(Vocabulary.id.in_(due_ids)).all()
