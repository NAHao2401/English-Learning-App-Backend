# English Learning App - Backend

Backend REST API cho ứng dụng học tiếng Anh, được xây dựng bằng **FastAPI**, **PostgreSQL**, **SQLAlchemy** và **JWT Authentication**.  
Project cung cấp các API phục vụ đăng ký, đăng nhập, quản lý bài học, từ vựng, câu hỏi, nộp bài, tính điểm, XP, streak và theo dõi tiến độ học tập.

---

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Tính năng chính](#tính-năng-chính)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Cấu trúc project](#cấu-trúc-project)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt và chạy project](#cài-đặt-và-chạy-project)
- [Cấu hình môi trường](#cấu-hình-môi-trường)
- [Seed dữ liệu mẫu](#seed-dữ-liệu-mẫu)
- [API chính](#api-chính)
- [Kết nối với Android app](#kết-nối-với-android-app)
- [Tài liệu API](#tài-liệu-api)
- [Troubleshooting](#troubleshooting)

---

## Giới thiệu

English Learning App Backend là phần server cho ứng dụng học tiếng Anh. Backend chịu trách nhiệm:

- Quản lý tài khoản người dùng.
- Xác thực người dùng bằng JWT.
- Cung cấp danh sách topic, lesson, question và vocabulary.
- Lưu câu trả lời trong quá trình làm bài.
- Chấm điểm khi người dùng nộp bài.
- Tính XP, level, streak và thống kê tiến độ học tập.
- Cung cấp API để tích hợp với frontend web hoặc Android app.

Project phù hợp cho ứng dụng học tiếng Anh theo lộ trình, nơi người học hoàn thành từng bài, mở khóa bài tiếp theo và theo dõi quá trình học của mình qua dashboard.

---

## Tính năng chính

### Authentication

- Đăng ký tài khoản mới.
- Đăng nhập bằng email và mật khẩu.
- Đăng nhập bằng OAuth2 form để test trực tiếp trên Swagger UI.
- Lấy thông tin người dùng hiện tại.
- Bảo vệ API bằng JWT Bearer Token.
- Hash mật khẩu bằng Argon2.

### Lesson & Quiz

- Lấy danh sách topic.
- Lấy danh sách lesson theo level hoặc topic.
- Xem chi tiết lesson.
- Lấy danh sách câu hỏi của lesson.
- Lưu câu trả lời từng câu trong quá trình làm bài.
- Nộp bài và tự động chấm điểm.
- Kiểm tra pass/fail.
- Cập nhật tiến độ học tập sau khi nộp bài.

### Vocabulary

- Lấy toàn bộ danh sách từ vựng.
- Lọc từ vựng theo level: `A0`, `A1`, `A2`, `B1`, `B2`.
- Lấy từ vựng theo từng topic.
- Dữ liệu từ vựng gồm: word, meaning, pronunciation, example sentence, audio URL và difficulty.

### Progress & Gamification

- Theo dõi số bài đã hoàn thành.
- Theo dõi bài đang học, bài chưa học và bài bị khóa.
- Tính XP sau khi hoàn thành bài.
- Tính level hiện tại dựa trên XP.
- Theo dõi streak học tập.
- Thống kê XP theo tuần.
- Lưu lịch sử nộp bài và lịch sử cộng XP.

---

## Công nghệ sử dụng

- **Python**
- **FastAPI**
- **Uvicorn**
- **PostgreSQL**
- **SQLAlchemy ORM**
- **Pydantic**
- **pydantic-settings**
- **python-jose**
- **pwdlib[argon2]**
- **python-multipart**
- **email-validator**

---

## Cấu trúc project

```text
English-Learning-App-Backend/
│
├── app/
│   ├── api/                 # Khai báo các API routes
│   │   ├── auth.py
│   │   ├── lesson.py
│   │   └── progress.py
│   │
│   ├── core/                # Cấu hình, bảo mật, JWT, exception handlers
│   │
│   ├── db/                  # Kết nối database
│   │
│   ├── models/              # SQLAlchemy ORM models
│   │
│   ├── schemas/             # Pydantic request/response schemas
│   │
│   ├── services/            # Business logic
│   │
│   └── main.py              # Entry point của FastAPI app
│
├── scripts/                 # Các script hỗ trợ
├── static/audio/            # File audio cho vocabulary/example
│
├── DatabaseSeeder.kt
├── seed_lessons.py
├── seed_vocabularies.py
├── generate_audio_files.py
├── update_vocabularies_audio.py
├── update_seed_with_edge_tts_audio.py
├── migrate_add_example_audio.py
│
├── PROJECT_OVERVIEW.md
├── QUICK_START.md
├── VOCABULARY_API_NEW.md
├── requirements.txt
└── README.md
```

---

## Yêu cầu hệ thống

Trước khi chạy project, cần cài đặt:

- Python 3.8 trở lên
- PostgreSQL
- pip
- Git

Nếu muốn kết nối với Android app qua USB, cần thêm:

- Android SDK / ADB tools
- Bật USB debugging trên điện thoại Android

---

## Cài đặt và chạy project

### 1. Clone repository

```bash
git clone https://github.com/NAHao2401/English-Learning-App-Backend.git
cd English-Learning-App-Backend
```

### 2. Tạo môi trường ảo

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Tạo database PostgreSQL

Mở PostgreSQL và tạo database:

```sql
CREATE DATABASE english_learning_app;
```

### 5. Tạo file `.env`

Tạo file `.env` ở thư mục gốc của project:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/english_learning_app
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Thay `your_password` bằng mật khẩu PostgreSQL trên máy của bạn.

### 6. Chạy server

```bash
uvicorn app.main:app --reload
```

Sau khi chạy thành công, truy cập:

```text
API Root:   http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs
ReDoc:      http://127.0.0.1:8000/redoc
```

---

## Cấu hình môi trường

Các biến môi trường chính:

| Biến môi trường | Ý nghĩa |
|---|---|
| `DATABASE_URL` | Chuỗi kết nối PostgreSQL |
| `SECRET_KEY` | Khóa bí mật dùng để ký JWT |
| `ALGORITHM` | Thuật toán ký JWT, thường dùng `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Thời gian hết hạn của access token |

Ví dụ:

```env
DATABASE_URL=postgresql+psycopg://postgres:123456@localhost:5432/english_learning_app
SECRET_KEY=my_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Seed dữ liệu mẫu

Project có các script để thêm dữ liệu mẫu vào database.

### Seed lessons

```bash
python seed_lessons.py
```

### Seed vocabularies

```bash
python seed_vocabularies.py
```

Dữ liệu vocabulary hiện có:

| Level | Topics | Số từ vựng |
|---|---|---:|
| A0 | Từ Vựng Mất Gốc | 15 |
| A1 | Daily Life, Food & Drink | 30 |
| A2 | Health & Body, Travel & Places | 30 |
| B1 | Work & Career, Technology, Nature & Environment | 45 |
| B2 | Arts & Culture | 15 |

Tổng cộng có **9 topics** và **135 vocabularies**.

---

## API chính

### Authentication

| Method | Endpoint | Mô tả |
|---|---|---|
| `POST` | `/auth/register` | Đăng ký tài khoản mới |
| `POST` | `/auth/login` | Đăng nhập bằng JSON body |
| `POST` | `/auth/login-form` | Đăng nhập bằng OAuth2 form |
| `GET` | `/auth/me` | Lấy thông tin user hiện tại |

### Lessons

| Method | Endpoint | Mô tả |
|---|---|---|
| `GET` | `/lessons/topics` | Lấy danh sách topic |
| `GET` | `/lessons` | Lấy danh sách lesson, hỗ trợ phân trang/lọc |
| `GET` | `/lessons/{lesson_id}` | Lấy chi tiết một lesson |
| `GET` | `/lessons/{lesson_id}/questions` | Lấy câu hỏi của lesson |
| `POST` | `/lessons/{lesson_id}/answers` | Lưu câu trả lời từng câu |
| `POST` | `/lessons/{lesson_id}/submit` | Nộp bài và chấm điểm |

### Vocabulary

| Method | Endpoint | Mô tả |
|---|---|---|
| `GET` | `/lessons/vocabularies/all` | Lấy tất cả vocabularies |
| `GET` | `/lessons/vocabularies/all?level=A1` | Lọc vocabulary theo level |
| `GET` | `/lessons/vocabularies/topic/{topic_id}` | Lấy vocabulary theo topic |

Ví dụ:

```text
GET http://127.0.0.1:8000/lessons/vocabularies/all?level=B1
GET http://127.0.0.1:8000/lessons/vocabularies/topic/9
```

### Progress

| Method | Endpoint | Mô tả |
|---|---|---|
| `GET` | `/progress/me/summary` | Lấy tổng quan tiến độ học tập |
| `GET` | `/progress/me/lessons` | Lấy tiến độ chi tiết theo từng lesson |

---

## Luồng sử dụng cơ bản

### 1. Đăng ký và đăng nhập

```text
POST /auth/register
POST /auth/login
```

Sau khi đăng nhập, client nhận access token và gửi token trong header:

```http
Authorization: Bearer <access_token>
```

### 2. Học bài

```text
GET /lessons
GET /lessons/{lesson_id}/questions
POST /lessons/{lesson_id}/answers
POST /lessons/{lesson_id}/submit
```

### 3. Xem tiến độ

```text
GET /progress/me/summary
GET /progress/me/lessons
```

---

## Kết nối với Android app

Khi chạy backend để Android app có thể gọi API, nên chạy server với host `0.0.0.0`:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Nếu test bằng điện thoại Android qua cáp USB, dùng ADB reverse:

```bash
adb devices
adb reverse tcp:8000 tcp:8000
```

Sau đó Android app có thể gọi backend bằng base URL:

```kotlin
val retrofit = Retrofit.Builder()
    .baseUrl("http://127.0.0.1:8000/")
    .addConverterFactory(GsonConverterFactory.create())
    .build()
```

Ví dụ interface Retrofit:

```kotlin
interface EnglishLearningApi {
    @GET("/lessons/topics")
    suspend fun getTopics(): List<TopicResponse>

    @GET("/lessons/vocabularies/all")
    suspend fun getAllVocabularies(
        @Query("level") level: String? = null
    ): List<VocabularyResponse>

    @GET("/lessons/vocabularies/topic/{topic_id}")
    suspend fun getVocabulariesByTopic(
        @Path("topic_id") topicId: Int
    ): List<VocabularyResponse>
}
```

---

## Tài liệu API

Sau khi chạy server, có thể test API trực tiếp tại:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Swagger UI hỗ trợ test các endpoint, truyền request body và authorize bằng JWT token.

---

## Troubleshooting

| Lỗi | Nguyên nhân có thể | Cách xử lý |
|---|---|---|
| `ModuleNotFoundError: psycopg` | Chưa cài dependencies | Chạy `pip install -r requirements.txt` |
| `Connection refused localhost:5432` | PostgreSQL chưa chạy hoặc sai port | Kiểm tra PostgreSQL service và `DATABASE_URL` |
| Không kết nối được database | Sai username/password/database name | Kiểm tra lại file `.env` |
| Android app không gọi được API | Chưa chạy ADB reverse | Chạy `adb reverse tcp:8000 tcp:8000` |
| `Vocabulary data already exists` | Dữ liệu đã được seed trước đó | Có thể bỏ qua thông báo này |
| Swagger không authorize được | Chưa truyền JWT token | Login trước, copy access token vào nút Authorize |

---

## Ghi chú phát triển

- `Vocabulary` hiện độc lập với `Lesson`, phù hợp để phát triển thêm chức năng flashcard hoặc luyện từ vựng riêng.
- Có thể mở rộng thêm `VocabularyProgress` để lưu tiến độ học từng từ.
- Có thể bổ sung migration tool như Alembic nếu project phát triển lớn hơn.
- Có thể thêm Docker Compose để chạy FastAPI và PostgreSQL dễ hơn.
- Có thể thêm test với pytest cho service layer và API layer.
