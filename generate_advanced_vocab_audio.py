import asyncio
import json
import sys
from pathlib import Path

import edge_tts

from advanced_vocab_topics import ADVANCED_VOCAB_TOPICS, audio_slug


SCRIPT_DIR = Path(__file__).parent.resolve()
AUDIO_DIR = SCRIPT_DIR / "static" / "audio"
WORD_AUDIO_DIR = AUDIO_DIR / "words"
EXAMPLE_AUDIO_DIR = AUDIO_DIR / "examples"
VOICE = "en-US-AriaNeural"

WORD_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
EXAMPLE_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def generate_audio(text: str, output_path: Path) -> str | None:
    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"  Skip existing: {output_path.name}")
        return str(output_path.relative_to(SCRIPT_DIR)).replace("\\", "/")

    try:
        communicate = edge_tts.Communicate(text, voice=VOICE)
        await communicate.save(str(output_path))
        return str(output_path.relative_to(SCRIPT_DIR)).replace("\\", "/")
    except Exception as exc:
        print(f"  Error generating audio for '{text}': {exc}")
        return None


def iter_vocabularies() -> list[dict[str, str]]:
    vocabularies = []
    for topic in ADVANCED_VOCAB_TOPICS:
        for item in topic["vocabularies"]:
            vocabularies.append(item)
    return vocabularies


async def process_advanced_vocab_audio() -> dict[str, dict[str, str | None]]:
    vocabularies = iter_vocabularies()
    mapping = {}

    print(f"Found {len(vocabularies)} advanced vocabulary entries")
    for index, item in enumerate(vocabularies, start=1):
        word = item["word"]
        slug = audio_slug(word)
        word_path = WORD_AUDIO_DIR / f"{slug}.mp3"
        example_path = EXAMPLE_AUDIO_DIR / f"{slug}_example.mp3"

        print(f"[{index}/{len(vocabularies)}] {word}")
        audio_url = await generate_audio(word, word_path)
        example_audio_url = await generate_audio(item["example_sentence"], example_path)
        mapping[word] = {
            "audio_url": audio_url,
            "example_audio_url": example_audio_url,
        }

    mapping_path = SCRIPT_DIR / "advanced_vocab_audio_mapping.json"
    mapping_path.write_text(
        json.dumps(mapping, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\nAdvanced vocabulary audio generation complete.")
    print(f"Audio files saved to: {AUDIO_DIR}")
    print(f"Mapping saved to: {mapping_path}")
    return mapping


if __name__ == "__main__":
    asyncio.run(process_advanced_vocab_audio())

