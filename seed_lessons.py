"""
Seed dữ liệu mẫu lớn hơn cho English Learning App.

Cách chạy từ thư mục gốc project:
    python seed_lessons.py

Xoá dữ liệu học tập cũ rồi seed lại:
    python seed_lessons.py --reset

Tài khoản test:
    Email: student@example.com
    Password: 123456

Ghi chú:
- multiple_choice: đáp án khi submit phải là option_text của đáp án đúng.
- fill_blank / typing: đáp án khi submit phải trùng correct_answer sau khi strip/lower.
"""

from __future__ import annotations

import sys
import re
from typing import Any

from sqlalchemy import inspect

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal
from app.db.session import engine
from app.models.lesson import AnswerOption, Lesson, Question, Topic
from app.models.progress import LessonSubmission, Progress, XpHistory
from app.models.vocabulary import Vocabulary
from app.models.user_vocabulary import SavedVocabulary, UserVocabulary
from app.models.user import User


TEST_USER_EMAIL = "student@example.com"
TEST_USER_PASSWORD = "123456"


def question_audio_text(text: str, correct: str | None = None) -> str:
    if correct and "____" in text:
        text = re.sub(r"^Complete the (?:sentence|phrase):\s*", "", text).strip()
        return text.replace("____", correct).strip()

    return text.strip()


def question_audio_url(audio_text: str) -> str:
    audio_slug = re.sub(r"[^a-z0-9]+", "_", audio_text.lower()).strip("_")
    return f"static/audio/question/{audio_slug}.mp3"


def mc(
    text: str,
    correct: str,
    wrong_1: str,
    wrong_2: str,
    wrong_3: str,
    explanation: str,
    order: int,
) -> dict[str, Any]:
    return {
        "question_type": "multiple_choice",
        "question_text": text,
        "correct_answer": correct,
        "explanation": explanation,
        "question_order": order,
        "answer_options": [
            (correct, True),
            (wrong_1, False),
            (wrong_2, False),
            (wrong_3, False),
        ],
    }


def blank(
    text: str,
    correct: str,
    explanation: str,
    order: int,
) -> dict[str, Any]:
    audio_text = question_audio_text(text, correct)

    return {
        "question_type": "fill_blank",
        "question_text": text,
        "audio_url": question_audio_url(audio_text),
        "correct_answer": correct,
        "explanation": explanation,
        "question_order": order,
        "answer_options": [],
    }


