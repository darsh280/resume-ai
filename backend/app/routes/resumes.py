"""
Resumes Router
==============
Endpoints for uploading and listing resumes.
"""

import json
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.resume import Resume
from ..schemas.resume import ResumeResponse
from ..services.resume_parser import ResumeParser
from ..services.skill_extractor import SkillExtractor
from ..utils.file_utils import save_upload, allowed_file

router = APIRouter(prefix="/api/resumes", tags=["resumes"])

_parser = ResumeParser()
_skill_extractor = SkillExtractor()


def _build_response(r: Resume) -> ResumeResponse:
    return ResumeResponse(
        id=r.id,
        filename=r.filename,
        candidate_name=r.candidate_name,
        email=r.email,
        phone=r.phone,
        years_experience=r.years_experience,
        extracted_skills=json.loads(r.extracted_skills or "[]"),
        education=json.loads(r.education or "[]"),
        work_experience=json.loads(r.work_experience or "[]"),
        projects=json.loads(r.projects or "[]"),
        certifications=json.loads(r.certifications or "[]"),
        uploaded_at=r.uploaded_at,
    )


@router.post("/upload", summary="Upload multiple resumes (PDF or DOCX)")
async def upload_resumes(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    """
    Accepts up to 20 resume files in a single batch.

    For each file:
    1. Validates the file type (PDF / DOCX only).
    2. Checks for duplicates (by filename).
    3. Saves file to disk.
    4. Parses text and extracts candidate information.
    5. Extracts technical skills.
    6. Stores everything in the database.
    """
    results = []
    errors = []

    for file in files:
        # --- Validation ---
        if not allowed_file(file.filename):
            errors.append({
                "filename": file.filename,
                "error": "Unsupported file type. Use PDF or DOCX.",
            })
            continue

        content = await file.read()

        if len(content) == 0:
            errors.append({"filename": file.filename, "error": "File is empty."})
            continue

        # --- Duplicate check ---
        existing = (
            db.query(Resume).filter(Resume.filename == file.filename).first()
        )
        if existing:
            errors.append({
                "filename": file.filename,
                "error": "Duplicate file — already uploaded.",
            })
            continue

        # --- Parse & save ---
        try:
            file_path = save_upload(content, file.filename)
            parsed = _parser.parse(file_path)
            skills = _skill_extractor.extract(parsed["raw_text"])

            resume = Resume(
                filename=file.filename,
                file_path=file_path,
                file_type=file.filename.rsplit(".", 1)[-1].lower(),
                candidate_name=parsed["candidate_name"],
                email=parsed["email"],
                phone=parsed["phone"],
                raw_text=parsed["raw_text"],
                extracted_skills=json.dumps(skills),
                education=json.dumps(parsed["education"]),
                work_experience=json.dumps(parsed["work_experience"]),
                projects=json.dumps(parsed["projects"]),
                certifications=json.dumps(parsed["certifications"]),
                years_experience=parsed["years_experience"],
            )
            db.add(resume)
            db.commit()
            db.refresh(resume)

            results.append({
                "id": resume.id,
                "filename": resume.filename,
                "candidate_name": resume.candidate_name,
                "status": "success",
            })

        except Exception as exc:
            errors.append({"filename": file.filename, "error": str(exc)})

    return {
        "uploaded": results,
        "errors": errors,
        "total": len(results),
    }


@router.get("", response_model=list[ResumeResponse], summary="List all uploaded resumes")
def list_resumes(db: Session = Depends(get_db)):
    resumes = (
        db.query(Resume).order_by(Resume.uploaded_at.desc()).all()
    )
    return [_build_response(r) for r in resumes]
