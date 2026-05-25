import asyncio
import json
import sys
from pathlib import Path

import edge_tts

from seed_lessons import SEED_DATA, question_audio_text


SCRIPT_DIR = Path(__file__).parent.resolve()
QUESTION_AUDIO_DIR = SCRIPT_DIR / "static" / "audio" / "question"
QUESTION_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "en-US-AriaNeural"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def extract_blank_questions() -> list[dict[str, str]]:
    questions = []
    seen_texts = set()

    for topic in SEED_DATA:
        for lesson in topic["lessons"]:
            for question in lesson["questions"]:
                if question["question_type"] != "fill_blank":
                    continue

                spoken_text = question_audio_text(
                    question["question_text"],
                    question.get("correct_answer"),
                )

                if spoken_text in seen_texts:
                    continue

                audio_url = question["audio_url"]
                filename = Path(audio_url).name
                seen_texts.add(spoken_text)
                questions.append(
                    {
                        "question_type": question["question_type"],
                        "question_text": question["question_text"],
                        "correct_answer": question.get("correct_answer"),
                        "spoken_text": spoken_text,
                        "filename": filename,
                        "audio_url": audio_url,
                    }
                )

    return questions


async def generate_audio(text: str, filename: str) -> str | None:
    output_path = QUESTION_AUDIO_DIR / filename

    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"  Skip existing: {filename}")
        return str(output_path.relative_to(SCRIPT_DIR)).replace("\\", "/")

    try:
        communicate = edge_tts.Communicate(text, voice=VOICE)
        await communicate.save(str(output_path))
        return str(output_path.relative_to(SCRIPT_DIR)).replace("\\", "/")
    except Exception as exc:
        print(f"  Error generating audio for '{text}': {exc}")
        return None


async def process_question_audio() -> list[dict[str, str]]:
    questions = extract_blank_questions()
    print(f"Found {len(questions)} unique fill_blank question audio files to generate")

    generated = []
    for index, question in enumerate(questions, start=1):
        print(f"[{index}/{len(questions)}] {question['spoken_text']}")
        audio_url = await generate_audio(question["spoken_text"], question["filename"])
        if audio_url:
            question["audio_url"] = audio_url
            generated.append(question)

    mapping_path = SCRIPT_DIR / "question_audio_mapping.json"
    mapping_path.write_text(
        json.dumps(generated, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\nQuestion audio generation complete.")
    print(f"Audio files saved to: {QUESTION_AUDIO_DIR}")
    print(f"Mapping saved to: {mapping_path}")

    return generated


if __name__ == "__main__":
    asyncio.run(process_question_audio())
