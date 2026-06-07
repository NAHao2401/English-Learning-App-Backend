
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Topic, Lesson, Question
from app.core.security import get_current_user
from app.models.models import User
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/speaking", tags=["speaking"])


class SpeakingTopicResponse(BaseModel):
    id: int
    name: str
    sentence_count: int

    class Config:
        from_attributes = True


class SpeakingSentenceResponse(BaseModel):
    id: int
    text: str           # câu cần đọc
    hint: str | None    # gợi ý phát âm nếu có
    difficulty: str     # beginner / intermediate / advanced

    class Config:
        from_attributes = True


@router.get("/topics", response_model=List[SpeakingTopicResponse])
def get_speaking_topics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy danh sách chủ đề để luyện nói"""
    topics = db.query(Topic).all()
    result = []
    for topic in topics:
        # Đếm số câu speaking trong topic (dùng lại bảng Question)
        count = (
            db.query(Question)
            .join(Lesson)
            .filter(Lesson.topic_id == topic.id)
            .count()
        )
        result.append(SpeakingTopicResponse(
            id=topic.id,
            name=topic.name,
            sentence_count=count
        ))
    return result


@router.get("/topics/{topic_id}/sentences",
            response_model=List[SpeakingSentenceResponse])
def get_sentences_by_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy danh sách câu luyện nói theo chủ đề"""
    questions = (
        db.query(Question)
        .join(Lesson)
        .filter(Lesson.topic_id == topic_id)
        .all()
    )
    if not questions:
        raise HTTPException(status_code=404,
                            detail="No sentences found for this topic")

    return [
        SpeakingSentenceResponse(
            id=q.id,
            # Dùng lại trường question_text làm câu mẫu để đọc
            text=q.question_text,
            hint=None,
            difficulty=q.lesson.level if hasattr(q, 'lesson') else "beginner"
        )
        for q in questions
    ]


class SpeakingResultRequest(BaseModel):
    question_id: int
    spoken_text: str
    score: int


@router.post("/result")
def save_speaking_result(
    body: SpeakingResultRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lưu kết quả luyện nói (tích hợp XP nếu cần)"""
    # Cộng XP nhỏ mỗi lần luyện nói
    if body.score >= 70:
        current_user.total_xp = (current_user.total_xp or 0) + 5
        db.commit()
    return {"message": "Saved", "xp_earned": 5 if body.score >= 70 else 0}
=======
# # POST /speaking/practices
# # Lưu kết quả 1 lần luyện nói (mobile gọi sau khi tính score xong)
# {
#   "target_text": "The quick brown fox",
#   "spoken_text": "The quick brown dog",
#   "score": 75,
#   "is_matched": True,
#   "lesson_id": None   # optional
# }

# # GET /speaking/practices/me
# # Lấy lịch sử luyện nói của user hiện tại
# # Response: list các practice, có phân trang

# # GET /speaking/practices/me/stats
# # Thống kê tổng hợp cho Progress screen
# # Response:
# {
#   "total_practices": 24,
#   "matched_count": 18,
#   "average_score": 76.5,
#   "best_score": 100,
#   "weekly_practices": [3, 0, 2, 5, 1, 4, 0]  # 7 ngày gần nhất
# }

# # GET /speaking/sentences
# # Trả về danh sách câu mẫu để luyện (thay vì hardcode trong app)
# # Query params: ?difficulty=beginner&topic=food&limit=10



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

@router.get("/topics", response_model=list[str])
def get_speaking_topics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lấy danh sách topic có sẵn trong bảng speaking_sentences."""
    rows = (
        db.query(SpeakingSentence.topic)
        .distinct()
        .filter(SpeakingSentence.topic.isnot(None))
        .all()
    )
    return [r[0] for r in rows]
>>>>>>> f14a31a (fix speaking feature + modify ui)