SEED_DATA = [
    {
        "name": "Food",
        "description": "Từ vựng và mẫu câu tiếng Anh cơ bản về đồ ăn, thức uống.",
        "level": "Beginner",
        "icon_url": "https://example.com/icons/food.png",
        "lessons": [
            {
                "title": "Food Vocabulary",
                "description": "Học các từ vựng đồ ăn phổ biến.",
                "lesson_order": 1,
                "difficulty": "Beginner",
                "estimated_time": 7,
                "is_locked": False,
                "questions": [
                    mc("What does 'apple' mean?", "Quả táo", "Con mèo", "Cái bàn", "Xe hơi", "'Apple' nghĩa là quả táo.", 1),
                    mc("Which word means 'bánh mì'?", "Bread", "Water", "Rice", "Chicken", "'Bread' nghĩa là bánh mì.", 2),
                    mc("What does 'rice' mean?", "Cơm / gạo", "Sữa", "Trứng", "Cá", "'Rice' nghĩa là cơm hoặc gạo.", 3),
                    mc("Which word means 'thịt gà'?", "Chicken", "Fish", "Beef", "Pork", "'Chicken' nghĩa là thịt gà.", 4),
                    blank("Complete the sentence: I eat ____ for breakfast.", "bread", "'Bread' là bánh mì.", 5),
                    blank("Complete the sentence: I drink ____ every day.", "water", "'Water' nghĩa là nước.", 6),
                ],
            },
            {
                "title": "Drinks",
                "description": "Học từ vựng về đồ uống.",
                "lesson_order": 2,
                "difficulty": "Beginner",
                "estimated_time": 7,
                "is_locked": False,
                "questions": [
                    mc("What does 'milk' mean?", "Sữa", "Nước", "Cà phê", "Trà", "'Milk' nghĩa là sữa.", 1),
                    mc("Which word means 'cà phê'?", "Coffee", "Tea", "Juice", "Soup", "'Coffee' nghĩa là cà phê.", 2),
                    mc("What does 'orange juice' mean?", "Nước cam", "Nước lọc", "Sữa", "Trà đá", "'Orange juice' nghĩa là nước cam.", 3),
                    mc("Choose the correct sentence: Tôi muốn nước.", "I want water.", "I want bread.", "I am water.", "I drink food.", "'I want water' nghĩa là tôi muốn nước.", 4),
                    blank("Complete the sentence: I drink ____ every day.", "water", "'I drink water every day' nghĩa là tôi uống nước mỗi ngày.", 5),
                    blank("Complete the sentence: This coffee is ____.", "hot", "'Hot' nghĩa là nóng.", 6),
                ],
            },
            {
                "title": "Ordering Food",
                "description": "Luyện các câu giao tiếp khi gọi món.",
                "lesson_order": 3,
                "difficulty": "Beginner",
                "estimated_time": 8,
                "is_locked": False,
                "questions": [
                    mc("How do you say: Tôi muốn gọi một cái bánh mì?", "I would like a sandwich.", "I am a sandwich.", "I have a table.", "I go to the airport.", "'I would like...' là cách lịch sự để gọi món.", 1),
                    mc("What does 'menu' mean?", "Thực đơn", "Hoá đơn", "Sân bay", "Phòng ngủ", "'Menu' nghĩa là thực đơn.", 2),
                    mc("What does 'bill' mean in a restaurant?", "Hoá đơn", "Bàn ăn", "Đầu bếp", "Cái ly", "'Bill' trong nhà hàng nghĩa là hoá đơn.", 3),
                    mc("Choose the polite request.", "Can I have the menu, please?", "You menu give me.", "I menu now.", "Menu is hungry.", "'Can I have..., please?' là cách hỏi lịch sự.", 4),
                    blank("Complete the sentence: I am ____.", "hungry", "'I am hungry' nghĩa là tôi đói.", 5),
                    blank("Complete the sentence: The food is ____.", "delicious", "'Delicious' nghĩa là ngon.", 6),
                ],
            },
        ],
    },
    {
        "name": "Travel",
        "description": "Từ vựng và mẫu câu hữu ích khi đi du lịch.",
        "level": "Beginner",
        "icon_url": "https://example.com/icons/travel.png",
        "lessons": [
            {
                "title": "Travel Vocabulary",
                "description": "Học các từ vựng cơ bản khi đi du lịch.",
                "lesson_order": 4,
                "difficulty": "Beginner",
                "estimated_time": 7,
                "is_locked": False,
                "questions": [
                    mc("What does 'airport' mean?", "Sân bay", "Nhà hàng", "Khách sạn", "Trường học", "'Airport' nghĩa là sân bay.", 1),
                    mc("Which word means 'vé'?", "Ticket", "Table", "Menu", "Bottle", "'Ticket' nghĩa là vé.", 2),
                    mc("What does 'passport' mean?", "Hộ chiếu", "Va li", "Bản đồ", "Tàu hỏa", "'Passport' nghĩa là hộ chiếu.", 3),
                    mc("What does 'luggage' mean?", "Hành lý", "Bữa sáng", "Chìa khóa", "Ghế ngồi", "'Luggage' nghĩa là hành lý.", 4),
                    blank("Complete the sentence: I need a ____.", "ticket", "'I need a ticket' nghĩa là tôi cần một vé.", 5),
                    blank("Complete the sentence: Where is the ____?", "airport", "'Where is the airport?' nghĩa là sân bay ở đâu?", 6),
                ],
            },
            {
                "title": "Hotel Check-in",
                "description": "Luyện giao tiếp khi nhận phòng khách sạn.",
                "lesson_order": 5,
                "difficulty": "Beginner",
                "estimated_time": 8,
                "is_locked": False,
                "questions": [
                    mc("How do you say: Tôi có đặt phòng?", "I have a reservation.", "I have a sandwich.", "I need water.", "I am late.", "'Reservation' nghĩa là đặt chỗ/đặt phòng.", 1),
                    mc("What does 'room key' mean?", "Chìa khóa phòng", "Số điện thoại", "Hộ chiếu", "Tầng trệt", "'Room key' nghĩa là chìa khóa phòng.", 2),
                    mc("Choose the correct sentence: Tôi muốn nhận phòng.", "I would like to check in.", "I would like to check out.", "I would like to eat rice.", "I would like to buy shoes.", "'Check in' nghĩa là nhận phòng/làm thủ tục.", 3),
                    mc("What does 'single room' mean?", "Phòng đơn", "Phòng đôi", "Phòng tắm", "Phòng bếp", "'Single room' nghĩa là phòng đơn.", 4),
                    blank("Complete the phrase: check ____", "in", "'Check in' nghĩa là nhận phòng.", 5),
                    blank("Complete the sentence: My room number is ____.", "five", "Ví dụ câu đơn giản: My room number is five.", 6),
                ],
            },
            {
                "title": "Asking for Directions",
                "description": "Học cách hỏi đường và hiểu chỉ dẫn cơ bản.",
                "lesson_order": 6,
                "difficulty": "Beginner",
                "estimated_time": 8,
                "is_locked": False,
                "questions": [
                    mc("What does 'turn left' mean?", "Rẽ trái", "Rẽ phải", "Đi thẳng", "Dừng lại", "'Turn left' nghĩa là rẽ trái.", 1),
                    mc("What does 'go straight' mean?", "Đi thẳng", "Quay lại", "Rẽ trái", "Qua đường", "'Go straight' nghĩa là đi thẳng.", 2),
                    mc("Which sentence means: Nhà ga ở đâu?", "Where is the station?", "Where is the menu?", "Where is the bread?", "Where is the water?", "'Station' nghĩa là nhà ga.", 3),
                    mc("What does 'near' mean?", "Gần", "Xa", "Trên", "Dưới", "'Near' nghĩa là gần.", 4),
                    blank("Complete the sentence: Turn ____ at the corner.", "right", "'Turn right' nghĩa là rẽ phải.", 5),
                    blank("Complete the sentence: The hotel is ____ the bank.", "near", "'Near' nghĩa là gần.", 6),
                ],
            },
        ],
    },
    {
        "name": "Daily Communication",
        "description": "Các câu giao tiếp hằng ngày cho người mới bắt đầu.",
        "level": "Beginner",
        "icon_url": "https://example.com/icons/chat.png",
        "lessons": [
            {
                "title": "Greetings",
                "description": "Học cách chào hỏi và giới thiệu bản thân.",
                "lesson_order": 7,
                "difficulty": "Beginner",
                "estimated_time": 6,
                "is_locked": False,
                "questions": [
                    mc("What does 'Good morning' mean?", "Chào buổi sáng", "Chúc ngủ ngon", "Tạm biệt", "Cảm ơn", "'Good morning' dùng để chào vào buổi sáng.", 1),
                    mc("Choose the correct translation: Rất vui được gặp bạn.", "Nice to meet you.", "See you tomorrow.", "I am hungry.", "Where is the hotel?", "'Nice to meet you' dùng khi mới gặp ai đó.", 2),
                    mc("What does 'Goodbye' mean?", "Tạm biệt", "Xin chào", "Cảm ơn", "Xin lỗi", "'Goodbye' nghĩa là tạm biệt.", 3),
                    mc("Which sentence introduces your name?", "My name is Anna.", "I need a ticket.", "Turn left.", "Can I have water?", "'My name is...' dùng để giới thiệu tên.", 4),
                    blank("Complete the sentence: My name ____ Anna.", "is", "Chủ ngữ 'My name' đi với 'is'.", 5),
                    blank("Complete the phrase: Nice to ____ you.", "meet", "'Nice to meet you' nghĩa là rất vui được gặp bạn.", 6),
                ],
            },
            {
                "title": "Daily Questions",
                "description": "Luyện hỏi và trả lời các câu đơn giản.",
                "lesson_order": 8,
                "difficulty": "Beginner",
                "estimated_time": 7,
                "is_locked": False,
                "questions": [
                    mc("What does 'How are you?' mean?", "Bạn khỏe không?", "Bạn ở đâu?", "Bạn tên gì?", "Bạn bao nhiêu tuổi?", "'How are you?' là câu hỏi thăm sức khỏe.", 1),
                    mc("Which answer is suitable for 'How are you?'", "I am fine.", "I am a ticket.", "I am an airport.", "I am a menu.", "'I am fine' nghĩa là tôi khỏe.", 2),
                    mc("What does 'Where are you from?' mean?", "Bạn đến từ đâu?", "Bạn đang làm gì?", "Bạn thích gì?", "Bạn có đói không?", "'Where are you from?' hỏi quê quán/quốc gia.", 3),
                    mc("Choose the correct translation: Tôi đến từ Việt Nam.", "I am from Vietnam.", "I am in Vietnam food.", "I go Vietnam table.", "I need Vietnam ticket.", "'I am from...' dùng để nói đến từ đâu.", 4),
                    blank("Complete the sentence: Thank ____.", "you", "'Thank you' nghĩa là cảm ơn bạn.", 5),
                    blank("Complete the sentence: I am ____ Vietnam.", "from", "'I am from Vietnam' nghĩa là tôi đến từ Việt Nam.", 6),
                ],
            },
            {
                "title": "Polite Expressions",
                "description": "Học các cách nói lịch sự trong giao tiếp.",
                "lesson_order": 9,
                "difficulty": "Beginner",
                "estimated_time": 7,
                "is_locked": False,
                "questions": [
                    mc("What does 'please' mean?", "Làm ơn / vui lòng", "Xin lỗi", "Tạm biệt", "Không sao", "'Please' dùng để nói lịch sự.", 1),
                    mc("What does 'sorry' mean?", "Xin lỗi", "Cảm ơn", "Xin chào", "Chúc ngủ ngon", "'Sorry' nghĩa là xin lỗi.", 2),
                    mc("Choose the polite sentence.", "Could you help me, please?", "Help me now.", "You help me.", "Me help please.", "'Could you..., please?' là cách nhờ lịch sự.", 3),
                    mc("What does 'Excuse me' mean?", "Xin lỗi / làm phiền một chút", "Tôi rất khỏe", "Tôi đói", "Tôi cần vé", "'Excuse me' dùng khi muốn gây chú ý lịch sự.", 4),
                    blank("Complete the sentence: I am ____.", "sorry", "'I am sorry' nghĩa là tôi xin lỗi.", 5),
                    blank("Complete the sentence: Please help ____.", "me", "'Please help me' nghĩa là làm ơn giúp tôi.", 6),
                ],
            },
        ],
    },
    {
        "name": "Family",
        "description": "Từ vựng về gia đình và cách nói về người thân.",
        "level": "Beginner",
        "icon_url": "https://example.com/icons/family.png",
        "lessons": [
            {
                "title": "Family Members",
                "description": "Học từ vựng về các thành viên trong gia đình.",
                "lesson_order": 10,
                "difficulty": "Beginner",
                "estimated_time": 7,
                "is_locked": False,
                "questions": [
                    mc("What does 'father' mean?", "Bố / cha", "Mẹ", "Anh trai", "Em gái", "'Father' nghĩa là bố/cha.", 1),
                    mc("What does 'mother' mean?", "Mẹ", "Bố", "Ông", "Bà", "'Mother' nghĩa là mẹ.", 2),
                    mc("Which word means 'anh/em trai'?", "Brother", "Sister", "Daughter", "Grandmother", "'Brother' nghĩa là anh/em trai.", 3),
                    mc("Which word means 'chị/em gái'?", "Sister", "Brother", "Son", "Father", "'Sister' nghĩa là chị/em gái.", 4),
                    blank("Complete the sentence: This is my ____.", "family", "'Family' nghĩa là gia đình.", 5),
                    blank("Complete the sentence: My ____ is kind.", "mother", "Ví dụ: My mother is kind.", 6),
                ],
            },
            {
                "title": "Talking About Family",
                "description": "Luyện câu đơn giản để nói về gia đình.",
                "lesson_order": 11,
                "difficulty": "Beginner",
                "estimated_time": 8,
                "is_locked": False,
                "questions": [
                    mc("Choose the correct translation: Tôi có một người chị.", "I have a sister.", "I am a sister.", "I need a sister.", "I go to sister.", "'I have...' nghĩa là tôi có.", 1),
                    mc("What does 'My father is a teacher' mean?", "Bố tôi là giáo viên", "Mẹ tôi là bác sĩ", "Anh tôi là học sinh", "Bà tôi ở nhà", "'Teacher' nghĩa là giáo viên.", 2),
                    mc("Which sentence is correct?", "My brother is tall.", "My brother are tall.", "My brother tall is.", "Brother my is tall.", "Chủ ngữ số ít dùng 'is'.", 3),
                    mc("What does 'parents' mean?", "Bố mẹ", "Con cái", "Anh chị em", "Ông bà", "'Parents' nghĩa là bố mẹ.", 4),
                    blank("Complete the sentence: I have two ____.", "brothers", "'Two brothers' nghĩa là hai anh/em trai.", 5),
                    blank("Complete the sentence: My sister ____ happy.", "is", "Chủ ngữ số ít 'my sister' đi với 'is'.", 6),
                ],
            },
        ],
    },
    {
        "name": "School",
        "description": "Từ vựng và mẫu câu thường dùng ở trường học.",
        "level": "Beginner",
        "icon_url": "https://example.com/icons/school.png",
        "lessons": [
            {
                "title": "Classroom Objects",
                "description": "Học từ vựng về đồ vật trong lớp học.",
                "lesson_order": 12,
                "difficulty": "Beginner",
                "estimated_time": 7,
                "is_locked": False,
                "questions": [
                    mc("What does 'book' mean?", "Quyển sách", "Cây bút", "Cái ghế", "Cái cửa", "'Book' nghĩa là quyển sách.", 1),
                    mc("Which word means 'cây bút'?", "Pen", "Bag", "Desk", "Window", "'Pen' nghĩa là cây bút.", 2),
                    mc("What does 'chair' mean?", "Cái ghế", "Cái bàn", "Cục tẩy", "Thước kẻ", "'Chair' nghĩa là cái ghế.", 3),
                    mc("What does 'board' mean in classroom?", "Bảng", "Cửa", "Sách", "Cặp", "'Board' trong lớp học nghĩa là bảng.", 4),
                    blank("Complete the sentence: Open your ____.", "book", "'Open your book' nghĩa là mở sách ra.", 5),
                    blank("Complete the sentence: I write with a ____.", "pen", "Ta dùng bút để viết.", 6),
                ],
            },
            {
                "title": "School Subjects",
                "description": "Học từ vựng về các môn học.",
                "lesson_order": 13,
                "difficulty": "Beginner",
                "estimated_time": 7,
                "is_locked": False,
                "questions": [
                    mc("What does 'English' mean?", "Môn tiếng Anh", "Môn toán", "Môn nhạc", "Môn thể dục", "'English' là môn tiếng Anh/ngôn ngữ tiếng Anh.", 1),
                    mc("Which word means 'môn toán'?", "Math", "Art", "Music", "History", "'Math' nghĩa là môn toán.", 2),
                    mc("What does 'Science' mean?", "Khoa học", "Địa lý", "Âm nhạc", "Mỹ thuật", "'Science' nghĩa là khoa học.", 3),
                    mc("Choose the correct sentence.", "I like English.", "I likes English.", "I English like.", "I am like English.", "Sau 'I' dùng động từ nguyên mẫu 'like'.", 4),
                    blank("Complete the sentence: My favorite subject is ____.", "English", "Ví dụ: My favorite subject is English.", 5),
                    blank("Complete the sentence: I study ____ at school.", "math", "Ví dụ: I study math at school.", 6),
                ],
            },
        ],
    },
    {
        "name": "Work",
        "description": "Từ vựng nghề nghiệp và câu giao tiếp công việc cơ bản.",
        "level": "Elementary",
        "icon_url": "https://example.com/icons/work.png",
        "lessons": [
            {
                "title": "Jobs",
                "description": "Học tên một số nghề nghiệp phổ biến.",
                "lesson_order": 14,
                "difficulty": "Elementary",
                "estimated_time": 8,
                "is_locked": False,
                "questions": [
                    mc("What does 'doctor' mean?", "Bác sĩ", "Giáo viên", "Kỹ sư", "Tài xế", "'Doctor' nghĩa là bác sĩ.", 1),
                    mc("Which word means 'giáo viên'?", "Teacher", "Nurse", "Farmer", "Singer", "'Teacher' nghĩa là giáo viên.", 2),
                    mc("What does 'engineer' mean?", "Kỹ sư", "Đầu bếp", "Học sinh", "Luật sư", "'Engineer' nghĩa là kỹ sư.", 3),
                    mc("Choose the correct translation: Cô ấy là y tá.", "She is a nurse.", "She is a doctor.", "He is a nurse.", "She are a nurse.", "'Nurse' nghĩa là y tá.", 4),
                    blank("Complete the sentence: He is a ____.", "doctor", "Ví dụ: He is a doctor.", 5),
                    blank("Complete the sentence: I am a ____.", "teacher", "Ví dụ: I am a teacher.", 6),
                ],
            },
            {
                "title": "At Work",
                "description": "Luyện một số câu đơn giản nơi làm việc.",
                "lesson_order": 15,
                "difficulty": "Elementary",
                "estimated_time": 8,
                "is_locked": False,
                "questions": [
                    mc("What does 'meeting' mean?", "Cuộc họp", "Bữa ăn", "Vé máy bay", "Khách sạn", "'Meeting' nghĩa là cuộc họp.", 1),
                    mc("Which sentence means: Tôi có một cuộc họp?", "I have a meeting.", "I have a ticket.", "I eat a meeting.", "I am a meeting.", "'I have a meeting' nghĩa là tôi có một cuộc họp.", 2),
                    mc("What does 'deadline' mean?", "Hạn chót", "Lịch nghỉ", "Tiền lương", "Địa chỉ", "'Deadline' nghĩa là hạn chót.", 3),
                    mc("Choose the correct sentence.", "I work in an office.", "I work on an office.", "I works in an office.", "I office work.", "'In an office' nghĩa là trong văn phòng.", 4),
                    blank("Complete the sentence: I go to ____ every day.", "work", "'Go to work' nghĩa là đi làm.", 5),
                    blank("Complete the sentence: The meeting is ____ 9 AM.", "at", "Dùng 'at' với giờ cụ thể.", 6),
                ],
            },
        ],
    },
]


