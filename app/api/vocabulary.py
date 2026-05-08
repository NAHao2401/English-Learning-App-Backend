from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud.vocabulary_crud import (
    get_due_review_words,
    get_new_words,
    get_next_review_at,
    get_topic_progress_map,
    rate_vocabulary,
)
from app.models.user import User
from app.models.vocabulary import Vocabulary
from app.schemas.lesson import TopicResponse
from app.schemas.vocabulary import (
    RateVocabRequest,
    SaveVocabularyRequest,
    SavedVocabularyResponse,
    TopicStudyResponse,
    UserVocabularyResponse,
    UserTopicCreateRequest,
    UserTopicResponse,
    VocabularyResponse,
)
from app.services.lesson_service import get_topics
from app.services.vocabulary_service import (
    create_user_topic,
    get_all_vocabularies,
    get_user_topic_vocabularies,
    get_user_topics,
    get_vocabularies_by_topic,
    remove_user_topic_vocabulary,
    save_vocabulary,
)

router = APIRouter(prefix="/vocabularies", tags=["Vocabularies"])


@router.get("/topics", response_model=list[TopicResponse])
def list_topics(db: Session = Depends(get_db)):
    return get_topics(db)


@router.get("/all", response_model=list[VocabularyResponse])
def list_vocabularies(level: str | None = None, db: Session = Depends(get_db)):
    return get_all_vocabularies(db, level)


@router.get("/topic/{topic_id}", response_model=list[VocabularyResponse])
def topic_vocabularies(topic_id: int, db: Session = Depends(get_db)):
    return get_vocabularies_by_topic(db, topic_id)


@router.get("/user-topics", response_model=list[UserTopicResponse])
def list_user_topics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_topics(db, current_user.id)


@router.post("/user-topics", response_model=UserTopicResponse, status_code=status.HTTP_201_CREATED)
def create_topic(
    request: UserTopicCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_user_topic(db, current_user.id, request.name, request.description)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/user-topics/{user_topic_id}/vocabularies", response_model=list[VocabularyResponse])
def list_user_topic_vocabularies(
    user_topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_topic_vocabularies(db, current_user.id, user_topic_id)


@router.delete("/user-topics/{user_topic_id}/vocabularies/{vocabulary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_topic_vocabulary(
    user_topic_id: int,
    vocabulary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        remove_user_topic_vocabulary(db, current_user.id, user_topic_id, vocabulary_id)
    except ValueError as exc:
        message = str(exc)
        if message in {"User topic not found", "Vocabulary is not saved in this topic"}:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


@router.post("/save", response_model=SavedVocabularyResponse, status_code=status.HTTP_201_CREATED)
def save_vocab_item(
    request: SaveVocabularyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return save_vocabulary(db, current_user.id, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/progress/rate", response_model=UserVocabularyResponse)
def rate_vocab(
    request: RateVocabRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if request.rating not in [1, 3, 5]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rating must be 1, 3, or 5")

    try:
        return rate_vocabulary(db, current_user.id, request.vocabulary_id, request.rating)
    except ValueError as exc:
        if str(exc) == "Vocabulary not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/progress/topic/{topic_id}", response_model=dict[int, UserVocabularyResponse])
def get_topic_progress(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    progress_map = get_topic_progress_map(db, current_user.id, topic_id)
    result: dict[int, UserVocabularyResponse] = {}
    for vocab_id, user_vocab in progress_map.items():
        user_vocab.__dict__["next_review_at"] = (
            get_next_review_at(user_vocab.mastery_level, user_vocab.last_reviewed_at)
            if user_vocab.last_reviewed_at
            else None
        )
        result[vocab_id] = user_vocab
    return result


@router.get("/progress/topic/{topic_id}/study", response_model=TopicStudyResponse)
def get_study_session(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    all_vocabs = db.query(Vocabulary).filter(Vocabulary.topic_id == topic_id).all()
    total = len(all_vocabs)

    new_words = get_new_words(db, current_user.id, topic_id)
    review_words = get_due_review_words(db, current_user.id, topic_id)

    progress_map = get_topic_progress_map(db, current_user.id, topic_id)
    learned_count = sum(1 for user_vocab in progress_map.values() if user_vocab.mastery_level >= 1)

    return TopicStudyResponse(
        topic_id=topic_id,
        total_words=total,
        new_words=new_words,
        due_review_words=review_words,
        learned_count=learned_count,
    )
