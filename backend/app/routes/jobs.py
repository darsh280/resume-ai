"""
Jobs Router
===========
Endpoints for creating and retrieving job descriptions.
"""

import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.job import JobDescription
from ..schemas.job import JobCreate, JobResponse
from ..services.skill_extractor import SkillExtractor
from ..services.experience_analyzer import ExperienceAnalyzer

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

_skill_extractor = SkillExtractor()
_exp_analyzer = ExperienceAnalyzer()


def _build_response(j: JobDescription) -> JobResponse:
    return JobResponse(
        id=j.id,
        title=j.title,
        description=j.description,
        required_experience=j.required_experience,
        extracted_skills=json.loads(j.extracted_skills or "[]"),
        required_qualifications=json.loads(j.required_qualifications or "[]"),
        created_at=j.created_at,
    )


@router.post("", response_model=JobResponse, summary="Create a job description")
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """
    Create a new job description and automatically extract skills using NLP.
    """
    skills = _skill_extractor.extract(job.description)

    # Use provided experience or parse from JD text
    req_exp = job.required_experience
    if req_exp <= 0:
        req_exp = _exp_analyzer.parse_required_experience(job.description)

    db_job = JobDescription(
        title=job.title,
        description=job.description,
        required_experience=req_exp,
        extracted_skills=json.dumps(skills),
        required_qualifications=json.dumps([]),
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return _build_response(db_job)


@router.get("", response_model=list[JobResponse], summary="List all job descriptions")
def list_jobs(db: Session = Depends(get_db)):
    jobs = (
        db.query(JobDescription)
        .order_by(JobDescription.created_at.desc())
        .all()
    )
    return [_build_response(j) for j in jobs]


@router.get("/{job_id}", response_model=JobResponse, summary="Get a job description")
def get_job(job_id: int, db: Session = Depends(get_db)):
    j = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="Job description not found")
    return _build_response(j)


@router.post("/upload-jd", summary="Upload a plain-text JD file")
async def upload_jd_file(file: UploadFile = File(...)):
    """Read a .txt file and return its content so the frontend can paste it."""
    content = await file.read()
    return {"content": content.decode("utf-8", errors="ignore")}
