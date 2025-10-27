import argparse
import os
import subprocess
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert video files to M4A and generate transcripts using Gemini 2.5 Flash."
        )
    )
    parser.add_argument(
        "--dir",
        required=True,
        type=Path,
        help="Directory containing the source video files.",
    )
    parser.add_argument(
        "--format",
        default="mp4",
        help="Video file extension to process (default: mp4).",
    )
    return parser.parse_args()


def ensure_env_configured() -> None:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY must be set in the environment or .env file.")
    genai.configure(api_key=api_key)


def convert_to_m4a(video_path: Path) -> Path:
    audio_path = video_path.with_suffix(".m4a")
    if audio_path.exists():
        print(f"[skip] {audio_path.name} already exists.")
        return audio_path

    print(f"[ffmpeg] Converting {video_path.name} -> {audio_path.name}")
    cmd = [
        "ffmpeg",
        "-i",
        str(video_path),
        "-vn",
        "-acodec",
        "aac",
        str(audio_path),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"ffmpeg failed on {video_path.name}: {exc.stderr.decode().strip()}"
        ) from exc

    return audio_path


def transcribe_audio(audio_path: Path) -> str:
    print(f"[gemini] Uploading {audio_path.name}")
    uploaded_file = genai.upload_file(path=str(audio_path))
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = (
        "Transcribe the provided audio file verbatim. "
        "Return plain text without extra commentary."
    )
    response = model.generate_content([prompt, uploaded_file])
    transcript_text = (response.text or "").strip()

    # Attempt to delete uploaded file to avoid storage buildup.
    try:
        genai.delete_file(uploaded_file.name)
    except Exception:
        pass

    if not transcript_text:
        raise RuntimeError(f"No transcript returned for {audio_path.name}.")
    return transcript_text


def process_directory(target_dir: Path, file_extension: str) -> None:
    if not target_dir.is_dir():
        raise NotADirectoryError(f"{target_dir} is not a directory.")

    video_files = sorted(target_dir.glob(f"*.{file_extension.lstrip('.')}"))
    if not video_files:
        print(f"No *.{file_extension} files found in {target_dir}.")
        return

    for video_file in video_files:
        audio_file = convert_to_m4a(video_file)
        transcript_path = video_file.with_suffix(".txt")
        if transcript_path.exists():
            print(f"[skip] Transcript already exists for {video_file.name}.")
            continue

        transcript = transcribe_audio(audio_file)
        transcript_path.write_text(transcript, encoding="utf-8")
        print(f"[done] Wrote transcript to {transcript_path}")


def main() -> None:
    args = parse_args()
    ensure_env_configured()
    process_directory(args.dir, args.format)


if __name__ == "__main__":
    main()
