from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud.vocabulary_crud import (
    get_due_review_words,
    get_learned_vocab_list,
    get_new_words,
    get_topic_progress_map,
    get_vocab_overview,
    rate_vocabulary,
)
from app.models.user import User
from app.models.user_vocabulary import SavedVocabulary, UserVocabulary
from app.models.vocabulary import Vocabulary
from app.schemas.lesson import TopicResponse
from app.schemas.vocabulary import (
    LearnedVocabItem,
    LearnedVocabListResponse,
    MasteryStatsResponse,
    RateVocabRequest,
    SaveVocabularyRequest,
    SavedVocabularyResponse,
    TopicStudyResponse,
    UserVocabularyResponse,
    UserTopicCreateRequest,
    UserTopicResponse,
    VocabOverviewResponse,
    VocabularyResponse,
)
from app.services.lesson_service import get_topics
from app.services.vocabulary_service import (
    get_batch_vocab_progress,
    create_user_topic,
    delete_user_topic,
    get_all_vocabularies,
    get_user_topic_vocabularies,
    get_user_topics,
    get_vocabularies_by_topic,
    get_vocabularies_by_prefix,
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


@router.get("/search", response_model=list[VocabularyResponse])
def search_vocabularies(prefix: str, db: Session = Depends(get_db)):
    """
    GET /vocabularies/search?prefix=...  — return up to 10 vocabularies whose word starts with prefix
    """
    return get_vocabularies_by_prefix(db, prefix)


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


@router.delete("/user-topics/{user_topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(
    user_topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_user_topic(db, current_user.id, user_topic_id)
    except ValueError as exc:
        if str(exc) == "User topic not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/user-topics/{user_topic_id}/vocabularies")
def list_user_topic_vocabularies(
    user_topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vocabularies = get_user_topic_vocabularies(db, current_user.id, user_topic_id)

    if not vocabularies:
        return []

    vocab_ids = [vocabulary.id for vocabulary in vocabularies]
    progress_map = {
        user_vocab.vocabulary_id: user_vocab.mastery_level
        for user_vocab in db.query(UserVocabulary).filter(
            UserVocabulary.user_id == current_user.id,
            UserVocabulary.vocabulary_id.in_(vocab_ids),
        ).all()
    }

    result = []
    for vocabulary in vocabularies:
        item = VocabularyResponse.model_validate(vocabulary).model_dump()
        item["mastery_level"] = progress_map.get(vocabulary.id, 0)
        result.append(item)

    return result


@router.get("/user-topics/all-saved-words")
def get_all_user_topic_words(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    GET /vocabularies/user-topics/all-saved-words
    Returns all vocabularies saved in any of the user's personal topics,
    sorted by mastery_level ASC (weakest words first).
    Words with no progress record come first (mastery=0).
    """
    saved = db.query(SavedVocabulary).filter(
        SavedVocabulary.user_id == current_user.id
    ).all()

    if not saved:
        return []

    vocab_ids = list({sv.vocabulary_id for sv in saved})

    progress_map = {
        uv.vocabulary_id: uv.mastery_level
        for uv in db.query(UserVocabulary).filter(
            UserVocabulary.user_id == current_user.id,
            UserVocabulary.vocabulary_id.in_(vocab_ids)
        ).all()
    }

    vocabs = db.query(Vocabulary).filter(
        Vocabulary.id.in_(vocab_ids)
    ).all()

    result = []
    for vocab in vocabs:
        item = VocabularyResponse.model_validate(vocab).model_dump()
        item["mastery_level"] = progress_map.get(vocab.id, 0)
        result.append(item)

    result.sort(key=lambda item: (item.get("mastery_level", 0), item.get("id", 0)))

    return result


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
    # Accept explicit mastery level 1..5 from client (e.g. current+1 or current-1).
    if not (1 <= request.rating <= 5):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rating must be an integer between 1 and 5")

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
        result[vocab_id] = user_vocab
    return result


@router.get("/progress/batch", response_model=dict[int, UserVocabularyResponse])
def get_batch_progress(
    vocab_ids: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    parsed_vocab_ids: list[int] = []
    for raw_id in vocab_ids.split(","):
        raw_id = raw_id.strip()
        if not raw_id:
            continue
        try:
            parsed_vocab_ids.append(int(raw_id))
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="vocab_ids must be a comma-separated list of integers",
            ) from exc

    progress_map = get_batch_vocab_progress(db, current_user.id, parsed_vocab_ids)
    result: dict[int, UserVocabularyResponse] = {}
    for vocab_id, user_vocab in progress_map.items():
        result[vocab_id] = UserVocabularyResponse.model_validate(user_vocab)
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


@router.get("/overview", response_model=VocabOverviewResponse)
def get_vocab_overview_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    GET /vocabularies/overview
    Returns learned count + mastery stats for VocabScreen header card.
    Called when user opens Vocab tab.
    """
    return get_vocab_overview(db, current_user.id)


@router.get("/learned", response_model=LearnedVocabListResponse)
def get_learned_vocab_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    GET /vocabularies/learned
    Returns all learned words with mastery level + due status.
    Used by LearnedWordsScreen (tap '>' on learned count card).
    """
    return get_learned_vocab_list(db, current_user.id)


@router.get("/learned/practice-pool")
def get_practice_pool(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    GET /vocabularies/learned/practice-pool
    Returns ALL vocabularies user has learned (mastery_level >= 1),
    sorted by mastery_level ASC (weakest words first).
    Used by free practice mode (no due date filter, no mastery changes).
    """
    user_vocabs = (
        db.query(UserVocabulary)
        .filter(
            UserVocabulary.user_id == current_user.id,
            UserVocabulary.mastery_level >= 1,
        )
        .order_by(UserVocabulary.mastery_level.asc(), UserVocabulary.vocabulary_id.asc())
        .all()
    )

    if not user_vocabs:
        return []

    ordered_progress = [
        (user_vocab.vocabulary_id, user_vocab.mastery_level)
        for user_vocab in user_vocabs
    ]
    vocab_ids = [vocab_id for vocab_id, _ in ordered_progress]

    vocabs_map = {
        vocab.id: vocab
        for vocab in db.query(Vocabulary).filter(
            Vocabulary.id.in_(vocab_ids)
        ).all()
    }

    result = []
    for vocab_id, mastery_level in ordered_progress:
        vocab = vocabs_map.get(vocab_id)
        if vocab is None:
            continue
        item = VocabularyResponse.model_validate(vocab).model_dump()
        item["mastery_level"] = mastery_level
        result.append(item)

    return result
