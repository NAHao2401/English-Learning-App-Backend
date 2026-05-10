from datetime import date, datetime, timedelta, timezone
from math import ceil

from sqlalchemy.orm import Session, selectinload

from app.api import progress
from app.core.exceptions import (
    BadRequestException,
    NotFoundException,
    TooManyRequestsException,
)
from app.models.lesson import Lesson, Question, Topic
from app.models.progress import LessonAnswer, LessonSubmission, Progress, XpHistory
from app.models.user import User
from app.schemas.lesson import SaveAnswerRequest


PASSING_SCORE = 60
BASE_XP_PER_CORRECT_ANSWER = 10
FIRST_PASS_BONUS_XP = 20
PERFECT_SCORE_BONUS_XP = 30
SUBMIT_COOLDOWN_SECONDS = 10


def get_topics(db: Session):
    return db.query(Topic).order_by(Topic.id.asc()).all()


def get_lessons(
    db: Session,
    user_id: int,
    level: str | None = None,
    topic_id: int | None = None,
    page: int = 1,
    limit: int = 10,
):
    query = db.query(Lesson).join(Topic)

    if level:
        query = query.filter(Topic.level == level)

    if topic_id:
        query = query.filter(Lesson.topic_id == topic_id)

    total = query.count()

    lessons = (
        query
        .order_by(Lesson.lesson_order.asc(), Lesson.id.asc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    lesson_ids = [lesson.id for lesson in lessons]

    progresses = (
        db.query(Progress)
        .filter(
            Progress.user_id == user_id,
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
        for progress in db.query(Progress)
        .filter(
            Progress.user_id == user_id,
            Progress.status == "completed",
        )
        .all()
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
                "id": lesson.id,
                "topic_id": lesson.topic_id,
                "title": lesson.title,
                "description": lesson.description,
                "lesson_order": lesson.lesson_order,
                "difficulty": lesson.difficulty,
                "estimated_time": lesson.estimated_time,
                "is_locked": is_locked,
                "completion_percent": progress.completion_percent if progress else 0,
                "status": progress.status if progress else "not_started",
            }
        )

    return {
        "items": result,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": ceil(total / limit) if total > 0 else 0,
    }


def get_lesson_by_id(db: Session, user_id: int, lesson_id: int):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if lesson is None:
        raise NotFoundException("Lesson not found")

    progress = (
        db.query(Progress)
        .filter(
            Progress.user_id == user_id,
            Progress.lesson_id == lesson_id,
        )
        .first()
    )

    return {
        "id": lesson.id,
        "topic_id": lesson.topic_id,
        "title": lesson.title,
        "description": lesson.description,
        "lesson_order": lesson.lesson_order,
        "difficulty": lesson.difficulty,
        "estimated_time": lesson.estimated_time,
        "is_locked": lesson.is_locked,
        "completion_percent": progress.completion_percent if progress else 0,
        "status": progress.status if progress else "not_started",
    }


def get_questions_by_lesson(db: Session, user_id: int, lesson_id: int):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if lesson is None:
        raise NotFoundException("Lesson not found")

    questions = (
        db.query(Question)
        .options(selectinload(Question.answer_options))
        .filter(Question.lesson_id == lesson_id)
        .order_by(Question.question_order.asc(), Question.id.asc())
        .all()
    )

    if not questions:
        raise NotFoundException("This lesson has no questions")

    return questions


def submit_lesson(
    db: Session,
    user: User,
    lesson_id: int,
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if lesson is None:
        raise NotFoundException("Lesson not found")

    _check_submit_cooldown(db, user.id, lesson_id)

    questions = (
        db.query(Question)
        .options(selectinload(Question.answer_options))
        .filter(Question.lesson_id == lesson_id)
        .order_by(Question.question_order.asc(), Question.id.asc())
        .all()
    )

    if not questions:
        raise BadRequestException("This lesson has no questions")

    saved_answers = (
        db.query(LessonAnswer)
        .filter(
            LessonAnswer.user_id == user.id,
            LessonAnswer.lesson_id == lesson_id,
        )
        .all()
    )

    answer_map = {
        item.question_id: item.answer.strip()
        for item in saved_answers
    }

    question_ids = {question.id for question in questions}
    answered_ids = set(answer_map.keys())

    missing_ids = question_ids - answered_ids

    if missing_ids:
        raise BadRequestException("You must answer all questions before final submitting")

    correct_count = 0

    for question in questions:
        user_answer = answer_map.get(question.id, "").strip()
        is_correct = _is_answer_correct(question, user_answer)

        if is_correct:
            correct_count += 1

    total_questions = len(questions)
    wrong_count = total_questions - correct_count
    score = int((correct_count / total_questions) * 100)
    passed = score >= PASSING_SCORE

    progress = _get_or_create_progress(db, user.id, lesson_id)

    was_completed_before = progress.status == "completed"

    now = datetime.now(timezone.utc)

    progress.status = "completed" if passed else "in_progress"
    progress.completion_percent = 100 if passed else 99
    progress.highest_score = max(progress.highest_score, score)
    progress.last_accessed_at = now

    if passed and progress.completed_at is None:
        progress.completed_at = now

    xp_earned = _calculate_xp(
        correct_count=correct_count,
        total_questions=total_questions,
        score=score,
        passed=passed,
        was_completed_before=was_completed_before,
    )

    if xp_earned > 0:
        user.total_xp = (user.total_xp or 0) + xp_earned

        db.add(
            XpHistory(
                user_id=user.id,
                lesson_id=lesson_id,
                source="lesson",
                xp_amount=xp_earned,
            )
        )

    _update_user_streak(user)

    db.add(
        LessonSubmission(
            user_id=user.id,
            lesson_id=lesson_id,
            score=score,
            correct_count=correct_count,
            total_questions=total_questions,
            xp_earned=xp_earned,
        )
    )

    db.commit()
    db.refresh(user)
    db.refresh(progress)

    return {
        "lesson_id": lesson_id,
        "total_questions": total_questions,
        "correct_count": correct_count,
        "wrong_count": wrong_count,
        "score": score,
        "xp_earned": xp_earned,
        "completion_percent": progress.completion_percent,
        "passed": passed,
        "streak_count": user.streak_count or 0,
        "message": "Lesson completed" if passed else "Keep practicing",
    }

def _is_answer_correct(question: Question, user_answer: str) -> bool:
    normalized_user_answer = user_answer.strip().lower()

    if question.question_type == "multiple_choice":
        correct_option = next(
            (
                option
                for option in question.answer_options
                if option.is_correct
            ),
            None,
        )

        if correct_option is None:
            return False

        return normalized_user_answer == correct_option.option_text.strip().lower()

    if question.correct_answer:
        return normalized_user_answer == question.correct_answer.strip().lower()

    return False


def _get_or_create_progress(
    db: Session,
    user_id: int,
    lesson_id: int,
) -> Progress:
    progress = (
        db.query(Progress)
        .filter(
            Progress.user_id == user_id,
            Progress.lesson_id == lesson_id,
        )
        .first()
    )

    if progress:
        return progress

    progress = Progress(
        user_id=user_id,
        lesson_id=lesson_id,
        status="not_started",
        completion_percent=0,
        highest_score=0,
    )

    db.add(progress)
    db.flush()

    return progress


def _calculate_xp(
    correct_count: int,
    total_questions: int,
    score: int,
    passed: bool,
    was_completed_before: bool,
) -> int:
    if not passed:
        return correct_count * 2

    if was_completed_before:
        return min(correct_count * 2, 10)

    xp = correct_count * BASE_XP_PER_CORRECT_ANSWER
    xp += FIRST_PASS_BONUS_XP

    if correct_count == total_questions:
        xp += PERFECT_SCORE_BONUS_XP

    return xp


def _get_last_study_date(user: User) -> date | None:
    last_activity = user.updated_at

    if last_activity is None:
        return None

    return last_activity.date()


def _update_user_streak(user: User):
    today = date.today()
    last_study_date = _get_last_study_date(user)

    if last_study_date is None:
        user.streak_count = 1
        return

    if last_study_date == today:
        return

    yesterday = today - timedelta(days=1)

    if last_study_date == yesterday:
        user.streak_count = (user.streak_count or 0) + 1
    else:
        user.streak_count = 1


def _check_submit_cooldown(db: Session, user_id: int, lesson_id: int):
    latest_submission = (
        db.query(LessonSubmission)
        .filter(
            LessonSubmission.user_id == user_id,
            LessonSubmission.lesson_id == lesson_id,
        )
        .order_by(LessonSubmission.submitted_at.desc())
        .first()
    )

    if latest_submission is None:
        return

    now = datetime.now(timezone.utc)
    submitted_at = latest_submission.submitted_at

    if submitted_at.tzinfo is None:
        submitted_at = submitted_at.replace(tzinfo=timezone.utc)

    diff_seconds = (now - submitted_at).total_seconds()

    if diff_seconds < SUBMIT_COOLDOWN_SECONDS:
        raise TooManyRequestsException(
            "You are submitting too quickly. Please wait a few seconds."
        )
    
def save_lesson_answer(
    db: Session,
    user: User,
    lesson_id: int,
    data: SaveAnswerRequest,
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if lesson is None:
        raise NotFoundException("Lesson not found")

    questions = (
        db.query(Question)
        .options(selectinload(Question.answer_options))
        .filter(Question.lesson_id == lesson_id)
        .order_by(Question.question_order.asc(), Question.id.asc())
        .all()
    )

    if not questions:
        raise BadRequestException("This lesson has no questions")

    question_map = {question.id: question for question in questions}

    question = question_map.get(data.question_id)

    if question is None:
        raise BadRequestException("This question does not belong to this lesson")

    user_answer = data.answer.strip()
    is_correct = _is_answer_correct(question, user_answer)

    existing_answer = (
        db.query(LessonAnswer)
        .filter(
            LessonAnswer.user_id == user.id,
            LessonAnswer.lesson_id == lesson_id,
            LessonAnswer.question_id == data.question_id,
        )
        .first()
    )

    if existing_answer:
        existing_answer.answer = user_answer
        existing_answer.is_correct = is_correct
    else:
        db.add(
            LessonAnswer(
                user_id=user.id,
                lesson_id=lesson_id,
                question_id=data.question_id,
                answer=user_answer,
                is_correct=is_correct,
            )
        )

    db.flush()

    progress = _get_or_create_progress(db, user.id, lesson_id)

    answered_count = (
        db.query(LessonAnswer)
        .filter(
            LessonAnswer.user_id == user.id,
            LessonAnswer.lesson_id == lesson_id,
        )
        .count()
    )

    total_questions = len(questions)

    completion_percent = int((answered_count / total_questions) * 100)

    now = datetime.now(timezone.utc)

    if progress.status != "completed":
        progress.status = "in_progress" if answered_count > 0 else "not_started"
        progress.completion_percent = min(completion_percent, 99)

    progress.last_accessed_at = now

    db.commit()
    db.refresh(progress)

    return {
        "lesson_id": lesson_id,
        "question_id": data.question_id,
        "answered_count": answered_count,
        "total_questions": total_questions,
        "completion_percent": progress.completion_percent,
        "status": progress.status,
        "is_correct": is_correct,
    }