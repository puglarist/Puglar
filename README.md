# Puglar

Utilities to **scrape existing audio files** from a webpage and **generate new audio** using the Hugging Face Inference API.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 1) Scrape audio files from a webpage

```bash
python3 audio_tools.py scrape "https://example.com" --output-dir scraped_audio
```

This command:
- fetches the page
- finds audio links in `<audio>`, `<source>`, and `<a>` tags
- downloads detected audio files into your output directory

## 2) Generate audio with Hugging Face API

Set your token first:

```bash
export HF_TOKEN="your_hugging_face_token"
```

Then run:

```bash
python3 audio_tools.py generate \
  --text "Hello from Puglar audio pipeline" \
  --model "suno/bark" \
  --output-file generated_audio.wav
```

Optional:

```bash
python3 audio_tools.py generate \
  --text "Test with a preset" \
  --model "suno/bark" \
  --voice-preset "v2/en_speaker_1" \
  --output-file preset_audio.wav
```

## Notes

- Not every Hugging Face model supports `voice_preset`.
- Some models need a warm-up period and may return JSON temporarily. Re-run after a short wait.
- You can pass `--token` directly instead of using `HF_TOKEN`.
