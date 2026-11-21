# ResumeAI – AI-Based Resume Matching & Candidate Ranking System

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-61DAFB.svg?logo=react)](https://react.dev)
[![TailwindCSS](https://img.shields.io/badge/Styles-Tailwind%20CSS-38B2AC.svg?logo=tailwind-css)](https://tailwindcss.com)
[![SentenceTransformers](https://img.shields.io/badge/NLP-all--MiniLM--L6--v2-orange.svg)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)

**ResumeAI** is a production-grade, full-stack intelligent recruitment platform that matches resumes to job descriptions using actual Natural Language Processing (NLP), semantic embeddings (`all-MiniLM-L6-v2`), comprehensive technical skill extraction, and explainable multi-component candidate scoring.

Unlike basic keyword search tools or prototype mockups, **every single score in ResumeAI is computed in real time from document text**.

---

## 📑 Table of Contents
1. [Application Architecture](#application-architecture)
2. [Key Features by Module](#key-features-by-module)
3. [Technology Stack](#technology-stack)
4. [Explainable AI Scoring Methodology](#explainable-ai-scoring-methodology)
5. [Project Structure](#project-structure)
6. [Prerequisites & Installation](#prerequisites--installation)
   - [Backend Setup](#backend-setup)
   - [Frontend Setup](#frontend-setup)
7. [Running the Application](#running-the-application)
8. [Sample Data & Automated Testing](#sample-data--automated-testing)
9. [REST API Documentation](#rest-api-documentation)
10. [Limitations & Future Roadmap](#limitations--future-roadmap)

---

## 1. Application Architecture

```
   ┌─────────────────────────────────────────────────────────────┐
   │             React 18 + Vite + Tailwind CSS UI               │
   │  Dashboard | Job Input | Bulk Upload | Rankings | Reports   │
   └──────────────────────────────┬──────────────────────────────┘
                                  │ HTTP REST / Axios
                                  ▼
   ┌─────────────────────────────────────────────────────────────┐
   │                    FastAPI Backend Router                   │
   │      /api/jobs  •  /api/resumes  •  /api/matching/analyze    │
   │      /api/candidates  •  /api/reports  •  /api/dashboard    │
   └───────┬──────────────────────┬──────────────────────┬───────┘
           │                      │                      │
           ▼                      ▼                      ▼
┌────────────────────┐ ┌────────────────────┐ ┌──────────────────┐
│   Resume Parser    │ │  Skill Extractor   │ │ Semantic Matcher │
│ PyMuPDF (PDF) &    │ │ Curated Taxonomy + │ │ Sentence-        │
│ python-docx (DOCX) │ │ NLP multi-word     │ │ Transformers     │
│ Sections & text    │ │ boundary matching  │ │ all-MiniLM-L6-v2 │
└──────────┬─────────┘ └──────────┬─────────┘ └────────┬─────────┘
           │                      │                    │
           └──────────────────────┼────────────────────┘
                                  ▼
                      ┌──────────────────────┐
                      │    Scoring Engine    │
                      │  Semantic:       40% │
                      │  Skills:         35% │
                      │  Experience:     15% │
                      │  Education:      10% │
                      └──────────┬───────────┘
                                 │
           ┌─────────────────────┴────────────────────┐
           ▼                                          ▼
┌────────────────────┐                     ┌────────────────────┐
│ SQLite / SQLAlchemy│                     │  Report Generator  │
│ Persistent Storage │                     │ CSV & ReportLab PDF│
└────────────────────┘                     └────────────────────┘
```

---

## 2. Key Features by Module

### Module 1: Recruiter Dashboard
- High-level KPIs: Total Resumes Uploaded, Candidates Ranked, Average Match Score, Top Matching Candidate.
- Recent analysis history with 1-click drill-down.
- Quick navigation shortcuts for new analyses and resume uploads.

### Module 2: Job Description Input
- Paste raw JD text or upload `.txt` files directly.
- Define job title and minimum experience expectations.
- Automatic NLP skill extraction preview before initiating analysis.

### Module 3: Bulk Resume Upload
- Drag-and-drop file dropzone supporting **PDF** and **DOCX** formats.
- Upload 10+ resumes in a single batch with progress tracking.
- Automated extraction of Candidate Name, Email, Phone, Years of Experience, Education, Projects, and Certifications.
- Duplicate detection by filename and validation error isolation.

### Module 4: AI Resume Matching Engine
- **Text Preprocessing**: Normalization, whitespace cleaning, section boundary parsing.
- **Semantic Similarity (40%)**: Dense sentence embeddings using `all-MiniLM-L6-v2` and scikit-learn cosine similarity.
- **Technical Skill Matching (35%)**: Evaluates overlap against a curated 100+ skill taxonomy spanning programming languages, backend, frontend, cloud, databases, and AI/ML.
- **Relevant Experience (15%)**: Proportional ratio comparing candidate experience against required years.
- **Education Level (10%)**: Level-based normalization (PhD, Master's, Bachelor's, Associate).

### Module 5: Candidate Ranking Dashboard
- Sortable, searchable table ranking candidates from highest to lowest composite score.
- Categorical recommendation badges:
  - **85–100%**: Excellent Match
  - **70–84%**: Good Match
  - **50–69%**: Moderate Match
  - **Below 50%**: Low Match
- Filter by target job or search by candidate name / skill.

### Module 6: Candidate-Level Analysis & Visual Breakdown
- Radar chart comparing multi-axis scores (Semantic, Skills, Experience, Education).
- Breakdown progress bars with individual component weights.
- Skill classification badges: **Matched Skills**, **Missing Required Skills**, and **Additional Skills**.
- Human-readable AI scoring rationale explaining why the candidate received their specific score.

### Module 7: Database & History
- Persistent SQLite storage using SQLAlchemy ORM.
- Stores full resume text, parsed entities, job descriptions, analysis snapshots, and ranking results.

### Module 8: Export Results
- 1-click export of complete candidate rankings as **CSV**.
- Individual candidate analysis report export as high-resolution **PDF** via ReportLab.

---

## 3. Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend UI** | React 18, Vite, Tailwind CSS, React Router v6, Lucide React Icons |
| **Data Visualization** | Recharts (Radar charts, score bars) |
| **HTTP Client** | Axios |
| **Backend Framework** | Python 3.11+, FastAPI, Uvicorn, Pydantic v2 |
| **AI / NLP Models** | Sentence-Transformers (`all-MiniLM-L6-v2`), PyTorch, scikit-learn |
| **Resume Parsing** | PyMuPDF (`fitz`), python-docx |
| **Database & ORM** | SQLite, SQLAlchemy 2.0 |
| **Report Generation** | ReportLab (PDF), Python `csv` module |

---

## 4. Explainable AI Scoring Methodology

Every candidate receives a normalized score between **0.0% and 100.0%** based on the following transparent formula:

$$\text{Final Score} = (\text{Semantic Similarity} \times 0.40) + (\text{Skill Match} \times 0.35) + (\text{Experience Match} \times 0.15) + (\text{Education Match} \times 0.10)$$

### Component Details

1. **Semantic Similarity (40% Weight)**
   - Model: `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense vectors).
   - Computes cosine similarity between JD text and resume body:
     $$\text{Cosine Similarity}(u, v) = \frac{u \cdot v}{\|u\| \|v\|}$$
   - Normalized directly to 0–100%.

2. **Technical Skill Match (35% Weight)**
   - Identifies candidate skills ($S_{cand}$) and job required skills ($S_{req}$) from a taxonomy of 100+ technologies.
   $$\text{Skill Match \%} = \frac{|S_{cand} \cap S_{req}|}{|S_{req}|} \times 100$$
   - Also tracks **Missing Skills** ($S_{req} \setminus S_{cand}$) and **Additional Skills** ($S_{cand} \setminus S_{req}$).

3. **Relevant Experience Match (15% Weight)**
   - If required experience $\le 0$, score is 100%.
   - If candidate experience $\ge$ required experience, score is 100%.
   - Otherwise:
     $$\text{Experience Score} = \min\left(100, \frac{\text{Years}_{cand}}{\text{Years}_{req}} \times 100\right)$$

4. **Education Qualification (10% Weight)**
   - Degrees are mapped to standard academic tiers: PhD (4), Master's (3), Bachelor's (2), Associate/Diploma (1).
   - If candidate degree level $\ge$ required degree level: 100%.
   - If JD specifies no degree requirement: 100%.

---

## 5. Project Structure

```
resume-ai/
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI entry point & CORS
│   │   ├── database.py                 # SQLAlchemy engine & session factory
│   │   ├── models/                     # Database models
│   │   │   ├── job.py                  # JobDescription model
│   │   │   ├── resume.py               # Resume metadata & extracted sections
│   │   │   ├── candidate.py            # CandidateRanking model
│   │   │   └── analysis.py             # Analysis history session model
│   │   ├── schemas/                    # Pydantic validation schemas
│   │   │   ├── job.py
│   │   │   ├── resume.py
│   │   │   ├── candidate.py
│   │   │   └── analysis.py
│   │   ├── routes/                     # REST API endpoints
│   │   │   ├── jobs.py                 # /api/jobs
│   │   │   ├── resumes.py              # /api/resumes
│   │   │   ├── matching.py             # /api/matching/analyze
│   │   │   ├── candidates.py           # /api/candidates
│   │   │   ├── reports.py              # /api/reports (CSV & PDF)
│   │   │   └── analysis.py             # /api/analysis/history
│   │   ├── services/                   # Core AI/NLP & business logic
│   │   │   ├── resume_parser.py        # PDF & DOCX parser
│   │   │   ├── skill_extractor.py      # Technical taxonomy & NLP matching
│   │   │   ├── semantic_matcher.py     # SentenceTransformers cosine similarity
│   │   │   ├── experience_analyzer.py  # Years & duration extractor
│   │   │   ├── scoring_engine.py       # 40/35/15/10 explainable scoring
│   │   │   └── report_generator.py     # CSV & ReportLab PDF generator
│   │   └── utils/
│   │       ├── file_utils.py           # Upload storage & file validation
│   │       └── text_utils.py           # Text cleaning & truncation
│   ├── uploads/                        # Stored uploaded resumes
│   ├── resume_ai.db                    # SQLite database file
│   └── requirements.txt                # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/                 # Reusable UI components
│   │   │   ├── Layout.jsx              # Main app wrapper with sidebar
│   │   │   ├── Sidebar.jsx             # Dark navy navigation
│   │   │   ├── StatCard.jsx            # KPI metric cards
│   │   │   ├── ScoreBar.jsx            # Animated score progress bars
│   │   │   ├── SkillBadge.jsx          # Matched / missing / additional tags
│   │   │   ├── FileDropzone.jsx        # Drag-and-drop multi-file uploader
│   │   │   ├── LoadingSpinner.jsx      # Loading state indicators
│   │   │   ├── EmptyState.jsx          # Empty state cards
│   │   │   └── Notification.jsx        # Alert banner toasts
│   │   ├── pages/                      # Application pages
│   │   │   ├── Dashboard.jsx           # Recruiter overview
│   │   │   ├── NewJobAnalysis.jsx      # Step-by-step job & matching flow
│   │   │   ├── ResumeUpload.jsx        # Bulk file upload page
│   │   │   ├── CandidateRankings.jsx   # Sortable rankings table
│   │   │   ├── CandidateDetails.jsx    # Candidate breakdown & radar chart
│   │   │   ├── AnalysisHistory.jsx     # Analysis session log
│   │   │   └── Settings.jsx            # System parameters & AI weights
│   │   ├── services/
│   │   │   └── api.js                  # Axios client & endpoint wrappers
│   │   ├── App.jsx                     # React Router routes
│   │   ├── main.jsx                    # React root render
│   │   └── index.css                   # Tailwind base & custom layers
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── sample_data/
│   ├── resumes/                        # 12 synthetic DOCX resumes
│   ├── job_descriptions/               # 3 realistic sample JD files
│   └── generate_resumes.py             # Synthetic resume generator script
│
├── .gitignore
└── README.md
```

---

## 6. Prerequisites & Installation

Ensure you have installed:
- **Python 3.10+** (Tested on Python 3.11, 3.12, and 3.13)
- **Node.js 18+** and **npm**

### Backend Setup

```bash
# 1. Navigate to the backend directory
cd backend

# 2. (Optional but recommended) Create and activate a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS / Linux:
# source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt
```

### Frontend Setup

```bash
# 1. Navigate to the frontend directory
cd ../frontend

# 2. Install Node dependencies
npm install
```

---

## 7. Running the Application

### 1. Start the FastAPI Backend
From the `backend` folder:
```bash
uvicorn app.main:app --reload --port 8000
```
- API will be accessible at: `http://localhost:8000`
- Interactive Swagger documentation: `http://localhost:8000/docs`

### 2. Start the React Frontend
In a new terminal, from the `frontend` folder:
```bash
npm run dev
```
- Web Application will be accessible at: `http://localhost:5173`

---

## 8. Sample Data & Automated Testing

The project includes **12 synthetic resumes** with distinct skills, years of experience, and degrees:

| Candidate | Target Specialty | Experience | Education | Key Skills |
|---|---|---|---|---|
| **Alex Johnson** | Senior Full Stack | 7 years | M.S. CS | Python, React, FastAPI, AWS, Docker |
| **Jordan Smith** | Machine Learning Engineer | 5 years | PhD AI | PyTorch, TensorFlow, HuggingFace, BERT |
| **Morgan Lee** | Backend Developer | 3 years | B.S. CS | Node.js, Express, Django, PostgreSQL |
| **Casey Williams** | Junior Frontend Developer | 1 year | B.S. IT | React, Vue, HTML, CSS, Tailwind |
| **Riley Davis** | DevOps Engineer | 6 years | B.S. CS | Docker, Kubernetes, Terraform, AWS, CI/CD |
| **Taylor Brown** | Data Scientist | 4 years | M.S. Data Science | Python, scikit-learn, XGBoost, Tableau, SQL |
| **Quinn Miller** | Mobile App Developer | 3 years | B.S. CS | Flutter, React Native, Swift, Firebase |
| **Sam Anderson** | Lead Full Stack Developer | 8 years | B.S. CS | React, Node.js, Python, MongoDB, Redis |
| **Jamie Wilson** | Frontend Developer | 2 years | B.S. Web Dev | React, TypeScript, Next.js, Tailwind CSS |
| **Drew Martinez** | Cloud Solutions Architect | 10 years | M.S. IS | AWS, Azure, GCP, Terraform, Kubernetes |
| **Avery Taylor** | Junior Data Analyst | 1.5 years | B.S. Statistics | Python, SQL, Excel, Tableau, pandas |
| **Blake Thomas** | Senior Backend Engineer | 9 years | M.S. CS | Python, FastAPI, Django, PostgreSQL, Redis |

To regenerate these resumes at any time:
```bash
cd sample_data
python generate_resumes.py
```

### Quick Walkthrough to Test in UI:
1. Open `http://localhost:5173/upload`.
2. Select or drag all 12 resumes from `sample_data/resumes/`.
3. Click **Upload & Parse Resumes** (all 12 will parse with metadata and skills).
4. Navigate to **New Job Analysis**.
5. Title: `Senior Full Stack Developer`.
6. Click **Upload .txt File** and pick `sample_data/job_descriptions/senior_full_stack_developer.txt`.
7. Click **Save Job & Auto-Extract Technical Skills**.
8. Click **Run AI Matching (All Resumes)**.
9. Review the ranked candidate table, click any candidate for the radar chart, and export as CSV/PDF.

---

## 9. REST API Documentation

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API status and root greeting |
| `GET` | `/api/dashboard/stats` | Recruiter dashboard counts, average scores, and top candidate |
| `POST` | `/api/jobs` | Create a job description and extract skills via NLP |
| `GET` | `/api/jobs` | List all existing job descriptions |
| `GET` | `/api/jobs/{id}` | Retrieve details of a specific job description |
| `POST` | `/api/jobs/upload-jd` | Upload a `.txt` job description file |
| `POST` | `/api/resumes/upload` | Bulk upload multiple PDF/DOCX resumes (up to 20 files) |
| `GET` | `/api/resumes` | List all parsed resumes in the database |
| `POST` | `/api/matching/analyze` | Run semantic & skill matching for a job against resumes |
| `GET` | `/api/candidates` | Retrieve candidate rankings (supports `job_id` and `analysis_id` query params) |
| `GET` | `/api/candidates/{id}` | Get candidate score breakdown, skills, and parsed sections |
| `GET` | `/api/analysis/history` | Retrieve previous analysis sessions |
| `GET` | `/api/reports/csv` | Download candidate rankings as a CSV file |
| `GET` | `/api/reports/pdf/{id}` | Download a formatted PDF report for an individual candidate |

### Example: Run Analysis via cURL
```bash
curl -X POST "http://localhost:8000/api/matching/analyze" \
     -H "Content-Type: application/json" \
     -d '{"job_id": 1, "resume_ids": []}'
```

---

## 10. Limitations & Future Roadmap

- **Prototype Screening Disclaimer**: ResumeAI is intended as an automated screening aid. Final interview and hiring decisions should always involve comprehensive human review.
- **OCR Support**: Current parser processes digital text PDF documents. Scanned image-only PDFs can be supported in future versions using Tesseract OCR.
- **Customizable Weights**: Future releases will allow recruiters to adjust scoring weight sliders directly from the UI per requisition.

---

## License
MIT License. Developed for technical assessment & educational demonstration.
