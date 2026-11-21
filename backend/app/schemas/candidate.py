from pydantic import BaseModel
from typing import List, Optional


class CandidateResponse(BaseModel):
    id: int
    resume_id: int
    job_id: int
    rank: int
    semantic_score: float
    skill_score: float
    experience_score: float
    education_score: float
    final_score: float
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    additional_skills: List[str] = []
    recommendation: str
    candidate_name: str = ""
    email: str = ""
    phone: str = ""
    years_experience: float = 0.0
    education: List[str] = []
    work_experience: List[str] = []
    projects: List[str] = []
    certifications: List[str] = []
    extracted_skills: List[str] = []
    filename: str = ""

    model_config = {"from_attributes": True}
