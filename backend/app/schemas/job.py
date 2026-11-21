from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class JobCreate(BaseModel):
    title: str
    description: str
    required_experience: float = 0.0


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    required_experience: float
    extracted_skills: List[str] = []
    required_qualifications: List[str] = []
    created_at: datetime

    model_config = {"from_attributes": True}
