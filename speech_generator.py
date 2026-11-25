import asyncio
import hashlib

from pathlib import Path
import edge_tts

import config


def get_audio_path(word):
    """Generate a unique cache filename for a word and voice."""

    identifier = f"{config.TTS_VOICE}_{word.casefold()}"

    filename = hashlib.sha256(
        identifier.encode("utf-8")
    ).hexdigest()

    return Path(config.AUDIO_CACHE_DIR) / f"{filename}.mp3"


async def generate_audio(word, output_file):
    """Generate speech for a single word using Edge TTS."""

    communicate = edge_tts.Communicate(
        text=word,
        voice=config.TTS_VOICE,
        rate=config.TTS_RATE
    )

    await communicate.save(str(output_file))


async def generate_all_audio(words):
    """Generate audio for all unique words."""

    for word in words:

        output_file = get_audio_path(word)

        # Reuse existing audio if available
        if output_file.exists():
            print(f"Using cached audio: {word}")
            continue

        print(f"Generating speech: {word}")

        await generate_audio(word, output_file)

    return {
        word.casefold(): get_audio_path(word)
        for word in words
    }


def prepare_speech(words):
    """Prepare speech files for all words."""

    Path(config.AUDIO_CACHE_DIR).mkdir(
        parents=True,
        exist_ok=True
    )

    return asyncio.run(generate_all_audio(words))