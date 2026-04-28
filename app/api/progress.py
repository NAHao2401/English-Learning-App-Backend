from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.progress import ProgressLessonResponse, ProgressSummaryResponse
from app.services.progress_service import get_lesson_progresses, get_progress_summary

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.get("/me/summary", response_model=ProgressSummaryResponse)
def my_progress_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_progress_summary(db, current_user)


@router.get("/me/lessons", response_model=list[ProgressLessonResponse])
def my_lesson_progresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_lesson_progresses(db, current_user)