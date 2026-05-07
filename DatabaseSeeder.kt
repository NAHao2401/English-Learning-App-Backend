package com.example.englishlearningapp.data.local.db

import android.content.Context
import androidx.room.RoomDatabase
import androidx.sqlite.db.SupportSQLiteDatabase
import com.example.englishlearningapp.data.local.db.entity.TopicEntity
import com.example.englishlearningapp.data.local.db.entity.VocabularyEntity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

object DatabaseSeeder {

    private data class VocabularySeed(
        val word: String,
        val meaning: String,
        val pronunciation: String,
        val exampleSentence: String
    )

    private data class TopicSeed(
        val name: String,
        val description: String,
        val iconUrl: String,
        val level: String,
        val vocabularies: List<VocabularySeed>
    )

    fun callback(context: Context): RoomDatabase.Callback {
        return object : RoomDatabase.Callback() {
            override fun onCreate(db: SupportSQLiteDatabase) {
                super.onCreate(db)
                CoroutineScope(Dispatchers.IO).launch {
                    seedDatabase(DatabaseProvider.getDatabase(context.applicationContext))
                }
            }

            override fun onOpen(db: SupportSQLiteDatabase) {
                super.onOpen(db)
                CoroutineScope(Dispatchers.IO).launch {
                    seedDatabase(DatabaseProvider.getDatabase(context.applicationContext))
                }
            }
        }
    }

