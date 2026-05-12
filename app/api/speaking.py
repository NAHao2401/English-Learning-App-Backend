# POST /speaking/practices
# Lưu kết quả 1 lần luyện nói (mobile gọi sau khi tính score xong)
{
  "target_text": "The quick brown fox",
  "spoken_text": "The quick brown dog",
  "score": 75,
  "is_matched": true,
  "lesson_id": null   # optional
}

# GET /speaking/practices/me
# Lấy lịch sử luyện nói của user hiện tại
# Response: list các practice, có phân trang

# GET /speaking/practices/me/stats
# Thống kê tổng hợp cho Progress screen
# Response:
{
  "total_practices": 24,
  "matched_count": 18,
  "average_score": 76.5,
  "best_score": 100,
  "weekly_practices": [3, 0, 2, 5, 1, 4, 0]  # 7 ngày gần nhất
}

# GET /speaking/sentences
# Trả về danh sách câu mẫu để luyện (thay vì hardcode trong app)
# Query params: ?difficulty=beginner&topic=food&limit=10