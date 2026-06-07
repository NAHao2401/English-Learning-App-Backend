from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.auth import router as auth_router
from app.api.lesson import router as lesson_router
from app.api.progress import router as progress_router
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
from app.models.lesson import Topic, Lesson, Question, AnswerOption
from app.models.progress import Progress, XpHistory, LessonSubmission
from app.core.logging import setup_logging
from app.api import speaking

setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="English Learning App API")

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(auth_router)
app.include_router(lesson_router)
app.include_router(progress_router)
app.include_router(notification_router)
app.include_router(speaking.router)

@app.get("/")
def root():
    return {"message": "API is running"}