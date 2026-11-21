"""
generate_video.py
=================
Generates a 1080p Full HD demonstration video (MP4) for ResumeAI.
Renders 7 clean product scenes with exact timing and compiles them
with FFmpeg.

Usage:
  python generate_video.py
"""

import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

VIDEO_DIR = Path(__file__).resolve().parent
OUTPUT_MP4 = VIDEO_DIR / "resume_ai_demo.mp4"
FRAMES_DIR = VIDEO_DIR / "temp_frames"
FRAMES_DIR.mkdir(exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 24

# Colors
DARK_BG = (10, 25, 47)         # #0a192f
CARD_BG = (17, 34, 64)         # #112240
CARD_BORDER = (35, 53, 84)     # #233554
WHITE = (255, 255, 255)
LIGHT_TEXT = (203, 213, 225)   # slate-300
MUTED_TEXT = (148, 163, 184)   # slate-400
ACCENT_BLUE = (59, 130, 246)   # #3b82f6
ACCENT_INDIGO = (99, 102, 241) # #6366f1
ACCENT_EMERALD = (16, 185, 129)# #10b981
ACCENT_AMBER = (245, 158, 11)  # #f59e0b
ACCENT_ROSE = (244, 63, 94)    # #f43f5e

# Fonts
FONT_PATH = "C:\\Windows\\Fonts\\segoeui.ttf"
FONT_BOLD_PATH = "C:\\Windows\\Fonts\\segoeuib.ttf"
if not os.path.exists(FONT_BOLD_PATH):
    FONT_BOLD_PATH = "C:\\Windows\\Fonts\\arialbd.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:\\Windows\\Fonts\\arial.ttf"

font_title = ImageFont.truetype(FONT_BOLD_PATH, 54)
font_subtitle = ImageFont.truetype(FONT_PATH, 26)
font_heading = ImageFont.truetype(FONT_BOLD_PATH, 34)
font_body = ImageFont.truetype(FONT_PATH, 22)
font_bold = ImageFont.truetype(FONT_BOLD_PATH, 22)
font_small = ImageFont.truetype(FONT_PATH, 18)
font_stat_val = ImageFont.truetype(FONT_BOLD_PATH, 42)

def draw_top_nav(draw, current_scene_num, total_scenes, current_title):
    # Top navbar
    draw.rectangle([0, 0, WIDTH, 80], fill=(15, 23, 42))
    draw.line([0, 80, WIDTH, 80], fill=(30, 41, 59), width=2)
    
    # Logo
    draw.rounded_rectangle([40, 16, 88, 64], radius=8, fill=ACCENT_INDIGO)
    draw.text((54, 20), "AI", font=ImageFont.truetype(FONT_BOLD_PATH, 28), fill=WHITE)
    draw.text((105, 22), "ResumeAI", font=ImageFont.truetype(FONT_BOLD_PATH, 26), fill=WHITE)
    draw.text((235, 26), "• Candidate Ranking System", font=font_subtitle, fill=MUTED_TEXT)
    
    # Scene indicator
    indicator = f"Scene {current_scene_num}/{total_scenes}: {current_title}"
    draw.text((WIDTH - 550, 26), indicator, font=font_subtitle, fill=ACCENT_BLUE)

def draw_card(draw, box, title=None, border_color=CARD_BORDER, fill_color=CARD_BG, radius=16):
    draw.rounded_rectangle(box, radius=radius, fill=fill_color, outline=border_color, width=2)
    if title:
        draw.text((box[0] + 25, box[1] + 20), title, font=font_heading, fill=WHITE)

def create_scene_1():
    """Scene 1: Title & Overview (15s)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), color=DARK_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, 1, 7, "Project Overview")
    
    # Big Hero Box
    draw_card(draw, [150, 150, 1770, 930])
    
    # Tag
    draw.rounded_rectangle([200, 200, 520, 245], radius=8, fill=(30, 58, 138))
    draw.text((215, 208), "AI / Full Stack Internship Project", font=font_small, fill=(191, 219, 254))
    
    # Main Title
    draw.text((200, 270), "ResumeAI – AI-Based Resume Matching\n& Candidate Ranking System", font=font_title, fill=WHITE)
    draw.text((200, 420), "End-to-End NLP Screening Architecture • Zero Mock Scores • Explainable AI", font=font_subtitle, fill=ACCENT_BLUE)
    
    # Key Highlights 3-col Grid
    cols = [
        ("FastAPI + React 18", "Production-grade REST architecture with SQLite persistence, SQLAlchemy ORM, and Tailwind CSS responsive interface."),
        ("all-MiniLM-L6-v2 Embeddings", "Dense 384-dimensional sentence transformer embeddings calculating cosine similarity on document semantics."),
        ("Explainable Scoring Model", "Transparent multi-component weighting: 40% Semantic, 35% Skills, 15% Experience, 10% Education.")
    ]
    
    col_width = 470
    start_x = 200
    for idx, (head, desc) in enumerate(cols):
        cx = start_x + idx * (col_width + 45)
        draw.rounded_rectangle([cx, 510, cx + col_width, 850], radius=12, fill=(15, 23, 42), outline=CARD_BORDER, width=2)
        # Dot accent
        draw.ellipse([cx + 25, 545, cx + 45, 565], fill=ACCENT_INDIGO)
        draw.text((cx + 60, 540), head, font=font_bold, fill=WHITE)
        
        # Word wrap desc
        words = desc.split()
        lines, cur = [], []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 34:
                lines.append(" ".join(cur))
                cur = []
        if cur: lines.append(" ".join(cur))
        
        y_off = 600
        for l in lines:
            draw.text((cx + 25, y_off), l, font=font_body, fill=LIGHT_TEXT)
            y_off += 34
            
    return img

def create_scene_2():
    """Scene 2: Recruiter Dashboard UI (25s)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), color=DARK_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, 2, 7, "Recruiter Dashboard")
    
    # Page Header
    draw.text((150, 115), "Module 1: Recruiter Analytics & KPIs", font=font_heading, fill=WHITE)
    draw.text((150, 160), "Real-time metrics aggregated directly from database analyses and candidate rankings", font=font_subtitle, fill=MUTED_TEXT)
    
    # 4 Stat Cards
    stats = [
        ("TOTAL RESUMES", "14", "Parsed from PDF & DOCX", ACCENT_BLUE),
        ("CANDIDATES RANKED", "14", "Evaluated against active JDs", ACCENT_INDIGO),
        ("AVERAGE MATCH SCORE", "55.7%", "Weighted AI composite score", ACCENT_EMERALD),
        ("TOP MATCH CANDIDATE", "Alex Johnson", "Highest scorer (85.2%)", ACCENT_AMBER),
    ]
    
    card_w = 370
    for idx, (label, val, sub, col) in enumerate(stats):
        x = 150 + idx * (card_w + 30)
        draw.rounded_rectangle([x, 220, x + card_w, 380], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=2)
        draw.text((x + 25, 245), label, font=font_small, fill=MUTED_TEXT)
        draw.text((x + 25, 280), val, font=font_stat_val, fill=col)
        draw.text((x + 25, 340), sub, font=font_small, fill=LIGHT_TEXT)
        
    # Lower Section: Recent Sessions Table
    draw_card(draw, [150, 420, 1770, 950], title="Recent Analysis History")
    
    headers = ["Analysis Session Name", "Target Job Posting", "Resumes Processed", "Average Score", "Top Match", "Status"]
    xs = [180, 560, 960, 1200, 1400, 1620]
    for h, x in zip(headers, xs):
        draw.text((x, 500), h, font=font_bold, fill=ACCENT_BLUE)
    draw.line([180, 540, 1740, 540], fill=CARD_BORDER, width=2)
    
    rows = [
        ("Demonstration Analysis", "Senior Full Stack Developer", "14 Resumes", "55.7%", "Alex Johnson", "Complete"),
        ("ML Engineering Screening", "Machine Learning Engineer", "12 Resumes", "62.4%", "Jordan Smith", "Complete"),
        ("Analytics Benchmark", "Data Scientist", "12 Resumes", "58.1%", "Taylor Brown", "Complete"),
    ]
    
    y = 570
    for r in rows:
        draw.rounded_rectangle([170, y - 10, 1750, y + 50], radius=8, fill=(15, 23, 42))
        for col, x in zip(r, xs):
            col_color = ACCENT_EMERALD if col == "Complete" else (WHITE if "%" not in col else ACCENT_AMBER)
            draw.text((x, y), col, font=font_body, fill=col_color)
        y += 80
        
    return img

