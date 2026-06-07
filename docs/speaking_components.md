# Thành phần liên quan đến "speaking" trong dự án

Tệp này mô tả chi tiết các thành phần liên quan đến chức năng luyện nói (speaking) trong dự án, bao gồm API, schemas, service, scripts và vị trí file.

---

## Tổng quan
- `speaking` gồm: endpoint để lưu kết quả luyện nói, lấy câu mẫu, lấy lịch sử và thống kê; service xử lý logic (XP, thống kê); schema định nghĩa request/response; script để seed dữ liệu câu luyện nói.

## API (router)
- `app/models/speaking.py`:
  - Router prefix: `/speaking` (tag `Speaking`).
  - Endpoints:
    - `POST /speaking/practices` — lưu 1 lần luyện nói. Request: `SaveSpeakingPracticeRequest` (xem `app/schemas/speaking.py`). Response: `SpeakingPracticeResponse`.
    - `GET /speaking/practices/me` — lấy lịch sử luyện nói của user (phân trang). Response: `PaginatedPracticeResponse`.
    - `GET /speaking/practices/me/stats` — lấy thống kê tổng hợp cho user (tổng lần luyện, điểm TB, best score, biểu đồ 7 ngày).
    - `GET /speaking/sentences` — lấy câu mẫu để luyện nói (lọc `difficulty`, `topic`, `limit`).
  - Ghi chú: hiện file này nằm trong `app/models/` (không phải `app/api/`); có thể xem lại vị trí để tránh nhầm lẫn.

- `app/api/speaking.py`:
  - Router prefix: `/speaking` (tag `speaking`).
  - Endpoints:
    - `GET /speaking/topics` — lấy danh sách chủ đề (Topic) kèm số câu.
    - `GET /speaking/topics/{topic_id}/sentences` — lấy câu theo chủ đề.
    - `POST /speaking/result` — (một route nhỏ dùng để lưu result/XP trong ví dụ cũ).
  - File này dùng `Topic`, `Lesson`, `Question` từ `app/models/lesson.py` để lấy câu.

> Lưu ý: Hiện có hai router cho `prefix=/speaking` ở hai vị trí khác nhau (`app/models/speaking.py` và `app/api/speaking.py`). Cần quyết định giữ router nào hoặc hợp nhất để tránh trùng route.

## Service
- `app/services/speaking_service.py` — chứa logic chính:
  - `save_practice(db, user, data: SaveSpeakingPracticeRequest) -> SpeakingPractice`:
    - Tạo `SpeakingPractice` record, cộng XP cho user (hàm `_calculate_speaking_xp`).
    - Ghi thêm record `XpHistory` khi có XP.
  - `get_practices(db, user_id, page, limit)` — trả về dict phân trang chứa `items`, `page`, `limit`, `total`, `total_pages`.
  - `get_stats(db, user_id)` — tính `total_practices`, `matched_count`, `average_score`, `best_score`, và `weekly_practices` (7 ngày gần nhất).
  - `get_sentences(db, difficulty, topic, limit)` — lấy câu mẫu từ `SpeakingSentence` (lọc difficulty/topic, random, limit).
  - Hằng số XP: `SPEAKING_MATCHED_XP = 5`, `SPEAKING_PERFECT_XP = 10`.

## Schemas (Pydantic)
- `app/schemas/speaking.py` chứa các lớp sau:
  - `SaveSpeakingPracticeRequest`:
    - `target_text: str`, `spoken_text: str | None`, `score: int (0-100)`, `is_matched: bool`, `lesson_id: int | None`.
  - `SpeakingPracticeResponse`:
    - `id, user_id, lesson_id, target_text, spoken_text, score, is_matched, created_at`.
  - `SpeakingStatsResponse`:
    - `total_practices, matched_count, average_score, best_score, weekly_practices` (list 7 phần tử).
  - `SpeakingSentenceResponse`:
    - `id, sentence, translation, difficulty, topic`.
  - `PaginatedPracticeResponse`:
    - `items: list[SpeakingPracticeResponse], page, limit, total, total_pages`.

## Models (DB)
- `app/services/speaking_service.py` tham chiếu đến các model `SpeakingPractice` và `SpeakingSentence` (ví dụ: `from app.models.speaking import SpeakingPractice, SpeakingSentence`).
- Tuy nhiên, hiện tại file `app/models/speaking.py` trong repo là một API router và không chứa định nghĩa các class DB `SpeakingPractice` / `SpeakingSentence`.
  - Kiểm tra cần thực hiện: tìm nơi định nghĩa DB model của `SpeakingPractice` và `SpeakingSentence`. Nếu chưa có, cần thêm file `app/models/speaking_models.py` hoặc di chuyển/ bổ sung các class model vào `app/models/speaking.py` và tách router sang `app/api/speaking.py`.
- Các model liên quan khác dùng chung: `Topic`, `Lesson`, `Question` (xem `app/models/lesson.py`).

## Scripts
- `scripts/seed_speaking_sentences.py` — script để seed dữ liệu `SpeakingSentence` vào DB (sử dụng `db.add(SpeakingSentence(**item))`).

## Luồng dữ liệu (tóm tắt)
1. Client gửi request (ví dụ `POST /speaking/practices`) với payload theo `SaveSpeakingPracticeRequest`.
2. Router (`app/models/speaking.py` hoặc `app/api/speaking.py`) nhận request, dùng `Depends(get_db)` và `Depends(get_current_user)` để lấy DB và user.
3. Router gọi `app/services/speaking_service.save_practice(...)` để lưu practice và tính XP.
4. `speaking_service` tạo/ cập nhật `SpeakingPractice`, `XpHistory` và cập nhật `user.total_xp`.

## Gợi ý hành động tiếp theo
- Kiểm tra/ bổ sung định nghĩa DB models `SpeakingPractice` và `SpeakingSentence` nếu chưa tồn tại.
- Hợp nhất router `prefix=/speaking` (giữa `app/models/speaking.py` và `app/api/speaking.py`) để tránh trùng lặp.
- Chạy seed script để kiểm thử endpoint lấy câu mẫu:

```bash
# kích hoạt environment (nếu dùng venv/conda)
uvicorn app.main:app --reload
# hoặc để chạy seed script
python scripts/seed_speaking_sentences.py
```

## Vị trí file tham khảo
- `app/models/speaking.py`  (hiện là router)
- `app/api/speaking.py`     (router khác liên quan đến topics/sentences)
- `app/services/speaking_service.py`
- `app/schemas/speaking.py`
- `scripts/seed_speaking_sentences.py`
- `app/models/lesson.py` (Topic / Lesson / Question)

---

Nếu bạn muốn, mình có thể:
- Tạo/di chuyển DB model `SpeakingPractice` và `SpeakingSentence` vào `app/models/` (mình sẽ tạo file model và migration mẫu),
- Hoặc hợp nhất hai router `prefix=/speaking` thành một file API duy nhất.

Bạn muốn mình làm tiếp bước nào?