# Gemini Video Transcript CLI

This repository provides a command-line workflow that converts batches of local video files to audio (`.m4a`) and submits them to Google’s Gemini 2.5 Flash model for automatic transcription. Use it to bulk-process recordings you already possess—no YouTube links, web UI, or manual uploads required.

## Features

- Scans a directory for videos with a specified extension (default `mp4`).
- Uses `ffmpeg` to extract audio only when an `.m4a` copy does not already exist.
- Uploads each audio file to Gemini 2.5 Flash and retrieves a verbatim transcript stored beside the source video.
- Cleans up uploaded assets from the Gemini account to avoid orphaned files.

## Requirements

- Python 3.10+
- `ffmpeg` available on your `PATH`
- Google Generative AI API access and a `GOOGLE_API_KEY`
- Python dependencies from `requirements.txt` (`google-generativeai`, `python-dotenv`)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
touch .env
echo "GOOGLE_API_KEY=your_key" >> .env
```

## Usage

```bash
python app.py --dir data/videos --format mp4
```

- `--dir` points to the folder with your source files.
- `--format` is the input video extension (omit the dot). The default is `mp4`; change to `mov`, `mkv`, etc., as needed.
- Each processed video produces:
  - `<name>.m4a` (audio) — skipped if it already exists.
  - `<name>.txt` — plain-text transcript emitted next to the video.

## Troubleshooting

- **ffmpeg missing**: install via your package manager (e.g., `brew install ffmpeg`, `choco install ffmpeg`) and reopen the shell.
- **Authentication errors**: ensure `.env` contains a valid `GOOGLE_API_KEY` and that the key has access to Gemini 2.5 Flash.
- **Quota limits**: the script stops when Gemini rejects an upload; retry after confirming usage limits or switch to a paid tier.

## Contributing

Issues and pull requests are welcome. Please describe the scenario you processed (`--dir`, sample formats), list commands you ran, and attach relevant logs or transcript snippets to expedite reviews.