def create_scene_3():
    """Scene 3: Job Description & Skill Extraction (30s)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), color=DARK_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, 3, 7, "Job Input & NLP Skill Extraction")
    
    draw.text((150, 115), "Module 2: Job Description & Automated Skill Extraction", font=font_heading, fill=WHITE)
    draw.text((150, 160), "NLP dictionary matching parses technical competencies and required experience automatically", font=font_subtitle, fill=MUTED_TEXT)
    
    # Left Box: JD Input
    draw_card(draw, [150, 220, 930, 950], title="Target Job: Senior Full Stack Developer")
    draw.text((180, 290), "Required Experience: 5+ Years  |  Format: Text/Upload", font=font_subtitle, fill=ACCENT_BLUE)
    
    sample_jd = [
        "Responsibilities & Requirements:",
        "• Design and develop scalable web applications using Python and React",
        "• Build and maintain RESTful APIs with FastAPI or Django",
        "• Deploy microservices on AWS with Docker and Kubernetes",
        "• Work with PostgreSQL, MongoDB, and Redis caching",
        "• Implement CI/CD pipelines via GitHub Actions",
        "• Strong background in TypeScript, Git, SQL, and agile practices"
    ]
    y = 350
    for line in sample_jd:
        draw.text((180, y), line, font=font_body, fill=LIGHT_TEXT)
        y += 44
        
    # Right Box: Extracted Skills
    draw_card(draw, [970, 220, 1770, 950], title="Extracted Technical Taxonomy (23 Detected)")
    draw.text((1000, 290), "Identified automatically via regex word-boundary taxonomy matching", font=font_subtitle, fill=ACCENT_EMERALD)
    
    skills = [
        "Python", "React", "FastAPI", "Django", "TypeScript", "JavaScript",
        "Docker", "Kubernetes", "AWS", "PostgreSQL", "MongoDB", "Redis",
        "CI/CD", "GitHub Actions", "Git", "REST APIs", "SQL", "HTML",
        "CSS", "Tailwind CSS", "Node.js", "Microservices", "TDD"
    ]
    
    sx, sy = 1000, 360
    for s in skills:
        w = len(s) * 14 + 30
        if sx + w > 1730:
            sx = 1000
            sy += 60
        draw.rounded_rectangle([sx, sy, sx + w, sy + 44], radius=8, fill=(30, 58, 138), outline=ACCENT_BLUE, width=1)
        draw.text((sx + 15, sy + 10), s, font=font_body, fill=WHITE)
        sx += w + 16
        
    draw.rounded_rectangle([1000, 720, 1730, 890], radius=12, fill=(15, 23, 42), outline=CARD_BORDER, width=2)
    draw.text((1030, 750), "AI Extraction Advantage:", font=font_bold, fill=ACCENT_AMBER)
    draw.text((1030, 790), "• Canonical normalization (e.g. 'react.js' -> 'react', 'k8s' -> 'kubernetes')", font=font_body, fill=LIGHT_TEXT)
    draw.text((1030, 830), "• Eliminates manual recruiter keyword tagging and typos", font=font_body, fill=LIGHT_TEXT)
    
    return img

def create_scene_4():
    """Scene 4: Bulk Resume Upload & Document Parsing (30s)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), color=DARK_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, 4, 7, "Bulk Resume Upload")
    
    draw.text((150, 115), "Module 3: Bulk Resume Upload & Dual Format Parsing", font=font_heading, fill=WHITE)
    draw.text((150, 160), "PyMuPDF (PDF) & python-docx (DOCX) extract full text, contact info, and structural sections", font=font_subtitle, fill=MUTED_TEXT)
    
    # Left: Drag and drop illustration
    draw_card(draw, [150, 220, 930, 950], title="Multi-File Drag-and-Drop Dropzone")
    draw.rounded_rectangle([200, 300, 880, 550], radius=16, fill=(15, 23, 42), outline=ACCENT_BLUE, width=2)
    draw.text((360, 380), "[ Upload PDF & DOCX Resumes ]", font=font_heading, fill=ACCENT_BLUE)
    draw.text((320, 450), "Supports batch upload of 10+ resumes in a single run", font=font_body, fill=MUTED_TEXT)
    
    draw.text((200, 590), "Extracted Entities per Candidate:", font=font_bold, fill=WHITE)
    items = [
        "1. Candidate Name (Header heuristic)",
        "2. Email & Phone (Standardized RegEx)",
        "3. Estimated Years of Experience (Date range analysis)",
        "4. Work Experience & Education Sections",
        "5. Key Projects & Certifications",
        "6. Technical Skills Matrix"
    ]
    y = 640
    for it in items:
        draw.text((200, y), it, font=font_body, fill=LIGHT_TEXT)
        y += 42
        
    # Right: Uploaded Candidates List
    draw_card(draw, [970, 220, 1770, 950], title="Parsed Batch Results (14 Candidates)")
    cands = [
        ("Alex Johnson", "alex.johnson@email.com", "7.0 Yrs Exp", "M.S. Computer Science", "Ready"),
        ("Blake Thomas", "blake.thomas@email.com", "9.0 Yrs Exp", "M.S. Computer Science", "Ready"),
        ("Sam Anderson", "sam.anderson@email.com", "8.0 Yrs Exp", "B.S. Computer Science", "Ready"),
        ("Morgan Lee", "morgan.lee@email.com", "3.0 Yrs Exp", "B.S. Computer Science", "Ready"),
        ("Riley Davis", "riley.davis@email.com", "6.0 Yrs Exp", "B.S. Computer Science", "Ready"),
        ("Drew Martinez", "drew.martinez@email.com", "10.0 Yrs Exp", "M.S. Information Systems", "Ready"),
        ("Jordan Smith", "jordan.smith@email.com", "5.0 Yrs Exp", "PhD Artificial Intelligence", "Ready"),
    ]
    y = 300
    for name, email, exp, edu, st in cands:
        draw.rounded_rectangle([1000, y, 1740, y + 68], radius=8, fill=(15, 23, 42), outline=CARD_BORDER, width=1)
        draw.text((1020, y + 18), name, font=font_bold, fill=WHITE)
        draw.text((1200, y + 20), exp, font=font_small, fill=ACCENT_BLUE)
        draw.text((1340, y + 20), edu, font=font_small, fill=MUTED_TEXT)
        draw.rounded_rectangle([1620, y + 14, 1715, y + 54], radius=6, fill=(6, 78, 59))
        draw.text((1640, y + 22), st, font=font_small, fill=(110, 231, 183))
        y += 84
        
    return img

