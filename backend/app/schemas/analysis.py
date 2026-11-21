from pydantic import BaseModel
from datetime import datetime


class AnalysisResponse(BaseModel):
    id: int
    job_id: int
    name: str
    total_resumes: int
    avg_score: float
    top_candidate: str
    created_at: datetime

    model_config = {"from_attributes": True}
