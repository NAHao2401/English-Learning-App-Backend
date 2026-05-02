from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import PaginatedResponse
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


@router.get("", response_model=PaginatedResponse[LessonResponse])
def list_lessons(
    level: str | None = None,
    topic_id: int | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_lessons(
        db=db,
        user_id=current_user.id,
        level=level,
        topic_id=topic_id,
        page=page,
        limit=limit,
    )


@router.get("/{lesson_id}", response_model=LessonResponse)
def lesson_detail(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_lesson_by_id(db, current_user.id, lesson_id)


@router.get("/{lesson_id}/questions", response_model=list[QuestionResponse])
def lesson_questions(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_questions_by_lesson(db, current_user.id, lesson_id)


@router.post("/{lesson_id}/submit", response_model=SubmitLessonResponse)
def submit_lesson_answers(
    lesson_id: int,
    request: SubmitLessonRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return submit_lesson(db, current_user, lesson_id, request)