def create_scene_5():
    """Scene 5: Candidate Ranking Table (35s)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), color=DARK_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, 5, 7, "Candidate Rankings")
    
    draw.text((150, 115), "Module 5: Ranked Candidate Leaderboard", font=font_heading, fill=WHITE)
    draw.text((150, 160), "Explainable sorting based on 40/35/15/10 weighted formula • Highest to lowest match", font=font_subtitle, fill=MUTED_TEXT)
    
    draw_card(draw, [150, 220, 1770, 950])
    
    cols = ["Rank", "Candidate Name", "Exp", "Overall Match", "Matched Skills", "Missing Skills", "Recommendation"]
    xs = [190, 290, 640, 770, 1020, 1310, 1550]
    for c, x in zip(cols, xs):
        draw.text((x, 260), c, font=font_bold, fill=ACCENT_BLUE)
    draw.line([180, 305, 1740, 305], fill=CARD_BORDER, width=2)
    
    ranked = [
        ("#1", "Alex Johnson", "7.0 yrs", "85.2%", "Python, React, FastAPI, Docker, AWS...", "HTML", "Excellent Match", ACCENT_EMERALD),
        ("#2", "Blake Thomas", "9.0 yrs", "81.4%", "FastAPI, Django, PostgreSQL, Redis...", "React", "Good Match", ACCENT_BLUE),
        ("#3", "Sam Anderson", "8.0 yrs", "78.9%", "React, Node.js, Python, MongoDB...", "FastAPI", "Good Match", ACCENT_BLUE),
        ("#4", "Morgan Lee", "3.0 yrs", "72.3%", "Node.js, Express, Django, PostgreSQL...", "Kubernetes", "Good Match", ACCENT_BLUE),
        ("#5", "Riley Davis", "6.0 yrs", "68.5%", "Docker, Kubernetes, AWS, CI/CD...", "React, FastAPI", "Moderate Match", ACCENT_AMBER),
        ("#6", "Casey Williams", "1.0 yrs", "46.2%", "React, Tailwind CSS, HTML, CSS...", "Python, FastAPI, AWS", "Low Match", ACCENT_ROSE),
    ]
    
    y = 330
    for r, name, exp, score, matched, missing, rec, rec_col in ranked:
        bg_col = (20, 30, 55) if r == "#1" else (15, 23, 42)
        draw.rounded_rectangle([170, y, 1750, y + 74], radius=10, fill=bg_col, outline=ACCENT_INDIGO if r == "#1" else CARD_BORDER, width=2 if r == "#1" else 1)
        
        draw.text((xs[0], y + 22), r, font=font_bold, fill=ACCENT_AMBER if r == "#1" else WHITE)
        draw.text((xs[1], y + 22), name, font=font_bold, fill=WHITE)
        draw.text((xs[2], y + 22), exp, font=font_body, fill=LIGHT_TEXT)
        draw.text((xs[3], y + 20), score, font=font_heading, fill=rec_col)
        draw.text((xs[4], y + 24), matched[:30] + "...", font=font_small, fill=ACCENT_EMERALD)
        draw.text((xs[5], y + 24), missing[:22], font=font_small, fill=ACCENT_ROSE)
        
        # Badge
        draw.rounded_rectangle([xs[6], y + 16, xs[6] + 175, y + 56], radius=6, fill=(15, 23, 42), outline=rec_col, width=1)
        draw.text((xs[6] + 16, y + 22), rec, font=font_small, fill=rec_col)
        y += 92
        
    return img

def create_scene_6():
    """Scene 6: Candidate-Level Deep Dive & Radar Chart (35s)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), color=DARK_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, 6, 7, "Candidate Deep Dive")
    
    draw.text((150, 115), "Module 6: Candidate Analysis & Explainable AI Breakdown", font=font_heading, fill=WHITE)
    draw.text((150, 160), "In-depth score components for Alex Johnson (Rank #1 • 85.2% Overall Match)", font=font_subtitle, fill=MUTED_TEXT)
    
    # Left Card: Profile & Overall Donut
    draw_card(draw, [150, 220, 680, 950], title="Alex Johnson Profile")
    draw.text((180, 290), "Email: alex.johnson@email.com", font=font_body, fill=LIGHT_TEXT)
    draw.text((180, 330), "Phone: +1-555-0101", font=font_body, fill=LIGHT_TEXT)
    draw.text((180, 370), "Experience: 7.0 Years Estimated", font=font_body, fill=LIGHT_TEXT)
    draw.text((180, 410), "Education: M.S. Computer Science", font=font_body, fill=LIGHT_TEXT)
    
    # Donut simulation
    draw.rounded_rectangle([250, 480, 580, 780], radius=16, fill=(15, 23, 42), outline=ACCENT_EMERALD, width=3)
    draw.text((340, 580), "85.2%", font=ImageFont.truetype(FONT_BOLD_PATH, 68), fill=ACCENT_EMERALD)
    draw.text((320, 670), "EXCELLENT MATCH", font=font_bold, fill=WHITE)
    draw.text((310, 710), "Composite Weighted Score", font=font_small, fill=MUTED_TEXT)
    
    draw.text((180, 830), "Recommendation: Strong Candidate for Interview", font=font_body, fill=ACCENT_AMBER)
    
    # Right Card: 4-Component Score Bars & Radar
    draw_card(draw, [720, 220, 1770, 950], title="Explainable Component Breakdown")
    
    components = [
        ("Semantic Similarity (all-MiniLM-L6-v2)", 66.9, "40% Weight", ACCENT_INDIGO),
        ("Technical Skill Match (22 of 23 matched)", 95.7, "35% Weight", ACCENT_BLUE),
        ("Relevant Experience (7 yrs vs 5 yrs req)", 100.0, "15% Weight", ACCENT_EMERALD),
        ("Education Qualification (M.S. Degree)", 100.0, "10% Weight", ACCENT_AMBER),
    ]
    
    y = 300
    for name, val, wt, col in components:
        draw.text((760, y), name, font=font_bold, fill=WHITE)
        draw.text((1450, y), f"{val:.1f}%  ({wt})", font=font_bold, fill=col)
        
        # Bar background
        draw.rounded_rectangle([760, y + 36, 1710, y + 60], radius=6, fill=(15, 23, 42))
        fill_w = int(760 + (val / 100.0) * 950)
        draw.rounded_rectangle([760, y + 36, fill_w, y + 60], radius=6, fill=col)
        y += 90
        
    # Skills Breakdown Boxes
    draw.rounded_rectangle([760, 680, 1210, 900], radius=10, fill=(15, 23, 42), outline=ACCENT_EMERALD, width=1)
    draw.text((780, 705), "Matched Skills (22)", font=font_bold, fill=ACCENT_EMERALD)
    draw.text((780, 750), "Python, React, FastAPI, Django, Docker,\nKubernetes, AWS, PostgreSQL, Redis,\nCI/CD, GitHub Actions, Git, TypeScript...", font=font_small, fill=LIGHT_TEXT)
    
    draw.rounded_rectangle([1250, 680, 1710, 900], radius=10, fill=(15, 23, 42), outline=ACCENT_ROSE, width=1)
    draw.text((1270, 705), "Missing Skill Gap (1)", font=font_bold, fill=ACCENT_ROSE)
    draw.text((1270, 750), "• HTML (Explicit mention missing\n  despite full stack experience)", font=font_small, fill=LIGHT_TEXT)
    
    return img

