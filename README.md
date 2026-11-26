# WordVideo

A Python-based video generator that displays a sequence of unique words while simultaneously pronouncing them using text-to-speech (TTS).

Each unique word is displayed once, for a configurable duration, with its total occurrence count shown underneath. The corresponding pronunciation is played while the word is visible.

## Features

- Reads words from a `.txt` input file.
- Automatically identifies unique words.
- Counts how often each word occurs in the original text.
- Displays each unique word exactly once.
- Uses a fixed minimum display duration per word.
- Generates speech using Microsoft Edge TTS.
- Supports audio speed adjustment while preserving pitch using Librosa.
- Caches generated audio to avoid unnecessary TTS requests.
- Exports the final video as an MP4 file.

---

## 1. Requirements

The project requires:

- Python 3.10 or newer (Python 3.12 or 3.13 is recommended for compatibility).
- FFmpeg.
- The Python packages listed below.
- An internet connection for generating new speech files through Edge TTS.

### 1.1 System dependencies

**Arch Linux / CachyOS**

Install FFmpeg:

```bash
sudo pacman -S ffmpeg
```

**Ubuntu / Linux Mint / Debian**

```bash
sudo apt update
sudo apt install ffmpeg
```

Verify the installation:

```bash
ffmpeg -version
```

FFmpeg is used by MoviePy to encode the final video and process media files.

### 1.2 Python environment

Clone or download the project and navigate to its directory:

```bash
cd WordVideo
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

### 1.3 Python packages

Install the required packages:

```bash
pip install moviepy pillow numpy edge-tts librosa soundfile
```

The packages serve the following purposes:

| Package | Purpose |
|---|---|
| `moviepy` | Video generation and audio/video synchronization |
| `pillow` | Drawing words and counters onto video frames |
| `numpy` | Converting images into arrays for MoviePy |
| `edge-tts` | Generating speech using Microsoft Edge neural voices |
| `librosa` | Speeding up audio while preserving pitch |
| `soundfile` | Saving processed audio as WAV files |

To verify the installation:

```bash
python -c "import moviepy, PIL, numpy, edge_tts, librosa, soundfile; print('All dependencies installed successfully.')"
```

---

## 2. Project structure

The project is organized into separate modules, each responsible for a specific task.

```text
WordVideo/
│
├── main.py
├── config.py
├── text_processor.py
├── speech_generator.py
├── video_generator.py
├── clear_cache.py
│
├── input/
│   └── words.txt
│
├── cache/
│   └── audio/
│
└── output/
    └── video.mp4
```

### File descriptions

| File | Description |
|---|---|
| `main.py` | Main entry point; coordinates the entire workflow |
| `config.py` | Contains all configurable parameters |
| `text_processor.py` | Reads the input and processes unique words and their frequencies |
| `speech_generator.py` | Generates, processes and caches speech audio |
| `video_generator.py` | Creates video frames and combines them with audio |
| `clear_cache.py` | Removes all cached audio files |
| `input/words.txt` | Input text containing the words to display |
| `cache/audio/` | Stores generated speech files |
| `output/` | Stores the final video |

---

## 3. Configuration

All important settings are defined in `config.py`.

### Video settings

```python
WIDTH = 1920
HEIGHT = 1080
FPS = 30

WORD_DURATION = 1.5
```

- `WIDTH`, `HEIGHT`: Video resolution.
- `FPS`: Frames per second.
- `WORD_DURATION`: Minimum duration of each word in seconds.

The actual display duration is determined by:

```python
duration = max(
    config.WORD_DURATION,
    audio.duration + config.AUDIO_TAIL
)
```

This ensures that words remain visible until their pronunciation is finished.

### Visual settings

```python
BACKGROUND_COLOR = "#000000"

TEXT_COLOR = "#FFFFFF"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 120

COUNT_COLOR = "#AAAAAA"
COUNT_FONT_SIZE = 35
```

These parameters control the appearance of the video.

`FONT_PATH` should point to an installed TrueType font (`.ttf`) on your system.

### Text-to-speech settings

```python
TTS_VOICE = "en-US-AriaNeural"
TTS_RATE = "+100%"