    private suspend fun seedDatabase(database: AppDatabase) {
        val existingA0Count = database.vocabularyDao().getVocabCountByDifficultySync("A0")
        if (existingA0Count == 0) {
            val a0TopicId = database.topicDao().insertTopic(
                TopicEntity(
                    name = "Từ Vựng Mất Gốc",
                    description = "Vocabulary for absolute beginners - the most basic words",
                    iconUrl = "🔤",
                    level = "A0",
                    createdAt = System.currentTimeMillis()
                )
            ).toInt()

            database.vocabularyDao().insertVocabularies(
                listOf(
                VocabularyEntity(
                    topicId = a0TopicId,
                    word = "hello",
                    meaning = "xin chào",
                    pronunciation = "/həˈloʊ/",
                    exampleSentence = "Hello! How are you?",
                    audioUrl = null,
                    difficulty = "A0",
                    createdAt = System.currentTimeMillis()
                ),
                VocabularyEntity(
                    topicId = a0TopicId,
                    word = "goodbye",
                    meaning = "tạm biệt",
                    pronunciation = "/ɡʊdˈbaɪ/",
                    exampleSentence = "Goodbye! See you tomorrow.",
                    audioUrl = null,
                    difficulty = "A0",
                    createdAt = System.currentTimeMillis()
                ),
                VocabularyEntity(
                    topicId = a0TopicId,
                    word = "yes",
                    meaning = "có / vâng",
                    pronunciation = "/jɛs/",
                    exampleSentence = "Yes, I understand.",
                    audioUrl = null,
                    difficulty = "A0",
                    createdAt = System.currentTimeMillis()
                ),
                VocabularyEntity(
                    topicId = a0TopicId,
                    word = "no",
                    meaning = "không",
                    pronunciation = "/noʊ/",
                    exampleSentence = "No, that is not right.",
                    audioUrl = null,
                    difficulty = "A0",
                    createdAt = System.currentTimeMillis()
                ),
                VocabularyEntity(
                    topicId = a0TopicId,
                    word = "please",
                    meaning = "làm ơn",
                    pronunciation = "/pliːz/",
                    exampleSentence = "Please help me.",
                    audioUrl = null,
                    difficulty = "A0",
                    createdAt = System.currentTimeMillis()
                ),
                VocabularyEntity(
                    topicId = a0TopicId,
                    word = "thank you",
                    meaning = "cảm ơn",
                    pronunciation = "/θæŋk juː/",
                    exampleSentence = "Thank you very much!",
                    audioUrl = null,
                    difficulty = "A0",
                    createdAt = System.currentTimeMillis()
                ),
                VocabularyEntity(
                    topicId = a0TopicId,
                    word = "sorry",
                    meaning = "xin lỗi",
                    pronunciation = "/ˈsɒri/",
                    exampleSentence = "I am sorry for being late.",
                    audioUrl = null,
                    difficulty = "A0",
                    createdAt = System.currentTimeMillis()
                ),
                VocabularyEntity(
                    topicId = a0TopicId,
                    word = "name",
                    meaning = "tên",
                    pronunciation = "/neɪm/",
                    exampleSentence = "My name is Anna.",
                    audioUrl = null,
                    difficulty = "A0",
                    createdAt = System.currentTimeMillis()
                ),
                VocabularyEntity(
                    topicId = a0TopicId,
                    word = "I",
                    meaning = "tôi",
                    pronunciation = "/aɪ/",
                    exampleSentence = "I am a student.",
                    audioUrl = null,
                    difficulty = "A0",
                    createdAt = System.currentTimeMillis()
                ),
                VocabularyEntity(
                    topicId = a0TopicId,
                    word = "you",
                    meaning = "bạn / anh / chị",
                    pronunciation = "/juː/",
                    exampleSentence = "Are you a teacher?",
                    audioUrl = null,
                    difficulty = "A0",
                    createdAt = System.currentTimeMillis()
                ),
                VocabularyEntity(
                    topicId = a0TopicId,
                    word = "he",
                    meaning = "anh ấy",
                    pronunciation = "/hiː/",
                    exampleSentence = "He is my friend.",
                    audioUrl = null,
                    difficulty = "A0",
                    createdAt = System.currentTimeMillis()
                ),
                VocabularyEntity(
                    topicId = a0TopicId,
                    word = "she",
                    meaning = "cô ấy",
                    pronunciation = "/ʃiː/",
                    exampleSentence = "She is very kind.",
                    audioUrl = null,
                    difficulty = "A0",
                    createdAt = System.currentTimeMillis()
                ),
                VocabularyEntity(
                    topicId = a0TopicId,
                    word = "this",
                    meaning = "cái này",
                    pronunciation = "/ðɪs/",
                    exampleSentence = "This is a book.",
                    audioUrl = null,
                    difficulty = "A0",
                    createdAt = System.currentTimeMillis()
                ),
                VocabularyEntity(
                    topicId = a0TopicId,
                    word = "that",
                    meaning = "cái đó / kia",
                    pronunciation = "/ðæt/",
                    exampleSentence = "What is that?",
                    audioUrl = null,
                    difficulty = "A0",
                    createdAt = System.currentTimeMillis()
                ),
                VocabularyEntity(
                    topicId = a0TopicId,
                    word = "good",
                    meaning = "tốt / giỏi",
                    pronunciation = "/ɡʊd/",
                    exampleSentence = "You did a good job!",
                    audioUrl = null,
                    difficulty = "A0",
                    createdAt = System.currentTimeMillis()
                )
                )
            )
        }

        topicSeeds().forEach { topicSeed ->
            val existingCount = database.vocabularyDao().getVocabCountByDifficultySync(topicSeed.level)
            val existingTopicCount = database.topicDao().getTopicCountByNameAndLevelSync(topicSeed.name, topicSeed.level)
            if (existingCount == 0 || existingTopicCount == 0) {
                val topicId = database.topicDao().insertTopic(
                    TopicEntity(
                        name = topicSeed.name,
                        description = topicSeed.description,
                        iconUrl = topicSeed.iconUrl,
                        level = topicSeed.level,
                        createdAt = System.currentTimeMillis()
                    )
                ).toInt()

                val vocabularies = topicSeed.vocabularies.map { seed ->
                    VocabularyEntity(
                        topicId = topicId,
                        word = seed.word,
                        meaning = seed.meaning,
                        pronunciation = seed.pronunciation,
                        exampleSentence = seed.exampleSentence,
                        difficulty = topicSeed.level,
                        createdAt = System.currentTimeMillis()
                    )
                }

                database.vocabularyDao().insertVocabularies(vocabularies)
            }
        }
    }

