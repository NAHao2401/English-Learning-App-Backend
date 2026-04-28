from app.db.session import SessionLocal
from app.models.lesson import AnswerOption, Lesson, Question, Topic


db = SessionLocal()

try:
    if db.query(Topic).count() > 0:
        print("Seed data already exists")
        raise SystemExit

    topic_food = Topic(
        name="Food",
        description="Basic food vocabulary",
        level="Beginner",
    )

    topic_travel = Topic(
        name="Travel",
        description="Useful travel sentences",
        level="Beginner",
    )

    db.add_all([topic_food, topic_travel])
    db.commit()
    db.refresh(topic_food)
    db.refresh(topic_travel)

    lesson_1 = Lesson(
        topic_id=topic_food.id,
        title="Food Basics",
        description="Learn simple food words",
        lesson_order=1,
        difficulty="Beginner",
        estimated_time=5,
        is_locked=False,
    )

    lesson_2 = Lesson(
        topic_id=topic_travel.id,
        title="Travel Basics",
        description="Learn simple travel phrases",
        lesson_order=2,
        difficulty="Beginner",
        estimated_time=5,
        is_locked=False,
    )

    db.add_all([lesson_1, lesson_2])
    db.commit()
    db.refresh(lesson_1)
    db.refresh(lesson_2)

    q1 = Question(
        lesson_id=lesson_1.id,
        question_type="multiple_choice",
        question_text="What does 'apple' mean?",
        correct_answer="Quả táo",
        question_order=1,
    )

    q2 = Question(
        lesson_id=lesson_1.id,
        question_type="multiple_choice",
        question_text="Choose the correct translation: Tôi thích đồ ăn.",
        correct_answer="I like food.",
        question_order=2,
    )

    q3 = Question(
        lesson_id=lesson_2.id,
        question_type="multiple_choice",
        question_text="What does 'airport' mean?",
        correct_answer="Sân bay",
        question_order=1,
    )

    db.add_all([q1, q2, q3])
    db.commit()
    db.refresh(q1)
    db.refresh(q2)
    db.refresh(q3)

    db.add_all(
        [
            AnswerOption(question_id=q1.id, option_text="Quả táo", is_correct=True, option_order=1),
            AnswerOption(question_id=q1.id, option_text="Con mèo", is_correct=False, option_order=2),
            AnswerOption(question_id=q1.id, option_text="Cái bàn", is_correct=False, option_order=3),
            AnswerOption(question_id=q1.id, option_text="Xe hơi", is_correct=False, option_order=4),

            AnswerOption(question_id=q2.id, option_text="I like food.", is_correct=True, option_order=1),
            AnswerOption(question_id=q2.id, option_text="I go to school.", is_correct=False, option_order=2),
            AnswerOption(question_id=q2.id, option_text="She is reading.", is_correct=False, option_order=3),
            AnswerOption(question_id=q2.id, option_text="They play football.", is_correct=False, option_order=4),

            AnswerOption(question_id=q3.id, option_text="Sân bay", is_correct=True, option_order=1),
            AnswerOption(question_id=q3.id, option_text="Nhà hàng", is_correct=False, option_order=2),
            AnswerOption(question_id=q3.id, option_text="Khách sạn", is_correct=False, option_order=3),
            AnswerOption(question_id=q3.id, option_text="Trường học", is_correct=False, option_order=4),
        ]
    )

    db.commit()
    print("Seed lesson data successfully")

finally:
    db.close()