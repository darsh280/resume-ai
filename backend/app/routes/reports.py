"""
Reports Router
==============
Export candidate data as CSV or PDF.
"""

import json

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.candidate import CandidateRanking
from ..models.resume import Resume
from ..services.report_generator import ReportGenerator

router = APIRouter(prefix="/api/reports", tags=["reports"])

_report_gen = ReportGenerator()


@router.get("/csv", summary="Export candidate ranking as CSV")
def export_csv(
    job_id: int = Query(None),
    analysis_id: int = Query(None),
    db: Session = Depends(get_db),
):
    """Download all candidates for a job/analysis as a CSV file."""
    query = db.query(CandidateRanking)
    if job_id:
        query = query.filter(CandidateRanking.job_id == job_id)
    if analysis_id:
        query = query.filter(CandidateRanking.analysis_id == analysis_id)

    rankings = query.order_by(CandidateRanking.final_score.desc()).all()

    candidates = []
    for r in rankings:
        resume = db.query(Resume).filter(Resume.id == r.resume_id).first()
        if resume:
            candidates.append({
                "rank": r.rank,
                "candidate_name": resume.candidate_name,
                "email": resume.email,
                "phone": resume.phone,
                "years_experience": resume.years_experience,
                "final_score": r.final_score,
                "semantic_score": r.semantic_score,
                "skill_score": r.skill_score,
                "experience_score": r.experience_score,
                "education_score": r.education_score,
                "recommendation": r.recommendation,
                "matched_skills": json.loads(r.matched_skills or "[]"),
                "missing_skills": json.loads(r.missing_skills or "[]"),
            })

    csv_content = _report_gen.generate_csv(candidates)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=candidate_ranking.csv"
        },
    )


@router.get("/pdf/{candidate_id}", summary="Export individual candidate PDF report")
def export_pdf(candidate_id: int, db: Session = Depends(get_db)):
    """Download a detailed PDF report for a single candidate."""
    ranking = (
        db.query(CandidateRanking)
        .filter(CandidateRanking.id == candidate_id)
        .first()
    )
    if not ranking:
        raise HTTPException(status_code=404, detail="Candidate not found")

    resume = db.query(Resume).filter(Resume.id == ranking.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    candidate_data = {
        "candidate_name": resume.candidate_name,
        "email": resume.email,
        "phone": resume.phone,
        "years_experience": resume.years_experience,
        "final_score": ranking.final_score,
        "semantic_score": ranking.semantic_score,
        "skill_score": ranking.skill_score,
        "experience_score": ranking.experience_score,
        "education_score": ranking.education_score,
        "recommendation": ranking.recommendation,
        "matched_skills": json.loads(ranking.matched_skills or "[]"),
        "missing_skills": json.loads(ranking.missing_skills or "[]"),
        "additional_skills": json.loads(ranking.additional_skills or "[]"),
    }

    pdf_bytes = _report_gen.generate_pdf(candidate_data)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=candidate_{candidate_id}_report.pdf"
        },
    )
