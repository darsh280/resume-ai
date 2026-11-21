"""
add_voiceover.py
================
Merges your recorded voice file (MP3, WAV, M4A, etc.) with the generated
ResumeAI demonstration video.

Usage:
  1. Record your voice reading the script.
  2. Save your audio file as 'my_voice.mp3' (or .wav / .m4a) in this folder.
  3. Run:
       python add_voiceover.py
  4. Your final combined video with your voice will be: 'resume_ai_final_presentation.mp4'
"""

import sys
import os
import subprocess
from pathlib import Path

VIDEO_DIR = Path(__file__).resolve().parent
VIDEO_INPUT = VIDEO_DIR / "resume_ai_demo.mp4"
OUTPUT_FINAL = VIDEO_DIR / "resume_ai_final_presentation.mp4"

# Supported audio names
AUDIO_CANDIDATES = [
    VIDEO_DIR / "my_voice.mp3",
    VIDEO_DIR / "my_voice.m4a",
    VIDEO_DIR / "my_voice.wav",
    VIDEO_DIR / "voiceover.mp3",
    VIDEO_DIR / "voiceover.m4a",
    VIDEO_DIR / "voiceover.wav",
    VIDEO_DIR / "audio.mp3",
]

def main():
    if not VIDEO_INPUT.exists():
        print(f"Error: Base video {VIDEO_INPUT} not found. Run generate_video.py first.")
        return

    # Find the audio file
    audio_file = None
    if len(sys.argv) > 1:
        audio_file = Path(sys.argv[1])
    else:
        for c in AUDIO_CANDIDATES:
            if c.exists():
                audio_file = c
                break

    if not audio_file or not audio_file.exists():
        print("=" * 60)
        print("AUDIO FILE NOT FOUND!")
        print("Please record your voice and save the file in this folder:")
        print(f"  {VIDEO_DIR}")
        print("Name it: 'my_voice.mp3' (or 'my_voice.m4a' / 'my_voice.wav')")
        print("\nThen run this script again:")
        print("  python add_voiceover.py")
        print("=" * 60)
        return

    print(f"Found audio file: {audio_file.name}")
    print(f"Merging with video: {VIDEO_INPUT.name}...")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(VIDEO_INPUT),
        "-i", str(audio_file),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(OUTPUT_FINAL)
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print("\n" + "=" * 60)
        print(f"CONGRATULATIONS! Your final video with your voice is ready:")
        print(f"  --> {OUTPUT_FINAL}")
        print(f"File size: {OUTPUT_FINAL.stat().st_size / (1024*1024):.2f} MB")
        print("=" * 60)
    else:
        print("Error during audio merge:", res.stderr)

if __name__ == "__main__":
    main()
