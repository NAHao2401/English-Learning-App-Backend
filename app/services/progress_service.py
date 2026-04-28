from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.progress import Progress, XpHistory
from app.models.user import User


def get_progress_summary(db: Session, user: User):
    total_lessons = db.query(Lesson).count()

    completed_lessons = (
        db.query(Progress)
        .filter(
            Progress.user_id == user.id,
            Progress.status == "completed",
        )
        .count()
    )

    completion_percent = 0
    if total_lessons > 0:
        completion_percent = int((completed_lessons / total_lessons) * 100)

    study_days = (
        db.query(func.count(func.distinct(func.date(XpHistory.created_at))))
        .filter(XpHistory.user_id == user.id)
        .scalar()
    ) or 0

    return {
        "total_xp": user.total_xp or 0,
        "streak_count": user.streak_count or 0,
        "current_level": user.current_level or "Beginner",
        "completed_lessons": completed_lessons,
        "total_lessons": total_lessons,
        "completion_percent": completion_percent,
        "study_days": study_days,
    }


def get_lesson_progresses(db: Session, user: User):
    lessons = db.query(Lesson).order_by(Lesson.lesson_order.asc(), Lesson.id.asc()).all()

    result = []

    for index, lesson in enumerate(lessons):
        progress = (
            db.query(Progress)
            .filter(
                Progress.user_id == user.id,
                Progress.lesson_id == lesson.id,
            )
            .first()
        )

        is_locked = lesson.is_locked

        if index > 0:
            previous_lesson = lessons[index - 1]
            previous_progress = (
                db.query(Progress)
                .filter(
                    Progress.user_id == user.id,
                    Progress.lesson_id == previous_lesson.id,
                    Progress.status == "completed",
                )
                .first()
            )
            if previous_progress is None:
                is_locked = True

        result.append(
            {
                "lesson_id": lesson.id,
                "title": lesson.title,
                "status": progress.status if progress else "not_started",
                "completion_percent": progress.completion_percent if progress else 0,
                "highest_score": progress.highest_score if progress else 0,
                "is_locked": is_locked,
            }
        )

    return result