def create_scene_7():
    """Scene 7: Export Reports & Conclusion (20s)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), color=DARK_BG)
    draw = ImageDraw.Draw(img)
    draw_top_nav(draw, 7, 7, "Exports & Submission")
    
    draw.text((150, 115), "Module 8: Automated Reporting & Summary", font=font_heading, fill=WHITE)
    draw.text((150, 160), "One-click export capabilities for recruiters and hiring managers", font=font_subtitle, fill=MUTED_TEXT)
    
    draw_card(draw, [150, 220, 930, 850], title="Export Capabilities")
    
    draw.rounded_rectangle([190, 300, 890, 480], radius=12, fill=(15, 23, 42), outline=ACCENT_BLUE, width=1)
    draw.text((220, 330), "CSV Ranking Spreadsheet", font=font_heading, fill=ACCENT_BLUE)
    draw.text((220, 385), "• Full candidate rankings, contact details, individual\n  component scores, and matched skill lists.", font=font_body, fill=LIGHT_TEXT)
    
    draw.rounded_rectangle([190, 520, 890, 700], radius=12, fill=(15, 23, 42), outline=ACCENT_INDIGO, width=1)
    draw.text((220, 550), "ReportLab PDF Dossier", font=font_heading, fill=ACCENT_INDIGO)
    draw.text((220, 605), "• Professional printable PDF for each candidate\n  featuring score breakdown tables and skill gap analysis.", font=font_body, fill=LIGHT_TEXT)
    
    draw_card(draw, [970, 220, 1770, 850], title="Project Summary")
    draw.text((1000, 300), "ResumeAI – Key Technical Accomplishments", font=font_bold, fill=ACCENT_AMBER)
    
    achievements = [
        "1. Complete full-stack React 18 + FastAPI + SQLite implementation",
        "2. Real NLP semantic embeddings using all-MiniLM-L6-v2",
        "3. Dual-engine PDF & DOCX resume parser (PyMuPDF & python-docx)",
        "4. Fully explainable 40/35/15/10 mathematical scoring formula",
        "5. Interactive charts (Radar, Score progress bars, KPI cards)",
        "6. Tested and verified on 12+ diverse synthetic candidate profiles"
    ]
    y = 370
    for a in achievements:
        draw.text((1000, y), a, font=font_body, fill=WHITE)
        y += 54
        
    draw.text((1000, 740), "Thank you for reviewing ResumeAI!", font=font_heading, fill=ACCENT_EMERALD)
    
    return img

def render_all_scenes():
    print("Generating scene still images...")
    scenes = [
        ("scene1.png", create_scene_1(), 15), # 15 seconds
        ("scene2.png", create_scene_2(), 25), # 25 seconds
        ("scene3.png", create_scene_3(), 30), # 30 seconds
        ("scene4.png", create_scene_4(), 30), # 30 seconds
        ("scene5.png", create_scene_5(), 35), # 35 seconds
        ("scene6.png", create_scene_6(), 35), # 35 seconds
        ("scene7.png", create_scene_7(), 20), # 20 seconds
    ]
    
    # Save base images and create concat file for ffmpeg
    concat_txt_path = VIDEO_DIR / "concat_list.txt"
    with open(concat_txt_path, "w", encoding="utf-8") as f:
        for fname, img, duration in scenes:
            p = FRAMES_DIR / fname
            img.save(p)
            f.write(f"file '{p.as_posix()}'\n")
            f.write(f"duration {duration}\n")
        # Repeat last file for ffmpeg concat requirement
        f.write(f"file '{(FRAMES_DIR / scenes[-1][0]).as_posix()}'\n")
        
    print(f"Created 7 high-resolution frames in {FRAMES_DIR}")
    
    # Compile with FFmpeg into MP4
    print("Encoding 1080p MP4 video with FFmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt_path),
        "-vf", "fps=24,format=yuv420p",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "22",
        str(OUTPUT_MP4)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"\nSUCCESS! Demo video created: {OUTPUT_MP4}")
        print(f"File size: {OUTPUT_MP4.stat().st_size / (1024*1024):.2f} MB")
    else:
        print("FFmpeg Error:", res.stderr)

if __name__ == "__main__":
    render_all_scenes()
