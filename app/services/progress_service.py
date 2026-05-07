from datetime import date, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.progress import LessonSubmission, Progress, XpHistory
from app.models.user import User


LEVELS = [
    {"name": "Beginner", "min_xp": 0},
    {"name": "Elementary", "min_xp": 300},
    {"name": "Intermediate", "min_xp": 800},
    {"name": "Upper Intermediate", "min_xp": 1500},
    {"name": "Advanced", "min_xp": 2500},
]


def get_progress_summary(db: Session, user: User):
    total_lessons = db.query(Lesson).count()

    progresses = (
        db.query(Progress)
        .filter(Progress.user_id == user.id)
        .all()
    )

    progress_map = {
        progress.lesson_id: progress
        for progress in progresses
    }

    completed_lessons = sum(
        1 for progress in progresses
        if progress.status == "completed"
    )

    in_progress_lessons = sum(
        1 for progress in progresses
        if progress.status == "in_progress"
    )

    not_started_lessons = max(
        total_lessons - completed_lessons - in_progress_lessons,
        0
    )

    locked_lessons = _calculate_locked_lessons(db, progress_map)

    completion_percent = 0
    if total_lessons > 0:
        completion_percent = int((completed_lessons / total_lessons) * 100)

    study_days = (
        db.query(func.count(func.distinct(func.date(XpHistory.created_at))))
        .filter(XpHistory.user_id == user.id)
        .scalar()
    ) or 0

    submission_stats = _get_submission_stats(db, user.id)
    weekly_xp = _get_weekly_xp(db, user.id)
    level_progress = _get_level_progress(user.total_xp or 0)
    recent_activities = _get_recent_activities(db, user.id)

    return {
        "total_xp": user.total_xp or 0,
        "streak_count": user.streak_count or 0,
        "current_level": level_progress["current_level"],
        "completed_lessons": completed_lessons,
        "total_lessons": total_lessons,
        "completion_percent": completion_percent,
        "study_days": study_days,

        "in_progress_lessons": in_progress_lessons,
        "not_started_lessons": not_started_lessons,
        "locked_lessons": locked_lessons,

        "total_submissions": submission_stats["total_submissions"],
        "average_score": submission_stats["average_score"],
        "best_score": submission_stats["best_score"],

        "remaining_lessons": max(total_lessons - completed_lessons, 0),
        "lessons_chart": {
            "completed": completed_lessons,
            "in_progress": in_progress_lessons,
            "not_started": not_started_lessons,
            "locked": locked_lessons,
        },
        "weekly_xp": weekly_xp,
        "level_progress": level_progress,
        "recent_activities": recent_activities,
    }


def get_lesson_progresses(db: Session, user: User):
    lessons = (
        db.query(Lesson)
        .order_by(Lesson.lesson_order.asc(), Lesson.id.asc())
        .all()
    )

    lesson_ids = [lesson.id for lesson in lessons]

    progresses = (
        db.query(Progress)
        .filter(
            Progress.user_id == user.id,
            Progress.lesson_id.in_(lesson_ids),
        )
        .all()
        if lesson_ids
        else []
    )

    progress_map = {
        progress.lesson_id: progress
        for progress in progresses
    }

    completed_lesson_ids = {
        progress.lesson_id
        for progress in progresses
        if progress.status == "completed"
    }

    result = []

    for index, lesson in enumerate(lessons):
        progress = progress_map.get(lesson.id)

        is_locked = lesson.is_locked

        if index > 0:
            previous_lesson = lessons[index - 1]

            if previous_lesson.id not in completed_lesson_ids:
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


def _calculate_locked_lessons(
    db: Session,
    progress_map: dict[int, Progress],
) -> int:
    lessons = (
        db.query(Lesson)
        .order_by(Lesson.lesson_order.asc(), Lesson.id.asc())
        .all()
    )

    locked_count = 0

    for index, lesson in enumerate(lessons):
        is_locked = lesson.is_locked

        if index > 0:
            previous_lesson = lessons[index - 1]
            previous_progress = progress_map.get(previous_lesson.id)

            if previous_progress is None or previous_progress.status != "completed":
                is_locked = True

        if is_locked:
            locked_count += 1

    return locked_count


