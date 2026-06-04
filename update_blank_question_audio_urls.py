from pathlib import Path

from seed_lessons import question_audio_text, question_audio_url

from app.db.session import SessionLocal
from app.models.lesson import Question


SCRIPT_DIR = Path(__file__).parent.resolve()


def update_blank_question_audio_urls() -> None:
    db = SessionLocal()
    try:
        old_water_question = (
            db.query(Question)
            .filter(
                Question.question_type == "fill_blank",
                Question.question_text == "Complete the word: w_t_r",
                Question.correct_answer == "water",
            )
            .first()
        )
        if old_water_question:
            old_water_question.question_text = "Complete the sentence: I drink ____ every day."

        questions = (
            db.query(Question)
            .filter(Question.question_type == "fill_blank")
            .order_by(Question.id)
            .all()
        )

        updated_count = 0
        for question in questions:
            audio_text = question_audio_text(
                question.question_text,
                question.correct_answer,
            )
            expected_audio_url = question_audio_url(audio_text)

            if question.audio_url != expected_audio_url:
                question.audio_url = expected_audio_url
                updated_count += 1

        missing_files = [
            question.audio_url
            for question in questions
            if question.audio_url
            and not (SCRIPT_DIR / question.audio_url).exists()
        ]

        db.commit()
        print(f"Updated {updated_count}/{len(questions)} fill_blank question audio URLs.")
        if missing_files:
            print("Missing audio files:")
            for audio_url in missing_files:
                print(f"- {audio_url}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    update_blank_question_audio_urls()
