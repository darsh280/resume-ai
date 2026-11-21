"""
generate_audio_and_merge.py
===========================
Generates ultra-realistic neural AI voiceover from the user's transcript
and merges it directly into 'resume_ai_demo.mp4' using FFmpeg.

Produces: 'resume_ai_final_presentation.mp4'
"""

import asyncio
import os
import subprocess
from pathlib import Path

VIDEO_DIR = Path(__file__).resolve().parent
VIDEO_INPUT = VIDEO_DIR / "resume_ai_demo.mp4"
AUDIO_OUTPUT = VIDEO_DIR / "generated_voice.mp3"
FINAL_VIDEO = VIDEO_DIR / "resume_ai_final_presentation.mp4"

FULL_TRANSCRIPT = (
    "Hello everyone, welcome to the technical demonstration of ResumeAI, an AI-based resume matching "
    "and candidate ranking system developed as a technical assignment for the AI and Full Stack Developer Internship. "
    "ResumeAI is a production-ready recruitment platform that evaluates resumes using genuine natural language processing semantics, "
    "sentence embeddings, and explainable AI for component scoring engines. "
    "\n\n"
    "Moving to Scene 2, the Recruiter Dashboard. Starting with Module 1, when a recruiter logs in, they are greeted "
    "with real-time KPI metrics aggregated directly from our SQLite database via FastAPI. We can see 14 resumes processed, "
    "an average match score of 55.7 percent, and our current top-scoring candidate is Alex Johnson at 85.2 percent. "
    "Below, recruiters can track previous analysis sessions, review batch benchmarks, and quickly navigate to a new requisition pipeline. "
    "\n\n"
    "Then, Scene 3 is Job Description and Skills Extraction. In Module 2, recruiters can define a job requisition by pasting raw text "
    "or uploading a text file. Here, we are targeting a senior full-stack developer role requiring 5 plus years of experience. "
    "Our NLP skill extractor scans that text against our curated technology taxonomy, automatically identifying 23 core skills "
    "including Python, React, FastAPI, Docker, Kubernetes, AWS, and PostgreSQL. It normalizes aliases like mapping ReactJS to React, "
    "eliminating manual tagging and human error. "
    "\n\n"
    "Next is Bulk Resume Upload. Module 3 handles bulk resume uploads where recruiters can drag and drop 10 to 20 resumes in either PDF or DOCX format. "
    "We implemented a dual engine parser using PyMuPDF for PDFs and python-docx for DOCX files, automatically extracting candidate names, contact details, "
    "years of experience, structural sections, and technical skills. "
    "\n\n"
    "Now to the Candidate Ranking Leaderboard. Module 5 presents the ranked candidate leaderboard, with every candidate evaluated and sorted "
    "from highest to lowest matching score. Alex Johnson takes the top spot with an 85.2 percent match, earning an Excellent Match screening recommendation. "
    "Blake Thomas follows at 81.4 percent, and Sam Anderson at 78.9 percent as good matches. Recruiters can sort by any column, search by skill, "
    "and review matched versus missing skills. "
    "\n\n"
    "Next is Candidate Deep Dive and Radar Chart. Clicking into Alex Johnson opens Module 6, Candidate Deep Dive. This is where explainable AI shines. "
    "Instead of a black box number, the recruiter sees a four-axis radar chart and breakdown bars reflecting our mathematical scoring formula: "
    "40 percent semantic similarity via all-MiniLM-L6-v2 embeddings, 35 percent technical skill match with 22 of 23 required skills matched, "
    "15 percent relevant experience where Alex has 7 years against the 5-year requirement, and 10 percent education for his Master's in Computer Science. "
    "We also clearly flag the one missing skill gap, which is HTML. "
    "\n\n"
    "Finally, in Module 8, recruiters can export the entire ranking table to CSV or download a high-resolution candidate PDF report generated with ReportLab. "
    "ResumeAI delivers a complete, transparent, and intelligent recruitment screening workflow. Thank you for your time and review!"
)

async def generate_speech():
    import edge_tts
    print("Generating neural voiceover using Microsoft Edge TTS...")
    # 'en-US-GuyNeural' or 'en-US-ChristopherNeural' are crisp professional presenter voices
    voice = "en-US-GuyNeural"
    communicate = edge_tts.Communicate(FULL_TRANSCRIPT, voice, rate="+4%")
    await communicate.save(str(AUDIO_OUTPUT))
    print(f"Audio generated successfully: {AUDIO_OUTPUT} ({AUDIO_OUTPUT.stat().st_size / 1024:.1f} KB)")

def merge_video_audio():
    print("Merging audio and video using FFmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(VIDEO_INPUT),
        "-i", str(AUDIO_OUTPUT),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(FINAL_VIDEO)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print("\n" + "=" * 60)
        print(f"FINAL PRESENTATION VIDEO WITH VOICEOVER IS READY!")
        print(f"File: {FINAL_VIDEO}")
        print(f"Size: {FINAL_VIDEO.stat().st_size / (1024 * 1024):.2f} MB")
        print("=" * 60)
    else:
        print("FFmpeg merge error:", res.stderr)

if __name__ == "__main__":
    asyncio.run(generate_speech())
    merge_video_audio()
