from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
import numpy as np

import config


def load_font(path, size):
    """Load a TrueType font."""

    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def fit_font(text, max_width, path, initial_size):
    """Reduce font size until the text fits within max_width."""

    size = initial_size

    while size > 10:
        font = load_font(path, size)

        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]

        if text_width <= max_width:
            return font

        size -= 5

    return load_font(path, size)


def create_frame(word, count):
    """Create one video frame containing a word and its occurrence count."""

    image = Image.new(
        "RGB",
        (config.WIDTH, config.HEIGHT),
        config.BACKGROUND_COLOR
    )

    draw = ImageDraw.Draw(image)

    # Main word
    font = fit_font(
        word,
        config.WIDTH * 0.9,
        config.FONT_PATH,
        config.FONT_SIZE
    )

    bbox = draw.textbbox((0, 0), word, font=font)

    text_width = bbox[2] - bbox[0]

    # Center horizontally
    x = (config.WIDTH - text_width) / 2 - bbox[0]

    # Fixed baseline for every word
    baseline = config.HEIGHT / 2

    y = baseline - font.getmetrics()[0]

    draw.text(
        (x, y),
        word,
        font=font,
        fill=config.TEXT_COLOR
    )

    # Occurrence counter (centered below the word)
    count_text = f"{count}x"

    count_font = load_font(
        config.FONT_PATH,
        config.COUNT_FONT_SIZE
    )

    bbox = draw.textbbox((0, 0), count_text, font=count_font)
    count_width = bbox[2] - bbox[0]

    x = (config.WIDTH - count_width) / 2 - bbox[0]

    # Fixed position below the baseline
    y = baseline + 60 - bbox[1]

    draw.text(
        (x, y),
        count_text,
        font=count_font,
        fill=config.COUNT_COLOR
    )

    return image


def generate_video(words, counts, audio_files, output_file):
    """Generate a video with synchronized speech and text."""

    clips = []
    audio_clips = []

    for word in words:

        count = counts[word.casefold()]

        # Generate visual frame
        frame = create_frame(word, count)

        # Load corresponding audio
        audio = AudioFileClip(
            str(audio_files[word.casefold()])
        )

        audio_clips.append(audio)

        # Ensure the word remains visible until speech finishes
        duration = max(
            config.WORD_DURATION,
            audio.duration + config.AUDIO_TAIL
        )

        # Combine image and audio
        clip = (
            ImageClip(np.array(frame))
            .with_duration(duration)
            .with_audio(audio)
        )

        clips.append(clip)

    # Combine all clips
    video = concatenate_videoclips(
        clips,
        method="chain"
    )

    video.write_videofile(
        output_file,
        fps=config.FPS,
        codec="libx264",
        audio_codec="aac"
    )

    # Close resources
    video.close()

    for clip in clips:
        clip.close()

    for audio in audio_clips:
        audio.close()