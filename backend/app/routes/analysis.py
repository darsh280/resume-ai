"""
Analysis History Router
=======================
Endpoint to retrieve past analysis sessions.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.analysis import Analysis
from ..models.job import JobDescription

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.get("/history", summary="Get analysis history")
def get_history(db: Session = Depends(get_db)):
    """Return all past analysis sessions, newest first."""
    analyses = (
        db.query(Analysis)
        .order_by(Analysis.created_at.desc())
        .all()
    )
    result = []
    for a in analyses:
        job = db.query(JobDescription).filter(JobDescription.id == a.job_id).first()
        result.append({
            "id": a.id,
            "job_id": a.job_id,
            "job_title": job.title if job else "Unknown",
            "name": a.name,
            "total_resumes": a.total_resumes,
            "avg_score": a.avg_score,
            "top_candidate": a.top_candidate,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        })
    return result
