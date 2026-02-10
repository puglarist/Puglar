# Puglar

## Netflix-style studio simulator

This repository now includes `studio_simulator.py`, which can turn:

- video footage into a narrative simulation timeline, and
- screen recordings into interaction-aware simulation beats.

It extracts technical metadata with `ffprobe` (duration, resolution, fps), then generates beat-by-beat simulation segments (`cold_open`, `story`/`interaction`, `cliffhanger`) and a `binge_score`.

### Requirements

- Python 3.10+
- `ffprobe` available on your PATH (typically from `ffmpeg`)

### Convert a video into a simulation

```bash
python studio_simulator.py input_video.mp4 --mode video --output simulation.json
```

### Convert a screen recording into a simulation

```bash
python studio_simulator.py screen_recording.mp4 --mode screen --output screen_simulation.json
```

### Tune pacing density

```bash
python studio_simulator.py episode.mp4 --mode video --beat-window-sec 8 --output dense_simulation.json
```

Lower `--beat-window-sec` values produce more simulation beats.
