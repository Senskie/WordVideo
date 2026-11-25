from pathlib import Path

import config

from text_processor import load_words, process_words
from speech_generator import prepare_speech
from video_generator import generate_video


def main():

    # Load and process input
    raw_words = load_words(config.INPUT_FILE)

    words, counts = process_words(raw_words)

    # Prepare speech
    if config.TTS_ENABLED:
        audio_files = prepare_speech(words)
    else:
        audio_files = {}

    # Create output directory
    Path(config.OUTPUT_FILE).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Generate video
    generate_video(
        words,
        counts,
        audio_files,
        config.OUTPUT_FILE
    )

    print(f"Video saved to {config.OUTPUT_FILE}")
    print(f"Unique words: {len(words)}")


if __name__ == "__main__":
    main()