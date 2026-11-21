from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ResumeResponse(BaseModel):
    id: int
    filename: str
    candidate_name: str
    email: str
    phone: str
    years_experience: float
    extracted_skills: List[str] = []
    education: List[str] = []
    work_experience: List[str] = []
    projects: List[str] = []
    certifications: List[str] = []
    uploaded_at: datetime

    model_config = {"from_attributes": True}
