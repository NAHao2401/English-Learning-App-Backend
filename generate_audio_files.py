import asyncio
import re
import json
import os
from pathlib import Path
import edge_tts

# Create audio directories
SCRIPT_DIR = Path(__file__).parent.resolve()
AUDIO_DIR = SCRIPT_DIR / "static" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

WORD_AUDIO_DIR = AUDIO_DIR / "words"
EXAMPLE_AUDIO_DIR = AUDIO_DIR / "examples"
WORD_AUDIO_DIR.mkdir(exist_ok=True)
EXAMPLE_AUDIO_DIR.mkdir(exist_ok=True)

async def generate_audio(text, filename, is_example=False):
    """Generate MP3 audio using edge-tts"""
    try:
        output_dir = EXAMPLE_AUDIO_DIR if is_example else WORD_AUDIO_DIR
        output_path = output_dir / filename
        
        # Skip if already exists
        if output_path.exists():
            print(f"  ⏭️  Already exists: {filename}")
            # Return relative URL path
            rel_path = output_path.relative_to(SCRIPT_DIR)
            return str(rel_path).replace("\\", "/")
        
        communicate = edge_tts.Communicate(text, voice="en-US-AriaNeural")
        await communicate.save(str(output_path))
        
        # Return relative URL path
        rel_path = output_path.relative_to(SCRIPT_DIR)
        return str(rel_path).replace("\\", "/")
    except Exception as e:
        print(f"  ❌ Error generating audio for '{text}': {e}")
        return None

async def process_all_audio():
    """Process all vocabulary words and examples"""
    
    # Extract vocabulary from seed_vocabularies.py
    with open('seed_vocabularies.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all Vocabulary entries
    pattern = r'Vocabulary\(([^)]+)\)'
    matches = re.findall(pattern, content)
    
    audio_mapping = {}
    
    print(f"Found {len(matches)} vocabulary entries\n")
    
    for i, vocab_params in enumerate(matches, 1):
        # Extract word and example_sentence
        word_match = re.search(r'word="([^"]+)"', vocab_params)
        example_match = re.search(r'example_sentence="([^"]+)"', vocab_params)
        
        if not word_match:
            continue
        
        word = word_match.group(1)
        example = example_match.group(1) if example_match else None
        
        # Create safe filenames
        word_filename = f"{word.replace(' ', '_')}.mp3"
        example_filename = f"{word.replace(' ', '_')}_example.mp3"
        
        print(f"[{i}/{len(matches)}] {word}")
        
        # Generate word audio
        word_audio_url = await generate_audio(word, word_filename, is_example=False)
        
        # Generate example audio
        example_audio_url = None
        if example:
            example_audio_url = await generate_audio(example, example_filename, is_example=True)
        
        audio_mapping[word] = {
            "audio_url": word_audio_url,
            "example_audio_url": example_audio_url
        }
    
    # Save mapping to JSON
    json_path = SCRIPT_DIR / 'audio_mapping.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(audio_mapping, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Audio generation complete!")
    print(f"Audio files saved to:")
    print(f"  - Words: {WORD_AUDIO_DIR}")
    print(f"  - Examples: {EXAMPLE_AUDIO_DIR}")
    print(f"  - Mapping: {json_path}")
    
    return audio_mapping

if __name__ == "__main__":
    asyncio.run(process_all_audio())
