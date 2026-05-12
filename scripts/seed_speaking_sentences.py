"""
Script seed dữ liệu câu mẫu vào bảng speaking_sentences.
Chạy: python -m scripts.seed_speaking_sentences
"""

from app.db.session import SessionLocal
from app.models.speaking import SpeakingSentence

SENTENCES = [
    # Beginner - Greetings
    {"sentence": "Hello, how are you?", "translation": "Xin chào, bạn có khỏe không?", "difficulty": "beginner", "topic": "greetings"},
    {"sentence": "My name is John.", "translation": "Tên tôi là John.", "difficulty": "beginner", "topic": "greetings"},
    {"sentence": "Nice to meet you.", "translation": "Rất vui được gặp bạn.", "difficulty": "beginner", "topic": "greetings"},
    {"sentence": "Good morning!", "translation": "Chào buổi sáng!", "difficulty": "beginner", "topic": "greetings"},
    {"sentence": "See you later.", "translation": "Hẹn gặp lại.", "difficulty": "beginner", "topic": "greetings"},

    # Beginner - Food
    {"sentence": "I like to eat pizza.", "translation": "Tôi thích ăn pizza.", "difficulty": "beginner", "topic": "food"},
    {"sentence": "Can I have a glass of water?", "translation": "Cho tôi một ly nước được không?", "difficulty": "beginner", "topic": "food"},
    {"sentence": "This food is delicious.", "translation": "Món ăn này ngon lắm.", "difficulty": "beginner", "topic": "food"},
    {"sentence": "I am hungry.", "translation": "Tôi đang đói.", "difficulty": "beginner", "topic": "food"},
    {"sentence": "What would you like to drink?", "translation": "Bạn muốn uống gì?", "difficulty": "beginner", "topic": "food"},

    # Beginner - Travel
    {"sentence": "Where is the bus station?", "translation": "Bến xe buýt ở đâu?", "difficulty": "beginner", "topic": "travel"},
    {"sentence": "How much does this cost?", "translation": "Cái này giá bao nhiêu?", "difficulty": "beginner", "topic": "travel"},
    {"sentence": "I need a taxi please.", "translation": "Tôi cần một chiếc taxi.", "difficulty": "beginner", "topic": "travel"},

    # Intermediate - Daily life
    {"sentence": "I usually wake up at seven in the morning.", "translation": "Tôi thường thức dậy lúc bảy giờ sáng.", "difficulty": "intermediate", "topic": "daily_life"},
    {"sentence": "Could you please repeat that more slowly?", "translation": "Bạn có thể nhắc lại chậm hơn không?", "difficulty": "intermediate", "topic": "daily_life"},
    {"sentence": "I have been studying English for two years.", "translation": "Tôi đã học tiếng Anh được hai năm rồi.", "difficulty": "intermediate", "topic": "daily_life"},
    {"sentence": "What do you usually do on weekends?", "translation": "Bạn thường làm gì vào cuối tuần?", "difficulty": "intermediate", "topic": "daily_life"},
    {"sentence": "I enjoy reading books in my free time.", "translation": "Tôi thích đọc sách vào thời gian rảnh.", "difficulty": "intermediate", "topic": "daily_life"},

    # Intermediate - Work
    {"sentence": "I work as a software engineer.", "translation": "Tôi làm kỹ sư phần mềm.", "difficulty": "intermediate", "topic": "work"},
    {"sentence": "The meeting has been postponed until next Monday.", "translation": "Cuộc họp đã bị hoãn đến thứ Hai tuần sau.", "difficulty": "intermediate", "topic": "work"},
    {"sentence": "Can we schedule a meeting for tomorrow afternoon?", "translation": "Chúng ta có thể lên lịch họp vào chiều mai không?", "difficulty": "intermediate", "topic": "work"},

    # Advanced
    {"sentence": "The rapid advancement of technology has significantly transformed the way we communicate.", "translation": "Sự phát triển nhanh chóng của công nghệ đã thay đổi đáng kể cách chúng ta giao tiếp.", "difficulty": "advanced", "topic": "technology"},
    {"sentence": "Environmental sustainability requires collective responsibility from both individuals and corporations.", "translation": "Bền vững môi trường đòi hỏi trách nhiệm tập thể từ cả cá nhân lẫn doanh nghiệp.", "difficulty": "advanced", "topic": "environment"},
    {"sentence": "Despite the challenges, she managed to complete the project ahead of schedule.", "translation": "Dù gặp nhiều thách thức, cô ấy vẫn hoàn thành dự án trước hạn.", "difficulty": "advanced", "topic": "daily_life"},
]


def seed():
    db = SessionLocal()
    try:
        existing = db.query(SpeakingSentence).count()
        if existing > 0:
            print(f"Đã có {existing} câu trong database, bỏ qua seed.")
            return

        for item in SENTENCES:
            db.add(SpeakingSentence(**item))

        db.commit()
        print(f"Đã seed {len(SENTENCES)} câu mẫu thành công.")
    except Exception as e:
        db.rollback()
        print(f"Lỗi khi seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()