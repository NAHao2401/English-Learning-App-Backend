from datetime import date, datetime, timedelta, timezone
from math import ceil

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.progress import XpHistory
from app.models.speaking import SpeakingPractice, SpeakingSentence
from app.models.user import User
from app.schemas.speaking import SaveSpeakingPracticeRequest

# XP cộng cho mỗi lần luyện speaking matched
SPEAKING_MATCHED_XP = 5
SPEAKING_PERFECT_XP = 10   # thêm nếu score == 100


def save_practice(
    db: Session,
    user: User,
    data: SaveSpeakingPracticeRequest,
) -> SpeakingPractice:
    practice = SpeakingPractice(
        user_id=user.id,
        lesson_id=data.lesson_id,
        target_text=data.target_text,
        spoken_text=data.spoken_text,
        score=data.score,
        is_matched=data.is_matched,
    )
    db.add(practice)
    db.flush()

    # Cộng XP nếu matched — tích hợp cùng XpHistory như lesson
    xp_earned = _calculate_speaking_xp(data.score, data.is_matched)
    if xp_earned > 0:
        user.total_xp = (user.total_xp or 0) + xp_earned
        db.add(
            XpHistory(
                user_id=user.id,
                lesson_id=data.lesson_id,
                source="speaking",
                xp_amount=xp_earned,
            )
        )

    db.commit()
    db.refresh(practice)
    return practice


def get_practices(
    db: Session,
    user_id: int,
    page: int = 1,
    limit: int = 10,
) -> dict:
    query = (
        db.query(SpeakingPractice)
        .filter(SpeakingPractice.user_id == user_id)
        .order_by(SpeakingPractice.created_at.desc())
    )

    total = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "items": items,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": ceil(total / limit) if total > 0 else 0,
    }


def get_stats(db: Session, user_id: int) -> dict:
    # Tổng số lần luyện
    total_practices = (
        db.query(func.count(SpeakingPractice.id))
        .filter(SpeakingPractice.user_id == user_id)
        .scalar()
        or 0
    )

    # Số lần matched
    matched_count = (
        db.query(func.count(SpeakingPractice.id))
        .filter(
            SpeakingPractice.user_id == user_id,
            SpeakingPractice.is_matched == True,
        )
        .scalar()
        or 0
    )

    # Điểm trung bình
    average_score = (
        db.query(func.avg(SpeakingPractice.score))
        .filter(SpeakingPractice.user_id == user_id)
        .scalar()
        or 0.0
    )

    # Điểm cao nhất
    best_score = (
        db.query(func.max(SpeakingPractice.score))
        .filter(SpeakingPractice.user_id == user_id)
        .scalar()
        or 0
    )

    # Số lần luyện theo 7 ngày gần nhất (index 0 = 6 ngày trước, index 6 = hôm nay)
    today = date.today()
    weekly_practices = []

    for i in range(6, -1, -1):
        target_date = today - timedelta(days=i)
        start = datetime(target_date.year, target_date.month, target_date.day, tzinfo=timezone.utc)
        end = start + timedelta(days=1)

        count = (
            db.query(func.count(SpeakingPractice.id))
            .filter(
                SpeakingPractice.user_id == user_id,
                SpeakingPractice.created_at >= start,
                SpeakingPractice.created_at < end,
            )
            .scalar()
            or 0
        )
        weekly_practices.append(count)

    return {
        "total_practices": total_practices,
        "matched_count": matched_count,
        "average_score": round(float(average_score), 1),
        "best_score": best_score,
        "weekly_practices": weekly_practices,
    }


def get_sentences(
    db: Session,
    difficulty: str | None = None,
    topic: str | None = None,
    limit: int = 10,
) -> list:
    query = db.query(SpeakingSentence)

    if difficulty:
        query = query.filter(SpeakingSentence.difficulty == difficulty)

    if topic:
        query = query.filter(SpeakingSentence.topic == topic)

    return query.order_by(func.random()).limit(limit).all()


def _calculate_speaking_xp(score: int, is_matched: bool) -> int:
    if not is_matched:
        return 0
    if score == 100:
        return SPEAKING_PERFECT_XP
    return SPEAKING_MATCHED_XP