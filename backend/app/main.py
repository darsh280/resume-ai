"""
ResumeAI – FastAPI Application Entry Point
==========================================
Starts the FastAPI server, registers all routers, and configures CORS.

Run with:
    cd backend
    uvicorn app.main:app --reload --port 8000
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from .routes import jobs, resumes, matching, candidates, reports, analysis

# ---------------------------------------------------------------------------
# Create all DB tables on startup
# ---------------------------------------------------------------------------
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# App instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title="ResumeAI API",
    description=(
        "AI-Based Resume Matching & Candidate Ranking System.\n\n"
        "Uses SentenceTransformers (all-MiniLM-L6-v2) for semantic similarity, "
        "a custom skills dictionary for skill extraction, and a weighted scoring "
        "formula to rank candidates."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS — allow React dev server
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(jobs.router)
app.include_router(resumes.router)
app.include_router(matching.router)
app.include_router(candidates.router)
app.include_router(reports.router)
app.include_router(analysis.router)


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------
@app.get("/", tags=["root"])
def root():
    return {
        "message": "ResumeAI API is running 🚀",
        "docs": "/docs",
        "version": "1.0.0",
    }


# ---------------------------------------------------------------------------
# Dashboard stats endpoint
# ---------------------------------------------------------------------------
@app.get("/api/dashboard/stats", tags=["dashboard"])
def dashboard_stats():
    """Return high-level counts for the recruiter dashboard."""
    from .models.resume import Resume
    from .models.candidate import CandidateRanking
    from .models.analysis import Analysis as AnalysisModel

    db: Session = SessionLocal()
    try:
        total_resumes = db.query(Resume).count()
        total_candidates = db.query(CandidateRanking).count()

        rankings = db.query(CandidateRanking).all()
        avg_score = (
            sum(r.final_score for r in rankings) / len(rankings)
            if rankings else 0.0
        )

        top_ranking = (
            db.query(CandidateRanking)
            .order_by(CandidateRanking.final_score.desc())
            .first()
        )
        top_candidate_name = ""
        if top_ranking:
            resume = db.query(Resume).filter(Resume.id == top_ranking.resume_id).first()
            top_candidate_name = resume.candidate_name if resume else ""

        recent = (
            db.query(AnalysisModel)
            .order_by(AnalysisModel.created_at.desc())
            .limit(5)
            .all()
        )
        recent_list = [
            {
                "id": a.id,
                "name": a.name,
                "total_resumes": a.total_resumes,
                "avg_score": a.avg_score,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in recent
        ]

        return {
            "total_resumes": total_resumes,
            "total_candidates": total_candidates,
            "avg_score": round(avg_score, 2),
            "top_candidate": top_candidate_name,
            "recent_analyses": recent_list,
        }
    finally:
        db.close()
