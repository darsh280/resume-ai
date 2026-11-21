"""
Matching Router
===============
Endpoint that runs the AI resume matching pipeline for a given job.

POST /api/matching/analyze
  - Accepts a job_id and optional list of resume_ids.
  - Scores every resume against the job description.
  - Ranks candidates by final score (highest first).
  - Persists results to the database.
  - Returns the full ranked candidate list.
"""

import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.job import JobDescription
from ..models.resume import Resume
from ..models.candidate import CandidateRanking
from ..models.analysis import Analysis
from ..services.scoring_engine import ScoringEngine

router = APIRouter(prefix="/api/matching", tags=["matching"])

_scoring_engine = ScoringEngine()


class AnalyzeRequest(BaseModel):
    job_id: int
    resume_ids: List[int] = []  # Empty list = analyze all uploaded resumes


@router.post("/analyze", summary="Run AI matching for a job")
def analyze_resumes(request: AnalyzeRequest, db: Session = Depends(get_db)):
    """
    Core AI matching pipeline:

    1. Load the job description and its extracted skills.
    2. Load the specified resumes (or all resumes if none specified).
    3. For each resume, call ScoringEngine.score_candidate() which:
        a. Computes semantic similarity via SentenceTransformers.
        b. Computes skill match % using the skills dictionary.
        c. Computes experience score.
        d. Computes education score.
        e. Computes weighted final score.
    4. Sort candidates by final score descending.
    5. Create an Analysis record and CandidateRanking records.
    6. Return the full result.
    """
    # --- Load job ---
    job = db.query(JobDescription).filter(JobDescription.id == request.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job description not found")

    # --- Load resumes ---
    if request.resume_ids:
        resumes = (
            db.query(Resume)
            .filter(Resume.id.in_(request.resume_ids))
            .all()
        )
    else:
        resumes = db.query(Resume).all()

    if not resumes:
        raise HTTPException(
            status_code=400,
            detail="No resumes found. Upload resumes before running analysis.",
        )

    jd_skills: List[str] = json.loads(job.extracted_skills or "[]")

    # --- Score each resume ---
    scored: List[tuple] = []  # (resume, score_result)

    for resume in resumes:
        resume_skills: List[str] = json.loads(resume.extracted_skills or "[]")
        result = _scoring_engine.score_candidate(
            jd_text=job.description,
            jd_skills=jd_skills,
            required_experience=job.required_experience,
            resume_text=resume.raw_text,
            resume_skills=resume_skills,
            candidate_experience=resume.years_experience,
        )
        scored.append((resume, result))

    # --- Sort descending by final score ---
    scored.sort(key=lambda x: x[1]["final_score"], reverse=True)

    # --- Create Analysis record ---
    avg_score = sum(r[1]["final_score"] for r in scored) / len(scored)
    top_candidate = scored[0][0].candidate_name if scored else ""

    analysis = Analysis(
        job_id=job.id,
        name=f"Analysis — {job.title}",
        total_resumes=len(scored),
        avg_score=round(avg_score, 2),
        top_candidate=top_candidate,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    # --- Persist candidate rankings ---
    candidate_records = []

    for rank, (resume, score_result) in enumerate(scored, start=1):
        # Remove any previous ranking for this resume + job
        db.query(CandidateRanking).filter(
            CandidateRanking.resume_id == resume.id,
            CandidateRanking.job_id == job.id,
        ).delete()

        ranking = CandidateRanking(
            resume_id=resume.id,
            job_id=job.id,
            analysis_id=analysis.id,
            rank=rank,
            semantic_score=score_result["semantic_score"],
            skill_score=score_result["skill_score"],
            experience_score=score_result["experience_score"],
            education_score=score_result["education_score"],
            final_score=score_result["final_score"],
            matched_skills=json.dumps(score_result["matched_skills"]),
            missing_skills=json.dumps(score_result["missing_skills"]),
            additional_skills=json.dumps(score_result["additional_skills"]),
            recommendation=score_result["recommendation"],
        )
        db.add(ranking)
        db.commit()
        db.refresh(ranking)

        candidate_records.append({
            "rank": rank,
            "id": ranking.id,
            "resume_id": resume.id,
            "candidate_name": resume.candidate_name,
            "email": resume.email,
            "phone": resume.phone,
            "years_experience": resume.years_experience,
            "final_score": score_result["final_score"],
            "semantic_score": score_result["semantic_score"],
            "skill_score": score_result["skill_score"],
            "experience_score": score_result["experience_score"],
            "education_score": score_result["education_score"],
            "matched_skills": score_result["matched_skills"],
            "missing_skills": score_result["missing_skills"],
            "additional_skills": score_result["additional_skills"],
            "recommendation": score_result["recommendation"],
        })

    return {
        "analysis_id": analysis.id,
        "job_title": job.title,
        "total_resumes": len(scored),
        "avg_score": round(avg_score, 2),
        "top_candidate": top_candidate,
        "candidates": candidate_records,
    }
