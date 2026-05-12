# English Learning App Backend - Tổng Quan Dự Án

## 1) Mục đích dự án
Backend này cung cấp API cho ứng dụng học tiếng Anh với các mục tiêu chính:
- Quản lý tài khoản người dùng và xác thực bằng JWT.
- Cung cấp nội dung học theo chủ đề/bài học/câu hỏi.
- Theo dõi tiến độ học tập theo từng bài.
- Chấm điểm, tính XP, streak và thống kê học tập.

Dự án tập trung vào trải nghiệm học theo lộ trình: làm bài theo thứ tự, hoàn thành bài trước để mở khóa bài sau, và có dashboard theo dõi kết quả.

## 2) Kiến trúc tổng thể
Dự án đang theo mô hình phân tầng rõ ràng:
- `API layer` (`app/api`): khai báo endpoint và request/response.
- `Service layer` (`app/services`): chứa logic nghiệp vụ (auth, lesson, progress).
- `Data layer` (`app/models`, `app/db`): ORM models và kết nối PostgreSQL.
- `Core layer` (`app/core`): cấu hình, bảo mật JWT/hash password, logging, exception handlers.

Điểm vào ứng dụng:
- `app/main.py`: khởi tạo FastAPI app, đăng ký routers, exception handlers, tạo bảng DB qua `Base.metadata.create_all(bind=engine)`.

## 3) Thành phần chính
### 3.1 Router/API
- `app/api/auth.py`
  - `POST /auth/register`: đăng ký.
  - `POST /auth/login`: đăng nhập bằng JSON body.
  - `POST /auth/login-form`: đăng nhập theo OAuth2 form (phục vụ Swagger Authorize).
  - `GET /auth/me`: lấy thông tin user hiện tại.

- `app/api/lesson.py`
  - `GET /lessons/topics`: danh sách chủ đề.
  - `GET /lessons`: danh sách bài học có phân trang + lọc level/topic.
  - `GET /lessons/{lesson_id}`: chi tiết bài học.
  - `GET /lessons/{lesson_id}/questions`: danh sách câu hỏi của bài.
  - `POST /lessons/{lesson_id}/answers`: lưu câu trả lời từng câu trong lúc làm bài.
  - `POST /lessons/{lesson_id}/submit`: nộp bài, chấm điểm, tính XP.

- `app/api/progress.py`
  - `GET /progress/me/summary`: tổng quan tiến độ học.
  - `GET /progress/me/lessons`: tiến độ chi tiết theo từng lesson.

### 3.2 Service (nghiệp vụ)
- `app/services/auth_service.py`
  - Đăng ký user mới, kiểm tra email trùng.
  - Đăng nhập: xác thực mật khẩu, tạo access token + refresh token.

- `app/services/lesson_service.py`
  - Lấy danh sách topic/lesson/question.
  - Logic khóa bài theo thứ tự lesson (phải hoàn thành bài trước).
  - Lưu đáp án từng câu (`LessonAnswer`) và cập nhật tiến độ tạm thời.
  - Nộp bài: kiểm tra đã trả lời đủ câu, chấm điểm, pass/fail, cập nhật `Progress`, cộng XP, tăng streak, lưu lịch sử nộp bài.
  - Có cơ chế chống spam submit (`SUBMIT_COOLDOWN_SECONDS`).

- `app/services/progress_service.py`
  - Tính tổng quan học tập: completed/in-progress/not-started/locked.
  - Tính level hiện tại dựa trên XP.
  - Thống kê tuần: XP theo ngày, số bài hoàn thành.
  - Lịch sử hoạt động gần đây.

### 3.3 Data models (ORM)
- `User`: thông tin người dùng, tổng XP, level hiện tại, streak.
- `Topic`: chủ đề học.
- `Lesson`: bài học thuộc chủ đề.
- `Question` + `AnswerOption`: câu hỏi và đáp án lựa chọn.
- `Progress`: tiến độ theo user-lesson.
- `LessonAnswer`: đáp án user lưu theo từng câu.
- `LessonSubmission`: bản ghi mỗi lần nộp bài.
- `XpHistory`: lịch sử cộng XP.

## 4) Luồng hoạt động chính
### Luồng A - Đăng ký/đăng nhập
1. Client gọi `POST /auth/register` để tạo tài khoản.
2. Client gọi `POST /auth/login` để nhận JWT.
3. Các API cần xác thực dùng `Authorization: Bearer <access_token>`.
4. `get_current_user` giải mã token, truy vấn DB, trả về user hiện tại.

### Luồng B - Học bài và nộp bài
1. Client lấy danh sách bài từ `GET /lessons`.
2. Chọn bài và lấy câu hỏi qua `GET /lessons/{lesson_id}/questions`.
3. Trong lúc làm bài, lưu từng đáp án qua `POST /lessons/{lesson_id}/answers`.
4. Khi hoàn tất, gọi `POST /lessons/{lesson_id}/submit`.
5. Backend kiểm tra đủ câu trả lời, chấm điểm, xác định pass/fail:
   - Pass: trạng thái `completed`, completion = 100%.
   - Fail: trạng thái `in_progress`, completion tạm giữ dưới 100%.
6. Backend cộng XP theo luật (đúng câu, thưởng qua bài đầu, thưởng tuyệt đối), cập nhật streak và lưu lịch sử.

### Luồng C - Theo dõi tiến độ
1. `GET /progress/me/summary`: dashboard tổng quan (XP, level, streak, chart lesson, weekly XP...).
2. `GET /progress/me/lessons`: danh sách tiến độ từng bài và trạng thái khóa/mở.

## 5) Các màn hình phía ứng dụng (frontend) tương ứng
Dù repo hiện tại là backend, các API cho thấy ứng dụng client sẽ có các màn hình chức năng sau:
- Màn hình Đăng ký.
- Màn hình Đăng nhập.
- Màn hình Hồ sơ cá nhân (`/auth/me`).
- Màn hình Danh sách chủ đề (`/lessons/topics`).
- Màn hình Danh sách bài học theo chủ đề/level (`/lessons`).
- Màn hình Chi tiết bài học (`/lessons/{lesson_id}`).
- Màn hình Làm bài (render câu hỏi + lưu đáp án tạm + nộp bài).
- Màn hình Kết quả nộp bài (score, đúng/sai, XP nhận được).
- Màn hình Dashboard tiến độ (`/progress/me/summary`).
- Màn hình Tiến độ theo từng bài (`/progress/me/lessons`).

## 6) Công nghệ sử dụng
Theo `requirements.txt` và source code:
- FastAPI: xây dựng REST API.
- Uvicorn: ASGI server.
- SQLAlchemy ORM: truy cập dữ liệu.
- PostgreSQL + psycopg: hệ quản trị CSDL và driver.
- Pydantic + pydantic-settings: validation schema + quản lý cấu hình `.env`.
- python-jose: ký/giải mã JWT.
- pwdlib[argon2]: băm/xác thực mật khẩu.
- python-multipart: hỗ trợ form data (OAuth2 form login).

## 7) Cấu hình môi trường
Biến môi trường cần thiết trong `.env`:
- `DATABASE_URL`
- `SECRET_KEY`
- `ALGORITHM` (mặc định thường là `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`

Ví dụ đang dùng local PostgreSQL database: `english_learning_app`.

## 8) Mục tiêu sản phẩm
- Xây dựng backend học tiếng Anh có lộ trình rõ ràng.
- Tăng động lực học qua cơ chế gamification (XP, level, streak).
- Dễ mở rộng thêm chủ đề, lesson, question và rule tính điểm.
- Sẵn sàng tích hợp frontend mobile/web thông qua API REST.
