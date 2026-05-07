# 🚀 Backend Setup & Android Connection - Quick Start

## 📋 Yêu Cầu

- PostgreSQL chạy trên `localhost:5432`
- Python 3.8+
- Android SDK / ADB tools
- USB debugging enabled trên Android

---

## 1️⃣ Chạy Backend

```powershell
# Cài dependencies
pip install -r requirements.txt

# Seed vocabulary data (nếu chưa có)
python seed_vocabularies.py

# Chạy server FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend ready: `http://127.0.0.1:8000/docs`

---

## 2️⃣ Kết Nối Android Qua USB

### Terminal 1 - Chạy Backend (giữ nguyên)
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Setup ADB Reverse
```powershell
# Kết nối điện thoại bằng cáp USB (bật USB debugging)
adb devices
# Output: 
# R58R81LT7PN   device

# Tạo tunnel
adb reverse tcp:8000 tcp:8000
# Output:
# reverse tcp:8000 tcp:8000
```

✅ Giờ app Android có thể gọi: `http://127.0.0.1:8000/`

---

## 3️⃣ Test API Từ Điện Thoại

### Retrofit Setup (Android)
```kotlin
val retrofit = Retrofit.Builder()
    .baseUrl("http://127.0.0.1:8000/")
    .addConverterFactory(GsonConverterFactory.create())
    .addCallAdapterFactory(RxJava3CallAdapterFactory.create())
    .build()

val api = retrofit.create(EnglishLearningApi::class.java)
```

### Gọi API Vocabulary
```kotlin
// Lấy tất cả topics
val topics = api.getTopics()

// Lấy từ vựng level A1
val vocabs = api.getAllVocabularies("A1")

// Lấy từ vựng của topic Daily Life (ID=2)
val dailyVocabs = api.getVocabulariesByTopic(2)
```

---

## 📊 Dữ Liệu Có Sẵn

| Level | Topics | Từ Vựng | API |
|-------|--------|--------|-----|
| A0 | Từ Vựng Mất Gốc | 15 | `?level=A0` |
| A1 | Daily Life + Food & Drink | 30 | `?level=A1` |
| A2 | Health & Body + Travel & Places | 30 | `?level=A2` |
| B1 | Work + Tech + Nature | 45 | `?level=B1` |
| B2 | Arts & Culture | 15 | `?level=B2` |

---

## 🔗 API Endpoints

```
GET  /lessons/topics                               # Lấy tất cả 9 topics
GET  /lessons/vocabularies/all?level=B1            # Lấy 45 từ vựng B1
GET  /lessons/vocabularies/all?level=A2            # Lấy 30 từ vựng A2
GET  /lessons/vocabularies/topic/{topic_id}       # Lấy 15 từ vựng của 1 topic
```

**Levels:** A0, A1, A2, B1, B2

---

## 🐛 Troubleshoot

| Lỗi | Giải Pháp |
|-----|----------|
| `ModuleNotFoundError: psycopg` | Chạy `pip install -r requirements.txt` |
| Connection refused `localhost:5432` | Bật PostgreSQL service |
| App Android không kết nối được backend | Chạy `adb reverse tcp:8000 tcp:8000` |
| `Vocabulary data already exists` | Seed data đã có, bỏ qua |

---

## 📚 Tài Liệu Đầy Đủ

Xem `VOCABULARY_API_GUIDE.md` để:
- Chi tiết API response
- Cách thêm topic/vocabulary mới
- Migration từ DatabaseSeeder.kt

---

**Chúc bạn thành công! 🎉**
