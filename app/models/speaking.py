from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.speaking import (
    PaginatedPracticeResponse,
    SaveSpeakingPracticeRequest,
    SpeakingPracticeResponse,
    SpeakingStatsResponse,
    SpeakingSentenceResponse,
)
from app.services import speaking_service

router = APIRouter(prefix="/speaking", tags=["Speaking"])


@router.post("/practices", response_model=SpeakingPracticeResponse, status_code=201)
def save_practice(
    data: SaveSpeakingPracticeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lưu kết quả 1 lần luyện nói. Mobile gọi sau khi tính score xong."""
    return speaking_service.save_practice(db, current_user, data)


@router.get("/practices/me", response_model=PaginatedPracticeResponse)
def get_my_practices(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lấy lịch sử luyện nói của user hiện tại, có phân trang."""
    return speaking_service.get_practices(db, current_user.id, page, limit)


@router.get("/practices/me/stats", response_model=SpeakingStatsResponse)
def get_my_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Thống kê tổng hợp cho Progress screen: tổng lần luyện, điểm TB, biểu đồ 7 ngày..."""
    return speaking_service.get_stats(db, current_user.id)


@router.get("/sentences", response_model=list[SpeakingSentenceResponse])
def get_sentences(
    difficulty: str | None = Query(default=None, description="beginner / intermediate / advanced"),
    topic: str | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lấy câu mẫu để luyện nói, lọc theo difficulty và topic."""
    return speaking_service.get_sentences(db, difficulty, topic, limit)