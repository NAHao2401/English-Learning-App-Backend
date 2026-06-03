from app.db.session import SessionLocal
from app.models.lesson import Topic
from app.models.vocabulary import Vocabulary
from advanced_vocab_topics import ADVANCED_VOCAB_TOPICS, audio_slug

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
        Vocabulary(topic_id=topic_a0.id, word="hello", meaning="xin chào", pronunciation="/həˈloʊ/", example_sentence="Hello! How are you?", audio_url="static/audio/words/hello.mp3", example_audio_url="static/audio/examples/hello_example.mp3", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="goodbye", meaning="tạm biệt", pronunciation="/ɡʊdˈbaɪ/", example_sentence="Goodbye! See you tomorrow.", audio_url="static/audio/words/goodbye.mp3", example_audio_url="static/audio/examples/goodbye_example.mp3", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="yes", meaning="có / vâng", pronunciation="/jɛs/", example_sentence="Yes, I understand.", audio_url="static/audio/words/yes.mp3", example_audio_url="static/audio/examples/yes_example.mp3", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="no", meaning="không", pronunciation="/noʊ/", example_sentence="No, that is not right.", audio_url="static/audio/words/no.mp3", example_audio_url="static/audio/examples/no_example.mp3", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="please", meaning="làm ơn", pronunciation="/pliːz/", example_sentence="Please help me.", audio_url="static/audio/words/please.mp3", example_audio_url="static/audio/examples/please_example.mp3", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="thank you", meaning="cảm ơn", pronunciation="/θæŋk juː/", example_sentence="Thank you very much!", audio_url="static/audio/words/thank_you.mp3", example_audio_url="static/audio/examples/thank_you_example.mp3", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="sorry", meaning="xin lỗi", pronunciation="/ˈsɒri/", example_sentence="I am sorry for being late.", audio_url="static/audio/words/sorry.mp3", example_audio_url="static/audio/examples/sorry_example.mp3", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="name", meaning="tên", pronunciation="/neɪm/", example_sentence="My name is Anna.", audio_url="static/audio/words/name.mp3", example_audio_url="static/audio/examples/name_example.mp3", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="I", meaning="tôi", pronunciation="/aɪ/", example_sentence="I am a student.", audio_url="static/audio/words/I.mp3", example_audio_url="static/audio/examples/I_example.mp3", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="you", meaning="bạn / anh / chị", pronunciation="/juː/", example_sentence="Are you a teacher?", audio_url="static/audio/words/you.mp3", example_audio_url="static/audio/examples/you_example.mp3", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="he", meaning="anh ấy", pronunciation="/hiː/", example_sentence="He is my friend.", audio_url="static/audio/words/he.mp3", example_audio_url="static/audio/examples/he_example.mp3", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="she", meaning="cô ấy", pronunciation="/ʃiː/", example_sentence="She is very kind.", audio_url="static/audio/words/she.mp3", example_audio_url="static/audio/examples/she_example.mp3", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="this", meaning="cái này", pronunciation="/ðɪs/", example_sentence="This is a book.", audio_url="static/audio/words/this.mp3", example_audio_url="static/audio/examples/this_example.mp3", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="that", meaning="cái đó / kia", pronunciation="/ðæt/", example_sentence="What is that?", audio_url="static/audio/words/that.mp3", example_audio_url="static/audio/examples/that_example.mp3", difficulty="A0"),
        Vocabulary(topic_id=topic_a0.id, word="good", meaning="tốt / giỏi", pronunciation="/ɡʊd/", example_sentence="You did a good job!", audio_url="static/audio/words/good.mp3", example_audio_url="static/audio/examples/good_example.mp3", difficulty="A0"),
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
        Vocabulary(topic_id=topic_a1_daily.id, word="house", meaning="ngôi nhà", pronunciation="/haʊs/", example_sentence="My house is near the school.", audio_url="static/audio/words/house.mp3", example_audio_url="static/audio/examples/house_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="family", meaning="gia đình", pronunciation="/ˈfæm.ə.li/", example_sentence="I love my family very much.", audio_url="static/audio/words/family.mp3", example_audio_url="static/audio/examples/family_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="room", meaning="phòng", pronunciation="/ruːm/", example_sentence="This room is clean.", audio_url="static/audio/words/room.mp3", example_audio_url="static/audio/examples/room_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="door", meaning="cửa ra vào", pronunciation="/dɔːr/", example_sentence="Please close the door.", audio_url="static/audio/words/door.mp3", example_audio_url="static/audio/examples/door_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="window", meaning="cửa sổ", pronunciation="/ˈwɪn.doʊ/", example_sentence="Open the window, please.", audio_url="static/audio/words/window.mp3", example_audio_url="static/audio/examples/window_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="bed", meaning="giường", pronunciation="/bed/", example_sentence="The bed is soft.", audio_url="static/audio/words/bed.mp3", example_audio_url="static/audio/examples/bed_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="kitchen", meaning="nhà bếp", pronunciation="/ˈkɪtʃ.ən/", example_sentence="She is in the kitchen.", audio_url="static/audio/words/kitchen.mp3", example_audio_url="static/audio/examples/kitchen_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="bathroom", meaning="phòng tắm", pronunciation="/ˈbæθ.ruːm/", example_sentence="The bathroom is small.", audio_url="static/audio/words/bathroom.mp3", example_audio_url="static/audio/examples/bathroom_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="clean", meaning="dọn dẹp", pronunciation="/kliːn/", example_sentence="I clean my room every day.", audio_url="static/audio/words/clean.mp3", example_audio_url="static/audio/examples/clean_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="cook", meaning="nấu ăn", pronunciation="/kʊk/", example_sentence="My mother can cook well.", audio_url="static/audio/words/cook.mp3", example_audio_url="static/audio/examples/cook_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="wash", meaning="rửa", pronunciation="/wɑːʃ/", example_sentence="I wash my hands before lunch.", audio_url="static/audio/words/wash.mp3", example_audio_url="static/audio/examples/wash_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="wake up", meaning="thức dậy", pronunciation="/weɪk ʌp/", example_sentence="I wake up at six o'clock.", audio_url="static/audio/words/wake_up.mp3", example_audio_url="static/audio/examples/wake_up_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="sleep", meaning="ngủ", pronunciation="/sliːp/", example_sentence="I sleep early at night.", audio_url="static/audio/words/sleep.mp3", example_audio_url="static/audio/examples/sleep_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="morning", meaning="buổi sáng", pronunciation="/ˈmɔːr.nɪŋ/", example_sentence="I drink tea in the morning.", audio_url="static/audio/words/morning.mp3", example_audio_url="static/audio/examples/morning_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_daily.id, word="evening", meaning="buổi tối", pronunciation="/ˈiːv.nɪŋ/", example_sentence="We walk together in the evening.", audio_url="static/audio/words/evening.mp3", example_audio_url="static/audio/examples/evening_example.mp3", difficulty="A1"),
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
        Vocabulary(topic_id=topic_a1_food.id, word="apple", meaning="táo", pronunciation="/ˈæp.əl/", example_sentence="I eat an apple every day.", audio_url="static/audio/words/apple.mp3", example_audio_url="static/audio/examples/apple_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="bread", meaning="bánh mì", pronunciation="/bred/", example_sentence="This bread is fresh.", audio_url="static/audio/words/bread.mp3", example_audio_url="static/audio/examples/bread_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="rice", meaning="cơm", pronunciation="/raɪs/", example_sentence="We eat rice for dinner.", audio_url="static/audio/words/rice.mp3", example_audio_url="static/audio/examples/rice_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="water", meaning="nước", pronunciation="/ˈwɔː.t̬ɚ/", example_sentence="Please drink more water.", audio_url="static/audio/words/water.mp3", example_audio_url="static/audio/examples/water_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="milk", meaning="sữa", pronunciation="/mɪlk/", example_sentence="The child drinks milk in the morning.", audio_url="static/audio/words/milk.mp3", example_audio_url="static/audio/examples/milk_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="coffee", meaning="cà phê", pronunciation="/ˈkɑː.fi/", example_sentence="He likes hot coffee.", audio_url="static/audio/words/coffee.mp3", example_audio_url="static/audio/examples/coffee_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="tea", meaning="trà", pronunciation="/tiː/", example_sentence="My grandmother drinks tea.", audio_url="static/audio/words/tea.mp3", example_audio_url="static/audio/examples/tea_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="breakfast", meaning="bữa sáng", pronunciation="/ˈbrek.fəst/", example_sentence="Breakfast is ready.", audio_url="static/audio/words/breakfast.mp3", example_audio_url="static/audio/examples/breakfast_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="lunch", meaning="bữa trưa", pronunciation="/lʌntʃ/", example_sentence="We have lunch at noon.", audio_url="static/audio/words/lunch.mp3", example_audio_url="static/audio/examples/lunch_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="dinner", meaning="bữa tối", pronunciation="/ˈdɪn.ɚ/", example_sentence="Dinner starts at seven.", audio_url="static/audio/words/dinner.mp3", example_audio_url="static/audio/examples/dinner_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="hungry", meaning="đói", pronunciation="/ˈhʌŋ.ɡri/", example_sentence="I am hungry after class.", audio_url="static/audio/words/hungry.mp3", example_audio_url="static/audio/examples/hungry_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="thirsty", meaning="khát", pronunciation="/ˈθɝː.sti/", example_sentence="She is thirsty after running.", audio_url="static/audio/words/thirsty.mp3", example_audio_url="static/audio/examples/thirsty_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="sweet", meaning="ngọt", pronunciation="/swiːt/", example_sentence="This cake is very sweet.", audio_url="static/audio/words/sweet.mp3", example_audio_url="static/audio/examples/sweet_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="salty", meaning="mặn", pronunciation="/ˈsɑːl.ti/", example_sentence="The soup is too salty.", audio_url="static/audio/words/salty.mp3", example_audio_url="static/audio/examples/salty_example.mp3", difficulty="A1"),
        Vocabulary(topic_id=topic_a1_food.id, word="delicious", meaning="ngon", pronunciation="/dɪˈlɪʃ.əs/", example_sentence="Your food is delicious.", audio_url="static/audio/words/delicious.mp3", example_audio_url="static/audio/examples/delicious_example.mp3", difficulty="A1"),
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
        Vocabulary(topic_id=topic_a2_health.id, word="head", meaning="đầu", pronunciation="/hed/", example_sentence="My head hurts today.", audio_url="static/audio/words/head.mp3", example_audio_url="static/audio/examples/head_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="stomach", meaning="dạ dày", pronunciation="/ˈstʌm.ək/", example_sentence="His stomach feels bad.", audio_url="static/audio/words/stomach.mp3", example_audio_url="static/audio/examples/stomach_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="fever", meaning="sốt", pronunciation="/ˈfiː.vɚ/", example_sentence="She has a high fever.", audio_url="static/audio/words/fever.mp3", example_audio_url="static/audio/examples/fever_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="cough", meaning="ho", pronunciation="/kɔːf/", example_sentence="I have a dry cough.", audio_url="static/audio/words/cough.mp3", example_audio_url="static/audio/examples/cough_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="medicine", meaning="thuốc", pronunciation="/ˈmed.ə.sɪn/", example_sentence="Take your medicine after meals.", audio_url="static/audio/words/medicine.mp3", example_audio_url="static/audio/examples/medicine_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="doctor", meaning="bác sĩ", pronunciation="/ˈdɑːk.tɚ/", example_sentence="The doctor is very kind.", audio_url="static/audio/words/doctor.mp3", example_audio_url="static/audio/examples/doctor_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="nurse", meaning="y tá", pronunciation="/nɝːs/", example_sentence="The nurse checks my temperature.", audio_url="static/audio/words/nurse.mp3", example_audio_url="static/audio/examples/nurse_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="hospital", meaning="bệnh viện", pronunciation="/ˈhɑː.spɪ.t̬əl/", example_sentence="He works at a hospital.", audio_url="static/audio/words/hospital.mp3", example_audio_url="static/audio/examples/hospital_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="exercise", meaning="tập thể dục", pronunciation="/ˈek.sɚ.saɪz/", example_sentence="I exercise every morning.", audio_url="static/audio/words/exercise.mp3", example_audio_url="static/audio/examples/exercise_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="healthy", meaning="khỏe mạnh", pronunciation="/ˈhel.θi/", example_sentence="Vegetables keep us healthy.", audio_url="static/audio/words/healthy.mp3", example_audio_url="static/audio/examples/healthy_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="tired", meaning="mệt", pronunciation="/taɪrd/", example_sentence="I feel tired after work.", audio_url="static/audio/words/tired.mp3", example_audio_url="static/audio/examples/tired_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="pain", meaning="cơn đau", pronunciation="/peɪn/", example_sentence="She has pain in her leg.", audio_url="static/audio/words/pain.mp3", example_audio_url="static/audio/examples/pain_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="toothache", meaning="đau răng", pronunciation="/ˈtuːθ.eɪk/", example_sentence="I cannot eat because of toothache.", audio_url="static/audio/words/toothache.mp3", example_audio_url="static/audio/examples/toothache_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="headache", meaning="đau đầu", pronunciation="/ˈhed.eɪk/", example_sentence="This noise gives me a headache.", audio_url="static/audio/words/headache.mp3", example_audio_url="static/audio/examples/headache_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_health.id, word="appointment", meaning="lịch hẹn", pronunciation="/əˈpɔɪnt.mənt/", example_sentence="I have a doctor appointment tomorrow.", audio_url="static/audio/words/appointment.mp3", example_audio_url="static/audio/examples/appointment_example.mp3", difficulty="A2"),
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
        Vocabulary(topic_id=topic_a2_travel.id, word="airport", meaning="sân bay", pronunciation="/ˈer.pɔːrt/", example_sentence="We arrived at the airport early.", audio_url="static/audio/words/airport.mp3", example_audio_url="static/audio/examples/airport_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="ticket", meaning="vé", pronunciation="/ˈtɪk.ɪt/", example_sentence="I bought a train ticket.", audio_url="static/audio/words/ticket.mp3", example_audio_url="static/audio/examples/ticket_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="passport", meaning="hộ chiếu", pronunciation="/ˈpæs.pɔːrt/", example_sentence="Do not forget your passport.", audio_url="static/audio/words/passport.mp3", example_audio_url="static/audio/examples/passport_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="hotel", meaning="khách sạn", pronunciation="/hoʊˈtel/", example_sentence="Our hotel is near the beach.", audio_url="static/audio/words/hotel.mp3", example_audio_url="static/audio/examples/hotel_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="map", meaning="bản đồ", pronunciation="/mæp/", example_sentence="This map shows the city center.", audio_url="static/audio/words/map.mp3", example_audio_url="static/audio/examples/map_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="station", meaning="nhà ga", pronunciation="/ˈsteɪ.ʃən/", example_sentence="Meet me at the station.", audio_url="static/audio/words/station.mp3", example_audio_url="static/audio/examples/station_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="luggage", meaning="hành lý", pronunciation="/ˈlʌɡ.ɪdʒ/", example_sentence="Her luggage is very heavy.", audio_url="static/audio/words/luggage.mp3", example_audio_url="static/audio/examples/luggage_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="journey", meaning="hành trình", pronunciation="/ˈdʒɝː.ni/", example_sentence="The journey was long but fun.", audio_url="static/audio/words/journey.mp3", example_audio_url="static/audio/examples/journey_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="direction", meaning="hướng đi", pronunciation="/dəˈrek.ʃən/", example_sentence="Can you give me directions?", audio_url="static/audio/words/direction.mp3", example_audio_url="static/audio/examples/direction_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="temple", meaning="đền chùa", pronunciation="/ˈtem.pəl/", example_sentence="We visited an old temple.", audio_url="static/audio/words/temple.mp3", example_audio_url="static/audio/examples/temple_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="beach", meaning="bãi biển", pronunciation="/biːtʃ/", example_sentence="The beach is very beautiful.", audio_url="static/audio/words/beach.mp3", example_audio_url="static/audio/examples/beach_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="mountain", meaning="ngọn núi", pronunciation="/ˈmaʊn.tən/", example_sentence="They climbed the mountain.", audio_url="static/audio/words/mountain.mp3", example_audio_url="static/audio/examples/mountain_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="bridge", meaning="cầu", pronunciation="/brɪdʒ/", example_sentence="The bridge crosses the river.", audio_url="static/audio/words/bridge.mp3", example_audio_url="static/audio/examples/bridge_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="museum", meaning="bảo tàng", pronunciation="/mjuːˈziː.əm/", example_sentence="The museum opens at nine.", audio_url="static/audio/words/museum.mp3", example_audio_url="static/audio/examples/museum_example.mp3", difficulty="A2"),
        Vocabulary(topic_id=topic_a2_travel.id, word="souvenir", meaning="quà lưu niệm", pronunciation="/ˌsuː.vəˈnɪr/", example_sentence="I bought a souvenir for my friend.", audio_url="static/audio/words/souvenir.mp3", example_audio_url="static/audio/examples/souvenir_example.mp3", difficulty="A2"),
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
        Vocabulary(topic_id=topic_b1_work.id, word="office", meaning="văn phòng", pronunciation="/ˈɔː.fɪs/", example_sentence="Our office is on the fifth floor.", audio_url="static/audio/words/office.mp3", example_audio_url="static/audio/examples/office_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="colleague", meaning="đồng nghiệp", pronunciation="/ˈkɑː.liːɡ/", example_sentence="My colleague helped me today.", audio_url="static/audio/words/colleague.mp3", example_audio_url="static/audio/examples/colleague_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="meeting", meaning="cuộc họp", pronunciation="/ˈmiː.tɪŋ/", example_sentence="We have a meeting at ten.", audio_url="static/audio/words/meeting.mp3", example_audio_url="static/audio/examples/meeting_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="project", meaning="dự án", pronunciation="/ˈprɑː.dʒekt/", example_sentence="This project is very important.", audio_url="static/audio/words/project.mp3", example_audio_url="static/audio/examples/project_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="deadline", meaning="hạn chót", pronunciation="/ˈded.laɪn/", example_sentence="The deadline is next Monday.", audio_url="static/audio/words/deadline.mp3", example_audio_url="static/audio/examples/deadline_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="salary", meaning="lương", pronunciation="/ˈsæl.ɚ.i/", example_sentence="Her salary increased this year.", audio_url="static/audio/words/salary.mp3", example_audio_url="static/audio/examples/salary_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="manager", meaning="quản lý", pronunciation="/ˈmæn.ɪ.dʒɚ/", example_sentence="The manager approved my plan.", audio_url="static/audio/words/manager.mp3", example_audio_url="static/audio/examples/manager_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="interview", meaning="phỏng vấn", pronunciation="/ˈɪn.t̬ɚ.vjuː/", example_sentence="I have a job interview tomorrow.", audio_url="static/audio/words/interview.mp3", example_audio_url="static/audio/examples/interview_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="resume", meaning="hồ sơ xin việc", pronunciation="/ˈrez.ə.meɪ/", example_sentence="Please send your resume by email.", audio_url="static/audio/words/resume.mp3", example_audio_url="static/audio/examples/resume_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="promotion", meaning="thăng chức", pronunciation="/prəˈmoʊ.ʃən/", example_sentence="He got a promotion last month.", audio_url="static/audio/words/promotion.mp3", example_audio_url="static/audio/examples/promotion_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="responsibility", meaning="trách nhiệm", pronunciation="/rɪˌspɑːn.səˈbɪl.ə.t̬i/", example_sentence="This task is my responsibility.", audio_url="static/audio/words/responsibility.mp3", example_audio_url="static/audio/examples/responsibility_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="schedule", meaning="lịch trình", pronunciation="/ˈskedʒ.uːl/", example_sentence="My schedule is full today.", audio_url="static/audio/words/schedule.mp3", example_audio_url="static/audio/examples/schedule_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="customer", meaning="khách hàng", pronunciation="/ˈkʌs.tə.mɚ/", example_sentence="The customer asked a question.", audio_url="static/audio/words/customer.mp3", example_audio_url="static/audio/examples/customer_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="team", meaning="đội nhóm", pronunciation="/tiːm/", example_sentence="Our team works very well together.", audio_url="static/audio/words/team.mp3", example_audio_url="static/audio/examples/team_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_work.id, word="commute", meaning="đi lại đi làm", pronunciation="/kəˈmjuːt/", example_sentence="My commute takes one hour.", audio_url="static/audio/words/commute.mp3", example_audio_url="static/audio/examples/commute_example.mp3", difficulty="B1"),
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
        Vocabulary(topic_id=topic_b1_tech.id, word="computer", meaning="máy tính", pronunciation="/kəmˈpjuː.t̬ɚ/", example_sentence="My computer is very fast.", audio_url="static/audio/words/computer.mp3", example_audio_url="static/audio/examples/computer_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="keyboard", meaning="bàn phím", pronunciation="/ˈkiː.bɔːrd/", example_sentence="This keyboard is comfortable.", audio_url="static/audio/words/keyboard.mp3", example_audio_url="static/audio/examples/keyboard_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="screen", meaning="màn hình", pronunciation="/skriːn/", example_sentence="The screen is too bright.", audio_url="static/audio/words/screen.mp3", example_audio_url="static/audio/examples/screen_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="internet", meaning="internet", pronunciation="/ˈɪn.t̬ɚ.net/", example_sentence="The internet is slow today.", audio_url="static/audio/words/internet.mp3", example_audio_url="static/audio/examples/internet_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="website", meaning="trang web", pronunciation="/ˈweb.saɪt/", example_sentence="I found it on a website.", audio_url="static/audio/words/website.mp3", example_audio_url="static/audio/examples/website_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="password", meaning="mật khẩu", pronunciation="/ˈpæs.wɝːd/", example_sentence="Change your password often.", audio_url="static/audio/words/password.mp3", example_audio_url="static/audio/examples/password_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="download", meaning="tải xuống", pronunciation="/ˈdaʊn.loʊd/", example_sentence="Please download this file.", audio_url="static/audio/words/download.mp3", example_audio_url="static/audio/examples/download_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="upload", meaning="tải lên", pronunciation="/ʌpˈloʊd/", example_sentence="I will upload the photo later.", audio_url="static/audio/words/upload.mp3", example_audio_url="static/audio/examples/upload_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="app", meaning="ứng dụng", pronunciation="/æp/", example_sentence="This app helps me study words.", audio_url="static/audio/words/app.mp3", example_audio_url="static/audio/examples/app_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="device", meaning="thiết bị", pronunciation="/dɪˈvaɪs/", example_sentence="The device is easy to use.", audio_url="static/audio/words/device.mp3", example_audio_url="static/audio/examples/device_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="battery", meaning="pin", pronunciation="/ˈbæt̬.ɚ.i/", example_sentence="My phone battery is low.", audio_url="static/audio/words/battery.mp3", example_audio_url="static/audio/examples/battery_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="update", meaning="cập nhật", pronunciation="/ʌpˈdeɪt/", example_sentence="You should update the app.", audio_url="static/audio/words/update.mp3", example_audio_url="static/audio/examples/update_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="message", meaning="tin nhắn", pronunciation="/ˈmes.ɪdʒ/", example_sentence="I sent you a message.", audio_url="static/audio/words/message.mp3", example_audio_url="static/audio/examples/message_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="camera", meaning="máy ảnh", pronunciation="/ˈkæm.rə/", example_sentence="The camera takes clear pictures.", audio_url="static/audio/words/camera.mp3", example_audio_url="static/audio/examples/camera_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_tech.id, word="software", meaning="phần mềm", pronunciation="/ˈsɔːft.wer/", example_sentence="This software is very useful.", audio_url="static/audio/words/software.mp3", example_audio_url="static/audio/examples/software_example.mp3", difficulty="B1"),
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
        Vocabulary(topic_id=topic_b1_nature.id, word="forest", meaning="rừng", pronunciation="/ˈfɔːr.ɪst/", example_sentence="The forest is full of birds.", audio_url="static/audio/words/forest.mp3", example_audio_url="static/audio/examples/forest_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="river", meaning="sông", pronunciation="/ˈrɪv.ɚ/", example_sentence="This river is very long.", audio_url="static/audio/words/river.mp3", example_audio_url="static/audio/examples/river_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="ocean", meaning="đại dương", pronunciation="/ˈoʊ.ʃən/", example_sentence="The ocean looks calm today.", audio_url="static/audio/words/ocean.mp3", example_audio_url="static/audio/examples/ocean_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="climate", meaning="khí hậu", pronunciation="/ˈklaɪ.mət/", example_sentence="Climate change affects everyone.", audio_url="static/audio/words/climate.mp3", example_audio_url="static/audio/examples/climate_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="pollution", meaning="ô nhiễm", pronunciation="/pəˈluː.ʃən/", example_sentence="Air pollution is a big problem.", audio_url="static/audio/words/pollution.mp3", example_audio_url="static/audio/examples/pollution_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="recycle", meaning="tái chế", pronunciation="/riːˈsaɪ.kəl/", example_sentence="We recycle plastic bottles.", audio_url="static/audio/words/recycle.mp3", example_audio_url="static/audio/examples/recycle_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="wildlife", meaning="động vật hoang dã", pronunciation="/ˈwaɪld.laɪf/", example_sentence="The park protects local wildlife.", audio_url="static/audio/words/wildlife.mp3", example_audio_url="static/audio/examples/wildlife_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="energy", meaning="năng lượng", pronunciation="/ˈen.ɚ.dʒi/", example_sentence="We should save energy at home.", audio_url="static/audio/words/energy.mp3", example_audio_url="static/audio/examples/energy_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="solar", meaning="thuộc năng lượng mặt trời", pronunciation="/ˈsoʊ.lɚ/", example_sentence="Solar power is becoming popular.", audio_url="static/audio/words/solar.mp3", example_audio_url="static/audio/examples/solar_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="wind", meaning="gió", pronunciation="/wɪnd/", example_sentence="Strong wind moved the trees.", audio_url="static/audio/words/wind.mp3", example_audio_url="static/audio/examples/wind_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="drought", meaning="hạn hán", pronunciation="/draʊt/", example_sentence="The farmers suffered from drought.", audio_url="static/audio/words/drought.mp3", example_audio_url="static/audio/examples/drought_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="flood", meaning="lũ lụt", pronunciation="/flʌd/", example_sentence="The flood damaged many houses.", audio_url="static/audio/words/flood.mp3", example_audio_url="static/audio/examples/flood_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="protect", meaning="bảo vệ", pronunciation="/prəˈtekt/", example_sentence="We must protect the environment.", audio_url="static/audio/words/protect.mp3", example_audio_url="static/audio/examples/protect_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="organic", meaning="hữu cơ", pronunciation="/ɔːrˈɡæn.ɪk/", example_sentence="They buy organic vegetables.", audio_url="static/audio/words/organic.mp3", example_audio_url="static/audio/examples/organic_example.mp3", difficulty="B1"),
        Vocabulary(topic_id=topic_b1_nature.id, word="ecosystem", meaning="hệ sinh thái", pronunciation="/ˈiː.koʊˌsɪs.təm/", example_sentence="A healthy ecosystem supports life.", audio_url="static/audio/words/ecosystem.mp3", example_audio_url="static/audio/examples/ecosystem_example.mp3", difficulty="B1"),
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
        Vocabulary(topic_id=topic_b2_arts.id, word="painting", meaning="hội họa", pronunciation="/ˈpeɪn.t̬ɪŋ/", example_sentence="She loves painting landscapes.", audio_url="static/audio/words/painting.mp3", example_audio_url="static/audio/examples/painting_example.mp3", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="sculpture", meaning="điêu khắc", pronunciation="/ˈskʌlp.tʃɚ/", example_sentence="The sculpture is made of stone.", audio_url="static/audio/words/sculpture.mp3", example_audio_url="static/audio/examples/sculpture_example.mp3", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="literature", meaning="văn học", pronunciation="/ˈlɪt̬.ɚ.ə.tʃɚ/", example_sentence="I study world literature at school.", audio_url="static/audio/words/literature.mp3", example_audio_url="static/audio/examples/literature_example.mp3", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="theater", meaning="nhà hát", pronunciation="/ˈθiː.ə.t̬ɚ/", example_sentence="We watched a play at the theater.", audio_url="static/audio/words/theater.mp3", example_audio_url="static/audio/examples/theater_example.mp3", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="audience", meaning="khán giả", pronunciation="/ˈɑː.di.əns/", example_sentence="The audience clapped loudly.", audio_url="static/audio/words/audience.mp3", example_audio_url="static/audio/examples/audience_example.mp3", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="melody", meaning="giai điệu", pronunciation="/ˈmel.ə.di/", example_sentence="This melody sounds peaceful.", audio_url="static/audio/words/melody.mp3", example_audio_url="static/audio/examples/melody_example.mp3", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="rhythm", meaning="nhịp điệu", pronunciation="/ˈrɪð.əm/", example_sentence="The song has a strong rhythm.", audio_url="static/audio/words/rhythm.mp3", example_audio_url="static/audio/examples/rhythm_example.mp3", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="exhibition", meaning="triển lãm", pronunciation="/ˌek.səˈbɪʃ.ən/", example_sentence="The exhibition opens this weekend.", audio_url="static/audio/words/exhibition.mp3", example_audio_url="static/audio/examples/exhibition_example.mp3", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="heritage", meaning="di sản", pronunciation="/ˈher.ɪ.t̬ɪdʒ/", example_sentence="This town has rich cultural heritage.", audio_url="static/audio/words/heritage.mp3", example_audio_url="static/audio/examples/heritage_example.mp3", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="tradition", meaning="truyền thống", pronunciation="/trəˈdɪʃ.ən/", example_sentence="Tet is an important tradition.", audio_url="static/audio/words/tradition.mp3", example_audio_url="static/audio/examples/tradition_example.mp3", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="festival", meaning="lễ hội", pronunciation="/ˈfes.t̬ə.vəl/", example_sentence="The festival attracts many visitors.", audio_url="static/audio/words/festival.mp3", example_audio_url="static/audio/examples/festival_example.mp3", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="masterpiece", meaning="tác phẩm xuất sắc", pronunciation="/ˈmæs.tɚ.piːs/", example_sentence="Many people call it a masterpiece.", audio_url="static/audio/words/masterpiece.mp3", example_audio_url="static/audio/examples/masterpiece_example.mp3", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="creative", meaning="sáng tạo", pronunciation="/kriˈeɪ.tɪv/", example_sentence="She has a very creative mind.", audio_url="static/audio/words/creative.mp3", example_audio_url="static/audio/examples/creative_example.mp3", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="performance", meaning="buổi biểu diễn", pronunciation="/pɚˈfɔːr.məns/", example_sentence="Their performance was excellent.", audio_url="static/audio/words/performance.mp3", example_audio_url="static/audio/examples/performance_example.mp3", difficulty="B2"),
        Vocabulary(topic_id=topic_b2_arts.id, word="portrait", meaning="chân dung", pronunciation="/ˈpɔːr.trət/", example_sentence="The portrait hangs on the wall.", audio_url="static/audio/words/portrait.mp3", example_audio_url="static/audio/examples/portrait_example.mp3", difficulty="B2"),
    ]
    db.add_all(vocab_b2_arts)
    db.commit()

    for topic_data in ADVANCED_VOCAB_TOPICS:
        topic = Topic(
            name=topic_data["name"],
            description=topic_data["description"],
            icon_url=topic_data["icon_url"],
            level=topic_data["level"],
        )
        db.add(topic)
        db.commit()
        db.refresh(topic)

        vocabularies = []
        for item in topic_data["vocabularies"]:
            slug = audio_slug(item["word"])
            vocabularies.append(
                Vocabulary(
                    topic_id=topic.id,
                    word=item["word"],
                    meaning=item["meaning"],
                    pronunciation=item["pronunciation"],
                    example_sentence=item["example_sentence"],
                    audio_url=f"static/audio/words/{slug}.mp3",
                    example_audio_url=f"static/audio/examples/{slug}_example.mp3",
                    difficulty=topic_data["level"],
                )
            )
        db.add_all(vocabularies)
        db.commit()

    print("✅ Vocabulary data seeded successfully!")
    print(f"   - Topics: {db.query(Topic).count()}")
    print(f"   - Vocabularies: {db.query(Vocabulary).count()}")

except Exception as e:
    print(f"❌ Error seeding data: {e}")
    db.rollback()

finally:
    db.close()