def reset_learning_data(db):
    """Xoá dữ liệu theo thứ tự tránh lỗi khoá ngoại."""
    existing_tables = set(inspect(db.get_bind()).get_table_names())

    def delete_if_exists(model):
        if model.__tablename__ in existing_tables:
            db.query(model).delete(synchronize_session=False)

    delete_if_exists(LessonSubmission)
    delete_if_exists(XpHistory)
    delete_if_exists(Progress)
    # delete saved/user vocabularies and vocabularies before topics
    delete_if_exists(SavedVocabulary)
    delete_if_exists(UserVocabulary)
    delete_if_exists(Vocabulary)
    delete_if_exists(AnswerOption)
    delete_if_exists(Question)
    delete_if_exists(Lesson)
    delete_if_exists(Topic)
    db.commit()


def get_or_create_test_user(db):
    user = db.query(User).filter(User.email == TEST_USER_EMAIL).first()

    if user:
        return user

    user = User(
        name="Test Student",
        email=TEST_USER_EMAIL,
        password_hash=hash_password(TEST_USER_PASSWORD),
        avatar_url="https://example.com/avatars/student.png",
        current_level="Beginner",
        total_xp=0,
        streak_count=0,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def seed_topics_lessons_questions(db):
    if db.query(Topic).count() > 0:
        print("Seed lesson data already exists. Use --reset to recreate.")
        return

    total_lessons = 0
    total_questions = 0
    total_options = 0

    for topic_data in SEED_DATA:
        topic = Topic(
            name=topic_data["name"],
            description=topic_data["description"],
            level=topic_data["level"],
            icon_url=topic_data["icon_url"],
        )
        db.add(topic)
        db.flush()

        for lesson_data in topic_data["lessons"]:
            lesson = Lesson(
                topic_id=topic.id,
                title=lesson_data["title"],
                description=lesson_data["description"],
                lesson_order=lesson_data["lesson_order"],
                difficulty=lesson_data["difficulty"],
                estimated_time=lesson_data["estimated_time"],
                is_locked=lesson_data["is_locked"],
            )
            db.add(lesson)
            db.flush()
            total_lessons += 1

            for question_data in lesson_data["questions"]:
                question = Question(
                    lesson_id=lesson.id,
                    question_type=question_data["question_type"],
                    question_text=question_data["question_text"],
                    audio_url=question_data.get("audio_url"),
                    correct_answer=question_data["correct_answer"],
                    explanation=question_data["explanation"],
                    question_order=question_data["question_order"],
                )
                db.add(question)
                db.flush()
                total_questions += 1

                for option_order, (option_text, is_correct) in enumerate(
                    question_data["answer_options"],
                    start=1,
                ):
                    db.add(
                        AnswerOption(
                            question_id=question.id,
                            option_text=option_text,
                            is_correct=is_correct,
                            option_order=option_order,
                        )
                    )
                    total_options += 1

    db.commit()
    print("Seed topics, lessons, questions and answer options successfully.")
    print(f"Topics: {len(SEED_DATA)}")
    print(f"Lessons: {total_lessons}")
    print(f"Questions: {total_questions}")
    print(f"Answer options: {total_options}")


def main():
    reset = "--reset" in sys.argv

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if reset:
            print("Resetting existing learning data...")
            reset_learning_data(db)

        user = get_or_create_test_user(db)
        seed_topics_lessons_questions(db)

        print("Seed completed.")
        print(f"Test user: {user.email}")
        print(f"Test password: {TEST_USER_PASSWORD}")

    except Exception as exc:
        db.rollback()
        print(f"Seed failed: {exc}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
