from datetime import datetime, timedelta, timezone

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.progress import ReviewHistory
from app.models.review_notification_state import ReviewNotificationState
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

def _rating_to_result(rating: int) -> str:
    # Map numeric rating/mastery to a textual result for history
    if rating >= 5:
        return "mastered"
    if rating >= 3:
        return "familiar"
    return "unknown"


def get_next_review_at(mastery_level: int, last_reviewed_at: datetime) -> datetime:
    days = REVIEW_INTERVALS.get(mastery_level, 1)
    return last_reviewed_at + timedelta(days=days)


def _normalize_datetime(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def _next_mastery_level(current_mastery: int, rating: int) -> int:
    """Increase mastery gradually to avoid jumping too fast between levels."""
    current = max(0, min(5, current_mastery))
    if current == 0:
        return rating

    if current >= 5:
        if rating < current:
            return rating
        return 5

    if rating < current:
        return rating

    if rating == 1:
        gain = 1 if current == 0 else 0
    elif rating == 3:
        gain = 2 if current == 0 else 1
    else:  # rating == 5
        if current == 0:
            gain = 3
        elif current == 1:
            gain = 2
        else:
            gain = 1

    return min(5, current + gain)


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

    # Treat incoming rating as explicit target mastery level (1..5)
    target = max(1, min(5, int(rating)))

    if user_vocab is None:
        user_vocab = UserVocabulary(
            user_id=user_id,
            vocabulary_id=vocabulary_id,
            is_saved=False,
            mastery_level=target,
            last_reviewed_at=now,
            next_review_at=get_next_review_at(target, now),
            review_count=1,
        )
        db.add(user_vocab)
    else:
        user_vocab.mastery_level = target
        user_vocab.last_reviewed_at = now
        user_vocab.next_review_at = get_next_review_at(target, now)
        user_vocab.review_count = (user_vocab.review_count or 0) + 1

    history = ReviewHistory(
        user_id=user_id,
        vocabulary_id=vocabulary_id,
        result=_rating_to_result(target),
        reviewed_at=now,
    )
    db.add(history)
    db.execute(
        insert(ReviewNotificationState)
        .values(user_id=user_id, last_review_activity_at=now)
        .on_conflict_do_update(
            index_elements=[ReviewNotificationState.user_id],
            set_={"last_review_activity_at": now},
        )
    )

    db.commit()
    db.refresh(user_vocab)

    if user_vocab.last_reviewed_at is not None and user_vocab.next_review_at is not None:
        user_vocab.last_reviewed_at = _normalize_datetime(user_vocab.last_reviewed_at)
        user_vocab.next_review_at = _normalize_datetime(user_vocab.next_review_at)

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

    due_ids = [
        row.vocabulary_id
        for row in (
            db.query(UserVocabulary.vocabulary_id)
            .join(Vocabulary, Vocabulary.id == UserVocabulary.vocabulary_id)
            .filter(
                Vocabulary.topic_id == topic_id,
                UserVocabulary.user_id == user_id,
                UserVocabulary.mastery_level > 0,
                UserVocabulary.next_review_at.isnot(None),
                UserVocabulary.next_review_at <= now,
            )
            .all()
        )
    ]

    if not due_ids:
        return []

    return db.query(Vocabulary).filter(Vocabulary.id.in_(due_ids)).all()


def get_vocab_overview(db: Session, user_id: int) -> dict:
    """
    Returns learned_count, due_review_count, and mastery breakdown.
    Only counts user_vocabularies where mastery_level >= 1.
    """
    now = datetime.now(timezone.utc)

    all_learned = db.query(UserVocabulary).filter(
        UserVocabulary.user_id == user_id,
        UserVocabulary.mastery_level >= 1
    ).all()

    learned_count = len(all_learned)

    # Count per mastery level
    level_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    due_count = 0

    for uv in all_learned:
        if uv.mastery_level in level_counts:
            level_counts[uv.mastery_level] += 1

        # Check if due for review
        if uv.next_review_at:
            if _normalize_datetime(uv.next_review_at) <= now:
                due_count += 1

    return {
        "learned_count":    learned_count,
        "due_review_count": due_count,
        "mastery_stats": {
            "level_1": level_counts[1],
            "level_2": level_counts[2],
            "level_3": level_counts[3],
            "level_4": level_counts[4],
            "level_5": level_counts[5],
        }
    }


def get_learned_vocab_list(db: Session, user_id: int) -> dict:
    """
    Returns all words user has learned (mastery >= 1) with full details.
    Sorted by: due words first, then by last_reviewed_at desc.
    """
    now = datetime.now(timezone.utc)

    records = (
        db.query(UserVocabulary, Vocabulary)
        .join(Vocabulary, Vocabulary.id == UserVocabulary.vocabulary_id)
        .filter(
            UserVocabulary.user_id == user_id,
            UserVocabulary.mastery_level >= 1
        )
        .all()
    )

    items = []
    due_count = 0

    for uv, vocab in records:
        next_review = None
        is_due = False

        if uv.next_review_at:
            next_review = _normalize_datetime(uv.next_review_at)
            is_due = next_review <= now

        if is_due:
            due_count += 1

        items.append({
            "vocabulary_id":   vocab.id,
            "word":            vocab.word,
            "meaning":         vocab.meaning,
            "pronunciation":   vocab.pronunciation,
            "audio_url":       vocab.audio_url,
            "example_audio_url": vocab.example_audio_url,
            "example_sentence":         vocab.example_sentence,
            "mastery_level":   uv.mastery_level,
            "review_count":    uv.review_count,
            "last_reviewed_at": uv.last_reviewed_at,
            "next_review_at":  next_review,
            "is_due":          is_due,
        })

    # Sort: due first, then by last_reviewed_at descending
    items.sort(key=lambda x: (not x["is_due"],
               -(x["last_reviewed_at"].timestamp()
                 if x["last_reviewed_at"] else 0)))

    return {
        "items":     items,
        "total":     len(items),
        "due_count": due_count,
    }