    private fun topicSeeds(): List<TopicSeed> {
        return listOf(
            TopicSeed(
                name = "🏠 Daily Life",
                description = "Basic words for home and daily routines",
                iconUrl = "#4F46E5",
                level = "A1",
                vocabularies = listOf(
                    VocabularySeed("house", "ngôi nhà", "/haʊs/", "My house is near the school."),
                    VocabularySeed("family", "gia đình", "/ˈfæm.ə.li/", "I love my family very much."),
                    VocabularySeed("room", "phòng", "/ruːm/", "This room is clean."),
                    VocabularySeed("door", "cửa ra vào", "/dɔːr/", "Please close the door."),
                    VocabularySeed("window", "cửa sổ", "/ˈwɪn.doʊ/", "Open the window, please."),
                    VocabularySeed("bed", "giường", "/bed/", "The bed is soft."),
                    VocabularySeed("kitchen", "nhà bếp", "/ˈkɪtʃ.ən/", "She is in the kitchen."),
                    VocabularySeed("bathroom", "phòng tắm", "/ˈbæθ.ruːm/", "The bathroom is small."),
                    VocabularySeed("clean", "dọn dẹp", "/kliːn/", "I clean my room every day."),
                    VocabularySeed("cook", "nấu ăn", "/kʊk/", "My mother can cook well."),
                    VocabularySeed("wash", "rửa", "/wɑːʃ/", "I wash my hands before lunch."),
                    VocabularySeed("wake up", "thức dậy", "/weɪk ʌp/", "I wake up at six o'clock."),
                    VocabularySeed("sleep", "ngủ", "/sliːp/", "I sleep early at night."),
                    VocabularySeed("morning", "buổi sáng", "/ˈmɔːr.nɪŋ/", "I drink tea in the morning."),
                    VocabularySeed("evening", "buổi tối", "/ˈiːv.nɪŋ/", "We walk together in the evening.")
                )
            ),
            TopicSeed(
                name = "🍎 Food & Drink",
                description = "Common food and drink vocabulary",
                iconUrl = "#F59E0B",
                level = "A1",
                vocabularies = listOf(
                    VocabularySeed("apple", "táo", "/ˈæp.əl/", "I eat an apple every day."),
                    VocabularySeed("bread", "bánh mì", "/bred/", "This bread is fresh."),
                    VocabularySeed("rice", "cơm", "/raɪs/", "We eat rice for dinner."),
                    VocabularySeed("water", "nước", "/ˈwɔː.t̬ɚ/", "Please drink more water."),
                    VocabularySeed("milk", "sữa", "/mɪlk/", "The child drinks milk in the morning."),
                    VocabularySeed("coffee", "cà phê", "/ˈkɑː.fi/", "He likes hot coffee."),
                    VocabularySeed("tea", "trà", "/tiː/", "My grandmother drinks tea."),
                    VocabularySeed("breakfast", "bữa sáng", "/ˈbrek.fəst/", "Breakfast is ready."),
                    VocabularySeed("lunch", "bữa trưa", "/lʌntʃ/", "We have lunch at noon."),
                    VocabularySeed("dinner", "bữa tối", "/ˈdɪn.ɚ/", "Dinner starts at seven."),
                    VocabularySeed("hungry", "đói", "/ˈhʌŋ.ɡri/", "I am hungry after class."),
                    VocabularySeed("thirsty", "khát", "/ˈθɝː.sti/", "She is thirsty after running."),
                    VocabularySeed("sweet", "ngọt", "/swiːt/", "This cake is very sweet."),
                    VocabularySeed("salty", "mặn", "/ˈsɑːl.ti/", "The soup is too salty."),
                    VocabularySeed("delicious", "ngon", "/dɪˈlɪʃ.əs/", "Your food is delicious.")
                )
            ),
            TopicSeed(
                name = "🏥 Health & Body",
                description = "Words for health, body parts, and medical care",
                iconUrl = "#EF4444",
                level = "A2",
                vocabularies = listOf(
                    VocabularySeed("head", "đầu", "/hed/", "My head hurts today."),
                    VocabularySeed("stomach", "dạ dày", "/ˈstʌm.ək/", "His stomach feels bad."),
                    VocabularySeed("fever", "sốt", "/ˈfiː.vɚ/", "She has a high fever."),
                    VocabularySeed("cough", "ho", "/kɔːf/", "I have a dry cough."),
                    VocabularySeed("medicine", "thuốc", "/ˈmed.ə.sɪn/", "Take your medicine after meals."),
                    VocabularySeed("doctor", "bác sĩ", "/ˈdɑːk.tɚ/", "The doctor is very kind."),
                    VocabularySeed("nurse", "y tá", "/nɝːs/", "The nurse checks my temperature."),
                    VocabularySeed("hospital", "bệnh viện", "/ˈhɑː.spɪ.t̬əl/", "He works at a hospital."),
                    VocabularySeed("exercise", "tập thể dục", "/ˈek.sɚ.saɪz/", "I exercise every morning."),
                    VocabularySeed("healthy", "khỏe mạnh", "/ˈhel.θi/", "Vegetables keep us healthy."),
                    VocabularySeed("tired", "mệt", "/taɪrd/", "I feel tired after work."),
                    VocabularySeed("pain", "cơn đau", "/peɪn/", "She has pain in her leg."),
                    VocabularySeed("toothache", "đau răng", "/ˈtuːθ.eɪk/", "I cannot eat because of toothache."),
                    VocabularySeed("headache", "đau đầu", "/ˈhed.eɪk/", "This noise gives me a headache."),
                    VocabularySeed("appointment", "lịch hẹn", "/əˈpɔɪnt.mənt/", "I have a doctor appointment tomorrow.")
                )
            ),
            TopicSeed(
                name = "💼 Work & Career",
                description = "Vocabulary for jobs and workplace communication",
                iconUrl = "#10B981",
                level = "B1",
                vocabularies = listOf(
                    VocabularySeed("office", "văn phòng", "/ˈɔː.fɪs/", "Our office is on the fifth floor."),
                    VocabularySeed("colleague", "đồng nghiệp", "/ˈkɑː.liːɡ/", "My colleague helped me today."),
                    VocabularySeed("meeting", "cuộc họp", "/ˈmiː.tɪŋ/", "We have a meeting at ten."),
                    VocabularySeed("project", "dự án", "/ˈprɑː.dʒekt/", "This project is very important."),
                    VocabularySeed("deadline", "hạn chót", "/ˈded.laɪn/", "The deadline is next Monday."),
                    VocabularySeed("salary", "lương", "/ˈsæl.ɚ.i/", "Her salary increased this year."),
                    VocabularySeed("manager", "quản lý", "/ˈmæn.ɪ.dʒɚ/", "The manager approved my plan."),
                    VocabularySeed("interview", "phỏng vấn", "/ˈɪn.t̬ɚ.vjuː/", "I have a job interview tomorrow."),
                    VocabularySeed("resume", "hồ sơ xin việc", "/ˈrez.ə.meɪ/", "Please send your resume by email."),
                    VocabularySeed("promotion", "thăng chức", "/prəˈmoʊ.ʃən/", "He got a promotion last month."),
                    VocabularySeed("responsibility", "trách nhiệm", "/rɪˌspɑːn.səˈbɪl.ə.t̬i/", "This task is my responsibility."),
                    VocabularySeed("schedule", "lịch trình", "/ˈskedʒ.uːl/", "My schedule is full today."),
                    VocabularySeed("customer", "khách hàng", "/ˈkʌs.tə.mɚ/", "The customer asked a question."),
                    VocabularySeed("team", "đội nhóm", "/tiːm/", "Our team works very well together."),
                    VocabularySeed("commute", "đi lại đi làm", "/kəˈmjuːt/", "My commute takes one hour.")
                )
            ),
            TopicSeed(
                name = "🌍 Travel & Places",
                description = "Useful travel words and place names",
                iconUrl = "#0EA5E9",
                level = "A2",
                vocabularies = listOf(
                    VocabularySeed("airport", "sân bay", "/ˈer.pɔːrt/", "We arrived at the airport early."),
                    VocabularySeed("ticket", "vé", "/ˈtɪk.ɪt/", "I bought a train ticket."),
                    VocabularySeed("passport", "hộ chiếu", "/ˈpæs.pɔːrt/", "Do not forget your passport."),
                    VocabularySeed("hotel", "khách sạn", "/hoʊˈtel/", "Our hotel is near the beach."),
                    VocabularySeed("map", "bản đồ", "/mæp/", "This map shows the city center."),
                    VocabularySeed("station", "nhà ga", "/ˈsteɪ.ʃən/", "Meet me at the station."),
                    VocabularySeed("luggage", "hành lý", "/ˈlʌɡ.ɪdʒ/", "Her luggage is very heavy."),
                    VocabularySeed("journey", "hành trình", "/ˈdʒɝː.ni/", "The journey was long but fun."),
                    VocabularySeed("direction", "hướng đi", "/dəˈrek.ʃən/", "Can you give me directions?"),
                    VocabularySeed("temple", "đền chùa", "/ˈtem.pəl/", "We visited an old temple."),
                    VocabularySeed("beach", "bãi biển", "/biːtʃ/", "The beach is very beautiful."),
                    VocabularySeed("mountain", "ngọn núi", "/ˈmaʊn.tən/", "They climbed the mountain."),
                    VocabularySeed("bridge", "cầu", "/brɪdʒ/", "The bridge crosses the river."),
                    VocabularySeed("museum", "bảo tàng", "/mjuːˈziː.əm/", "The museum opens at nine."),
                    VocabularySeed("souvenir", "quà lưu niệm", "/ˌsuː.vəˈnɪr/", "I bought a souvenir for my friend.")
                )
            ),
            TopicSeed(
                name = "📱 Technology",
                description = "Everyday technology and digital communication",
                iconUrl = "#8B5CF6",
                level = "B1",
                vocabularies = listOf(
                    VocabularySeed("computer", "máy tính", "/kəmˈpjuː.t̬ɚ/", "My computer is very fast."),
                    VocabularySeed("keyboard", "bàn phím", "/ˈkiː.bɔːrd/", "This keyboard is comfortable."),
                    VocabularySeed("screen", "màn hình", "/skriːn/", "The screen is too bright."),
                    VocabularySeed("internet", "internet", "/ˈɪn.t̬ɚ.net/", "The internet is slow today."),
                    VocabularySeed("website", "trang web", "/ˈweb.saɪt/", "I found it on a website."),
                    VocabularySeed("password", "mật khẩu", "/ˈpæs.wɝːd/", "Change your password often."),
                    VocabularySeed("download", "tải xuống", "/ˈdaʊn.loʊd/", "Please download this file."),
                    VocabularySeed("upload", "tải lên", "/ʌpˈloʊd/", "I will upload the photo later."),
                    VocabularySeed("app", "ứng dụng", "/æp/", "This app helps me study words."),
                    VocabularySeed("device", "thiết bị", "/dɪˈvaɪs/", "The device is easy to use."),
                    VocabularySeed("battery", "pin", "/ˈbæt̬.ɚ.i/", "My phone battery is low."),
                    VocabularySeed("update", "cập nhật", "/ʌpˈdeɪt/", "You should update the app."),
                    VocabularySeed("message", "tin nhắn", "/ˈmes.ɪdʒ/", "I sent you a message."),
                    VocabularySeed("camera", "máy ảnh", "/ˈkæm.rə/", "The camera takes clear pictures."),
                    VocabularySeed("software", "phần mềm", "/ˈsɔːft.wer/", "This software is very useful.")
                )
            ),
            TopicSeed(
                name = "🎭 Arts & Culture",
                description = "Vocabulary for art, culture, and creative expression",
                iconUrl = "#F43F5E",
                level = "B2",
                vocabularies = listOf(
                    VocabularySeed("painting", "hội họa", "/ˈpeɪn.t̬ɪŋ/", "She loves painting landscapes."),
                    VocabularySeed("sculpture", "điêu khắc", "/ˈskʌlp.tʃɚ/", "The sculpture is made of stone."),
                    VocabularySeed("literature", "văn học", "/ˈlɪt̬.ɚ.ə.tʃɚ/", "I study world literature at school."),
                    VocabularySeed("theater", "nhà hát", "/ˈθiː.ə.t̬ɚ/", "We watched a play at the theater."),
                    VocabularySeed("audience", "khán giả", "/ˈɑː.di.əns/", "The audience clapped loudly."),
                    VocabularySeed("melody", "giai điệu", "/ˈmel.ə.di/", "This melody sounds peaceful."),
                    VocabularySeed("rhythm", "nhịp điệu", "/ˈrɪð.əm/", "The song has a strong rhythm."),
                    VocabularySeed("exhibition", "triển lãm", "/ˌek.səˈbɪʃ.ən/", "The exhibition opens this weekend."),
                    VocabularySeed("heritage", "di sản", "/ˈher.ɪ.t̬ɪdʒ/", "This town has rich cultural heritage."),
                    VocabularySeed("tradition", "truyền thống", "/trəˈdɪʃ.ən/", "Tet is an important tradition."),
                    VocabularySeed("festival", "lễ hội", "/ˈfes.t̬ə.vəl/", "The festival attracts many visitors."),
                    VocabularySeed("masterpiece", "tác phẩm xuất sắc", "/ˈmæs.tɚ.piːs/", "Many people call it a masterpiece."),
                    VocabularySeed("creative", "sáng tạo", "/kriˈeɪ.tɪv/", "She has a very creative mind."),
                    VocabularySeed("performance", "buổi biểu diễn", "/pɚˈfɔːr.məns/", "Their performance was excellent."),
                    VocabularySeed("portrait", "chân dung", "/ˈpɔːr.trət/", "The portrait hangs on the wall.")
                )
            ),
            TopicSeed(
                name = "🌿 Nature & Environment",
                description = "Words about nature, climate, and sustainability",
                iconUrl = "#22C55E",
                level = "B1",
                vocabularies = listOf(
                    VocabularySeed("forest", "rừng", "/ˈfɔːr.ɪst/", "The forest is full of birds."),
                    VocabularySeed("river", "sông", "/ˈrɪv.ɚ/", "This river is very long."),
                    VocabularySeed("ocean", "đại dương", "/ˈoʊ.ʃən/", "The ocean looks calm today."),
                    VocabularySeed("climate", "khí hậu", "/ˈklaɪ.mət/", "Climate change affects everyone."),
                    VocabularySeed("pollution", "ô nhiễm", "/pəˈluː.ʃən/", "Air pollution is a big problem."),
                    VocabularySeed("recycle", "tái chế", "/riːˈsaɪ.kəl/", "We recycle plastic bottles."),
                    VocabularySeed("wildlife", "động vật hoang dã", "/ˈwaɪld.laɪf/", "The park protects local wildlife."),
                    VocabularySeed("energy", "năng lượng", "/ˈen.ɚ.dʒi/", "We should save energy at home."),
                    VocabularySeed("solar", "thuộc năng lượng mặt trời", "/ˈsoʊ.lɚ/", "Solar power is becoming popular."),
                    VocabularySeed("wind", "gió", "/wɪnd/", "Strong wind moved the trees."),
                    VocabularySeed("drought", "hạn hán", "/draʊt/", "The farmers suffered from drought."),
                    VocabularySeed("flood", "lũ lụt", "/flʌd/", "The flood damaged many houses."),
                    VocabularySeed("protect", "bảo vệ", "/prəˈtekt/", "We must protect the environment."),
                    VocabularySeed("organic", "hữu cơ", "/ɔːrˈɡæn.ɪk/", "They buy organic vegetables."),
                    VocabularySeed("ecosystem", "hệ sinh thái", "/ˈiː.koʊˌsɪs.təm/", "A healthy ecosystem supports life.")
                )
            )
        )
    }
}