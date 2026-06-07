"""
Seed dữ liệu câu mẫu cho bảng speaking_sentences.
Chạy: python -m app.db.seed_speaking
"""

from app.db.session import SessionLocal
from app.models.speaking import SpeakingSentence

SENTENCES = [
    # ── FOOD ────────────────────────────────────────────────────────
    {
        "sentence": "I would like a cup of coffee, please.",
        "translation": "Cho tôi một tách cà phê.",
        "difficulty": "beginner",
        "topic": "food",
    },
    {
        "sentence": "This dish is delicious!",
        "translation": "Món này rất ngon!",
        "difficulty": "beginner",
        "topic": "food",
    },
    {
        "sentence": "Can I see the menu, please?",
        "translation": "Cho tôi xem thực đơn được không?",
        "difficulty": "beginner",
        "topic": "food",
    },
    {
        "sentence": "I am allergic to peanuts.",
        "translation": "Tôi bị dị ứng với đậu phộng.",
        "difficulty": "intermediate",
        "topic": "food",
    },
    {
        "sentence": "The restaurant was fully booked, so we ordered takeaway instead.",
        "translation": "Nhà hàng đã đặt hết chỗ nên chúng tôi đặt mang về.",
        "difficulty": "intermediate",
        "topic": "food",
    },
    {
        "sentence": "The chef sources all ingredients locally to ensure freshness.",
        "translation": "Đầu bếp lấy nguyên liệu từ địa phương để đảm bảo độ tươi ngon.",
        "difficulty": "advanced",
        "topic": "food",
    },

    # ── TRAVEL ──────────────────────────────────────────────────────
    {
        "sentence": "Where is the nearest bus stop?",
        "translation": "Trạm xe buýt gần nhất ở đâu?",
        "difficulty": "beginner",
        "topic": "travel",
    },
    {
        "sentence": "I need to check in for my flight.",
        "translation": "Tôi cần làm thủ tục cho chuyến bay.",
        "difficulty": "beginner",
        "topic": "travel",
    },
    {
        "sentence": "Could you recommend a good hotel in the city center?",
        "translation": "Bạn có thể giới thiệu khách sạn tốt ở trung tâm không?",
        "difficulty": "intermediate",
        "topic": "travel",
    },
    {
        "sentence": "My luggage was lost during the connecting flight.",
        "translation": "Hành lý của tôi bị thất lạc trong chuyến bay nối chuyến.",
        "difficulty": "intermediate",
        "topic": "travel",
    },
    {
        "sentence": "Traveling broadens your perspective and deepens cultural understanding.",
        "translation": "Du lịch mở rộng tầm nhìn và hiểu biết văn hóa.",
        "difficulty": "advanced",
        "topic": "travel",
    },

    # ── DAILY LIFE ──────────────────────────────────────────────────
    {
        "sentence": "Good morning! How are you today?",
        "translation": "Chào buổi sáng! Hôm nay bạn khỏe không?",
        "difficulty": "beginner",
        "topic": "daily_life",
    },
    {
        "sentence": "I usually wake up at seven o'clock.",
        "translation": "Tôi thường thức dậy lúc bảy giờ.",
        "difficulty": "beginner",
        "topic": "daily_life",
    },
    {
        "sentence": "I forgot to set my alarm and woke up late.",
        "translation": "Tôi quên đặt báo thức và thức dậy muộn.",
        "difficulty": "intermediate",
        "topic": "daily_life",
    },
    {
        "sentence": "Maintaining a healthy work-life balance is important.",
        "translation": "Duy trì cân bằng giữa công việc và cuộc sống rất quan trọng.",
        "difficulty": "advanced",
        "topic": "daily_life",
    },

    # ── WORK ────────────────────────────────────────────────────────
    {
        "sentence": "I have a meeting at nine.",
        "translation": "Tôi có cuộc họp lúc chín giờ.",
        "difficulty": "beginner",
        "topic": "work",
    },
    {
        "sentence": "Could you send me the report by Friday?",
        "translation": "Bạn có thể gửi báo cáo cho tôi trước thứ Sáu không?",
        "difficulty": "intermediate",
        "topic": "work",
    },
    {
        "sentence": "The project deadline was extended due to unforeseen circumstances.",
        "translation": "Hạn chót dự án được gia hạn do tình huống không lường trước.",
        "difficulty": "advanced",
        "topic": "work",
    },

    # ── HEALTH ──────────────────────────────────────────────────────
    {
        "sentence": "I have a headache.",
        "translation": "Tôi bị đau đầu.",
        "difficulty": "beginner",
        "topic": "health",
    },
    {
        "sentence": "You should drink more water every day.",
        "translation": "Bạn nên uống nhiều nước hơn mỗi ngày.",
        "difficulty": "beginner",
        "topic": "health",
    },
    {
        "sentence": "Regular exercise helps reduce stress and improve sleep quality.",
        "translation": "Tập thể dục thường xuyên giúp giảm căng thẳng và cải thiện giấc ngủ.",
        "difficulty": "intermediate",
        "topic": "health",
    },
    {
        "sentence": "The doctor advised me to monitor my blood pressure daily.",
        "translation": "Bác sĩ khuyên tôi theo dõi huyết áp hàng ngày.",
        "difficulty": "advanced",
        "topic": "health",
    },

    # ── SHOPPING ────────────────────────────────────────────────────
    {
        "sentence": "How much does this cost?",
        "translation": "Cái này giá bao nhiêu?",
        "difficulty": "beginner",
        "topic": "shopping",
    },
    {
        "sentence": "Do you have this in a larger size?",
        "translation": "Bạn có cái này cỡ lớn hơn không?",
        "difficulty": "beginner",
        "topic": "shopping",
    },
    {
        "sentence": "I would like to return this item because it is defective.",
        "translation": "Tôi muốn trả lại sản phẩm này vì nó bị lỗi.",
        "difficulty": "intermediate",
        "topic": "shopping",
    },
]


def seed():
    db = SessionLocal()
    try:
        existing = db.query(SpeakingSentence).count()
        if existing > 0:
            print(f"Already have {existing} sentences. Skipping seed.")
            return

        db.bulk_insert_mappings(SpeakingSentence, SENTENCES)
        db.commit()
        print(f"Seeded {len(SENTENCES)} speaking sentences.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()