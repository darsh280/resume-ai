"""
Candidates Router
=================
Endpoints to retrieve ranked candidate data.
"""

import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.candidate import CandidateRanking
from ..models.resume import Resume

router = APIRouter(prefix="/api/candidates", tags=["candidates"])


def _build_candidate(ranking: CandidateRanking, resume: Resume) -> dict:
    return {
        "id": ranking.id,
        "resume_id": ranking.resume_id,
        "job_id": ranking.job_id,
        "analysis_id": ranking.analysis_id,
        "rank": ranking.rank,
        "semantic_score": ranking.semantic_score,
        "skill_score": ranking.skill_score,
        "experience_score": ranking.experience_score,
        "education_score": ranking.education_score,
        "final_score": ranking.final_score,
        "matched_skills": json.loads(ranking.matched_skills or "[]"),
        "missing_skills": json.loads(ranking.missing_skills or "[]"),
        "additional_skills": json.loads(ranking.additional_skills or "[]"),
        "recommendation": ranking.recommendation,
        "candidate_name": resume.candidate_name,
        "email": resume.email,
        "phone": resume.phone,
        "years_experience": resume.years_experience,
        "education": json.loads(resume.education or "[]"),
        "work_experience": json.loads(resume.work_experience or "[]"),
        "projects": json.loads(resume.projects or "[]"),
        "certifications": json.loads(resume.certifications or "[]"),
        "extracted_skills": json.loads(resume.extracted_skills or "[]"),
        "filename": resume.filename,
    }


@router.get("", summary="Get ranked candidates")
def get_candidates(
    job_id: int = Query(None, description="Filter by job ID"),
    analysis_id: int = Query(None, description="Filter by analysis ID"),
    db: Session = Depends(get_db),
):
    """
    Return candidates sorted by final score (descending).
    Optionally filter by job_id or analysis_id.
    """
    query = db.query(CandidateRanking)
    if job_id:
        query = query.filter(CandidateRanking.job_id == job_id)
    if analysis_id:
        query = query.filter(CandidateRanking.analysis_id == analysis_id)

    rankings = query.order_by(CandidateRanking.final_score.desc()).all()

    result = []
    for r in rankings:
        resume = db.query(Resume).filter(Resume.id == r.resume_id).first()
        if resume:
            result.append(_build_candidate(r, resume))
    return result


@router.get("/{candidate_id}", summary="Get a single candidate's details")
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """Return full profile + scores for a single candidate ranking."""
    ranking = (
        db.query(CandidateRanking)
        .filter(CandidateRanking.id == candidate_id)
        .first()
    )
    if not ranking:
        raise HTTPException(status_code=404, detail="Candidate ranking not found")

    resume = db.query(Resume).filter(Resume.id == ranking.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume record not found")

    return _build_candidate(ranking, resume)