AUDIO_SPEED = 2.0
AUDIO_TAIL = 0
```

- `TTS_VOICE`: Voice used by Microsoft Edge TTS.
- `TTS_RATE`: Speech rate requested from Edge TTS.
- `AUDIO_SPEED`: Additional playback speed multiplier applied through Librosa.
- `AUDIO_TAIL`: Extra time added after the pronunciation finishes.

`AUDIO_SPEED` uses pitch-preserving time stretching. Higher values produce shorter audio, although extreme values can introduce audio artefacts.

Available voices can be listed using:

```bash
edge-tts --list-voices
```

### File settings

```python
INPUT_FILE = "input/words.txt"
OUTPUT_FILE = "output/video.mp4"

AUDIO_CACHE_DIR = "cache/audio"
```

These settings determine where input, output and cached audio files are stored.

---

## 4. Input format

The input is a plain-text file located at:

```text
input/words.txt
```

Words can be separated by spaces, tabs or newlines.

Example:

```text
apple banana apple pear
banana apple orange
```

The program treats words case-insensitively when counting occurrences.

For this example, the resulting video contains four unique words:

| Word | Occurrences |
|---|---:|
| apple | 3 |
| banana | 2 |
| pear | 1 |
| orange | 1 |

The order of appearance is preserved: each word is displayed according to its first occurrence in the input.

---

## 5. How the code works

The main program coordinates four processing stages.

### 5.1 Text processing

`text_processor.py` reads the input file and extracts all words.

It then uses `collections.Counter` to calculate the occurrence count of each word.

Duplicate words are removed while preserving their original order.

The result consists of:

- A list of unique words.
- A dictionary-like `Counter` containing the occurrence counts.

### 5.2 Speech generation

`speech_generator.py` handles text-to-speech conversion.

For every unique word:

1. Check whether a corresponding audio file already exists in the cache.
2. If not, request speech generation from Microsoft Edge TTS.
3. Save the original speech temporarily as an MP3.
4. Load the audio using Librosa.
5. Apply time stretching to change its duration while preserving pitch.
6. Save the processed audio as a WAV file.
7. Remove the temporary MP3.

The cache prevents repeated TTS requests when generating subsequent videos.

The cache filename is based on a hash of the word and relevant TTS settings.

### 5.3 Video generation

`video_generator.py` is responsible for creating the actual video.

For each unique word:

1. Generate a frame with the word centered horizontally.
2. Position the word using a fixed typographic baseline to prevent vertical jumping.
3. Display its total occurrence count underneath.
4. Load the corresponding WAV file.
5. Combine the image and audio into a MoviePy clip.

All clips are concatenated in their original order.

The resulting video is encoded using H.264, with AAC audio.

### 5.4 Main program

`main.py` connects all the modules.

The execution order is:

```text
Load input text
      |
      v
Process unique words and counts
      |
      v
Generate or load cached audio
      |
      v
Generate video clips
      |
      v
Concatenate clips
      |
      v
Export MP4
```

---

## 6. Running the project

After installing the dependencies and configuring the project, activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the main program:

```bash
python main.py
```

The generated video will be saved to:

```text
output/video.mp4
```

---

## 7. Managing the audio cache

Generated audio files are stored in:

```text
cache/audio/
```

If you change the input text, voice or TTS settings, the program will reuse existing cached audio whenever the cache filename matches.

To remove all cached audio files, execute:

```bash
python clear_cache.py
```

This forces the program to generate the audio again on its next execution.

---

## 8. Troubleshooting

### FFmpeg not found

Verify that FFmpeg is installed and accessible:

```bash
ffmpeg -version
```

### Edge TTS fails to generate speech

Check your internet connection and verify that the selected voice exists:

```bash
edge-tts --list-voices
```

### Changes to speech settings are not reflected

Clear the audio cache:

```bash
python clear_cache.py
```

### Audio sounds unnatural at high speeds

Reduce `AUDIO_SPEED` in `config.py`. Time stretching preserves pitch, but excessive acceleration can still introduce artefacts.

### Font not found

Check whether the font path in `config.py` points to an existing `.ttf` file.

---

## 9. Future improvements

Possible extensions include:

- Automatic language detection and voice selection.
- Per-word pronunciation overrides.
- Configurable word ordering and randomization.
- More advanced visual effects and backgrounds.
- Progress indicators during speech generation and video rendering.
- Parallel audio generation to reduce processing time.
- More flexible timing and audio synchronization.

