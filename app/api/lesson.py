from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.lesson import (
    LessonResponse,
    QuestionResponse,
    SubmitLessonRequest,
    SubmitLessonResponse,
    TopicResponse,
)
from app.services.lesson_service import (
    get_lesson_by_id,
    get_lessons,
    get_questions_by_lesson,
    get_topics,
    submit_lesson,
)

router = APIRouter(prefix="/lessons", tags=["Lessons"])


@router.get("/topics", response_model=list[TopicResponse])
def list_topics(db: Session = Depends(get_db)):
    return get_topics(db)


@router.get("", response_model=list[LessonResponse])
def list_lessons(
    level: str | None = None,
    topic_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_lessons(db, current_user.id, level, topic_id)


@router.get("/{lesson_id}", response_model=LessonResponse)
def lesson_detail(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lesson = get_lesson_by_id(db, current_user.id, lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    return lesson


@router.get("/{lesson_id}/questions", response_model=list[QuestionResponse])
def lesson_questions(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_questions_by_lesson(db, lesson_id)


@router.post("/{lesson_id}/submit", response_model=SubmitLessonResponse)
def submit_lesson_answers(
    lesson_id: int,
    request: SubmitLessonRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return submit_lesson(db, current_user, lesson_id, request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )