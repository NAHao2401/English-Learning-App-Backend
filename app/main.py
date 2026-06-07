import os
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.auth import router as auth_router
from app.api.lesson import router as lesson_router
from app.api.notification import router as notification_router
from app.api.progress import router as progress_router
from app.api.vocabulary import router as vocabulary_router
from app.core.exception_handlers import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)
from app.core.exceptions import AppException
from app.db.base import Base
from app.db.session import engine

from app.models.user import User
from app.models.device_token import DeviceToken
from app.models.user_vocabulary import SavedVocabulary, UserTopic
from app.models.vocabulary import Vocabulary
from app.models.lesson import Topic, Lesson, Question, AnswerOption
from app.models.progress import Progress, XpHistory, LessonSubmission
from app.core.logging import setup_logging
from app.api import speaking

setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="English Learning App API")

# Mount static files directory for audio files
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(auth_router)
app.include_router(vocabulary_router)
app.include_router(lesson_router)
app.include_router(progress_router)
app.include_router(notification_router)
app.include_router(speaking.router)

@app.get("/")
def root():
    return {"message": "API is running"}
