from pathlib import Path

import config
from text_processor import load_words, count_words
from video_generator import generate_video


def main():

    # Load input
    words = load_words(config.INPUT_FILE)

    # Count occurrences
    counts = count_words(words)

    # Create output directory
    Path(config.OUTPUT_FILE).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Generate video
    generate_video(
        words,
        counts,
        config.OUTPUT_FILE
    )

    print(f"Video saved to {config.OUTPUT_FILE}")
    print(f"Number of words: {len(words)}")
    print(f"Video duration: {len(words) * config.WORD_DURATION:.2f} seconds")


if __name__ == "__main__":
    main()