import json
import re

# Load audio mapping
with open('audio_mapping.json', 'r', encoding='utf-8') as f:
    audio_mapping = json.load(f)

# Read the original file
with open('seed_vocabularies.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace each Vocabulary creation to add audio URLs
def add_audio_urls_to_vocab(match):
    vocab_str = match.group(0)
    
    # Extract the word from the vocabulary string
    word_match = re.search(r'word="([^"]+)"', vocab_str)
    if word_match:
        word = word_match.group(1)
        audio_data = audio_mapping.get(word)
        
        # If audio data exists, add both URLs
        if audio_data:
            audio_url = audio_data.get('audio_url')
            example_audio_url = audio_data.get('example_audio_url')
            
            # Build the new parameters string
            updated_vocab = vocab_str
            
            # Remove existing audio_url and example_audio_url if present
            updated_vocab = re.sub(r',\s*audio_url="[^"]*"', '', updated_vocab)
            updated_vocab = re.sub(r',\s*example_audio_url="[^"]*"', '', updated_vocab)
            
            # Insert new audio URLs before difficulty parameter
            if audio_url:
                updated_vocab = updated_vocab.replace(
                    ', difficulty=',
                    f', audio_url="{audio_url}", example_audio_url="{example_audio_url}", difficulty='
                )
            
            return updated_vocab
    
    return vocab_str

# Pattern to match Vocabulary(...) calls
pattern = r'Vocabulary\([^)]+\)'

# Replace all Vocabulary entries
updated_content = re.sub(pattern, add_audio_urls_to_vocab, content)

# Write updated content back
with open('seed_vocabularies.py', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("✅ seed_vocabularies.py updated with audio URLs!")

# Show some examples
lines = updated_content.split('\n')
vocab_lines = [line for line in lines if 'Vocabulary(' in line]
print(f"\nUpdated {len(vocab_lines)} vocabulary entries")
print("\nFirst 5 examples:")
for line in vocab_lines[:5]:
    print(line.strip())
