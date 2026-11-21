# ResumeAI – Backend Service

FastAPI-powered intelligent resume matching and candidate ranking engine.

## Quick Start

### 1. Requirements
Ensure Python 3.10+ is installed.

```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
uvicorn app.main:app --reload --port 8000
```

- API Base URL: `http://localhost:8000`
- Swagger UI Documentation: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Features & Services
- **`app/services/resume_parser.py`**: Multi-format resume parsing (PDF via PyMuPDF, DOCX via python-docx).
- **`app/services/skill_extractor.py`**: Curated dictionary and regex-based multi-word skill extraction.
- **`app/services/semantic_matcher.py`**: SentenceTransformers `all-MiniLM-L6-v2` embedding generation and cosine similarity.
- **`app/services/experience_analyzer.py`**: Experience extraction and ratio calculation.
- **`app/services/scoring_engine.py`**: 40/35/15/10 explainable scoring model.
- **`app/services/report_generator.py`**: CSV and ReportLab PDF report generation.
