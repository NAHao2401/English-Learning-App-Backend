from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.lesson import AnswerOption, Lesson, Question, Topic
from app.models.progress import Progress, XpHistory
from app.models.user import User
from app.schemas.lesson import SubmitLessonRequest


def get_topics(db: Session):
    return db.query(Topic).order_by(Topic.id.asc()).all()


def get_lessons(
    db: Session,
    user_id: int,
    level: str | None = None,
    topic_id: int | None = None,
):
    query = db.query(Lesson).join(Topic)

    if level:
        query = query.filter(Topic.level == level)

    if topic_id:
        query = query.filter(Lesson.topic_id == topic_id)

    lessons = query.order_by(Lesson.lesson_order.asc(), Lesson.id.asc()).all()

    result = []
    for index, lesson in enumerate(lessons):
        progress = (
            db.query(Progress)
            .filter(
                Progress.user_id == user_id,
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
                    Progress.user_id == user_id,
                    Progress.lesson_id == previous_lesson.id,
                    Progress.status == "completed",
                )
                .first()
            )
            if previous_progress is None:
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

    return result


def get_lesson_by_id(db: Session, user_id: int, lesson_id: int):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        return None

    progress = (
        db.query(Progress)
        .filter(Progress.user_id == user_id, Progress.lesson_id == lesson_id)
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


def get_questions_by_lesson(db: Session, lesson_id: int):
    return (
        db.query(Question)
        .filter(Question.lesson_id == lesson_id)
        .order_by(Question.question_order.asc(), Question.id.asc())
        .all()
    )


def submit_lesson(
    db: Session,
    user: User,
    lesson_id: int,
    data: SubmitLessonRequest,
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        raise ValueError("Lesson not found")

    questions = (
        db.query(Question)
        .filter(Question.lesson_id == lesson_id)
        .order_by(Question.question_order.asc(), Question.id.asc())
        .all()
    )

    if not questions:
        raise ValueError("This lesson has no questions")

    answer_map = {item.question_id: item.answer.strip() for item in data.answers}

    correct_count = 0

    for question in questions:
        user_answer = answer_map.get(question.id)

        if user_answer is None:
            continue

        is_correct = False

        if question.question_type == "multiple_choice":
            correct_option = (
                db.query(AnswerOption)
                .filter(
                    AnswerOption.question_id == question.id,
                    AnswerOption.is_correct == True,
                )
                .first()
            )
            if correct_option:
                is_correct = user_answer.lower() == correct_option.option_text.strip().lower()
            elif question.correct_answer:
                is_correct = user_answer.lower() == question.correct_answer.strip().lower()
        else:
            if question.correct_answer:
                is_correct = user_answer.lower() == question.correct_answer.strip().lower()

        if is_correct:
            correct_count += 1

    total_questions = len(questions)
    wrong_count = total_questions - correct_count
    score = int((correct_count / total_questions) * 100)
    passed = score >= 60
    xp_earned = correct_count * 10

    progress = (
        db.query(Progress)
        .filter(
            Progress.user_id == user.id,
            Progress.lesson_id == lesson_id,
        )
        .first()
    )

    now = datetime.now(timezone.utc)

    if progress is None:
        progress = Progress(
            user_id=user.id,
            lesson_id=lesson_id,
            status="completed" if passed else "in_progress",
            completion_percent=100 if passed else 50,
            highest_score=score,
            last_accessed_at=now,
            completed_at=now if passed else None,
        )
        db.add(progress)
    else:
        progress.status = "completed" if passed else "in_progress"
        progress.completion_percent = 100 if passed else max(progress.completion_percent, 50)
        progress.highest_score = max(progress.highest_score, score)
        progress.last_accessed_at = now
        if passed and progress.completed_at is None:
            progress.completed_at = now

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

    db.commit()

    return {
        "lesson_id": lesson_id,
        "total_questions": total_questions,
        "correct_count": correct_count,
        "wrong_count": wrong_count,
        "score": score,
        "xp_earned": xp_earned,
        "completion_percent": progress.completion_percent,
        "passed": passed,
    }