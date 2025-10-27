# Repository Guidelines

## Project Structure & Module Organization
- `app.py` is the CLI entry point: it parses `--dir`/`--format`, calls ffmpeg for audio extraction, and streams files to Gemini 2.5 Flash for transcription.
- `requirements.txt` pins runtime dependencies (Streamlit is legacy; keep for now unless you remove UI code entirely). Place `.env` next to `app.py` with `GOOGLE_API_KEY`.
- Store raw assets (screenshots, docs) under `images/`. Any future Python packages should live in `src/` with mirrored tests under `tests/`.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` — prepare an isolated interpreter before running the CLI.
- `pip install -r requirements.txt` — install `google-generativeai`, `python-dotenv`, and other helpers.
- `python app.py --dir data/videos --format mp4` — convert MP4s under `data/videos/` to M4A (if missing) and emit transcripts beside the originals.
- `python -m pytest` — run when `tests/` is populated; use `pytest -k convert_to_m4a` for targeted debugging.

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation and snake_case helpers (`convert_to_m4a`, `transcribe_audio`). Keep module-level constants UPPER_SNAKE_CASE if added later.
- Small orchestration steps live in `process_directory`; longer routines should move into standalone modules once logic grows.
- Run `python -m black app.py tests/` plus `ruff check .` (if installed) before committing to keep formatting/linting aligned.

## Testing Guidelines
- Use `pytest` with descriptive names such as `test_convert_to_m4a_skips_existing_audio`. Place fixtures/mocks inside `tests/conftest.py`.
- Mock `subprocess.run`, `genai.upload_file`, and `genai.GenerativeModel.generate_content` to keep tests deterministic and offline.
- Target coverage on all branches that touch filesystem decisions (skipping existing audio/transcripts) and API-key handling.

## Commit & Pull Request Guidelines
- Follow the short, imperative style already in history (`Update README.md`, `Add transcript pipeline`). Group logical changes per commit.
- Every PR should explain: purpose, commands executed (e.g., `python app.py --dir sample`), and artifacts produced (paths to transcript files).
- Reference tracking issues (`Fixes #12`) and mention any new environment variables, ffmpeg flags, or external prerequisites added by the change.

## Security & Configuration Tips
- Keep `.env` out of version control; document required keys in README and supply `GOOGLE_API_KEY=` examples only.
- Validate `--dir` inputs to avoid traversing unintended paths and surface clear errors if ffmpeg is missing.
- Delete uploaded Gemini files when feasible (`genai.delete_file`) to limit residual artifacts in the API account.
