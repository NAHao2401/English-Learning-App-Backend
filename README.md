# English Learning App - Backend

Backend cho ứng dụng học tiếng Anh được xây dựng bằng **FastAPI + PostgreSQL + SQLAlchemy**.

---

## 🚀 Công nghệ sử dụng

- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Pydantic
- JWT Authentication
- Uvicorn

---

## 📦 Cài đặt & chạy project

### 1. Clone repository

```
git clone https://github.com/NAHao2401/English-Learning-App-Backend.git
cd English-Learning-App-Backend
```
### 2. Tạo môi trường ảo
```
python -m venv .venv

Kích hoạt môi trường:

Windows:

.venv\Scripts\activate
```
### 3. Cài đặt dependencies
```
pip install -r requirements.txt
```
### 4. Cấu hình biến môi trường
```
Tạo file .env ở thư mục gốc:

DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/english_learning_app
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
FIREBASE_CREDENTIALS_PATH=C:\secure\firebase-service-account.json
```
### 5. Tạo database PostgreSQL
```
Mở PostgreSQL và chạy:

CREATE DATABASE english_learning_app;
```
### 6. Chạy server
```
uvicorn app.main:app --reload
🌐 Truy cập ứng dụng
API: http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

## FCM vocabulary review notifications

Install dependencies and run the database migration:

```powershell
pip install -r requirements.txt
python migrate_add_fcm_notifications.py
```

`FIREBASE_CREDENTIALS_PATH` must point to the Firebase service-account JSON on the backend host.
When it is omitted, the job falls back to Application Default Credentials. Do not store that JSON
in the Android project or commit it to git.

Run the reminder job every five minutes with the hosting platform scheduler. For Linux cron:

```cron
*/5 * * * * cd /path/to/English-Learning-App-Backend && .venv/bin/python -m app.jobs.review_notifications
```

For a manual run:

```powershell
python -m app.jobs.review_notifications
```

The job sends at most one vocabulary reminder per user per run. It only includes words where
`next_review_at <= NOW()` and skips users who reviewed vocabulary during the previous five minutes.
