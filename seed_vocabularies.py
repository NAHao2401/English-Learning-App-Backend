from app.db.session import SessionLocal
from app.models.lesson import Topic
from app.models.vocabulary import Vocabulary

db = SessionLocal()

try:
    if db.query(Vocabulary).count() > 0:
        print("Vocabulary data already exists")
        raise SystemExit

    # A0 Level - Absolute Beginners
    topic_a0 = Topic(
        name="Từ Vựng Mất Gốc",
        description="Vocabulary for absolute beginners - the most basic words",
        icon_url="🔤",
        level="A0",
    )
    db.add(topic_a0)
    db.commit()
    db.refresh(topic_a0)

    vocab_a0 = [
        Vocabulary(topic_id=topic_a0.id, word="hello", meaning="xin chào", pronunciation="/həˈloʊ/", example_sentence="Hello! How are you?", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="goodbye", meaning="tạm biệt", pronunciation="/ɡʊdˈbaɪ/", example_sentence="Goodbye! See you tomorrow.", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="yes", meaning="có / vâng", pronunciation="/jɛs/", example_sentence="Yes, I understand.", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="no", meaning="không", pronunciation="/noʊ/", example_sentence="No, that is not right.", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="please", meaning="làm ơn", pronunciation="/pliːz/", example_sentence="Please help me.", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="thank you", meaning="cảm ơn", pronunciation="/θæŋk juː/", example_sentence="Thank you very much!", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="sorry", meaning="xin lỗi", pronunciation="/ˈsɒri/", example_sentence="I am sorry for being late.", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="name", meaning="tên", pronunciation="/neɪm/", example_sentence="My name is Anna.", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="I", meaning="tôi", pronunciation="/aɪ/", example_sentence="I am a student.", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="you", meaning="bạn / anh / chị", pronunciation="/juː/", example_sentence="Are you a teacher?", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="he", meaning="anh ấy", pronunciation="/hiː/", example_sentence="He is my friend.", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="she", meaning="cô ấy", pronunciation="/ʃiː/", example_sentence="She is very kind.", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="this", meaning="cái này", pronunciation="/ðɪs/", example_sentence="This is a book.", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="that", meaning="cái đó / kia", pronunciation="/ðæt/", example_sentence="What is that?", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="good", meaning="tốt / giỏi", pronunciation="/ɡʊd/", example_sentence="You did a good job!", difficulty="A0"),
    ]
    db.add_all(vocab_a0)
    db.commit()

    # A1 Level - Daily Life
    topic_a1_daily = Topic(
        name="🏠 Daily Life",
        description="Basic words for home and daily routines",
        icon_url="#4F46E5",
        level="A1",
    )
    db.add(topic_a1_daily)
    db.commit()
    db.refresh(topic_a1_daily)

    vocab_a1_daily = [
        Vocabulary(topic_id=topic_a1_daily.id, word="house", meaning="ngôi nhà", pronunciation="/haʊs/", example_sentence="My house is near the school.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="family", meaning="gia đình", pronunciation="/ˈfæm.ə.li/", example_sentence="I love my family very much.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="room", meaning="phòng", pronunciation="/ruːm/", example_sentence="This room is clean.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="door", meaning="cửa ra vào", pronunciation="/dɔːr/", example_sentence="Please close the door.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="window", meaning="cửa sổ", pronunciation="/ˈwɪn.doʊ/", example_sentence="Open the window, please.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="bed", meaning="giường", pronunciation="/bed/", example_sentence="The bed is soft.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="kitchen", meaning="nhà bếp", pronunciation="/ˈkɪtʃ.ən/", example_sentence="She is in the kitchen.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="bathroom", meaning="phòng tắm", pronunciation="/ˈbæθ.ruːm/", example_sentence="The bathroom is small.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="clean", meaning="dọn dẹp", pronunciation="/kliːn/", example_sentence="I clean my room every day.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="cook", meaning="nấu ăn", pronunciation="/kʊk/", example_sentence="My mother can cook well.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="wash", meaning="rửa", pronunciation="/wɑːʃ/", example_sentence="I wash my hands before lunch.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="wake up", meaning="thức dậy", pronunciation="/weɪk ʌp/", example_sentence="I wake up at six o'clock.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="sleep", meaning="ngủ", pronunciation="/sliːp/", example_sentence="I sleep early at night.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="morning", meaning="buổi sáng", pronunciation="/ˈmɔːr.nɪŋ/", example_sentence="I drink tea in the morning.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="evening", meaning="buổi tối", pronunciation="/ˈiːv.nɪŋ/", example_sentence="We walk together in the evening.", difficulty="A1"),
    ]
    db.add_all(vocab_a1_daily)
    db.commit()

    # A1 Level - Food & Drink
    topic_a1_food = Topic(
        name="🍎 Food & Drink",
        description="Common food and drink vocabulary",
        icon_url="#F59E0B",
        level="A1",
    )
    db.add(topic_a1_food)
    db.commit()
    db.refresh(topic_a1_food)

    vocab_a1_food = [
        Vocabulary(topic_id=topic_a1_food.id, word="apple", meaning="táo", pronunciation="/ˈæp.əl/", example_sentence="I eat an apple every day.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="bread", meaning="bánh mì", pronunciation="/bred/", example_sentence="This bread is fresh.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="rice", meaning="cơm", pronunciation="/raɪs/", example_sentence="We eat rice for dinner.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="water", meaning="nước", pronunciation="/ˈwɔː.t̬ɚ/", example_sentence="Please drink more water.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="milk", meaning="sữa", pronunciation="/mɪlk/", example_sentence="The child drinks milk in the morning.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="coffee", meaning="cà phê", pronunciation="/ˈkɑː.fi/", example_sentence="He likes hot coffee.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="tea", meaning="trà", pronunciation="/tiː/", example_sentence="My grandmother drinks tea.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="breakfast", meaning="bữa sáng", pronunciation="/ˈbrek.fəst/", example_sentence="Breakfast is ready.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="lunch", meaning="bữa trưa", pronunciation="/lʌntʃ/", example_sentence="We have lunch at noon.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="dinner", meaning="bữa tối", pronunciation="/ˈdɪn.ɚ/", example_sentence="Dinner starts at seven.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="hungry", meaning="đói", pronunciation="/ˈhʌŋ.ɡri/", example_sentence="I am hungry after class.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="thirsty", meaning="khát", pronunciation="/ˈθɝː.sti/", example_sentence="She is thirsty after running.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="sweet", meaning="ngọt", pronunciation="/swiːt/", example_sentence="This cake is very sweet.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="salty", meaning="mặn", pronunciation="/ˈsɑːl.ti/", example_sentence="The soup is too salty.", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="delicious", meaning="ngon", pronunciation="/dɪˈlɪʃ.əs/", example_sentence="Your food is delicious.", difficulty="A1"),
    ]
    db.add_all(vocab_a1_food)
    db.commit()

    # A2 Level - Health & Body
    topic_a2_health = Topic(
        name="🏥 Health & Body",
        description="Words for health, body parts, and medical care",
        icon_url="#EF4444",
        level="A2",
    )
    db.add(topic_a2_health)
    db.commit()
    db.refresh(topic_a2_health)

    vocab_a2_health = [
        Vocabulary(topic_id=topic_a2_health.id, word="head", meaning="đầu", pronunciation="/hed/", example_sentence="My head hurts today.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="stomach", meaning="dạ dày", pronunciation="/ˈstʌm.ək/", example_sentence="His stomach feels bad.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="fever", meaning="sốt", pronunciation="/ˈfiː.vɚ/", example_sentence="She has a high fever.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="cough", meaning="ho", pronunciation="/kɔːf/", example_sentence="I have a dry cough.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="medicine", meaning="thuốc", pronunciation="/ˈmed.ə.sɪn/", example_sentence="Take your medicine after meals.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="doctor", meaning="bác sĩ", pronunciation="/ˈdɑːk.tɚ/", example_sentence="The doctor is very kind.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="nurse", meaning="y tá", pronunciation="/nɝːs/", example_sentence="The nurse checks my temperature.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="hospital", meaning="bệnh viện", pronunciation="/ˈhɑː.spɪ.t̬əl/", example_sentence="He works at a hospital.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="exercise", meaning="tập thể dục", pronunciation="/ˈek.sɚ.saɪz/", example_sentence="I exercise every morning.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="healthy", meaning="khỏe mạnh", pronunciation="/ˈhel.θi/", example_sentence="Vegetables keep us healthy.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="tired", meaning="mệt", pronunciation="/taɪrd/", example_sentence="I feel tired after work.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="pain", meaning="cơn đau", pronunciation="/peɪn/", example_sentence="She has pain in her leg.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="toothache", meaning="đau răng", pronunciation="/ˈtuːθ.eɪk/", example_sentence="I cannot eat because of toothache.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="headache", meaning="đau đầu", pronunciation="/ˈhed.eɪk/", example_sentence="This noise gives me a headache.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="appointment", meaning="lịch hẹn", pronunciation="/əˈpɔɪnt.mənt/", example_sentence="I have a doctor appointment tomorrow.", difficulty="A2"),
    ]
    db.add_all(vocab_a2_health)
    db.commit()

    # A2 Level - Travel & Places
    topic_a2_travel = Topic(
        name="🌍 Travel & Places",
        description="Useful travel words and place names",
        icon_url="#0EA5E9",
        level="A2",
    )
    db.add(topic_a2_travel)
    db.commit()
    db.refresh(topic_a2_travel)

    vocab_a2_travel = [
        Vocabulary(topic_id=topic_a2_travel.id, word="airport", meaning="sân bay", pronunciation="/ˈer.pɔːrt/", example_sentence="We arrived at the airport early.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="ticket", meaning="vé", pronunciation="/ˈtɪk.ɪt/", example_sentence="I bought a train ticket.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="passport", meaning="hộ chiếu", pronunciation="/ˈpæs.pɔːrt/", example_sentence="Do not forget your passport.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="hotel", meaning="khách sạn", pronunciation="/hoʊˈtel/", example_sentence="Our hotel is near the beach.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="map", meaning="bản đồ", pronunciation="/mæp/", example_sentence="This map shows the city center.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="station", meaning="nhà ga", pronunciation="/ˈsteɪ.ʃən/", example_sentence="Meet me at the station.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="luggage", meaning="hành lý", pronunciation="/ˈlʌɡ.ɪdʒ/", example_sentence="Her luggage is very heavy.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="journey", meaning="hành trình", pronunciation="/ˈdʒɝː.ni/", example_sentence="The journey was long but fun.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="direction", meaning="hướng đi", pronunciation="/dəˈrek.ʃən/", example_sentence="Can you give me directions?", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="temple", meaning="đền chùa", pronunciation="/ˈtem.pəl/", example_sentence="We visited an old temple.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="beach", meaning="bãi biển", pronunciation="/biːtʃ/", example_sentence="The beach is very beautiful.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="mountain", meaning="ngọn núi", pronunciation="/ˈmaʊn.tən/", example_sentence="They climbed the mountain.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="bridge", meaning="cầu", pronunciation="/brɪdʒ/", example_sentence="The bridge crosses the river.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="museum", meaning="bảo tàng", pronunciation="/mjuːˈziː.əm/", example_sentence="The museum opens at nine.", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="souvenir", meaning="quà lưu niệm", pronunciation="/ˌsuː.vəˈnɪr/", example_sentence="I bought a souvenir for my friend.", difficulty="A2"),
    ]
    db.add_all(vocab_a2_travel)
    db.commit()

    # B1 Level - Work & Career
    topic_b1_work = Topic(
        name="💼 Work & Career",
        description="Vocabulary for jobs and workplace communication",
        icon_url="#10B981",
        level="B1",
    )
    db.add(topic_b1_work)
    db.commit()
    db.refresh(topic_b1_work)

    vocab_b1_work = [
        Vocabulary(topic_id=topic_b1_work.id, word="office", meaning="văn phòng", pronunciation="/ˈɔː.fɪs/", example_sentence="Our office is on the fifth floor.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="colleague", meaning="đồng nghiệp", pronunciation="/ˈkɑː.liːɡ/", example_sentence="My colleague helped me today.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="meeting", meaning="cuộc họp", pronunciation="/ˈmiː.tɪŋ/", example_sentence="We have a meeting at ten.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="project", meaning="dự án", pronunciation="/ˈprɑː.dʒekt/", example_sentence="This project is very important.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="deadline", meaning="hạn chót", pronunciation="/ˈded.laɪn/", example_sentence="The deadline is next Monday.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="salary", meaning="lương", pronunciation="/ˈsæl.ɚ.i/", example_sentence="Her salary increased this year.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="manager", meaning="quản lý", pronunciation="/ˈmæn.ɪ.dʒɚ/", example_sentence="The manager approved my plan.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="interview", meaning="phỏng vấn", pronunciation="/ˈɪn.t̬ɚ.vjuː/", example_sentence="I have a job interview tomorrow.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="resume", meaning="hồ sơ xin việc", pronunciation="/ˈrez.ə.meɪ/", example_sentence="Please send your resume by email.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="promotion", meaning="thăng chức", pronunciation="/prəˈmoʊ.ʃən/", example_sentence="He got a promotion last month.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="responsibility", meaning="trách nhiệm", pronunciation="/rɪˌspɑːn.səˈbɪl.ə.t̬i/", example_sentence="This task is my responsibility.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="schedule", meaning="lịch trình", pronunciation="/ˈskedʒ.uːl/", example_sentence="My schedule is full today.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="customer", meaning="khách hàng", pronunciation="/ˈkʌs.tə.mɚ/", example_sentence="The customer asked a question.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="team", meaning="đội nhóm", pronunciation="/tiːm/", example_sentence="Our team works very well together.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="commute", meaning="đi lại đi làm", pronunciation="/kəˈmjuːt/", example_sentence="My commute takes one hour.", difficulty="B1"),
    ]
    db.add_all(vocab_b1_work)
    db.commit()

    # B1 Level - Technology
    topic_b1_tech = Topic(
        name="📱 Technology",
        description="Everyday technology and digital communication",
        icon_url="#8B5CF6",
        level="B1",
    )
    db.add(topic_b1_tech)
    db.commit()
    db.refresh(topic_b1_tech)

    vocab_b1_tech = [
        Vocabulary(topic_id=topic_b1_tech.id, word="computer", meaning="máy tính", pronunciation="/kəmˈpjuː.t̬ɚ/", example_sentence="My computer is very fast.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="keyboard", meaning="bàn phím", pronunciation="/ˈkiː.bɔːrd/", example_sentence="This keyboard is comfortable.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="screen", meaning="màn hình", pronunciation="/skriːn/", example_sentence="The screen is too bright.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="internet", meaning="internet", pronunciation="/ˈɪn.t̬ɚ.net/", example_sentence="The internet is slow today.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="website", meaning="trang web", pronunciation="/ˈweb.saɪt/", example_sentence="I found it on a website.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="password", meaning="mật khẩu", pronunciation="/ˈpæs.wɝːd/", example_sentence="Change your password often.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="download", meaning="tải xuống", pronunciation="/ˈdaʊn.loʊd/", example_sentence="Please download this file.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="upload", meaning="tải lên", pronunciation="/ʌpˈloʊd/", example_sentence="I will upload the photo later.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="app", meaning="ứng dụng", pronunciation="/æp/", example_sentence="This app helps me study words.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="device", meaning="thiết bị", pronunciation="/dɪˈvaɪs/", example_sentence="The device is easy to use.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="battery", meaning="pin", pronunciation="/ˈbæt̬.ɚ.i/", example_sentence="My phone battery is low.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="update", meaning="cập nhật", pronunciation="/ʌpˈdeɪt/", example_sentence="You should update the app.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="message", meaning="tin nhắn", pronunciation="/ˈmes.ɪdʒ/", example_sentence="I sent you a message.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="camera", meaning="máy ảnh", pronunciation="/ˈkæm.rə/", example_sentence="The camera takes clear pictures.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="software", meaning="phần mềm", pronunciation="/ˈsɔːft.wer/", example_sentence="This software is very useful.", difficulty="B1"),
    ]
    db.add_all(vocab_b1_tech)
    db.commit()

    # B1 Level - Nature & Environment
    topic_b1_nature = Topic(
        name="🌿 Nature & Environment",
        description="Words about nature, climate, and sustainability",
        icon_url="#22C55E",
        level="B1",
    )
    db.add(topic_b1_nature)
    db.commit()
    db.refresh(topic_b1_nature)

    vocab_b1_nature = [
        Vocabulary(topic_id=topic_b1_nature.id, word="forest", meaning="rừng", pronunciation="/ˈfɔːr.ɪst/", example_sentence="The forest is full of birds.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="river", meaning="sông", pronunciation="/ˈrɪv.ɚ/", example_sentence="This river is very long.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="ocean", meaning="đại dương", pronunciation="/ˈoʊ.ʃən/", example_sentence="The ocean looks calm today.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="climate", meaning="khí hậu", pronunciation="/ˈklaɪ.mət/", example_sentence="Climate change affects everyone.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="pollution", meaning="ô nhiễm", pronunciation="/pəˈluː.ʃən/", example_sentence="Air pollution is a big problem.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="recycle", meaning="tái chế", pronunciation="/riːˈsaɪ.kəl/", example_sentence="We recycle plastic bottles.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="wildlife", meaning="động vật hoang dã", pronunciation="/ˈwaɪld.laɪf/", example_sentence="The park protects local wildlife.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="energy", meaning="năng lượng", pronunciation="/ˈen.ɚ.dʒi/", example_sentence="We should save energy at home.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="solar", meaning="thuộc năng lượng mặt trời", pronunciation="/ˈsoʊ.lɚ/", example_sentence="Solar power is becoming popular.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="wind", meaning="gió", pronunciation="/wɪnd/", example_sentence="Strong wind moved the trees.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="drought", meaning="hạn hán", pronunciation="/draʊt/", example_sentence="The farmers suffered from drought.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="flood", meaning="lũ lụt", pronunciation="/flʌd/", example_sentence="The flood damaged many houses.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="protect", meaning="bảo vệ", pronunciation="/prəˈtekt/", example_sentence="We must protect the environment.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="organic", meaning="hữu cơ", pronunciation="/ɔːrˈɡæn.ɪk/", example_sentence="They buy organic vegetables.", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="ecosystem", meaning="hệ sinh thái", pronunciation="/ˈiː.koʊˌsɪs.təm/", example_sentence="A healthy ecosystem supports life.", difficulty="B1"),
    ]
    db.add_all(vocab_b1_nature)
    db.commit()

    # B2 Level - Arts & Culture
    topic_b2_arts = Topic(
        name="🎭 Arts & Culture",
        description="Vocabulary for art, culture, and creative expression",
        icon_url="#F43F5E",
        level="B2",
    )
    db.add(topic_b2_arts)
    db.commit()
    db.refresh(topic_b2_arts)

    vocab_b2_arts = [
        Vocabulary(topic_id=topic_b2_arts.id, word="painting", meaning="hội họa", pronunciation="/ˈpeɪn.t̬ɪŋ/", example_sentence="She loves painting landscapes.", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="sculpture", meaning="điêu khắc", pronunciation="/ˈskʌlp.tʃɚ/", example_sentence="The sculpture is made of stone.", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="literature", meaning="văn học", pronunciation="/ˈlɪt̬.ɚ.ə.tʃɚ/", example_sentence="I study world literature at school.", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="theater", meaning="nhà hát", pronunciation="/ˈθiː.ə.t̬ɚ/", example_sentence="We watched a play at the theater.", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="audience", meaning="khán giả", pronunciation="/ˈɑː.di.əns/", example_sentence="The audience clapped loudly.", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="melody", meaning="giai điệu", pronunciation="/ˈmel.ə.di/", example_sentence="This melody sounds peaceful.", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="rhythm", meaning="nhịp điệu", pronunciation="/ˈrɪð.əm/", example_sentence="The song has a strong rhythm.", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="exhibition", meaning="triển lãm", pronunciation="/ˌek.səˈbɪʃ.ən/", example_sentence="The exhibition opens this weekend.", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="heritage", meaning="di sản", pronunciation="/ˈher.ɪ.t̬ɪdʒ/", example_sentence="This town has rich cultural heritage.", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="tradition", meaning="truyền thống", pronunciation="/trəˈdɪʃ.ən/", example_sentence="Tet is an important tradition.", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="festival", meaning="lễ hội", pronunciation="/ˈfes.t̬ə.vəl/", example_sentence="The festival attracts many visitors.", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="masterpiece", meaning="tác phẩm xuất sắc", pronunciation="/ˈmæs.tɚ.piːs/", example_sentence="Many people call it a masterpiece.", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="creative", meaning="sáng tạo", pronunciation="/kriˈeɪ.tɪv/", example_sentence="She has a very creative mind.", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="performance", meaning="buổi biểu diễn", pronunciation="/pɚˈfɔːr.məns/", example_sentence="Their performance was excellent.", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="portrait", meaning="chân dung", pronunciation="/ˈpɔːr.trət/", example_sentence="The portrait hangs on the wall.", difficulty="B2"),
    ]
    db.add_all(vocab_b2_arts)
    db.commit()

    print("✅ Vocabulary data seeded successfully!")
    print(f"   - Topics: {db.query(Topic).count()}")
    print(f"   - Vocabularies: {db.query(Vocabulary).count()}")

except Exception as e:
    print(f"❌ Error seeding data: {e}")
    db.rollback()

finally:
    db.close()