def _get_submission_stats(db: Session, user_id: int):
    total_submissions = (
        db.query(LessonSubmission)
        .filter(LessonSubmission.user_id == user_id)
        .count()
    )

    average_score = (
        db.query(func.avg(LessonSubmission.score))
        .filter(LessonSubmission.user_id == user_id)
        .scalar()
    )

    best_score = (
        db.query(func.max(LessonSubmission.score))
        .filter(LessonSubmission.user_id == user_id)
        .scalar()
    )

    return {
        "total_submissions": total_submissions,
        "average_score": int(average_score or 0),
        "best_score": int(best_score or 0),
    }


def _get_weekly_xp(db: Session, user_id: int):
    today = date.today()
    start_date = today - timedelta(days=6)

    rows = (
        db.query(
            func.date(XpHistory.created_at).label("day"),
            func.coalesce(func.sum(XpHistory.xp_amount), 0).label("xp"),
            func.count(func.distinct(XpHistory.lesson_id)).label("completed_lessons"),
        )
        .filter(
            XpHistory.user_id == user_id,
            func.date(XpHistory.created_at) >= start_date,
            func.date(XpHistory.created_at) <= today,
        )
        .group_by(func.date(XpHistory.created_at))
        .all()
    )

    row_map = {
        str(row.day): {
            "xp": int(row.xp or 0),
            "completed_lessons": int(row.completed_lessons or 0),
        }
        for row in rows
    }

    result = []

    for offset in range(7):
        current_day = start_date + timedelta(days=offset)
        key = current_day.isoformat()
        data = row_map.get(
            key,
            {
                "xp": 0,
                "completed_lessons": 0,
            },
        )

        result.append(
            {
                "date": key,
                "xp": data["xp"],
                "completed_lessons": data["completed_lessons"],
            }
        )

    return result


def _get_level_progress(total_xp: int):
    current_level = LEVELS[0]
    next_level = None

    for index, level in enumerate(LEVELS):
        if total_xp >= level["min_xp"]:
            current_level = level
            next_level = LEVELS[index + 1] if index + 1 < len(LEVELS) else None

    if next_level is None:
        return {
            "current_level": current_level["name"],
            "current_xp": total_xp,
            "current_level_min_xp": current_level["min_xp"],
            "next_level": None,
            "next_level_min_xp": None,
            "progress_percent": 100,
        }

    current_min_xp = current_level["min_xp"]
    next_min_xp = next_level["min_xp"]
    xp_in_level = total_xp - current_min_xp
    xp_needed = next_min_xp - current_min_xp

    progress_percent = 0
    if xp_needed > 0:
        progress_percent = int((xp_in_level / xp_needed) * 100)

    return {
        "current_level": current_level["name"],
        "current_xp": total_xp,
        "current_level_min_xp": current_min_xp,
        "next_level": next_level["name"],
        "next_level_min_xp": next_min_xp,
        "progress_percent": min(max(progress_percent, 0), 100),
    }


def _get_recent_activities(db: Session, user_id: int):
    rows = (
        db.query(LessonSubmission, Lesson)
        .join(Lesson, Lesson.id == LessonSubmission.lesson_id)
        .filter(LessonSubmission.user_id == user_id)
        .order_by(LessonSubmission.submitted_at.desc())
        .limit(5)
        .all()
    )

    return [
        {
            "lesson_id": lesson.id,
            "lesson_title": lesson.title,
            "score": submission.score,
            "xp_earned": submission.xp_earned,
            "submitted_at": submission.submitted_at.isoformat()
            if submission.submitted_at
            else "",
        }
        for submission, lesson in rows
    ]