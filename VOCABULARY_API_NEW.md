# English Learning App Backend - Vocabulary API Guide

## 📚 Dữ Liệu Vocabulary Đã Được Import

Dữ liệu từ `DatabaseSeeder.kt` (Android) đã được convert và lưu vào PostgreSQL database.

### Cấu Trúc Dữ Liệu

- **9 Topics** (Chủ đề):
  - **A0 - Từ Vựng Mất Gốc** (15 từ): Absolute beginners
  - **A1 - 🏠 Daily Life** (15 từ): Home and routines  
  - **A1 - 🍎 Food & Drink** (15 từ): Food vocabulary
  - **A2 - 🏥 Health & Body** (15 từ): Health and medical terms
  - **A2 - 🌍 Travel & Places** (15 từ): Travel and locations
  - **B1 - 💼 Work & Career** (15 từ): Job and workplace
  - **B1 - 📱 Technology** (15 từ): Tech and digital
  - **B1 - 🌿 Nature & Environment** (15 từ): Nature and climate
  - **B2 - 🎭 Arts & Culture** (15 từ): Art and culture

- **135 Vocabularies** (Tổng từ vựng): Mỗi từ có word, meaning, pronunciation, example_sentence

---

## 🔌 API Endpoints

### 1. Lấy Tất Cả Topics
```
GET http://127.0.0.1:8000/lessons/topics
```

**Response:**
```json
[
  {
    "id": 4,
    "name": "Từ Vựng Mất Gốc",
    "description": "Vocabulary for absolute beginners - the most basic words",
    "icon_url": "🔤",
    "level": "A0"
  },
  ...
]
```

---

### 2. Lấy Tất Cả Vocabularies
```
GET http://127.0.0.1:8000/lessons/vocabularies/all
```

**Tham số tùy chọn:**
- `?level=A0` - Lọc theo level (A0, A1, A2, B1, B2)

**Ví dụ:**
```
GET http://127.0.0.1:8000/lessons/vocabularies/all?level=B1
GET http://127.0.0.1:8000/lessons/vocabularies/all?level=A2
```

**Response:**
```json
[
  {
    "id": 1,
    "topic_id": 4,
    "word": "hello",
    "meaning": "xin chào",
    "pronunciation": "/həˈloʊ/",
    "example_sentence": "Hello! How are you?",
    "audio_url": null,
    "difficulty": "A0"
  },
  ...
]
```

---

### 3. Filter Vocabularies Theo Level

**Available Levels & Topics:**

| Level | Topics | Từ Vựng |
|-------|--------|--------|
| A0 | Từ Vựng Mất Gốc | 15 |
| A1 | Daily Life, Food & Drink | 30 |
| A2 | Health & Body, Travel & Places | 30 |
| B1 | Work & Career, Technology, Nature & Environment | 45 |
| B2 | Arts & Culture | 15 |

**Request:**
```
GET http://127.0.0.1:8000/lessons/vocabularies/all?level=B1
```

**Response:** 45 vocabularies từ B1 level (tất cả 3 topics)

---

### 4. Lấy Vocabularies Của Một Topic
```
GET http://127.0.0.1:8000/lessons/vocabularies/topic/{topic_id}
```

**Ví dụ:** 
```
GET http://127.0.0.1:8000/lessons/vocabularies/topic/9
```

**Response:** Danh sách 15 từ vựng của topic Work & Career (ID=9)

---

## 📊 Danh Sách Topics & IDs

| ID | Topic | Level | Từ Vựng |
|----|-------|-------|---------|
| 4 | Từ Vựng Mất Gốc | A0 | 15 |
| 5 | 🏠 Daily Life | A1 | 15 |
| 6 | 🍎 Food & Drink | A1 | 15 |
| 7 | 🏥 Health & Body | A2 | 15 |
| 8 | 🌍 Travel & Places | A2 | 15 |
| 9 | 💼 Work & Career | B1 | 15 |
| 10 | 📱 Technology | B1 | 15 |
| 11 | 🌿 Nature & Environment | B1 | 15 |
| 12 | 🎭 Arts & Culture | B2 | 15 |

---

## 🚀 Cách Sử Dụng Từ Android App

### 1. Retrofit/OkHttp Interface

```kotlin
interface EnglishLearningApi {
    @GET("/lessons/topics")
    suspend fun getTopics(): List<Topic>

    @GET("/lessons/vocabularies/all")
    suspend fun getAllVocabularies(
        @Query("level") level: String? = null
    ): List<Vocabulary>

    @GET("/lessons/vocabularies/topic/{topic_id}")
    suspend fun getVocabulariesByTopic(
        @Path("topic_id") topicId: Int
    ): List<Vocabulary>
}
```

### 2. Gọi API Từ Coroutine

```kotlin
val api = retrofit.create(EnglishLearningApi::class.java)

// Lấy tất cả topics
val topics = api.getTopics()

// Lấy từ vựng B1 (45 từ từ 3 topics)
val b1Vocabs = api.getAllVocabularies("B1")

// Lấy từ vựng A2 (30 từ từ 2 topics)
val a2Vocabs = api.getAllVocabularies("A2")

// Lấy từ vựng của topic Work & Career (ID=9)
val workVocabs = api.getVocabulariesByTopic(9)

// Lấy từ vựng của topic Technology (ID=10)
val techVocabs = api.getVocabulariesByTopic(10)
```

---

## 📱 Chạy Backend Khi Kết Nối Android

### 1. Bật USB Debugging trên điện thoại

### 2. Chạy Backend Trên Máy Tính
```powershell
cd d:\Project\English-Learning-App-Backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Setup ADB Reverse (Cáp USB)
```powershell
adb reverse tcp:8000 tcp:8000
```

### 4. Trong Android App - Base URL
```kotlin
val retrofit = Retrofit.Builder()
    .baseUrl("http://127.0.0.1:8000/")
    .addConverterFactory(GsonConverterFactory.create())
    .build()
```

---

## 🗂️ Files Đã Thay Đổi

### Backend

1. **app/models/lesson.py** - Thêm `Vocabulary` model
   - Liên kết với Topic (Foreign Key)
   - Lưu: word, meaning, pronunciation, example_sentence, audio_url, difficulty

2. **app/schemas/lesson.py** - Thêm `VocabularyResponse` schema
   - Serialize Vocabulary model thành JSON

3. **app/services/lesson_service.py** - Thêm hàm queries
   - `get_vocabularies_by_topic(db, topic_id)` - Lấy vocab theo topic
   - `get_all_vocabularies(db, level)` - Lấy vocab theo level

4. **app/api/lesson.py** - Thêm 2 endpoints
   - `GET /lessons/vocabularies/all?level=X` - Lấy vocab theo level
   - `GET /lessons/vocabularies/topic/{id}` - Lấy vocab theo topic

5. **seed_vocabularies.py** - Script seed dữ liệu
   - Import dữ liệu từ DatabaseSeeder.kt
   - Chạy: `python seed_vocabularies.py`

---

## ✅ Test Nhanh Trên Swagger UI

1. Mở: http://127.0.0.1:8000/docs
2. Tìm section **Lessons**
3. Test các endpoint tương ứng

---

## 📝 Notes

- **Vocabulary** model độc lập với Lesson (có thể dùng cho flash card, vocabulary learning)
- **Lesson** dùng cho quiz/tests (có Questions và AnswerOptions)
- **Level filter** trả về tất cả từ vựng của level đó từ tất cả topics
- **Topic filter** trả về chỉ 15 từ vựng của topic đó
- Có thể mở rộng thêm model VocabularyProgress để track từ vựng đã học
